#!/usr/bin/env python3

import hashlib
import glob
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path as P

PARSER = ArgumentParser()
PARSER.add_argument('command', choices=['build', 'test'])
PARSER.add_argument('--build-dir', type=P)
PARSER.add_argument('--source-dir', type=P)
PARSER.add_argument('--root-dir', type=P)
PARSER.add_argument('--build-type', choices=['release', 'debug'])
PARSER.add_argument('--include-directories', nargs='*', default=[])
PARSER.add_argument('--extra-env-vars', nargs='*', default=[])
PARSER.add_argument('--prefix', type=P)
PARSER.add_argument('--libdir', type=P)
PARSER.add_argument('--version', default=None)
PARSER.add_argument('--local-include-dir', default=None)
PARSER.add_argument('--exts', nargs="+", default=[])
PARSER.add_argument('--depfile')

if __name__ == "__main__":
    opts = PARSER.parse_args()
   # print(opts)

    logfile = open(opts.root_dir / 'meson-logs' / f'{opts.source_dir.name}-cargo-wrapper.log', 'w')

    print(opts, file=logfile)
    cargo_target_dir = opts.build_dir / 'target'

    env = os.environ.copy()
    env['CARGO_TARGET_DIR'] = str(cargo_target_dir)

    pkg_config_path = env.get('PKG_CONFIG_PATH', '').split(':')
    pkg_config_path.append(str(opts.root_dir / 'meson-uninstalled'))
    env['PKG_CONFIG_PATH'] = ':'.join(pkg_config_path)

    env['CARGO_HOME'] = str(opts.build_dir / 'cargo-home')

    for e in opts.extra_env_vars:
        k, v = e.split(':')
        env[k] = v

    if opts.command == 'build':
        cargo_cmd = ['cargo', 'build']
        if opts.build_type == 'release':
            cargo_cmd.append('--release')
    elif opts.command == 'test':
        # cargo test
        cargo_cmd = ['cargo', 'ctest', '--no-fail-fast', '--color=always']
    else:
        print("Unknown command:", opts.command, file=logfile)
        sys.exit(1)

    cargo_cmd.extend(['--manifest-path', opts.source_dir / 'Cargo.toml'])
    #cargo_cmd.extend(['--prefix', opts.prefix, '--libdir', opts.prefix / opts.libdir])

    def run(cargo_cmd, env):
        try:
            subprocess.run(cargo_cmd, env=env, check=True)
        except subprocess.SubprocessError:
            sys.exit(1)

    for p in opts.include_directories:
        cargo_cmd.extend(['-p', p])
    run(cargo_cmd, env)

    if opts.command == 'build':
        target_dir = cargo_target_dir / '**' / opts.build_type

        # Copy so files to build dir
        depfile_content = ""
        for ext in opts.exts:
            for f in glob.glob(str(target_dir / f'*.{ext}'), recursive=True):
                libfile = P(f)
                with open(libfile.parent / (libfile.stem + '.d'), 'r') as libdepfile:
                    content = libdepfile.read()
                    # Write our own depfile
                    content = content.replace(f"{str(libfile)}:",
                                              f"{str(opts.build_dir / libfile.name)}:")
                    depfile_content += f"{content}\n"
                shutil.copy(f, opts.build_dir)
                #shutil.copy(f, opts.build_dir / f'{P(f).name}.0')

        with open(opts.depfile, 'w') as depfile:
            depfile.write(depfile_content)

        # Copy generated pkg-config files
#        for f in glob.glob(str(target_dir / '*.pc'), recursive=True):
#            shutil.copy(f, opts.build_dir)

        for include in opts.include_directories:
            include_dirs = target_dir / 'include' / f'{include}'
            for include_dir in glob.glob(str(include_dirs), recursive=True):
                for root, dirs, files in os.walk(include_dir):
                    root = P(root)
                    incdir = opts.source_dir / opts.local_include_dir
                    #incdir = incdir / f'{include}'
                    #if root != include_dir:
                    #    incdir /= P(root).name
                    os.makedirs(incdir, exist_ok=True)
                    for f in files:
                        copied_f = incdir / f
                        generated_f = root / f
                        try:
                            local_md5 = hashlib.md5(open(copied_f, 'rb').read()).hexdigest()
                        except FileNotFoundError:
                            local_md5 = None

                        if local_md5:
                            if local_md5 == hashlib.md5(open(generated_f, 'rb').read()).hexdigest():
                                print(f"{copied_f} has not changed.", file=logfile)
                                continue

                        print(f"Copying {generated_f} into {copied_f}.", file=logfile)
                        shutil.copyfile(generated_f, copied_f)

        # Move -uninstalled.pc to meson-uninstalled
        # uninstalled = opts.root_dir / 'meson-uninstalled'
        # if not uninstalled.exists():
        #     os.mkdir(uninstalled)

        # for f in glob.glob(str(opts.build_dir / '*-uninstalled.pc')):
            # move() does not allow us to update the file so remove it if it already exists
        #     dest = uninstalled / P(f).name
        #     if dest.exists():
        #         dest.unlink()
        #     shutil.move(f, uninstalled)
