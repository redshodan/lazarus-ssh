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


import os, pwd
from subprocess import Popen
from utils import (LsshTestCase, CriticalTest, ROOT, TEST, USER, TESTUSER,
                   TESTPASS)
import log



# The initial test which tests basic ssh and fails all of the tests if
# ssh fails
class BasicTests(LsshTestCase):
    def __init__(self, name, timeout=2):
        LsshTestCase.__init__(self, name, timeout)
    
    @CriticalTest
    def test00SudoForTests(self):
        p = pwd.getpwnam(TESTUSER)
        ret = self.runCmd(TEST, "echo $UID", fail="Can not run sudo.")
        self.assertEquals(int(ret[1].strip()), p.pw_uid,
                          "Can not sudo as test user")

    @CriticalTest
    def test01MakeSshKey(self):
        ret = self.runCmd(TEST,
                          "[[ -f ~/.ssh/id_rsa && -f ~/.ssh/authorized_keys &&" +
                          " -f ~/.ssh/authorized_keys_ ]]", fail=False)
        if ret[0] == 0:
            log.info("SSH key files already exist, skipping creation")
            return
        self.runCmd(
            TEST, "rm -f ~/.ssh/id_rsa ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
        self.runCmd(
            TEST, "ssh-keygen -f ~/.ssh/id_rsa -t rsa -N foobar -q",
            fail="Can not generate test user sshkey")
        self.runCmd(TEST, "echo foobar > /tmp/lssh-test")
        self.runCmd(TEST,
                          "openssl rsa -in ~/.ssh/id_rsa -passin " +
                          "file:/tmp/lssh-test > ~/.ssh/id_rsa.foo")
        self.runCmd(TEST, "mv ~/.ssh/id_rsa.foo ~/.ssh/id_rsa")
        self.runCmd(TEST, "chmod 600 ~/.ssh/id_rsa")
        self.runCmd(TEST, "cp -f ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys")
        self.runCmd(TEST, "cp -f ~/.ssh/authorized_keys ~/.ssh/authorized_keys_")
    
    @CriticalTest
    def test02SshNoPass(self):
        ret = self.runCmd(
            TEST, "ssh localhost /bin/true",
            fail="Can not ssh to localhost without a password, can not " +
            "continue with tests")
