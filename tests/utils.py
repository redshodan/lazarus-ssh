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

import os, sys, unittest2

import log

##
## unittest behavior adjustment
##
class LsshTestCase(unittest2.TestCase):
    def __init__(self, name):
        unittest2.TestCase.__init__(self, name)
        self.orgtest = getattr(self, name)
        setattr(self, name, self._run)

    def setUp(self):
        unittest2.TestCase.setUp(self)
        log.info("=========Starting test: %s=========", str(self))

    def tearDown(self):
        unittest2.TestCase.tearDown(self)
        log.info("=========Ending test: %s=========", str(self))

    def _run(self):
        try:
            self.orgtest()
        except KeyboardInterrupt:
            log.exception("Keyboard Interrupt")
            raise
        except:
            log.exception("Exception during test")
            raise

class ModuleRef(object):
    def __init__(self, obj=None):
        self.__setobj__(obj)

    def __setobj__(self, obj):
        self.__dict__["__obj__"] = obj

    def __getattr__(self, name):
        if not self.__obj__:
            raise AttributeError("name")
        return getattr(self.__obj__, name)

    def __setattr__(self, name, val):
        self.__obj__.__setattr__(name, val)


def init():
    log.init("test")
    log.logger.setLevel(log.DEBUG)
