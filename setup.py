#!/usr/bin/python
# -*- coding: latin-1 -*-

#
# The ManPageFormatter and build_manpage were borrowed from:
# http://crunchyfrog.googlecode.com/svn/tags/0.3.4/utils/command/build_manpage.py
#

import sys, os, optparse, datetime
from distutils.command.build import build
from distutils.errors import DistutilsOptionError
from distutils.core import setup, Command

import imp
lssh = imp.load_source("lssh", "lssh")
# Remove the compiled file, ignore failures
try:
    os.unlink("lsshc")
except:
    pass

MANDIR = "man/man1"
BUILD_MANDIR = os.path.join("build", MANDIR)
BUILD_MANPAGE = os.path.join(BUILD_MANDIR, "lssh.1")
COPYRIGHT = \
  ("Copyright © 2012 Chris Newton. License GPLv2: GNU GPL version 2 " +
  "<http://gnu.org/licenses/gpl.html>. This is free software: you are free " +
  "to change and redistribute it.  There is NO WARRANTY, to the extent " +
  "permitted by law.")

parser = None

class ManPageFormatter(lssh.LongHelpFormatter):

    def __init__(self, indent_increment=2, max_help_position=24,
                 width=None, short_first=1):
        """Constructor. Unfortunately HelpFormatter is no new-style class."""
        lssh.LongHelpFormatter.__init__(self, True, indent_increment,
                                        max_help_position, width, short_first)

    def _markup(self, txt):
        """Prepares txt to be used in man pages."""
        return txt.replace('-', '\\-')

    def format_usage(self, usage):
        """Formate the usage/synopsis line."""
        return self._markup(usage)

    def format_heading(self, heading):
        """Format a heading.
        If level is 0 return an empty string. This usually is the string
        'Options'.
        """
        if self.level == 0:
            return ''
        return '.TP\n%s\n' % self._markup(heading.upper())

    def format_option(self, option):
        """Format a single option.
        The base class takes care to replace custom optparse values.
        """
        result = []
        opts = self.option_strings[option]
        result.append('.TP\n.B %s\n' % self._markup(opts))
        if option.long_help:
            option.help = option.long_help
        if option.help:
            help_text = '%s\n' % self._markup(self.expand_default(option))
            result.append(help_text)
        return ''.join(result)


class build_manpage(Command):

    description = 'Generate man page.'

    user_options = [('output=', 'O', 'output file')]

    def initialize_options(self):
        if not os.path.isdir(BUILD_MANDIR):
            os.makedirs(BUILD_MANDIR)
        self.output = BUILD_MANPAGE
        self.parser = None

    def finalize_options(self):
        parser.formatter = ManPageFormatter()
        parser.formatter.set_parser(parser)
        self.announce('Writing man page %s' % self.output)
        self._today = datetime.date.today()

    def _markup(self, txt):
        return txt.replace('-', '\\-')

    def _write_header(self):
        appname = self.distribution.get_name()
        ret = []
        ret.append('.TH %s 1 %s\n' % (self._markup(appname),
                                      self._today.strftime('%Y\\-%m\\-%d')))
        description = self.distribution.get_description()
        if description:
            name = self._markup('%s - %s' % (self._markup(appname),
                                             description.splitlines()[0]))
        else:
            name = self._markup(appname)
        ret.append('.SH NAME\n%s\n' % name)
        synopsis = parser.get_usage()
        if synopsis:
            synopsis = synopsis.replace('%s ' % appname, '')
            ret.append('.SH SYNOPSIS\n.B %s\n%s\n' % (self._markup(appname),
                                                      synopsis))
        long_desc = self.distribution.get_long_description()
        if long_desc:
            ret.append('.SH DESCRIPTION\n%s\n' % self._markup(long_desc))
        return ''.join(ret)

    def _write_options(self):
        ret = ['.SH OPTIONS\n']
        ret.append(parser.format_option_help())
        return ''.join(ret)

    def _write_footer(self):
        ret = []
        appname = self.distribution.get_name()
        author = '%s <%s>' % (self.distribution.get_author(),
                              self.distribution.get_author_email())
        ret.append(('.SH AUTHOR\n.B %s\nwas written by %s.\n'
                    % (self._markup(appname), self._markup(author))))
        ret.append((".SH COPYRIGHT\n" + COPYRIGHT + "\n"))
        homepage = self.distribution.get_url()
        ret.append(('.SH DISTRIBUTION\nThe latest version of %s may '
                    'be downloaded from\n'
                    '.UR %s\n.UE\n'
                    % (self._markup(appname), self._markup(homepage),)))
        ret.append('.SH "SEE ALSO"\n.BR ssh(1)\n')
        return ''.join(ret)

    def run(self):
        manpage = []
        manpage.append(self._write_header())
        manpage.append(self._write_options())
        manpage.append(self._write_footer())
        stream = open(self.output, 'w')
        stream.write(''.join(manpage))
        stream.close()

build.sub_commands.append(('build_manpage', None))


if __name__=='__main__':
    parser = lssh.buildParser(False, "lssh")
    setup(name="lssh",
          version=lssh.version,
          description="resurrecting SSH from the dead",
          long_description=lssh.LONG_DESC,
          author="Chris Newton",
          author_email="redshodan@gmail.com",
          license="GNU GPL v2",
          url="http://code.google.com/p/lazarus-ssh/",
          data_files=[('man/man1', [BUILD_MANPAGE])],
          scripts=['lssh', 'lssh'],
          cmdclass={'build_manpage': build_manpage},
          )
