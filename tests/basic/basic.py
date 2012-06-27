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


import os, subprocess, signal
from utils import LsshTestCase
import log


class BasicTests(LsshTestCase):
    def _sigalarm(self, sig, frame):
        log.info("ssh login test failed to complete in time")
        self.ssh_timeout = True
        self.ssh.kill()

    # An ugly test which asserts that we can run ssh the way we expect it
    # before testing lssh.
    def testSshForTests(self):
        log.info("Starting ssh login test")
        signal.signal(signal.SIGALRM, self._sigalarm)
        signal.alarm(2)
        self.ssh_timeout = False
        self.ssh = subprocess.Popen(
            ["ssh", "-T", "localhost", "/bin/true"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ret = self.ssh.communicate()
        signal.alarm(0)
        log.info("Finised ssh login test: ret=%d: %s", self.ssh.returncode,
                 ret[0])
        if self.ssh_timeout:
            extra = "ssh login test failed to complete in time: "
        else:
            extra = ""
        if self.ssh.returncode != 0:
            self._resultForDoCleanups.stop()
        self.assertIs(
            self.ssh.returncode, 0,
            "Can not ssh to localhost without a password, can not continue " +
            "with tests: %sret=%d: %s" % (extra, self.ssh.returncode, ret[0]))
