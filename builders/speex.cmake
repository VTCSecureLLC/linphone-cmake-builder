############################################################################
# speex.cmake
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

set(EP_speex_GIT_REPOSITORY "git://git.linphone.org/speex.git")
set(EP_speex_GIT_TAG_LATEST "linphone")
set(EP_speex_GIT_TAG "d1f9185cd8bba2e44ab38dda04f9d5d02b288c46")

set(EP_speex_LINKING_TYPE "-DENABLE_STATIC=0")
if(MSVC)
	set(EP_speex_EXTRA_LDFLAGS "/SAFESEH:NO")
endif()
