# PyFreeLing3

This is the documentation for a FreeLing wrapper written in Python.

The main purpose of this software is to process (Spanish) texts with FreeLing.

# Dependencies

There are 4 types of dependencies:

- FreeLing 3.1 (install it via homebrew, it will take care of any depencies required), or in Ubuntu install it by downloading from SVN and compiling
- Python 3
- Python 3 modules
- Dependencies of Python 3 modules

## Install in Mac OS X El Capitan

<!-- provide here the command line -->

## Install FreeLing in Ubuntu

# Contents

- docs: documentation about the FreeLingWrapper
    - `FreeLingWrapper.Rmd`, this file
- config: configuration files
- `freeling.py`, the wrapper for `vrt` file input/output format, for Python 3, and FreeLing 3 and FreeLing 4 (this can be used for `conll` output format)
- `freeling_constituents.py`, the wrapper for `vrt` input, `xml` output, for Python 3, and FreeLing 4, the aim is to get the text parsed for constituents in XML format.

# Specification

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


# Configuration files

Configuration files help to set up options by default.

Configuration file directives are overriden by command line options. Command line options is a more flexible approach.

features | spa.cfg | eng.cfg
---|---|---
Language | spa | eng


# Server list

All server configurations as reference for future use.

port | config | lang | command | requires | yields
---|---|---|---|---|---
50100 | eng | eng.cfg | `analyze -f ~/Projects/freeling/config/eng1.cfg --sense ukb --server --port 50101 &` | token, lemma, POS | sense, WSD
50200 | spa | spa.cfg | `analyze -f ~/Projects/freeling/config/spa1 .cfg --server --port 50201 &` | token, lemma, POS | sense, WSD
50110 | eng | eng.cfg | `analyze -f ~/Projects/freeling/config/eng2.cfg --server --port 50106 &` | sentence | token, POS, lemma, probability
50210 | spa | spa.cfg | `analyze -f ~/Projects/freeling/config/spa2.cfg --server --port 50202 &` | sentence | token, POS, lemma, probability

# Examples

# getting FreeLing 1 annotation

FreeLing 1 is for us the annotation with all MWEs modules activated

## start the appropriate server

```bash
analyze -f ~/Projects/freeling/config/spa1.cfg --server --port 50201 &
```

## run the wrapper

```bash
python freeling.py -s ~/Dropbox/PhD/TraDiCorp/tt/ep2/ori/ -t ./freeling1 -p 50201 -f "*.xml" --sentence -e s
```

# getting FreeLing 2 annotation

FreeLing 2 is for us the annotation with all MWEs modules deactivated

## start the appropriate server

```bash
analyze -f ~/Projects/freeling/config/spa2.cfg --server --port 50202 &
```

## run the wrapper

```bash
python freeling.py -s ~/Dropbox/PhD/TraDiCorp/tt/ep2/ori/ -t ./freeling2 -p 50202 -f "*.xml" --sentence -e s
```

# getting FreeLing 3 annotation

FreeLing 3 is for us the annotation with all MWEs modules deactivated and returning the parsed constituents tree

## start the appropriate server

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

## run the wrapper

```bash
python freeling_constituents.py -s /media/sf_PhD/TraDiCorp/st/ori/ -t /media/sf_PhD/TraDiCorp/st/flg3/ -p 50107 -f "*.xml" --sentence -e s
```

```bash
python freeling.py -s /media/sf_PhD/TraDiCorp/st/ori/ -t /media/sf_PhD/TraDiCorp/st/flg3/ -p 50108 -f "*.xml" --sentence -e s
```


# Usage

```
usage: freeling.py [-h] -s SOURCE -t TARGET -p PORT [-f FPATTERN] [--sentence]
                   -e ELEMENT

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        path to directory where the source files are located.
  -t TARGET, --target TARGET
                        path to the directory where the translations are
                        located.
  -p PORT, --port PORT  port number of the FreeLing server.
  -f FPATTERN, --fpattern FPATTERN
                        pattern to find the relevant files.
  --sentence            if provided sentences are already tagged as XML.
  -e ELEMENT, --element ELEMENT
                        element where text to be processed is contained
```

# TO DO / Wish list

It would be good to have readers/writters (VRT, XML, TCF).
