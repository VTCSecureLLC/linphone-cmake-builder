#!/usr/bin/env python

############################################################################
# prepare.py
# Copyright (C) 2015  Belledonne Communications, Grenoble France
#
############################################################################
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
############################################################################

import argparse
import os
import platform
import shutil
import stat
import subprocess
import sys

class Target:
	def __init__(self, name):
		self.name = name
		self.output = 'OUTPUT'
		self.generator = None
		self.config_file = None
		self.toolchain_file = None

	def output_dir(self):
		output_dir = self.output
		if not os.path.isabs(self.output):
			top_dir = os.getcwd()
			output_dir = os.path.join(top_dir, self.output)
		if platform.system() == 'Windows':
			output_dir = output_dir.replace('\\', '/')
		return output_dir

	def cmake_command(self, build_type, latest, list_cmake_variables, additional_args):
		cmd = ['cmake', '../..']
		if self.generator is not None:
			cmd += ['-G', self.generator]
		cmd += ['-DCMAKE_BUILD_TYPE=' + build_type]
		cmd += ['-DCMAKE_PREFIX_PATH=' + self.output_dir(), '-DCMAKE_INSTALL_PREFIX=' + self.output_dir()]
		if self.toolchain_file is not None:
			cmd += ['-DCMAKE_TOOLCHAIN_FILE=' + self.toolchain_file]
		if self.config_file is not None:
			cmd += ['-DLINPHONE_BUILDER_CONFIG_FILE=' + self.config_file]
		if latest:
			cmd += ['-DLINPHONE_BUILDER_LATEST=YES']
		if list_cmake_variables:
			cmd += ['-L']
		for arg in additional_args:
			cmd += [arg]
		cmd_str = ''
		for w in cmd:
			if ' ' in w:
				cmd_str += ' \"' + w + '\"'
			else:
				cmd_str += ' ' + w
		print(cmd_str)
		return cmd

	def clean(self):
		if os.path.isdir('WORK'):
			shutil.rmtree('WORK', ignore_errors=False, onerror=self.handle_remove_read_only)

	def veryclean(self):
		self.clean()
		if os.path.isdir(self.output_dir()):
			shutil.rmtree(self.output_dir(), ignore_errors=False, onerror=self.handle_remove_read_only)

	def handle_remove_read_only(self, func, path, exc):
		if not os.access(path, os.W_OK):
			os.chmod(path, stat.S_IWUSR)
			func(path)
		else:
			raise

	def build_instructions(self, debug = False):
		if self.generator is None:
			return "Run the following command to build:\n\tmake -C WORK/cmake-{target}".format(target=self.name)
		elif self.generator.startswith('Visual Studio'):
			config = "Release"
			if debug:
				config = "Debug"
			return "Open the \"WORK\\cmake-{target}\\Project.sln\" Visual Studio solution and build with the \"{config}\" configuration".format(target=self.name, config=config)

class BB10Target(Target):
	def __init__(self, arch):
		Target.__init__(self, 'bb10-' + arch)
		self.config_file = 'configs/config-bb10-' + arch + '.cmake'
		self.toolchain_file = 'toolchains/toolchain-bb10-' + arch + '.cmake'
		self.output = 'OUTPUT/liblinphone-bb10-sdk/' + arch

class BB10i486Target(BB10Target):
	def __init__(self):
		BB10Target.__init__(self, 'i486')

class BB10armTarget(BB10Target):
	def __init__(self):
		BB10Target.__init__(self, 'arm')

class DesktopTarget(Target):
	def __init__(self):
		Target.__init__(self, 'desktop')
		self.config_file = 'configs/config-desktop.cmake'
		if platform.system() == 'Windows':
			self.generator = 'Visual Studio 12 2013'

class IOSTarget(Target):
	def __init__(self, arch):
		Target.__init__(self, 'ios-' + arch)
		self.config_file = 'configs/config-ios-' + arch + '.cmake'
		self.toolchain_file = 'toolchains/toolchain-ios-' + arch + '.cmake'
		self.output = 'OUTPUT/liblinphone-ios-sdk/' + arch

class IOSi386Target(IOSTarget):
	def __init__(self):
		IOSTarget.__init__(self, 'i386')

class IOSarmv7Target(IOSTarget):
	def __init__(self):
		IOSTarget.__init__(self, 'armv7')

class IOSarmv7sTarget(IOSTarget):
	def __init__(self):
		IOSTarget.__init__(self, 'armv7s')

class PythonTarget(Target):
	def __init__(self):
		Target.__init__(self, 'python')
		self.config_file = 'configs/config-python.cmake'
		if platform.system() == 'Windows':
			self.generator = 'Visual Studio 9 2008'

class PythonRaspberryTarget(Target):
	def __init__(self):
		Target.__init__(self, 'python-raspberry')
		self.config_file = 'configs/config-python-raspberry.cmake'
		self.toolchain_file = 'toolchains/toolchain-raspberry.cmake'


targets = {}
targets['bb10-arm'] = BB10armTarget()
targets['bb10-i486'] = BB10i486Target()
targets['desktop'] = DesktopTarget()
targets['ios-i386'] = IOSi386Target()
targets['ios-armv7'] = IOSarmv7Target()
targets['ios-armv7s'] = IOSarmv7sTarget()
targets['python'] = PythonTarget()
targets['python-raspberry'] = PythonRaspberryTarget()
target_names = sorted(targets.keys())


def run(target, debug, latest, list_cmake_variables, additional_args):
	build_type = 'Release'
	if debug:
		build_type = 'Debug'

	work_dir = 'WORK/cmake-' + target.name
	if not os.path.isdir(work_dir):
		os.makedirs(work_dir)
	proc = subprocess.Popen(target.cmake_command(build_type, latest, list_cmake_variables, additional_args), cwd=work_dir, shell=False)
	proc.communicate()
	return proc.returncode

def main(argv = None):
	if argv is None:
		argv = sys.argv
	argparser = argparse.ArgumentParser(description="Prepare build of Linphone and its dependencies.")
	argparser.add_argument('-c', '--clean', help="Clean a previous build instead of preparing a build.", action='store_true')
	argparser.add_argument('-C', '--veryclean', help="Clean a previous build and its installation directory.", action='store_true')
	argparser.add_argument('-d', '--debug', help="Prepare a debug build.", action='store_true')
	argparser.add_argument('-l', '--latest', help="Build latest versions of all dependencies.", action='store_true')
	argparser.add_argument('-o', '--output', help="Specify output directory.")
	argparser.add_argument('-G', '--generator', metavar='generator', help="CMake generator to use.")
	argparser.add_argument('-L', '--list-cmake-variables', help="List non-advanced CMake cache variables.", action='store_true', dest='list_cmake_variables')
	argparser.add_argument('target', choices=target_names, help="The target to build.")
	args, additional_args = argparser.parse_known_args()

	target = targets[args.target]
	if args.generator:
		target.generator = args.generator
	if args.output:
		target.output = args.output

	if args.veryclean:
		target.veryclean()
		return 0
	if args.clean:
		target.clean()
		return 0

	retcode = run(target, args.debug, args.latest, args.list_cmake_variables, additional_args)
	if retcode == 0:
		print("\n" + target.build_instructions(args.debug))
	return retcode

if __name__ == "__main__":
	sys.exit(main())