# Run: python3 parse_korpus.py N.xml BelRusVorvul/BelRusVorvul, where
#     N.xml - file with words from grammar db
#     BelRusVorvul/BelRusVorvul - name of belarusian-russian dict in StarDict format (script was tested only with A. Vorvul's dict)
# Output:
#     uwords.txt - file with words that have no translations in format:
#           <word_in_bel>
#     pwords.txt - file with words that were translated in format:
#           <word_in_bel> | <gender_in_bel> | <word/words_in_rus>

import sys, xml
import xml.etree.ElementTree as ET
from pystardict import Dictionary

f = ET.parse(sys.argv[1]);
unknown_words_f = open('uwords.txt', 'w')
words_f = open('pwords.txt', 'w')
dict_bel_rus = Dictionary(sys.argv[2])

words = set()

path = './/Paradigm'
for paradigm in f.findall(path):
    lem = paradigm.attrib['Lemma'].replace('´', '')
    words.add(lem)

print("Parsed: {} words".format(len(words)))

translated = 0
for element in words:
    if dict_bel_rus.has_key(element):
        translated += 1
        rus_eq = dict_bel_rus.get(element).split("\n")[1]
        words_f.write("{} | {}\n".format(element, rus_eq))
    else:
        unknown_words_f.write(element + "\n")

print("{} were translated".format(translated))

unknown_words_f.close()
words_f.close()

