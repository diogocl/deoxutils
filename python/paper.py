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
from pip.locations import src_prefix
from xml.dom import minidom

inputfile = ".paper.xml"
database_path = ".database"
bibtex_path = ".bibtex"

# Targets used to build the link scheme
targets = ['author', 'year', 'journal']

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

def mkDir(path):
    if os.path.isdir(path) is False:
        os.mkdir(path)

def prettify(elem):
    """ Return a pretty-printed XML string for the Element. """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

class bibTex:
    """ A class to handle bibtex (*.bib) files. """
    def readFile(self, fname):
        try:
            with open(fname) as bibtex_file:
                bibtex_str = bibtex_file.read()
                self.bibdb = bibtexparser.loads(bibtex_str)
            self.fname = fname
        except IOError as e:
            print("I/O error({0}): '%s': {1}".\
                    format(e.errno, e.strerror) % fname)
        except:
            print("Unexpected error:", sys.exc_info()[0])
    
    def writeFile(self, fname):
        try:
            btex = bibtexparser.dumps(self.bibdb)
            fd = open(fname, 'w')
            fd.write(btex.encode('utf8', 'replace'))
            fd.close()
        except IOError as e:
            print("I/O error({0}): '%s': {1}".\
                    format(e.errno, e.strerror) % fname)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        
class database:
    def __init__(self, fname):
        self.fname = fname
        self.items = 0
        self.db_path = database_path
        self.bi_path = bibtex_path
    
    """ A class to store the informations about a given database. """
    def readFile(self):
        try:
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(self.fname, parser=parser)
            self.root = tree.getroot()
            for child in self.root:
                if child.tag in "config":
                    self.parseConfig(child)
                if child.tag in "entries":
                    self.parseEntries(child)
            printColor(bcolors.HEADER, "File '%s' read, %d entries found." %
                       (self.fname, self.items))
        except IOError as e:
            raise IOError("Could not read file")
    
    def parseConfig(self, cfg):
        for child in cfg:
            if child.tag in "database":
                self.db_path = child.get("path")
            if child.tag in "bibtex":
                self.bi_path = child.get("path")
    
    def parseEntries(self, ent):
        self.items = int(ent.get("items"))
        self.ids = []
        for child in ent:
            self.ids.append(child.tag)
    
    def writeXML(self):
        xmlstr = prettify(self.root)
        fd = open(self.fname, 'w')
        print("Creating a new XML file...")
        fd.write(xmlstr)
        fd.close()
    
    def newFile(self):
        self.root = ET.Element("root")
        config = ET.SubElement(self.root, "config")
        database = ET.SubElement(config, "database")
        database.set("path", self.db_path)
        bibtex = ET.SubElement(config, "bibtex")
        bibtex.set("path", self.bi_path)
        entries = ET.SubElement(self.root, "entries")
        entries.set('items', '0')
        self.tree = ET.ElementTree(self.root)
        self.writeXML()
    
    def add(self, b):
        for c in self.root:
            if c.tag in "entries":
                entries = c
                break
        newentry = ET.SubElement(entries, b.id)
        """ Write the new entry """
        for t in targets:
            newentry.set(t, getattr(b, t))
        newentry.set("id", b.id)
        self.items += 1
        entries.set('items', '%d' % self.items)
        self.tree = ET.ElementTree(self.root)
        self.writeXML()

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
            print ("%03d --- %s" % (i, self.db.ids[i]))

    def checkFile(self, msg):
        while True:
            fname = userInput(msg)
            if os.path.isfile(fname):
                return fname
            printColor(bcolors.FAIL, "File '%s' does not exist!" % fname)
    
    def parseBibtex(self, bib):
        b = bibTex()
        b.readFile(bib);
        entries = b.bibdb.entries[0]
        def notfound(label):
            raise ValueError("Label '%s' not found in the BibTeX file '%s'" \
                             % (label, bib))
        print ("\t-----------")
        label = u'ENTRYTYPE'
        if label in entries:
            print ("\t%s: %s" % (label, entries[label]))
        else:
            notfound(label)
        label = u'ID'
        if label in entries:
            print ("\t%s: %s" % (label, entries[label]))
        else:
            notfound(label)
        label = u'author'
        if label in entries:
            print ("\t%s: %s" % (label, entries[label]))
            b.author = re.findall(r"[\w']+", entries[label])[0]
        else:
            notfound(label)
        label = u'year'
        if label in entries:
            print ("\t%s: %s" % (label, entries[label]))
            b.year = entries[label]
        else:
            notfound(label)
        label = u'title'
        if label in entries:
            print ("\t%s: %s" % (label, entries[label]))
            entries[label] = '{%s}' % entries[label]
        else:
            notfound(label)
        label1 = u'booktitle'
        label1 = u'journal'
        if label1 in entries:
            print ("\t%s: %s" % (label1, entries[label1]))
            b.journal = entries[label1]
        elif label2 in entries:
            print ("\t%s: %s" % (label2, entries[label2]))
            b.journal = entries[label2]
        else:
            notfound('%s | %s' % (label1, label2)) 
        b.id = '%s%s' % (b.author, b.year)
        b.bibdb.entries[0][u'ID'] = b.id
        return b
    
    def makeLinks(self, b, src):
        for t in targets:
            p = t + "/" + getattr(b, t)
            mkDir(p)
            try:
                os.symlink("../../" + src, "%s/%s.pdf" % (p, b.id))
            except OSError as e:
                printColor(bcolors.FAIL, "%s/%s.pdf: %s" % (p, b.id, e))
    
    def add(self, pdf=None, bib=None, YES=False):
        printColor(bcolors.OKGREEN, "Adding a new entry...")
        if (pdf != None) and (not os.path.isfile(pdf)):
            printColor(bcolors.FAIL, "File '%s' does not exist!" % pdf)
            pdf = None
        if pdf == None:
            pdf = self.checkFile("\tPDF file path")
        if (bib != None) and (not os.path.isfile(bib)):
            printColor(bcolors.FAIL, "File '%s' does not exist!" % bib)
            bib = None
        if bib == None:
            bib = self.checkFile("\tBibtex file path")
        b = self.parseBibtex(bib)
        newpdf = "%s/%s.pdf" % (self.db.db_path, b.id)
        newbib = "%s/%s.bib" % (self.db.bi_path, b.id)
        shutil.copyfile(pdf, newpdf)
        b.writeFile(newbib)
        if YES or userBoolInput("Remove old files?", True):
            os.remove(pdf)
            os.remove(bib)
        self.makeLinks(b, newpdf)
        self.db.add(b)
    
    def rm(self):
        print "rm..."

    def edit(self):
        print "edit..."
        #b.writeFile("b.bib")

def _usage(arg0):
    print ('Usage: %s [PDF file] [Bibtex file]' % arg0)
    print ('       No arguments to enter in loop mode.\n')

""" Entry point
=============== """
if __name__ == "__main__":
    x = database(inputfile);
    try:
        x.readFile()
    except IOError as e:
        printColor(bcolors.FAIL, "%s: %s" % (inputfile, e))
        if userBoolInput("Want to create a new empty file?", True):
            x.newFile()
        else:
            exit();
    except ET.ParseError as e:
        printColor(bcolors.FAIL, "%s: %s" % (inputfile, e))
        exit()
    try:
        for t in targets:
            mkDir(t)
        hmi = PaperHMI(x)
        if len(sys.argv) is 1:
            hmi.loop()
        elif len(sys.argv) is 3:
            hmi.add(sys.argv[1], sys.argv[2], False)
        else:
            printColor(bcolors.FAIL, "\nBad arguments: %s\n" % str(sys.argv))
            _usage(sys.argv[0])
    except SystemExit as e:
        printColor(bcolors.WARNING,"\nSystemExit")
    except KeyboardInterrupt as e:
        printColor(bcolors.WARNING, "\nKeyboardInterrupt")
    except ValueError as e:
        printColor(bcolors.FAIL, "\nValueError: %s" % e)
    except:
        print("Unexpected error:", sys.exc_info()[0])