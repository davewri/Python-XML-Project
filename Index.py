'''
Created on 23 Oct 2015

@author: davidwright

usage: python index.py <starting dir> <output dir>

'''

import os
import sys


from os import stat
from os import listdir
from os import popen
from stat import S_ISDIR
from time import ctime

from xml.sax.saxutils import escape
from __builtin__ import str

XML_ENC = "ISO-8859-1"

class Index:
    '''
    This class indexes files and builds
    a resultant XML document
    '''


    def __init__(self, startingDir, outputFile):
        '''
        init: sets output file
        '''
        self.outputFile = outputFile
        self.startingDir = startingDir
    
    def indexDirectoryFiles(self, dir):
        """ Index a directory structure and creates an XML output file """
        #prepare output XML file
        self.__fd = open(self.outputFile, "w")
        self.__fd.write('<?xml version="1.0" encoding="' +
                        XML_ENC + '"?>\n')
        self.__fd.write("<IndexedFiles>\n")
        
        # do actual indexing
        self.__indexDir(dir)
        
        #Close out XML file
        self.__fd.write("</IndexedFiles>\n")
        self.__fd.close()
        
    def __indexDir(self, dir):
        """ Recursive function to do the actual indexing """
        
        #Create an indexFile for each regular file
        #and call the function again for each directory
        files = listdir(dir)
        for file in files:
            fullname = os.path.join(dir, file)
            st_values = stat(fullname)
            
            #Check if its a directory
            if S_ISDIR(st_values[0]):
                print file
                
                #Create directory element
                self.__fd.write("<Directory ")
                self.__fd.write(' name="' + escape(fullname) + '">\n')
                self.__indexDir(fullname)
                self.__fd.write("</Directory>\n")
            else:
                #Create regular file entry
                print dir + file
                lf = IndexFile(fullname, st_values)
                self.__fd.write(lf.getXML( ))

#CLASS: IndexFile(filename, stat-tuple)                
class IndexFile:
    """
    Simple file representation object with XML
    """
    def __init__(self, filename, st_vals):
        """Extract properties from supplied stat object """
        self.filename = filename
        self.uid = st_vals[4]
        self.gid = st_vals[5]
        self.size = st_vals[6]
        self.accessed = ctime(st_vals[7])
        self.modified = ctime(st_vals[8])
        self.created = ctime(st_vals[9])
        
        #try for filename extension
        self.extension = os.path.splitext(filename)[1]
        
        #check contents using file command on linux
        if os.name == "posix":
            #open a process to check the file contents
            fd = popen("file \"" + filename + "\"")
            self.contents = fd.readline().strip( )
            fd.close()
            
        else:
            #No content information
            self.contents = self.extension
            
    def getXML(self):
        """Returns XML version of all data members """
        return ("<file name=\"" + escape(self.filename) + "\">" +
                "\n<userID>" + str(self.uid) + "</userID>" +
                "\n<groupID>" + str(self.gid) + "</groupID>" +
                "\n<size>" + str(self.size) + "</size>" +
                "\n<lastAccessed>" + str(self.accessed) + "</lastAccessed>" +
                "\n<lastModified>" + str(self.modified) + "</lastModified>" +
                "\n\t<created>" + str(self.created) + "</created>" +
                "\n\t<extension>" + str(self.extension) + "</extension>" +
                "\n\t<contents>" + str(self.contents) + "</contents>" +
                "\n</file>")
        

if __name__ == "__main__":
    index = Index(sys.argv[1], sys.argv[2])
    print "Starting Dir:" , index.startingDir
    print "Output file:" , index.outputFile
    
    index.indexDirectoryFiles(index.startingDir)
    
            
        
    
                
        
                        
        