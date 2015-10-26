'''
Created on 25 Oct 2015

@author: davidwright

saxfinder.py - generates HTML from pyxml.xml

'''

import sys

from xml.sax import make_parser
from xml.sax import ContentHandler

class FileHandler(ContentHandler):

    def __init__(self, contentType):
        self.getCont = 0
        self.contents = ""
        self.filename = ""
        self.contentType = contentType

    def startElement(self, name, attrs):
        if name == "file":
            self.filename = attrs.get('name', "")
        elif name == "contents":
            self.getCont = 1
    
    def characters(self, ch):
        if self.getCont:
            self.contents += ch
    
    def endElement(self, name):
        if name == "contents":
            self.getCont = 0
            if self.contents.find(self.contentType) > 1:
                print self.filename, "has", self.contentType, "content."
            self.contents = ""

fh = FileHandler(sys.argv[1])
parser = make_parser( )
parser.setContentHandler(fh)
parser.parse(sys.stdin)
    