#!/usr/bin/env python3

import os
import sys
import shutil

from setuptools import setup
from distutils.core import Extension
from distutils.command.build_ext import build_ext

NAME = 'komodo-python3-dbgp'


class Dbgp_build_ext(build_ext):
    # a fake build_ext, copy our provided pre-built binaries to the right target

    def build_extensions(self):
        scriptdir = os.path.dirname(os.path.abspath(sys.argv[0]))
        # weird, for me plat_name is 'linux-i686' on a 32bit linux
        if 'win32' in self.plat_name:
            plat = 'win32-x86'
        elif 'linux' in self.plat_name:
            if '64' in self.plat_name:
                plat = 'linux-x86_64'
            else:
                plat = 'linux-x86'
        sourcepath = os.path.join(scriptdir, 'libs', plat)
        if os.path.exists(sourcepath):
            # not all platforms have binaries
            buildpath = os.path.dirname(self.get_ext_fullpath('dbgp._client'))
            targetpath = os.path.join(os.getcwd(), buildpath)

            for fn in os.listdir(sourcepath):
                src = os.path.join(sourcepath, fn)
                tgt = os.path.join(targetpath, fn)
                shutil.copyfile(src, tgt)

            print(NAME)
            print("prebuilt binaries were copied")


setup(
    name=NAME,
    version='11.1.2.hath1',
    description='The ActiveState Komodo DBGP server',

    author="Shane Caraveo, Trent Mick",
    author_email="komodo-feedback@ActiveState.com",
    maintainer='Alex Hathaway',
    maintainer_email='alex@hathaway.xyz',

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],


    url='http://github.com/agroszer/komodo-python3-dbgp',
    packages=['dbgp'],
    scripts=['bin/pydbgp',
             'bin/pydbgpproxy'],
    zip_safe=False,

    ext_modules=[Extension("dbgp._client", ["_client.c"])],  # dummy
    cmdclass={"build_ext": Dbgp_build_ext},  # WE provide our own build
)
