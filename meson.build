project('rdylib',
        'rust',
        'c',
        version: '0.1.0',
        meson_version : '>= 0.56')

if get_option('debug')
  target = 'debug'
else
  target = 'release'
endif

pkgconfig = import('pkgconfig')

cargo = find_program('cargo', version:'>=1.40')
rustc = find_program('rustc', version:'>=1.52')

gobject_dep = dependency('gobject-2.0')

output = []

system = build_machine.system()
extension = 'a'
if system == 'windows'
  extension = 'lib'
endif

output += ['lib' + meson.project_name() + '.' + extension]

cargo_wrapper = find_program('build-aux/cargo_wrapper.py')

rdylib_lib = custom_target('rdylib.tmp',
  build_by_default: true,
  build_always_stale: true,
  output: output,
  console: true,
  #install: true,
  install_dir: get_option('libdir'),
  #depends: depends,
  depfile: 'rdylib.dep',
  command: [cargo_wrapper,
    'build',
  '--build-dir', meson.current_build_dir(),
  '--source-dir', meson.current_source_dir(),
  '--include-directories', 'rdylib',
  '--root-dir', meson.global_build_root(),
  '--build-type', target,
  '--prefix', get_option('prefix'),
  '--libdir', get_option('libdir'),
  '--local-include-dir', 'include',
  '--depfile', '@DEPFILE@',
  '--exts', extension
  ])

install_headers('include/rdylib.h', subdir: 'rdylib')
rdylibinc = include_directories('include')

lib = library('rdylib',
  link_whole: rdylib_lib,
  install: true,
   dependencies: [
     gobject_dep,
   ],
  )

pkgconfig.generate(lib,
  subdirs: 'rdylib'
  )

rdylib_dep = declare_dependency(link_with: lib, include_directories: [rdylibinc])
meson.override_dependency('rdylib', rdylib_dep)

executable ('main', 'main.c', dependencies: [rdylib_dep])