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


import os, pwd, unittest2, re
from subprocess import Popen, PIPE, STDOUT
from utils import (LsshTestCase, CriticalTest, ROOT, TEST, USER, TESTUSER,
                   TESTPASS, TESTPORT)
import log


class LsshTests(LsshTestCase):
    def testSshCmd(self):
        self.runCmd(TEST, "ssh localhost /bin/true")

    def testLsshCmd(self):
        ret = self.runCmd(TEST, "./lssh --cmd='echo xxx$$; exit' localhost")
        self.assertTrue(re.search("xxx[0-9]+", ret[1]))

    # FIXME:
    @unittest2.skip("Test needs to do the tty drain-wait password prompt " +
                    "to feed the password to ssh.")
    def testCmdWithPass(self):
        self.disableSshKey()
        self.runCmd(TEST, "./lssh localhost /bin/true")
        self.enableSshKey()


class NetworkTests(LsshTestCase):
    THE_SSH = None
    
    @classmethod
    def setUpClass(cls):
        cls.THE_SSH = Popen(["sudo", "/usr/sbin/sshd", "-Dp", TESTPORT],
                            stdout=PIPE, stderr=STDOUT)
        log.info("Started custom sshd, pid=%d" % cls.THE_SSH.pid)

    @classmethod
    def tearDownClass(cls):
        log.info("Killing custom sshd, pid=%d" % cls.THE_SSH.pid)
        cls._runCmd(["sudo", "kill", str(cls.THE_SSH.pid)])
        cls.unfilterSsh()

    @classmethod
    def filterSsh(cls):
        log.info("Filtering custom ssh")
        cls._runCmd(["sudo", "iptables", "-t", "filter", "-A", "INPUT", "-p",
                     "tcp", "--dport", TESTPORT, "-j", "REJECT",
                     "--reject-with", "icmp-host-unreachable"])

    @classmethod
    def unfilterSsh(cls):
        log.info("Unfiltering custom ssh")
        cls._runCmd(["sudo", "iptables", "-t", "filter", "-D", "INPUT", "-p",
                     "tcp", "--dport", TESTPORT, "-j", "REJECT",
                     "--reject-with", "icmp-host-unreachable"])

    def testSshNoReconnFiltered(self):
        self.filterSsh()
        ret = self.runCmd(
            TEST, "./lssh --norecon -p %s localhost" % TESTPORT,
            fail=False)
        self.assertTrue(ret[0] != 0, "ssh should have returned non-zero")
