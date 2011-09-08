#!/usr/bin/env python

from distutils.command.install_scripts import install_scripts
from distutils import log
import os

def eprefix():
	return os.getenv('EPREFIX', '')

from distutils.command.build import build
import fileinput
import sys

class my_build(build):

	def initialize_options(self):
		build.initialize_options(self)

	def finalize_options(self):
		build.finalize_options(self)
		
	def run(self):
		# TODO Should make a copy first. -sera
		for base, dirs, files in os.walk('src'):
			for f in files:
				for line in fileinput.input(os.path.join(base, f),inplace=True):
					sys.stdout.write(line.replace('@GENTOO_PORTAGE_EPREFIX@', eprefix()))
		build.run(self)

class my_install_scripts(install_scripts):
	"""Specialized data file install to handle our symlinks"""
	install_scripts.user_options.append(('symlink-tools=', None,
		'List of files to symlink to run-java-tool in script directory'))

	def initialize_options(self):
		install_scripts.initialize_options(self)
		self.symlink_tools = None

	def finalize_options(self):
		install_scripts.finalize_options(self)
		self.ensure_string_list('symlink_tools')
		
	def run(self):
		install_scripts.run(self)
		for tool in self.symlink_tools:
			s = self.install_dir + '/' + tool
			log.info("symbolically linking %s -> %s" % ('run-java-tool', s))
			if not self.dry_run:
				# os.symlink fails to overwrite existing files
				if os.path.exists(s):
					os.remove(s)
				# copy_file is not able to handle relative symlinks with --root
				os.symlink('run-java-tool', s)

from distutils.core import setup
from glob import glob

setup (
	cmdclass={'build' : my_build, 'install_scripts': my_install_scripts},
	name = 'java-config',
	version = '2.1.11',
	description = 'java enviroment configuration tool',
	long_description = \
	"""
		java-config is a tool for configuring various enviroment
		variables and configuration files involved in the java
		enviroment for Gentoo Linux.
	""",
	maintainer = 'Gentoo Java Team',
	maintainer_email = 'java@gentoo.org',
	url = 'http://www.gentoo.org',
	packages = ['java_config_2'],
	package_dir = { 'java_config_2' : 'src/java_config_2' },
	scripts = ['src/java-config-2','src/depend-java-query','src/run-java-tool', 'src/gjl'],
	data_files = [
		('share/applications/', ['data/javaws.desktop']),
		('share/icons/hicolor/48x48/mimetypes/', ['data/application-x-java-jnlp-file.png']),
		('share/pixmaps/', ['data/java-icon48.png']),
		('share/java-config-2/launcher', ['src/launcher.bash']),
		('share/eselect/modules', glob('src/eselect/*.eselect')),
		(eprefix() + '/etc/java-config-2/build/', ['config/jdk.conf','config/compilers.conf']),
		(eprefix() + '/etc/env.d/',['config/20java-config']),
		(eprefix() + '/etc/profile.d/', glob('src/profile.d/*')),
		(eprefix() + '/etc/revdep-rebuild/', ['src/revdep-rebuild/60-java'])
	]
)

# vim: noet:ts=4:
