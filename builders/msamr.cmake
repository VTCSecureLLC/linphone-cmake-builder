############################################################################
# msamr.cmake
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

set(EP_msamr_GIT_REPOSITORY "git://git.linphone.org/msamr.git")
set(EP_msamr_GIT_TAG_LATEST "master")
set(EP_msamr_GIT_TAG "d328ef1154dc68da817690bb22e5698f1980321a")

set(EP_msamr_CMAKE_OPTIONS )
set(EP_msamr_DEPENDENCIES EP_ms2 EP_opencoreamr)

if(ENABLE_AMRNB)
	list(APPEND EP_msamr_CMAKE_OPTIONS "-DENABLE_NARROWBAND=YES")
else()
	list(APPEND EP_msamr_CMAKE_OPTIONS "-DENABLE_NARROWBAND=NO")
endif()
if(ENABLE_AMRWB)
	list(APPEND EP_msamr_CMAKE_OPTIONS "-DENABLE_WIDEBAND=YES")
	list(APPEND EP_msamr_DEPENDENCIES EP_voamrwbenc)
else()
	list(APPEND EP_msamr_CMAKE_OPTIONS "-DENABLE_WIDEBAND=NO")
endif()
