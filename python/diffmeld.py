#!/usr/bin/env python
#-----------------------------------------------------------------------------
#         FILE: diffmeld.py
#        USAGE: diffmeld [file1] [file2]
#  DESCRIPTION: Call the meld program. Used was a wrapper to meld when using
#               git diff command.
# REQUIREMENTS: Needs meld and git installed in the system.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

import sys
import os
import re

try:
    os.system('meld "%s" "%s"' % (sys.argv[2], sys.argv[5]))
except:
    print (str(sys.argv[0]) + ': error!')
    print ('Do you have the program "meld" installed in your system?')
    exit(1)
