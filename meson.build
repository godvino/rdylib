project('rdylib',
        'c',
        version: '0.1.0',
        meson_version : '>= 0.58')

if get_option('debug')
  target = 'debug'
else
  target = 'release'
endif

pkgconfig = import('pkgconfig')

cargo = find_program('cargo', version:'>=1.40')
rustc = find_program('rustc', version:'>=1.52')

gio_dep = dependency('gio-2.0')

system = host_machine.system()
extension = 'a'
output = 'lib' + meson.project_name() + '.' + extension
if system == 'windows'
  extension = 'lib'
  output = meson.project_name() + '.' + extension
endif

buildtype = 'native'
if meson.is_cross_build()
  buildtype = 'cross'
endif

 conf = configuration_data()
 conf.set_quoted('VERSION', meson.project_version())

 configure_file(
     input: 'config.rs.in',
     output: 'config.rs',
     configuration: conf
 )

cargo_wrapper = find_program('build-aux/cargo_wrapper.py')

rdylib_lib = custom_target('rdylib.tmp',
  build_by_default: true,
  build_always_stale: true,
  output: output,
  console: true,
  depfile: 'rdylib.dep',
  command: [cargo_wrapper,
  '--build-dir', meson.current_build_dir(),
  '--source-dir', meson.current_source_dir(),
  '--root-dir', meson.global_build_root(),
  '--build-type', target,
  '--depfile', '@DEPFILE@',
  '--exts', extension,
  '--buildtype', buildtype
  ])

install_headers('include/rdylib.h', subdir: 'rdylib')
rdylibinc = include_directories('include')

lib = library('rdylib',
  link_whole: rdylib_lib,
  install: true,
   dependencies: [
     gio_dep,
   ],
  )

pkgconfig.generate(lib,
  subdirs: 'rdylib'
  )

rdylib_dep = declare_dependency(link_with: lib, include_directories: [rdylibinc])
meson.override_dependency('rdylib', rdylib_dep)

executable ('main', 'main.c', dependencies: [rdylib_dep], install: true)

devenv = environment()
devenv.set('CARGO_HOME', meson.project_build_root() / 'cargo-home')
devenv.set('CARGO_TARGET_DIR', meson.project_build_root() / 'target')

meson.add_devenv(devenv)
