#!/bin/bash
# start the server for English default
echo 'Starting server for English in ...'
osascript -e 'tell app "Terminal" to do script "analyze -f en.cfg --server --port 50005 &"'
sleep 10
# process file with sentences
echo '---'
echo 'freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_w_sentences.xml" --sentence -e s'
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_w_sentences.xml" --sentence -e s
TEST="$(diff -y --suppress-common-lines test/en/output/en_w_sentences.flg test/en/output/en_wo_sentences.flg | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
echo 'freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_w_sentences.xml" --sentence -e s -o vrt'
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_w_sentences.xml" --sentence -e s -o vrt
TEST="$(diff -y --suppress-common-lines test/en/output/en_w_sentences.vrt test/en/output/en_wo_sentences.vrt | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
# process file without sentences
echo 'freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_wo_sentences.xml" -e p'
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_wo_sentences.xml" -e p
TEST="$(diff -y --suppress-common-lines test/en/output/en_wo_sentences.flg test/en/output/en_wo_sentences.flg | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
echo 'freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_wo_sentences.xml" -e p -o vrt'
python freeling.py -s ./test/en/ -t ./test/en/output/ -p 50005 -f "en_wo_sentences.xml" -e p -o vrt
TEST="$(diff -y --suppress-common-lines test/en/output/en_wo_sentences.vrt test/en/output/en_wo_sentences.vrt | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
# kill the server using port 50005
echo 'Killing server for English.'
lsof -i tcp:50005 | awk 'NR!=1 {print $2}' | xargs kill

# start the server for Spanish default
echo 'Starting server for Spanish in ...'
osascript -e 'tell app "Terminal" to do script "analyze -f es.cfg --server --port 50005 &"'
sleep 10
# process file with sentences
echo '---'
echo 'freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "es_w_sentences.xml" --sentence -e s'
python freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "es_w_sentences.xml" --sentence -e s
TEST="$(diff -y --suppress-common-lines test/es/output/es_w_sentences.flg test/es/output/es_wo_sentences.flg | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
echo 'freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "es_w_sentences.xml" --sentence -e s -o vrt'
python freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "es_w_sentences.xml" --sentence -e s -o vrt
TEST="$(diff -y --suppress-common-lines test/es/output/es_w_sentences.vrt test/es/output/es_wo_sentences.vrt | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
# process file without sentences
echo 'freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "*_wo_sentences.xml" -e p'
python freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "*_wo_sentences.xml" -e p
TEST="$(diff -y --suppress-common-lines test/es/output/es_wo_sentences.flg test/es/output/es_wo_sentences.flg | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
echo 'freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "*_wo_sentences.xml" -e p -o vrt'
python freeling.py -s ./test/es/ -t ./test/es/output/ -p 50005 -f "*_wo_sentences.xml" -e p -o vrt
TEST="$(diff -y --suppress-common-lines test/es/output/es_wo_sentences.vrt test/es/output/es_wo_sentences.vrt | grep '^' | wc -l)"
TEST="${TEST#"${TEST%%[![:space:]]*}"}"
if [ "${TEST}" -ne "0" ]
    then
        echo "Test finished with $TEST differences!"
    else
        echo "Test successful!"
fi
echo '---'
# kill the server using port 50005
echo 'Killing server for Spanish.'
lsof -i tcp:50005 | awk 'NR!=1 {print $2}' | xargs kill
