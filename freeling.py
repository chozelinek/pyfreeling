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
            default = 'flg',
            choices=['flg','vrt','conll','xml'],
            help="output format")
        parser.add_argument(
            "--constituency",
            action='store_true',
            help="if provided output are constituents. Only meaningful in combination with --oformat xml."
            )
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
        self.constituency = args.constituency
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
    def unprettify(self, tree):
        """Remove any indentation introduced by pretty print."""
        tree = etree.tostring(  # convert XML tree to string
            tree,
            encoding="utf-8",
            method="xml",
            xml_declaration=True).decode(encoding='UTF-8')
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
            sentences = tree.findall('.//s')
        for sentence in sentences:
            sentence.text = re.sub(r' ', r'\t', sentence.text) # to get VRT directly
            sentence.text = re.sub(r'\t\d(\.\d+)?$', r'', sentence.text, flags=re.MULTILINE) # to remove probability
            sentence.text = re.sub(r'^(.+?)\t(.+?)\t(.+?)$', r'\1\t\3\t\2', sentence.text, flags=re.MULTILINE) # to remove probability
        pass
    
    def get_leafs(self, sentence):
        """Get leaf nodes from constituency tree.
        
        Keyword arguments:
        sentence -- XML element containing a parsed sentence
        """
        counter = 0
        nodes = sentence.find('./constituents/node')
        s = etree.Element('s')
        s.append(nodes)
        leafs = s.findall('.//node[@leaf]')
        for leaf in leafs:
            ancestors = leaf.iterancestors(tag='node')
            depth = sum([1 for x in ancestors])
            if re.match(r'.+_.+',leaf.attrib['word']):
                words = leaf.attrib['word'].split('_')
                leaf.attrib['word'] = words[0]
                leaf.attrib['token'] = 't_'+str(counter)
                leaf.attrib['depth'] = str(depth)
                leaf.text = '\n{}\n'.format(words[0])
                counter += 1
                parent = leaf.getparent()
                leaf_counter = 2
                for word in words[1:]:
                    child = etree.SubElement(parent, 'node')
                    child.text = '\n{}\n'.format(word)
                    child.attrib['leaf'] = str(leaf_counter)
                    leaf_counter += 1
                    child.attrib['token'] = 't_'+str(counter)
                    counter += 1
                    child.attrib['word'] = word
                    child.attrib['depth'] = str(depth)
                    if 'head' in leaf.attrib:
                        child.attrib['head'] = leaf.attrib['head']
            else:
                leaf.text = '\n{}\n'.format(leaf.attrib['word'])
                leaf.attrib['depth'] = str(depth)
                leaf.attrib['token'] = 't_'+str(counter)
                counter += 1
        return s
                
    def get_constituency(self, element):
        """Get constituency parsing of the text contained in a XML element.
        
        Keyword arguments:
        element -- XML element containing text to be parsed.
        """
        analysis = self.process_with_freeling(element.text.strip('\n'))
        analysis = etree.fromstring('<analysis>'+analysis.strip('\n')+'</analysis>')
        if self.sentence is True:
            sentence = analysis.find('.//sentence')
            element.text = None
            parsed_sentence = self.get_leafs(sentence)
            element.getparent().replace(element, parsed_sentence)
        else:
            sentences = analysis.findall('.//sentence')
            new_sentences = []
            for sentence in sentences:
                new_sentences.append(self.get_leafs(sentence))
            element.text = None
            for new_sentence in new_sentences:
                element.append(new_sentence)

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
                        if self.oformat == 'xml' and self.constituency is True:
                            self.get_constituency(s)
                        elif self.oformat == 'xml':
                            sys.exit("XML output only for constituency!")
                        else:
                            s.text = u'{}'.format(
                                        self.process_with_freeling(
                                            s.text.strip('\n')))
            else:
                elements = tree.findall('.//{}'.format(self.element))
                if len(elements) == 0:
                    sys.exit('I cannot find any "{}"'.format(self.element))
                else:
                    for element in elements:
                        if self.oformat == 'xml' and self.constituency is True:
                            self.get_constituency(element)
                        elif self.oformat == 'xml':
                            sys.exit("XML output only for constituency!")
                        else:
                            sentences = self.process_with_freeling(
                                element.text.strip('\n')).split('\n\n')
                            element.text = None
                            for sentence in sentences:
                                s_element = etree.SubElement(element, "s")
                                s_element.text = u'\n{}\n'.format(sentence)
            if self.oformat == 'vrt':
                self.flg_to_vrt(tree)
            output = self.unprettify(tree)
            self.serialize(output, i)
print(freelingWrapper())
