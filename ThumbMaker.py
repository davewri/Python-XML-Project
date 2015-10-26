'''
Created on 25 Oct 2015

@author: davidwright
'''

import sys

from xml.sax import make_parser
from SAXThumbs import SAXThumbs

ch = SAXThumbs(sys.argv[1])
parser = make_parser( )

parser.setContentHandler(ch)
parser.parse(sys.stdin)
