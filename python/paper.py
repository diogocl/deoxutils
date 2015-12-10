#!/usr/bin/env paper
#-----------------------------------------------------------------------------
#         FILE: paper.py
#        USAGE: paper
#  DESCRIPTION: Not ready yet!
# REQUIREMENTS: Needs the packages bibtexparser and xml.etree / dom.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.1
#      CREATED: 10/12/2015
#      CHANGED: 10/12/2015
#-----------------------------------------------------------------------------

import os, sys
import shutil
import signal
import re

import bibtexparser

import xml.dom.minidom as minidom
import xml.etree.cElementTree as cet
import xml.etree.ElementTree as et

bibfile = "test.bib"

""" Utilities functions:
======================== """
def _ch(text):
    if text[-1] is '/':
        return text[:-1]
    return text

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def printColor(color, vmsg):
    print (color + vmsg + bcolors.ENDC)

class bibTex:
    """ A class to handle bibtex (*.bib) files. """
    def readFile(self, fname):
        try:
            with open(bibfile) as bibtex_file:
                bibtex_str = bibtex_file.read()
                self.bibdb = bibtexparser.loads(bibtex_str)
            self.fname = fname
        except IOError as e:
            print("I/O error({0}): '%s': {1}".\
                    format(e.errno, e.strerror) % fname)
        except:
            print("Unexpected error:", sys.exc_info()[0])

"""
@function: _signal_handler
@brief: Exit if reach here
"""
def _signal_handler(signal, frame):
    print (bcolors.WARNING + "Reached signal handler, exiting" + bcolors.ENDC)
    sys.exit(0)

"""
@function: _usage
@brief: Helper usage function
"""
def _usage(progname):
    printColor(bcolors.WARNING, "Usage: " + progname + " <video-output>")

""" Entry point
=============== """
if __name__ == "__main__":
    signal.signal(signal.SIGABRT, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    try:
        b = bibTex();
        b.readFile(bibfile);
        print(b.bibdb.entries)
        #if len(sys.argv) < 2:
        #    _usage(sys.argv[0])
        #    raise Exception(bcolors.FAIL + "Bad arguments: " + str(sys.argv))
        #main(sys.argv[1:])
    except Exception as e:
       print (str(e) + bcolors.ENDC)
       sys.exit(1)
