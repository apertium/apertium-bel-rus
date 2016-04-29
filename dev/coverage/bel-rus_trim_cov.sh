#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Usage: ./coverage.sh <path_to_corpora>"
else
    cat $1 | apertium -d ../.. bel-rus-morph | sed 's/\$\W*\^/$\n^/g' > /tmp/bel.trim.coverage.txt
    calc `cat /tmp/bel.trim.coverage.txt | grep -v '\*' | wc -l `/`cat /tmp/bel.trim.coverage.txt | wc -l`
fi
