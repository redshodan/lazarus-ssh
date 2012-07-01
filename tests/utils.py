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

import os, sys, unittest2, subprocess, signal, termios

import log

THE_TEST = None
TESTUSER = None
TESTPASS = None
ROOT = 1
TEST = 2
USER = 3

SCREEN_NONE = "No Sockets found in /var/run/screen/S-test."

##
## unittest behavior adjustment
##
class LsshTestCase(unittest2.TestCase):
    
    def __init__(self, name, timeout=10):
        unittest2.TestCase.__init__(self, name)
        self.test_name = str(self)
        self.orgtest = getattr(self, name)
        setattr(self, name, self._run)
        if hasattr(self.orgtest, "timeout"):
            self.timeout = self.orgtest.timeout
        else:
            self.timeout = timeout
        self.error = ""

    def _sigalarm(self, sig, frame):
        log.info("_sigalarm: test failed to complete in time")
        self.error = "Test failed to complete in time: "
        self.cmd_timeout = True
        self.cmd.kill()
                
    def setUp(self):
        global THE_TEST
        unittest2.TestCase.setUp(self)
        log.info("---------Starting test: %s(timeout=%d)---------",
                 self.test_name, self.timeout)
        THE_TEST = self
        self.cmd_timeout = False
        self.error = ""
        signal.signal(signal.SIGALRM, self._sigalarm)
        signal.alarm(self.timeout)

    def tearDown(self):
        signal.alarm(0)
        unittest2.TestCase.tearDown(self)
        log.info("---------Ending test: %s---------", self.test_name)

    def runCmd(self, who, cmd, **kwargs):
        if who == ROOT:
            args = ["/usr/bin/sudo"]
        elif who == TEST:
            args = ["/usr/bin/sudo", "-u", TESTUSER, "-i"]
        elif who == USER:
            args = ["bash", "-c", cmd]
        else:
            raise Exception("Invalid 'who' for runCmd")
        args.extend(["bash", "-c"])
        args.append(cmd)
        expect_fail = True
        if "fail" in kwargs:
            expect_fail = kwargs["fail"]
            del kwargs["fail"]
        if "stdout" not in kwargs:
            kwargs["stdout"] = subprocess.PIPE
        if "stderr" not in kwargs:
            kwargs["stderr"] = subprocess.STDOUT
        log.info("Starting cmd: %s, %s" % (str(args), str(kwargs)))
        self.cmd = subprocess.Popen(args, **kwargs)
        try:
            ret = self.cmd.communicate()
        except IOError, e:
            if e.errno == 4:
                ret = ["", ""]
                self.cmd.returncode = -127
        log.info("Finised cmd: ret=%d: %s", self.cmd.returncode,
                 ret[0])
        if expect_fail:
            if expect_fail is True:
                expect_fail = " ".join(args)
            self.assertIs(
                self.cmd.returncode, 0,
                expect_fail + (" : %sret=%d: %s" % (self.error,
                                                    self.cmd.returncode,
                                                    ret[1])))
        return [self.cmd.returncode] + list(ret)

    def enableSshKey(self):
        self.runCmd(TEST, "cp -f ~/.ssh/authorized_keys_ ~/.ssh/authorized_keys")

    def disableSshKey(self):
        self.runCmd(TEST, "rm -f ~/.ssh/authorized_keys")
        
    def _run(self):
        try:
            self.orgtest()
        except KeyboardInterrupt:
            log.exception("Keyboard Interrupt")
            raise
        except:
            log.exception("Exception during test")
            raise
        finally:
            try:
                # Restore the tty in case ssh trashed it.
                termios.tcsetattr(sys.stdin, termios.TCSANOW, ORIG_TTY)
            except:
                pass
            

def CriticalTest(func):
    def _failingTest(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            THE_TEST._resultForDoCleanups.stop()
            raise
    return _failingTest

def init():
    global TESTUSER, TESTPASS, ORIG_TTY
    
    log.init("test")
    log.logger.setLevel(log.DEBUG)
    if "DISPLAY" in os.environ:
        del os.environ["DISPLAY"]
    
    if "TESTUSER" in os.environ:
        TESTUSER = os.environ["TESTUSER"]
    else:
        print ("The environment variable TESTUSER is not set. It must be set " +
               "to a test user")
        sys.exit(-1)

    ORIG_TTY = termios.tcgetattr(sys.stdin)

    # Make a test user password
    r = os.urandom(12)
    p = []
    for c in r:
        c = ord(c)
        if c & 0x8:
            p.append(chr(0x41 + c % 26))
        else:
            p.append(chr(0x61 + c % 26))
    TESTPASS = "".join(p)
    print "Will set the '%s' user's password to: %s" % (TESTUSER, TESTPASS)
