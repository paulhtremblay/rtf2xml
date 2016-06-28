#!/usr/bin/env python
import os, sys

command = 'scp *.html *.css paultremblay@shell.sourceforge.net:/home/groups/r/rt/rtf2xml/htdocs/docs'
print command
os.system(command)
