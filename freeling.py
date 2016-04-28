# -*- coding: utf8 -*-

# USAGE
"""
First, a FreeLing server process must be initialized:

analyze -f esm5.cfg --server --port 50116 &

Once the FreeLing server is running we can execute the script providing the following arguments:

python freeling_spa.py infile element outfile FreeLingClient
python freeling_spa.py infile.xml s 'analyzer_client 50116'
"""

# DESCRIPTION
"""
This script extracts all instances of a given element containing text in an XML file.
Element content can be only PCDATA, no mixed elements.
Output is incorporated into the XML.
We assume that the text is already splitted into sentences.
In fact, we expect to be reading sentences.
Therefore, we set AlwaysFlush=yes in the configuration file.
"""

# LICENSE
"""
Author: José Manuel Martínez Martínez <jmmtra@gmail.com>
Created: April 2015
License: CC-BY
"""
import subprocess # To run shell commands
import sys # To use the argv list
from lxml import etree # To read an write XML files
import re # To use regular expressions
import os
import glob
import argparse
import time
import fnmatch # To match files by pattern


# reload(sys)
# sys.setdefaultencoding('utf-8')

#===============================================================================
# Function to time functions
#===============================================================================
        
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args,**kw)
        te = time.time()

#         print '%r (%r, %r) %2.2f sec' % \
#               (method.__name__, args, kw, te-ts)
        print('%r %2.2f sec' % \
              (method.__name__, te-ts))
        return result

    return timed

class freelingWrapper(object):
    """Wraps FreeLing!"""

    @timeit
    def __init__(self):
        self.indir = ''
        self.outdir = ''
        self.pattern = ''
        self.port = ''
        self.cliparser()
        self.infiles = self.get_files(self.indir,self.pattern) # corpus name where to perform the analysis
        self.main() # function running in the background
        
    def __str__(self):
        message = ["files processed!"]
#         message = [str(len(self.infiles)),"files processed!"]
        return " ".join(message)
    
    def cliparser(self):
        #===============================================================================
        # Parse command-line arguments
        #===============================================================================
        parser = argparse.ArgumentParser()
        parser.add_argument("-s","--source", required=True, help="path to directory where the source files are located.")
        parser.add_argument("-t","--target", required=True, help="path to the directory where the translations are located.")
        parser.add_argument("-p","--port", required=True, help="port number of the FreeLing server.")
        parser.add_argument("-f","--fpattern", required=False, help="pattern to find the relevant files.")
        parser.add_argument("--sentence", action='store_true', help="if provided sentences are already tagged as XML.")
        parser.add_argument("-e","--element", required=True, help="element where text to be processed is contained")
        args = parser.parse_args()
        self.indir = args.source
        self.outdir = args.target
        if args.fpattern == None:
            self.pattern = "*.*"
        else:
            self.pattern = args.fpattern
        self.port = args.port
        self.sentence = args.sentence
        self.element = args.element
#         if not os.path.exists(self.outdir):
#             os.makedirs(self.outdir)
        pass

    # Function to get all files in a directory
    def get_files(self, directory, fileclue):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, fileclue):
                matches.append(os.path.join(root, filename))
        return matches    
    
    def read_xml(self,infile):
        """Parse the XML file."""
        parser = etree.XMLParser(remove_blank_text=True)
        with open(infile, encoding='utf-8',mode='r') as input:
            return etree.parse(input, parser)
        
    def remove_leading_spaces(self,input):
        input = input.split('\n')
        counter = 0
        for i in input:
            del input[counter]
            input.insert(counter,i.lstrip())
            counter +=1
        return '\n'.join(input)
    
    def rename_element(self,root,xpathold,newtag):
        elements = root.findall(xpathold)
        for element in elements:
            element.tag = newtag
        pass
    
    def process_with_freeling(self,itext):
        itext = re.sub(r'\"', r'\\"', itext)
        command = 'echo "{}" | analyzer_client {}'.format(itext,self.port)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        otext, error = process.communicate()
        otext = otext.decode("utf-8").strip()
        return otext
    
    def deprettyfy(self,tree):
        # tree to string
        tree = etree.tostring(tree, encoding="utf-8", method="xml", xml_declaration=True).decode()
        tree = re.sub(r"(\n) +(<)", r"\1\2", tree)
        tree = re.sub(r"> *<", r">\n<", tree)
        tree = re.sub(r"(<{}.+?>)".format(self.element),r"\1\n", tree)
        tree = re.sub(r"(</{}>)".format(self.element),r"\n\1", tree)
        tree = re.sub(r"\n\n+", r"\n", tree)
        # save
        return tree
        
    def serialize(self,tree_as_string,infile):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        outpath=  os.path.join(self.outdir,os.path.basename(infile))
        with open(outpath, mode='w', encoding='utf8') as outfile:
            outfile.write(tree_as_string)
        pass

    def main(self):
        for i in self.infiles:
            print(i)
            tree = self.read_xml(i)
            if self.sentence == True:
                sentences = tree.findall('.//{}'.format(self.element))
                for s in sentences:
                    # remove sentence element if empty
                    if s.text == None:
                        s.getparent().remove(s)
                    else:
                        s.text = u'{}'.format(self.process_with_freeling(s.text.strip('\n')))
            else:
                elements = tree.findall('.//{}'.format(self.element))
                if len(elements) == 0:
                    sys.exit('I cannot find any "{}"'.format(self.element))
                    # stop execution
                else:
                    sentence_counter = 0
                    for element in elements:
                        sentences = self.process_with_freeling(element.text.strip('\n')).split('\n\n')
                        element.text = None
                        for sentence in sentences:
                            s_element = etree.SubElement(element, "s", attrib={'id':'s_{}'.format(str(sentence_counter))})
                            s_element.text = u'\n{}\n'.format(sentence)
                            sentence_counter += 1
                        
#                         element.text = self.process_with_freeling(element.text.strip('\n'))
#             print etree.tostring(tree, encoding="utf-8", method="xml", xml_declaration=True)
            output = self.deprettyfy(tree)
            self.serialize(output,i)

print(freelingWrapper())