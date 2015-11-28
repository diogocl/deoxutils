#!/usr/bin/env python
#-----------------------------------------------------------------------------
#         FILE: keygen.py
#        USAGE: keygen [-s]
#                   -s : include symbols
#  DESCRIPTION: Outputs a randomly key word. 
# REQUIREMENTS: .
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.2
#      CREATED: 11/07/2014
#      CHANGED: 28/11/2015
#-----------------------------------------------------------------------------

import os, sys
import random
import string
import signal

def main(chs, cnum):
    l = random.sample(chs, cnum)
    s = ''.join(l)
    print (s)

def _signal_handler(signal, frame):
        sys.exit(0)

def _usage(progname):
    print ("Usage: " + progname + " <options>")
    print ("    options:")
    print ("          -s      include symbols")

if __name__ == "__main__":
    signal.signal(signal.SIGABRT, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    try:
        ch_std = \
                string.digits + \
                string.ascii_uppercase + \
                string.ascii_lowercase

        if len(sys.argv) is 2:
            opt=sys.argv[1]
            if opt == "-s":
                ch_std = ch_std + string.punctuation
            else:
                _usage(sys.argv[0])
                raise Exception("bad arguments: " + str(sys.argv))
        main(ch_std, 16)
    except Exception as e:
        print (str(e))
        sys.exit(1)
