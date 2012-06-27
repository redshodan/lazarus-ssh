#
# Copyright (C) 2009 Chris Newton <redshodan@gmail.com>
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
#
# Author: Chris Newton <redshodan@gmail.com>
# $Revision$
#


import os
from utils import LsshTestCase
import log


class BasicTests(LsshTestCase):
    # The initial test which tests basic ssh and fails all of the tests if
    # ssh fails
    def test1SshForTests(self):
        ret = self.runCmd(["ssh", "-T", "localhost", "/bin/true"])
        if ret[0] != 0:
            self._resultForDoCleanups.stop()
        self.assertIs(ret[0], 0,
                      "Can not ssh to localhost without a password, can not " +
                      "continue with tests: %sret=%d: %s" %
                      (self.error, ret[0], ret[1]))
    test1SshForTests.timeout = 2

    def testBasic(self):
        ret = self.runCmd(["ssh", "-T", "localhost", "/bin/true"])
        self.assertIs(ret[0], 0,
                      "Can not ssh to localhost without a password, can not " +
                      "continue with tests: %sret=%d: %s" %
                      (self.error, ret[0], ret[1]))
