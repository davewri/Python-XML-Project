'''
Created on 25 Oct 2015

@author: davidwright
'''

import os
from xml.sax import ContentHandler

class SAXThumbs(ContentHandler):
    """
    This is the SAX handler that generates a full-
    image display (an .html page) for each image file
    contained in the XML file.
    
    It also adds an anchor on the thumbs page showing
    the thumbnail, and linking to the big image page
    that was created first.
    """
   
    def __init__(self, thumbsFilename):
        self.filename = thumbsFilename
        
    def startDocument(self):
        self.fd = open(self.filename, "w")
        self.fd.write("<html><body>\n")
    
    def endDocument(self):
        self.fd.write("<html><body>\n")
        self.fd.close( )
    
    def startElement(self, name, attrs):
        if name == "file":
            filename = attrs.get("name", "")
            
            #pull out just the filename
            dir, localname = os.path.split(filename)
            localname, ext = os.path.splitext(localname)
            
            if localname.startswith("t-") and ext == ".jpg":
                #create anchor tag in thumbs.html
                fullImgLink = localname[2:] + ".html"
                self.fd.write('<br><a href="%s"><img src="%s%s"></a>\n'
                              % (fullImgLink, localname, ext))
            fullImageFile = os.path.join(dir, localname) + ".html"
            print "Will create:", fullImageFile
            fullImageHTML = ('<html><body><img src="%s%s"></body></html>\n'
                             % (localname, ext))
            lfd = open(fullImageFile, "w")
            lfd.write(fullImageHTML)
            lfd.close(  )
            
        