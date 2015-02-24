############################################################################
# msx264.cmake
# Copyright (C) 2014  Belledonne Communications, Grenoble France
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

set(EP_msx264_GIT_REPOSITORY "git://git.linphone.org/msx264.git")
set(EP_msx264_GIT_TAG_LATEST "master")
set(EP_msx264_GIT_TAG "dff7452939033d8749c4e9d445a64172f4bb7a3d")

set(EP_msx264_BUILD_METHOD "autotools")
set(EP_msx264_USE_AUTOGEN "yes")
set(EP_msx264_CROSS_COMPILATION_OPTIONS
	"--prefix=${CMAKE_INSTALL_PREFIX}"
	"--host=${LINPHONE_BUILDER_HOST}"
)
set(EP_msx264_LINKING_TYPE "--disable-static" "--enable-shared")
set(EP_msx264_DEPENDENCIES EP_ms2 EP_x264)
