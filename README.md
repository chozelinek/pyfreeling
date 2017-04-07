# PyFreeLing

This is the documentation for a wrapper for FreeLing 4. This wrapper was developed to ease the processing of texts for my PhD. It is written in Python 3 and tested on macOS Sierra.

This project was started to meet my own needs. I don't plan to include extra features upon request. I don't provide any kind of support, specially regarding other platforms. But feel free to fork, clone and play with the code.

## Contents

```
├── README.md
├── config
├── freeling.py
├── freeling_constituency.py
├── test
└── test_freeling.sh
```

- `README.md`: this documentation
- `config/`: folder containing different analyzer's configuration files
- `freeling.py`: general wrapper for `VRT`, `XML` or plain text input formats outputing `VRT` or `CONLL` formats. <!-- this could be a script to serialize in VRT/XML format, each layer in a different VRT file, or in CONLL format, all in one tab/space-separated file. -->
- `freeling_constituents.py`, the wrapper for `vrt` input, `xml` output. The aim is to get constituency parsing in XML format. <!-- this could be a script to serialize layers in XML format like constituents -->
- `test/`: folder containing test data.
- `test_freeling.sh`: shell script to test English and Spanish basic processing.
<!-- We might need utilities to retokenize MWE in to individual tokens and keep MWE information as XML annotation -->
<!-- We need examples and tests. -->

## Setting up PyFreeLing in Mac OS Sierra

There are 4 types of dependencies:

- [Homebrew](https://brew.sh), a package manager to install software in Mac
- [FreeLing](http://nlp.lsi.upc.edu/freeling), an open source language analysis tool suite
- [Python 3](https://www.python.org)
- [lxml](http://lxml.de), a Python library to work with XML
- [libxml2](http://xmlsoft.org) and [libxslt](http://xmlsoft.org/libxslt) C libraries which are dependencies of `lxml`

### Install Homebrew

Follow [Neil Gee's guide](https://coolestguidesontheplanet.com/installing-homebrew-on-macos-sierra-package-manager-for-unix-apps) to install and set up homebrew for Mac OS Sierra

### Install FreeLing

Use Homebrew to install FreeLing by running this command:

```shell
brew install freeling
```

Homebrew will take care of any dependencies.

### Install Python 3

You can install Python 3 with Homebrew following the instructions from [The Hitchhiker's Guide to Python](http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/) or following the very complete [Lisa Tagliaferri's guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos).

Basically:

```shell
brew install python3
```

### Install libxml2 and libxslt

macOS Sierra already provides `libxml2` and `libxslt`. They can be installed through Homebrew though:

```shell
brew install libxml2
brew install libxslt
```

### Install lxml

Now, you are ready to install `lxml`:

```shell
pip3 install lxml
```

## Using PyFreeLing

Once you have installed FreeLing and all the dependencies, you will always do two things:

1. start a FreeLing analyzer in server mode
1. run the wrapper script

### Starting a FreeLing analyzer in server mode

As our wrapper is devised to process batches of files and each file can be split into smaller text units, we want to avoid the downtime of loading parameters for each (chunk of) text to be processed. If we start a server, parameters are loaded only once.

The options of the server can be declared in a configuration file or via command line options. Command line options override configuration file's directives.

For more details check the FreeLing documentation for the [analyzer](https://talp-upc.gitbooks.io/freeling-user-manual/content/analyzer.html).

A server to analyze texts in English with default options can be invoked with the following command:

```shell
analyze -f en.cfg --server --port 50005 &
```

You will see after a few seconds in the terminal window some information (like how to stop the server). Keep that terminal window open to monitor the server.

### Usage of freeling.py

Once a server is up and running we can use `freeling.py` to process the files. Below is an explanation of the options that can be passed to the wrapper.

```
usage: freeling.py [-h] -s SOURCE -t TARGET -p PORT [-f FPATTERN] [--sentence] -e ELEMENT
                   [-o {flg,vrt}]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        path to directory where the source files are located.
  -t TARGET, --target TARGET
                        path to the directory where the translations are located.
  -p PORT, --port PORT  port number of the FreeLing server.
  -f FPATTERN, --fpattern FPATTERN
                        pattern to find the relevant files.
  --sentence            if provided sentences are already tagged as XML.
  -e ELEMENT, --element ELEMENT
                        element where text to be processed is contained
  -o {flg,vrt}, --oformat {flg,vrt}
                        output format
```

And this would be an example to process a text in English with an analyzer running with the default configuration:

```
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "*_w_sentences.xml" --sentence -e s -o vrt
```

## Examples

port | config | lang | command | requires | yields
---|---|---|---|---|---
50100 | eng | eng.cfg | `analyze -f ~/Projects/freeling/config/eng1.cfg --sense ukb --server --port 50101 &` | token, lemma, POS | sense, WSD
50200 | spa | spa.cfg | `analyze -f ~/Projects/freeling/config/spa1 .cfg --server --port 50201 &` | token, lemma, POS | sense, WSD
50110 | eng | eng.cfg | `analyze -f ~/Projects/freeling/config/eng2.cfg --server --port 50106 &` | sentence | token, POS, lemma, probability
50210 | spa | spa.cfg | `analyze -f ~/Projects/freeling/config/spa2.cfg --server --port 50202 &` | sentence | token, POS, lemma, probability


### With MWEs

#### start the appropriate server

```bash
analyze -f ~/Projects/freeling/config/spa1.cfg --server --port 50201 &
```

#### run the wrapper

```bash
python freeling.py -s ~/Dropbox/PhD/TraDiCorp/tt/ep2/ori/ -t ./freeling1 -p 50201 -f "*.xml" --sentence -e s
```

### Without MWEs

FreeLing 2 is for us the annotation with all MWEs modules deactivated

#### start the appropriate server

```bash
analyze -f ~/Projects/freeling/config/spa2.cfg --server --port 50202 &
```

#### run the wrapper

```bash
python freeling.py -s ~/Dropbox/PhD/TraDiCorp/tt/ep2/ori/ -t ./freeling2 -p 50202 -f "*.xml" --sentence -e s
```

## FreeLing 4

FreeLing 3 is for us the annotation with all MWEs modules deactivated and returning the parsed constituents tree

### start the appropriate server

```bash
analyze -f /media/sf_Projects/freeling/config/eng4.cfg --inplv text --input text --outlv parsed --output xml --server --port 50107&
```

```bash
analyze -f /media/sf_Projects/freeling/config/en.cfg --inplv text --input text --outlv parsed --output xml --server --port 50109&
```

or

```bash
analyze -f /media/sf_Projects/freeling/config/eng4.cfg --inplv text --input text --outlv parsed --output conll --server --port 50108&
```

### run the wrapper

```bash
python freeling_constituents.py -s /media/sf_PhD/TraDiCorp/st/ori/ -t /media/sf_PhD/TraDiCorp/st/flg3/ -p 50107 -f "*.xml" --sentence -e s
```

```bash
python freeling.py -s /media/sf_PhD/TraDiCorp/st/ori/ -t /media/sf_PhD/TraDiCorp/st/flg3/ -p 50108 -f "*.xml" --sentence -e s
```

## Specification

The wrapper expects a FreeLing server running. The server can be invoked either using a configuration file or command line options. A combination of configuration file and command line options should offer full control.

Requirements:

- A command line argument parser
- input file reader(s)
- output file writer(s)
- encapsulate in functions/classes

## Input

There are two aspects to consider regarding input: file format, expected FreeLing format.

By file format I mean XML, plain text, VRT, TCF, FreeLing...

By expected FreeLing format I mean which layers of annotation (in FreeLing output format) are expected by the analyzer as input. This information has to be provided to the server (at start-up time) and to the script to read/extract the information as required.

By now, I would just use XML format. Until we are not done with the processing of the corpus, I would leave FreeLing output format as it is. Even for sentences. Once we finish, we can write a tool to transform the annotation into the appropriate final format. Moreover, we can run two parallel processes: MWE and non-MWE. Although this might be overkill.

In the first run through FreeLing, I would use `<div>` as the greatest unit containing text. And let FreeLing split into sentences. For subsequent runs. We will use already assigned tokenisation and sentences following FreeLing convention.

With this design and workflow decission we simplify the logic and leave all the responsability to the server we will start up. There might be just an option: sentence splitted or not. If text is sentence splitted (like right now) we don't need to worry about it, just look for sentence elements `<s>`. If it is not sentence splitted, then we need to indicate the element containing text to be processed and sentences identified `<p>` or `<div>`.

In the end the output should be FreeLing friendly. And we can finish the sentence marking as XML element at the end of the FreeLing processing.

Sentences will be just empty line separated.

Once we are finished, we will produce other output formats.

For as it is only relevant to know what strings we have to give to FreeLing.

Expected string input is one token per line?

## Testing

Run:

```shell
sh test/test_freeling.sh
```

## TO DO / Wish list

- readers/writers for different formats VRT, XML, TCF
- implement output formats for processed text:
    - `conll` (as outputed by FreeLing)

## Source of test texts

- English: [European Parliament debate intervention by Raül Romeva i Rueda](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//TEXT+CRE+20090504+ITEM-016+DOC+XML+V0//EN&query=INTERV&detail=1-088)
- Spanish: [European Parliament debate intervention by Raül Romeva i Rueda](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//TEXT+CRE+20090504+ITEM-016+DOC+XML+V0//ES&query=INTERV&detail=1-088)
