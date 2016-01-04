#!/usr/bin/env python
#-----------------------------------------------------------------------------
#         FILE: paper.py
#        USAGE: paper
#  DESCRIPTION: Not ready yet!
# REQUIREMENTS: Needs the packages bibtexparser, xml.etree and.
#       AUTHOR: Diogo Luvizon <diogo@luvizon.com>
#      VERSION: 0.1
#      CREATED: 10/12/2015
#      CHANGED: 04/01/2016
#-----------------------------------------------------------------------------
import os, sys
import shutil
import signal
import re

import bibtexparser

import xml.etree.ElementTree as ET

bibfile = "test.bib"
inputfile = "paper.xml"

""" Holds the version of the interpreter of this f* language, because some
functions have changed after some *improved* new versions... """
_version = sys.version_info[0] + sys.version_info[1] / 10;

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

def userInput(msg, expected=[], retry=False):
    if len(expected):
        h = re.sub(r"[^A-Za-z1-9,]+", '', str(expected))
        h = h.replace(',', '/')
        expected = h.split('/')
    else:
        h = '*'
    while True:
        if _version > 3.0:
            var = input("%s (%s): " % (msg, h))
        else:
            var = raw_input("%s (%s): " % (msg, h))
        if len(expected) == 0:
            return var
        for e in expected:
            if var == e:
                return var
        if not retry:
            raise ValueError("Invalid user input")
        printColor(bcolors.WARNING, "Bad answer! Try again.")

def userBoolInput(msg, default=False):
    yes = set(['Y', 'y', 'YES', 'YEs', 'Yes', 'yes', 'ye', 'ys', 'yeah',])
    if default:
        if _version > 3.0:
            var = input("%s (Y/n): " % msg)
        else:
            var = raw_input("%s (Y/n): " % msg)
    else:
        if _version > 3.0:
            var = input("%s (y/N): " % msg)
        else:
            var = raw_input("%s (y/N): " % msg)
    if len(var) == 0:
        return default
    if var in yes:
        return True
    return False

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
        
class database:
    """ A class to store the informations about a given database. """
    def readFile(self, fname):
        try:
            self.fname = fname
            tree = ET.parse(fname)
            root = tree.getroot()
            for child in root:
                if child.tag in "config":
                    self.parseConfig(child)
                if child.tag in "entries":
                    self.parseEntries(child)
            printColor(bcolors.HEADER, "File '%s' read, %d entries found." %
                       (fname ,self.items))
        except IOError as e:
            raise IOError("Could not read file")
        except:
            print("Unexpected error:", sys.exc_info()[0])
    
    def parseConfig(self, cfg):
        for child in cfg:
            if child.tag in "database":
                self.db_path = child.get("path")
            if child.tag in "bibtex":
                self.bi_path = child.get("path")
    
    def parseEntries(self, ent):
        self.items = int(ent.get("items"))
        for child in ent:
            print child.tag
    
    def newFile(self, fname):
        self.root = ET.Element("root")
        config = ET.SubElement(self.root, "config")
        database = ET.SubElement(config, "database")
        database.set('path', './database')
        bibtex = ET.SubElement(config, "bibtex")
        bibtex.set('path', './bibtex')
        entries = ET.SubElement(self.root, "entries")
        entries.set('items', '0')
        self.tree = ET.ElementTree(self.root)
        self.tree.write(fname)
        print("Creating a new XML file...")

class PaperHMI:
    """ The human-machine interface class. """
    def __init__(self, db):
        self.db = db
    
    def loop(self):
        self.listAll()
        var = userInput("Add, remove, or edit an article entry",
                        expected=["a", "r", "e"], retry=True)
        if var in "a":
            self.add()
        elif var in "r":
            self.rm()
        elif var in "e":
            self.edit()
    
    def listAll(self):
        for i in range(0, self.db.items):
            print ("list entry %d ..." % i)
    
    def add(self):
        printColor(bcolors.OKGREEN, "Adding a new entry...")
        pdf = self.checkFile("\tPDF file path")
        bib = self.checkFile("\tBibtex file path")

    def checkFile(self, msg):
        while True:
            fname = userInput(msg)
            if os.path.isfile(fname):
                return fname
            printColor(bcolors.FAIL, "File '%s' does not exist!" % fname)

    def rm(self):
        print "rm..."

    def edit(self):
        print "edit..."

"""
@function: _signal_handler
@brief: Exit if reach here
"""
def _signal_handler(signal, frame):
    print("\n" + bcolors.WARNING + \
          "Reached signal handler, exiting" + bcolors.ENDC)
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
    #b = bibTex();
    #b.readFile(bibfile);
    #print(b.bibdb.entries)
    x = database();
    try:
        x.readFile(inputfile)
        hmi = PaperHMI(x)
        hmi.loop()
    except IOError as e:
        printColor(bcolors.FAIL, "%s: %s" % (inputfile, e))
        if userBoolInput("Want to create a new empty file?", True):
            x.newFile(inputfile)
        
        #userInput("teste 123", expected=["Y", "y", "n"], retry=True)
        #userInput("teste 123", expected=["Y", "y", "n"], retry=False)
        
            
        #if len(sys.argv) < 2:
        #    _usage(sys.argv[0])
        #    raise Exception(bcolors.FAIL + "Bad arguments: " + str(sys.argv))
        #main(sys.argv[1:])
    #except Exception as e:
    #   print (str(e) + bcolors.ENDC)
    #   sys.exit(1)
