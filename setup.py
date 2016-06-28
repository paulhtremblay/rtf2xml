#!/usr/bin/env python
import sys, os, shutil
from distutils.core import setup

def remove_build():
    if os.path.isdir('build'):
        shutil.rmtree('build')

# get the script name
def get_script_name():
    if os.path.exists(os.path.join('scripts' , 'rtf2xml')):
        return os.path.join('scripts', 'rtf2xml')
    if os.path.exists(os.path.join('scripts', 'rtf2xml.py')):
        return os.path.join('scripts', 'rtf2xml.py')
    sys.stderr.write('Script not found\n')
    sys.stderr.write('Did you name it something other than rtf2xml.py?\n')
    sys.exit(1)

# remove_build()
script_name = get_script_name()

setup(name="rtf2xml",
    version= '1.33' ,
    description="Convert Microsoft RTF to XML",
    author="Paul Tremblay",
    author_email="paulhtremblay@gmail.com",
    license = 'MIT',
    url = "http://rtf2xml.sourceforge.net/",
    packages=['rtf2xml'],
    scripts=[script_name],
    # data_files = [
        # ('/usr/share/man/man1', ['data/rtf2xml.1']),
        # ],
    )







## os.remove('var_file')
