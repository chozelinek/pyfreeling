# PyFreeLing

This is the documentation for a wrapper for FreeLing 4. This wrapper was developed to ease the processing of texts for my PhD. It is written in Python 3 and tested on macOS Sierra.

This project was started to meet my own needs. I don't plan to include extra features upon request. I don't provide any kind of support, specially regarding other platforms. But feel free to fork, clone and play with the code.

# Contents

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

# Setting up PyFreeLing in Mac OS Sierra

There are 4 types of dependencies:

- [Homebrew](https://brew.sh), a package manager to install software in Mac
- [FreeLing](http://nlp.lsi.upc.edu/freeling), an open source language analysis tool suite
- [Python 3](https://www.python.org)
- [lxml](http://lxml.de), a Python library to work with XML
- [libxml2](http://xmlsoft.org) and [libxslt](http://xmlsoft.org/libxslt) C libraries which are dependencies of `lxml`

## Install Homebrew

Follow [Neil Gee's guide](https://coolestguidesontheplanet.com/installing-homebrew-on-macos-sierra-package-manager-for-unix-apps) to install and set up homebrew for Mac OS Sierra

## Install FreeLing

Use Homebrew to install FreeLing by running this command:

```bash
brew install freeling
```

Homebrew will take care of any dependencies.

## Install Python 3

You can install Python 3 with Homebrew following the instructions from [The Hitchhiker's Guide to Python](http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/) or following the very complete [Lisa Tagliaferri's guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos).

Basically:

```bash
brew install python3
```

## Install libxml2 and libxslt

macOS Sierra already provides `libxml2` and `libxslt`. They can be installed through Homebrew though:

```bash
brew install libxml2
brew install libxslt
```

## Install lxml

Now, you are ready to install `lxml`:

```bash
pip3 install lxml
```

# Using PyFreeLing

Once you have installed FreeLing and all the dependencies, you will always do two things:

1. start a FreeLing analyzer in server mode
1. run the wrapper script

## Starting a FreeLing analyzer in server mode

As our wrapper is devised to process batches of files and each file can be split into smaller text units, we want to avoid the downtime of loading parameters for each (chunk of) text to be processed. If we start a server, parameters are loaded only once.

The options of the server can be declared in a configuration file or via command line options. Command line options override configuration file's directives.

For more details check the FreeLing documentation for the [analyzer](https://talp-upc.gitbooks.io/freeling-user-manual/content/analyzer.html).

A server to analyze texts in English with default options can be invoked with the following command:

```bash
analyze -f en.cfg --server --port 50005 &
```

You will see after a few seconds in the terminal window some information (like how to stop the server). Keep that terminal window open to monitor the server.

### Most frequent FreeLing command line options

option | meaning | default | values
------|------------------------|---------|------------------------
`--input` | Input format in which to expect text to analyze | `text` | `text`, `freeling`, `conll`
`--output` | Output format to produce with analysis results | `freeling` | `freeling`, `conll`, `xml`, `json`, `naf`, `train`
`--inplv` | Analysis level of input data (already tagged) | `text` | `text`, `token`, `splitted`, `morfo`, `tagged`, `shallow`, `dep`, `coref`
`--outlv` | Analysis level of output data (to be tagged) | `tagged` | `token`, `splitted`, `morfo`, `tagged`, `shallow`, `parsed`, `dep`, `coref`, `semgraph`
`--sense` | Kind of sense annotation to perform | `no` | `no`, `all`, `mfs`, `ukb`

### Configuration files

These are a series of customized files to ease the invokation of servers from the command line:

- `en_nomwe.cfg` and `es_nomwe.cfg`: no module carrying out multiword expression detection is activated.
- `en_mwe.cfg` and `es_mwe.cfg`: all modules carrying out multiword expression detection are activated.
- `en_mwe_nec.cfg` and `es_mwe_nec.cfg`: like `*_mwe.cfg` but performing NEC.

## Usage of freeling.py

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

```bash
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "*_w_sentences.xml" --sentence -e s -o vrt
```

# Examples

List of my most frequent server configurations.

port | command | requires | yields
------|------------------------------------------------|------------|---------------
50101 | `analyze -f ./config/en_nomwe.cfg --server --port 50101 &` | text | token, lemma, POS
50102 | `analyze -f ./config/en_mwe.cfg --server --port 50102 &` | text | token, lemma, POS
50103 | `analyze -f ./config/en_mwe_nec.cfg --server --port 50103 &` | text | token, lemma, POS
50104 | `analyze -f ./config/en_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --server --port 50104 &` | token, lemma, POS | WSD
50105 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv shallow --server --port 50105 &` | token, lemma, POS | constituency
50106 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv dep --server --port 50106 &` | token, lemma, POS | dependency
50111 | `analyze -f ./config/en_nomwe.cfg --output conll --server --port 50101 &` | text | token, lemma, POS
50112 | `analyze -f ./config/en_mwe.cfg --output conll --server --port 50102 &` | text | token, lemma, POS
50113 | `analyze -f ./config/en_mwe_nec.cfg --output conll --server --port 50103 &` | text | token, lemma, POS
50114 | `analyze -f ./config/en_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --output conll --server --port 50104 &` | token, lemma, POS | WSD
50115 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv shallow --output conll --server --port 50105 &` | token, lemma, POS | constituency
50116 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv dep --output conll --server --port 50106 &` | token, lemma, POS | dependency
50121 | `analyze -f ./config/en_nomwe.cfg --output xml --server --port 50101 &` | text | token, lemma, POS
50122 | `analyze -f ./config/en_mwe.cfg --output xml --server --port 50102 &` | text | token, lemma, POS
50123 | `analyze -f ./config/en_mwe_nec.cfg --output xml --server --port 50103 &` | text | token, lemma, POS
50124 | `analyze -f ./config/en_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --output xml --server --port 50104 &` | token, lemma, POS | WSD
50125 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv shallow --output xml --server --port 50105 &` | token, lemma, POS | constituency
50126 | `analyze -f ./config/en_mwe_nec.cfg --input freeling --inplv tagged --outlv dep --output xml --server --port 50106 &` | token, lemma, POS | dependency
50201 | `analyze -f ./config/es_nomwe.cfg --server --port 50201 &` | sentence | token, lemma, POS
50202 | `analyze -f ./config/es_mwe.cfg --server --port 50202 &` | sentence | token, lemma, POS
50203 | `analyze -f ./config/es_mwe_nec.cfg --server --port 50203 &` | sentence | token, lemma, POS

## Token, lemma, POS without MWEs and sentences preannotated

### Output in FreeLing or VRT format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --server --port 50101 &
# Spanish
analyze -f ./config/es_nomwe.cfg --server --port 50201 &
```

#### run the wrapper: output FLG

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50101 -f "*w_sentences.xml" --sentence -e s -o flg
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50201 -f "*w_sentences.xml" --sentence -e s -o flg
```

#### run the wrapper: output VRT

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50101 -f "*w_sentences.xml" --sentence -e s -o vrt
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50201 -f "*w_sentences.xml" --sentence -e s -o vrt
```

### Output in CONLL format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --output conll --server --port 50111 &
# Spanish
analyze -f ./config/es_nomwe.cfg --output conll --server --port 50211 &
```

#### run the wrapper: output CONLL

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50111 -f "*w_sentences.xml" --sentence -e s -o conll
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50211 -f "*w_sentences.xml" --sentence -e s -o conll
```

## Token, lemma, POS with MWEs, NEC and sentences preannotated

### Output in FreeLing or VRT format

#### start a server

```bash
# English
analyze -f ./config/en_mwe_nec.cfg --server --port 50103 &
# Spanish
analyze -f ./config/es_mwe_nec.cfg --server --port 50203 &
```

#### run the wrapper: output FLG

```bash
# English
python freeling.py -s en/ -t ./test/en/tmp_output/mwe -p 50103 -f "*w_sentences.xml" --sentence -e s -o flg
# Spanish
python freeling.py -s es/ -t ./test/es/tmp_output/mwe -p 50203 -f "*w_sentences.xml" --sentence -e s -o flg
```

#### run the wrapper: output VRT

```bash
# English
python freeling.py -s en/ -t ./test/en/tmp_output/mwe -p 50103 -f "*w_sentences.xml" --sentence -e s -o vrt
# Spanish
python freeling.py -s es/ -t ./test/es/tmp_output/mwe -p 50203 -f "*w_sentences.xml" --sentence -e s -o vrt
```

### Output in CONLL format

#### start a server

```bash
# English
analyze -f ./config/en_mwe_nec.cfg --output conll --server --port 50113 &
# Spanish
analyze -f ./config/es_mwe_nec.cfg --output conll --server --port 50213 &
```

#### run the wrapper: output CONLL

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/mwe -p 50103 -f "*w_sentences.xml" --sentence -e s -o conll
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/mwe -p 50203 -f "*w_sentences.xml" --sentence -e s -o conll
```

## Token, sentence, lemma, POS without MWEs

### Output in FreeLing or VRT format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --server --port 50101 &
# Spanish
analyze -f ./config/es_nomwe.cfg --server --port 50201 &
```

#### run the wrapper: output FLG

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50101 -f "*wo_sentences.xml" -e p -o flg
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50201 -f "*wo_sentences.xml" -e p -o flg
```

#### run the wrapper: output VRT

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50101 -f "*wo_sentences.xml" -e p -o vrt
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50201 -f "*wo_sentences.xml" -e p -o vrt
```

### Output in CONLL format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --output conll --server --port 50111 &
# Spanish
analyze -f ./config/es_nomwe.cfg --output conll --server --port 50211 &
```

#### run the wrapper: output CONLL

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50101 -f "*wo_sentences.xml" -e p -o conll
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50201 -f "*wo_sentences.xml" -e p -o conll
```

## Token, sentence, lemma, POS with MWES and NEC

### Output in FreeLing or VRT format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --server --port 50103 &
# Spanish
analyze -f ./config/es_nomwe.cfg --server --port 50203 &
```

#### run the wrapper: output FLG

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50103 -f "*wo_sentences.xml" -e p -o flg
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50203 -f "*wo_sentences.xml" -e p -o flg
```

#### run the wrapper: output VRT

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50103 -f "*wo_sentences.xml" -e p -o vrt
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50203 -f "*wo_sentences.xml" -e p -o vrt
```

### Output in CONLL format

#### start a server

```bash
# English
analyze -f ./config/en_nomwe.cfg --output conll --server --port 50113 &
# Spanish
analyze -f ./config/es_nomwe.cfg --output conll --server --port 50213 &
```

#### run the wrapper: output CONLL

```bash
# English
python freeling.py -s ./test/en/ -t ./test/en/tmp_output/nomwe -p 50113 -f "*wo_sentences.xml" -e p -o conll
# Spanish
python freeling.py -s ./test/es/ -t ./test/es/tmp_output/nomwe -p 50213 -f "*wo_sentences.xml" -e p -o conll
```

## WSD

### Output in FreeLing or VRT format

#### start server

```bash
# English
analyze -f ./config/en_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --server --port 50104 &
# Spanish
analyze -f ./config/es_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --server --port 50204 &
```

#### run the wrapper: output FreeLing

```bash
# English
python freeling.py -s ./test/en/tmp_output/mwe -t ./test/en/tmp_output/wsd -p 50104 -f "*.flg" -e p -o flg
# Spanish
python freeling.py -s ./test/es/tmp_output/mwe -t ./test/es/tmp_output/wsd -p 50204 -f "*.flg" -e p -o flg
```

#### run the wrapper: output VRT

```bash
# English
python freeling.py -s ./test/en/tmp_output/mwe -t ./test/en/tmp_output/wsd -p 50104 -f "*.flg" -e p -o vrt
# Spanish
python freeling.py -s ./test/es/tmp_output/mwe -t ./test/es/tmp_output/wsd -p 50204 -f "*.flg" -e p -o vrt
```

### Output in CONLL

#### start server

```bash
# English
analyze -f ./config/en_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --output conll --server --port 50114 &
# Spanish
analyze -f ./config/es_mwe_nec.cfg --sense ukb --input freeling --inplv tagged --output conll --server --port 50214 &
```

#### run the wrapper

```bash
# English
python freeling.py -s ./test/en/tmp_output/mwe -t ./test/en/tmp_output/wsd -p 50114 -f "*.flg" -e p -o vrt
# Spanish
python freeling.py -s ./test/es/tmp_output/mwe -t ./test/es/tmp_output/wsd -p 50214 -f "*.flg" -e p -o vrt
```

## Shallow parsing

### Output in XML

#### start server

#### run the wrapper

### Output in CONLL

#### start the server

#### run the wrapper

## Dependency parsing

### Output in XML

#### start server

#### run the wrapper

### Output in CONLL

#### start the server

#### run the wrapper

# Testing

Run:

```bash
sh test/test_freeling.sh
```

# TO DO / Wish list

- readers/writers for different formats VRT, XML, TCF
- implement output formats for processed text:
    - `multilayer vrt` (output each layer of information in a separate VRT file)

# Source of test texts

- English: [European Parliament debate intervention by Raül Romeva i Rueda](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//TEXT+CRE+20090504+ITEM-016+DOC+XML+V0//EN&query=INTERV&detail=1-088)
- Spanish: [European Parliament debate intervention by Raül Romeva i Rueda](http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//TEXT+CRE+20090504+ITEM-016+DOC+XML+V0//ES&query=INTERV&detail=1-088)
