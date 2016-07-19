#!/usr/bin/env python
import sys, os, shutil
from distutils.core import setup


# get the script name
def get_script_name():
    if os.path.exists(os.path.join('scripts', 'rtf2xml.py')):
        return os.path.join('scripts', 'rtf2xml.py')
    sys.stderr.write('Script not found\n')
    sys.exit(1)

script_name = get_script_name()

setup(name="rtf2xml",
    version= '1.33' ,
    description="Convert Microsoft RTF to XML",
    author="Paul Tremblay",
    author_email="paulhtremblay@gmail.com",
    license = 'MIT',
    url = "https://github.com/paulhtremblay/rtf2xml",
    packages=['rtf2xml'],
    scripts=[script_name],
    )
