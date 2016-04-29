# usage: python3 make_bidix.py success.txt apertium-rus.rus.dix pwords.txt 1> entries.dix
# input:
#   success.txt – speling file
#   apertium-rus.rus.dix – russian monodix
#   pwords.txt – file produced by parse_korpus.py
# output:
#   stdin – entries
#   stderr – entries count

import sys

s_wrap = lambda x: '<s n="' + x.strip(' ') + '"/>'
p_wrap = lambda x: ''.join([s_wrap(n) for n in x])
nums = ['¹', '²', '³', '⁴', '⁵', '⁶']

speling_file = open(sys.argv[1], 'r')
parsed_korpus_file = open(sys.argv[3], 'r')
rus_monodix = open(sys.argv[2], 'r')

properties = {}
for x in rus_monodix.readlines():
    # <e lm="сын"><p><l>сын</l><r>сын</r></p><par n="сын__n_m_aa"/></e>
    if x.find("<e lm=") != -1:
        paradigm = x[x.find('<par n="') + 8:x.find('"/>', x.find('<par n='))]
        properties[x[x.find('<e lm="') + 7:x.find('">', x.find('<e lm="'))]] = paradigm.split("__")[1].split('_')
get_pr = lambda x: properties[x] if x in properties else []

translations = {}
for x in parsed_korpus_file.readlines():
    p = x.split('|')
    if p[0].strip(' ') in translations:
        translations[p[0].strip(' ')].add(p[1].strip('\n'))
    else:
        translations[p[0].strip(' ')] = set([p[1].strip('\n')])

lemmas = set()
for x in speling_file.readlines():
    p = x.split(';')
    lemmas.add((p[0], p[-1].strip('\n')))

translated = 0
for lemma in lemmas:
    if lemma[0] in translations:
        for translation in map(lambda x: x.strip(' '), translations[lemma[0].strip(' ')]):
            # bel word has one word in russian
            if translation.find(' ') == -1:
                properties_rus = get_pr(translation)
                properties_bel = lemma[1].split('.')
                # only words which have same animacy (why?)
                if properties_rus[2:] == properties_bel[2:]:
                    translated += 1
                    # <e><p><l>{}{}</l><r>{}{}</r></p></e>
                    print("<e><p><l>{}{}</l><r>{}{}</r></p></e>".format(lemma[0], p_wrap(properties_bel), translation, p_wrap(properties_rus)))

    # to be continued...
print(translated, file=sys.stderr)
