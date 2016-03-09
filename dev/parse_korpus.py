# Run: python3 parse_korpus.py N.xml BelRusVorvul/BelRusVorvul, where
#     N.xml - file with nouns from grammar db
#     BelRusVorvul/BelRusVorvul - name of belarusian-russian dict in StarDict format (script was tested only with A. Vorvul's dict)
# Output:
#     uwords.txt - file with words that have unknown gender in format:
#           <word_in_bel> | <gender_in_bel>
#     pwords.txt - file with words that were translated in format:
#           <word_in_bel> | <gender_in_bel> | <word/words_in_rus>

import sys, xml
import xml.etree.ElementTree as ET
from pystardict import Dictionary

gender = {'M': 'm', 'F': 'f', 'N': 'nt'}

f = ET.parse(sys.argv[1]);
unknown_words_f = open('uwords.txt', 'w')
words_f = open('pwords.txt', 'w')
dict_bel_rus = Dictionary(sys.argv[2])

unknown_words = set()
words = set()

path = './/Paradigm'
cnt = [0, 0]
for paradigm in f.findall(path):
	lem = paradigm.attrib['Lemma'].replace('´', '')
	tag = paradigm.attrib['Tag']

	if tag[-2] not in gender:
		cnt[0] += 1
		unknown_words.add((lem, tag[-2]))
	else:
		cnt[1] += 1
		words.add((lem, gender[tag[-2]]))

print("Parsed: {} good / {} unknown".format(cnt[1], cnt[0]))

translated = 0
for element in words:
	if dict_bel_rus.has_key(element[0]):
		translated += 1
		rus_eq = dict_bel_rus.get(element[0]).split("\n")[1]
		words_f.write("{} | {} | {}\n".format(*element, rus_eq))

print("{} were translated".format(translated))

for element in unknown_words:
	unknown_words_f.write("{}|{}\n".format(*element))

unknown_words_f.close()
words_f.close()
