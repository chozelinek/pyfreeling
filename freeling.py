# -*- coding: utf8 -*-

import subprocess  # To run shell commands
import sys  # To use  the argv list
from lxml import etree  # To read an write XML files
import re  # To use regular expressions
import os
import glob
import argparse  # To parse command line arguments
import time
import fnmatch  # To match files by pattern

def timeit(method):
    """Time functions."""
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args,**kw)
        te = time.time()
        print('%r %2.2f sec' % \
              (method.__name__, te-ts))
        return result
    return timed

class freelingWrapper(object):
    """Wrap FreeLing."""

    @timeit
    def __init__(self):
        """Instantiate a wrapper."""
        self.cliparser()
        self.infiles = self.get_files(self.indir, self.pattern)
        self.main()

    def __str__(self):
        """Print final message."""
        nfiles = len(self.infiles)
        if nfiles == 1:
            message = [str(nfiles),"file processed!"]
        elif nfiles == 0:
            message = ["no file processed!"]
        else:
            message = [str(nfiles),"files processed!"]
        return " ".join(message)

    def cliparser(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s",
            "--source",
            required=True,
            help="path to directory where the source files are located.")
        parser.add_argument(
            "-t",
            "--target",
            required=True,
            help="path to the directory where the translations are located.")
        parser.add_argument(
            "-p",
            "--port",
            required=True,
            help="port number of the FreeLing server.")
        parser.add_argument(
            "-f",
            "--fpattern",
            required=False,
            help="pattern to find the relevant files.")
        parser.add_argument(
            "--sentence",
            action='store_true',
            help="if provided sentences are already tagged as XML.")
        parser.add_argument(
            "-e",
            "--element",
            required=True,
            help="element where text to be processed is contained")
        parser.add_argument(
            "-o",
            "--oformat",
#             required=True,
            default = 'flg',
            choices=['flg','vrt'],
            help="output format")
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
        self.oformat = args.oformat
        pass

    def get_files(self, directory, fileclue):
        """Get all files in a directory matching a pattern.
        
        Keyword arguments:
        directory -- a string for the input folder path
        fileclue -- a string as glob pattern
        """
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, fileclue):
                matches.append(os.path.join(root, filename))
        return matches

    def read_xml(self, infile):
        """Parse a XML file."""
        parser = etree.XMLParser(remove_blank_text=True)
        with open(infile, encoding='utf-8',mode='r') as input:
            return etree.parse(input, parser)

    def process_with_freeling(self, itext):
        """Process a string with FreeLing.
        
        Keyword arguments:
        itext -- a string containing input text to be processed
        """
        itext = re.sub(r'\"', r'\\"', itext)  # scape double quotation marks
        command = 'echo "{}" | analyzer_client {}'.format(  # create command string
            itext,
            self.port)
        process = subprocess.Popen(  # declare process
            command,
            stdout=subprocess.PIPE,
            stderr=None,
            shell=True)
        otext, error = process.communicate()  # run process
        otext = otext.decode("utf-8").strip()
        return otext

# for CWB encoding is not a problem if the XML is pretty,
# there is an option to cope with it at encoding
    def deprettyfy(self, tree):
        """Remove any indentation introduced by pretty print."""
        tree = etree.tostring(  # convert XML tree to string
            tree,
            encoding="utf-8",
            method="xml",
            xml_declaration=True).decode()
        tree = re.sub(  # remove trailing spaces before tag
            r"(\n) +(<)",
            r"\1\2",
            tree)
        tree = re.sub(  # put each XML element in a different line
            r"> *<",
            r">\n<",
            tree)
        tree = re.sub(  # put opening tag and FL output in different lines
            r"(<{}.+?>)".format(self.element),
            r"\1\n",
            tree)
        tree = re.sub(  # put FL output and closing tag in different liens
            r"(</{}>)".format(self.element),
            r"\n\1",
            tree)
        tree = re.sub(
            r"(>)([^.])",
            r"\1\n\2",
            tree)
        tree = re.sub(  # remove unnecessary empty lines
            r"\n\n+",
            r"\n",
            tree)
        return tree

    def serialize(self, tree_as_string, infile):
        """Serialize output.
        
        Keyword arguments:
        tree_as_string -- tree as string
        infile -- path to the input file as string
        """
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        outpath = os.path.join(  # output path
            self.outdir,
            os.path.splitext(os.path.basename(infile))[0]+'.'+self.oformat)  # depending on the output formats able to choose output extension
        with open(outpath, mode='w', encoding='utf8') as outfile:
            outfile.write(tree_as_string)
        pass
    
    def flg_to_vrt(self, tree):
        """Transform FreeLing output to VRT."""
        if self.sentence == True:
            sentences = tree.findall('.//{}'.format(self.element))
        else:
            sentences = tree.findall('.//{s}')
        for sentence in sentences:
            sentence.text = re.sub(r' ', r'\t', sentence.text) # to get VRT directly
            sentence.text = re.sub(r'\t\d(\.\d+)?$', r'', sentence.text, flags=re.MULTILINE) # to remove probability
        pass

    def main(self):
        """Process a batch of files with FreeLing."""
        for i in self.infiles:
            print(i)
            tree = self.read_xml(i)
            if self.sentence == True:
                sentences = tree.findall('.//{}'.format(self.element))
                for s in sentences:
                    if s.text == None:  # remove sentence element if empty
                        s.getparent().remove(s)
                    else:
                        s.text = u'{}'.format(
                            self.process_with_freeling(
                                s.text.strip('\n')))
            else:
                elements = tree.findall('.//{}'.format(self.element))
                if len(elements) == 0:
                    sys.exit('I cannot find any "{}"'.format(self.element))
                else:
                    sentence_counter = 0
                    for element in elements:
                        sentences = self.process_with_freeling(
                            element.text.strip('\n')).split('\n\n')
                        element.text = None
                        for sentence in sentences:
#                             sentence = re.sub(r'^(-se?) .+$',r'\1 se P0300000 1',sentence, flags=re.MULTILINE) # for Catalan
                            s_element = etree.SubElement(
                                element,
                                "s",
                                attrib={'id':'s_{}'.format(
                                    str(sentence_counter))})
                            s_element.text = u'\n{}\n'.format(sentence)
                            sentence_counter += 1
            if self.oformat == 'vrt':
                self.flg_to_vrt(tree)
            output = self.deprettyfy(tree)
            self.serialize(output, i)
print(freelingWrapper())
