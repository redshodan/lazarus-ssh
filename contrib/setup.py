#!/usr/bin/python

from distutils.core import setup, Extension

if __name__=='__main__':
    setup(name="lssh",
          description="",
          author="James Newton",
          license="GNU GPL",
          
          package_dir={"": "src"},
          packages=["lssh"],
          ext_package="lssh",
          ext_modules=[Extension("sendfd", ["src/lssh/sendfd.c"],
                                 extra_compile_args=['-Werror'])])
