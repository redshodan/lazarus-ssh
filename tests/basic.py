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


import os, pwd, unittest2
from subprocess import Popen
from utils import (LsshTestCase, CriticalTest, ROOT, TEST, USER, TESTUSER,
                   TESTPASS)
import log


class LsshTests(LsshTestCase):
    def testSshCmd(self):
        self.runCmd(TEST, "./lssh localhost /bin/true")

    # FIXME:
    @unittest2.skip("lssh --cmd doesn't exit after running cmd")
    def testLsshCmd(self):
        self.runCmd(TEST, "./lssh --cmd=/bin/true localhost")

    # FIXME:
    @unittest2.skip("Test needs to do the tty drain-wait password prompt " +
                    "to feed the password to ssh.")
    def testCmdWithPass(self):
        self.disableSshKey()
        self.runCmd(TEST, "./lssh localhost /bin/true")
        self.enableSshKey()
