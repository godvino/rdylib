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

cargo = find_program('cargo', version:'>=1.40')
rustc = find_program('rustc', version:'>=1.52')

system = build_machine.system()
if system == 'windows'
  ext_dynamic = 'dll'
  ext_static = 'lib'
elif system == 'darwin'
  ext_dynamic = 'dylib'
  ext_static = 'a'
else
  ext_dynamic = 'so'
  ext_static = 'a'
endif

output = []
extensions = []

if get_option('default_library') == 'shared' or get_option('default_library') == 'both'
extensions += [ext_dynamic]
output += ['lib' + meson.project_name() + '.' + ext_dynamic]
endif

if get_option('default_library') == 'static' or get_option('default_library') == 'both'
extensions += [ext_static]
  if get_option('default_library') != 'both'
    output += ['lib' + meson.project_name() + '.' + ext_static]
  endif
endif

cargo_wrapper = find_program('build-aux/cargo_wrapper.py')

rdylib_lib = custom_target('rdylib',
  build_by_default: true,
  build_always_stale: true,
  output: output,
  console: true,
  install: true,
  install_dir: get_option('libdir'),
  #depends: depends,
  depfile: 'rdylib.dep',
  command: [cargo_wrapper,
    'build',
  '--build-dir', meson.current_build_dir(),
  '--source-dir', meson.current_source_dir(),
  '--include-directories', 'rdylib',
  '--root-dir', meson.project_build_root(),
  '--build-type', target,
  '--prefix', get_option('prefix'),
  '--libdir', get_option('libdir'),
  '--local-include-dir', 'include',
  '--depfile', '@DEPFILE@',
  '--exts', extensions
  ])

install_headers('include/rdylib.h', subdir: 'rdylib')
rdylibinc = include_directories('include')

d = declare_dependency(link_with: rdylib_lib, include_directories: [rdylibinc])

meson.override_dependency('rdylib', d)

#executable ('main', 'main.c', dependencies: [d])