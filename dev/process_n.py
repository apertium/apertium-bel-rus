# usage: python process_nouns.py N.xml meanings.txt 1> success.txt 2> errors.txt
# where:
#   N.xml – file with nouns (bnkorpus grammar DB)
#   meanings.txt – file for dump words with multiple paradigms
# it prints speling-file to stdout and errors to stderr

import sys, xml
import xml.etree.ElementTree as ET
from BelarusianTagsAnalyzer.BelarusianTagsAnalyzer import Analyzer

class Form(object):
    lemma = None
    form = None
    pr1 = None
    pr2 = None
    def __init__(self, lemma, form, parameter1, parameter2):
        self.lemma = lemma
        self.form = form
        self.pr1 = parameter1
        self.pr2 = parameter2
    def __str__(self):
        return '; '.join([self.lemma, self.form, self.pr1, self.pr2])
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.lemma == other.lemma and self.form == other.form and self.pr1 == other.pr1 and self.pr2 == other.pr2
    def __ne__(self, other):
        return not self.__eq__(other)


class Paradigm:
    forms = []
    def __init__(self, forms):
        self.forms = forms
    def __str__(self):
        return "\n".join([str(form) for form in self.forms])
    def add_suffix(self, suffix):
        self.forms = [Form(f.lemma + suffix, f.form, f.pr1, f.pr2) for f in self.forms]

def compare_paradigms(f, s):
    if len(f.forms) > len(s.forms):
        f, s = s, f
    common = 0
    for form1 in f.forms:
        for form2 in s.forms:
            if form1 == form2:
                common += 1
                break
    return common == len(f.forms)

gender = {'мужчынскі': 'm', 'жаночы': 'f', 'ніякі': 'nt'}
animacy = {'адушаўлёны': 'aa', 'неадушаўлёны': 'nn'}
case = {'назоўны': 'nom', 'родны': 'gen', 'давальны': 'dat', 'вінавальны': 'acc', 'творны': 'ins', 'месны': 'loc'}
num = {'адзіночны': 'sg', 'множны': 'pl'}
nums = ['¹', '²', '³', '⁴', '⁵']
        
f = ET.parse(sys.argv[1])
file_meanings = open(sys.argv[2], 'w')

paradigms = []
lem_cnt = {}
path = './/Paradigm'
analyzer = Analyzer()
for paradigm in f.findall(path):
    lem = paradigm.attrib['Lemma'].replace('´', '')
    tag = paradigm.attrib['Tag']
    meaning = paradigm.get('meaning', '')

    try:
        p = analyzer.describe(tag)
    except:
        continue

    lem_cnt[lem] = [(p[2] + "." + p[5], meaning)] if lem not in lem_cnt else lem_cnt[lem] + [(p[2] + "." + p[5], meaning)]

    forms = []
    for form in paradigm.findall('.//Form'): 
        full_tag = tag + form.attrib['Tag']
        forma = ''
        for i in form.itertext(): 
            forma = forma + i
        forma = forma.replace('´', '')
        try:
            p = analyzer.describe(full_tag)
        except:
            print("{} | {} | {}".format(lem, forma, full_tag), file=sys.stderr)
        else:
            canim = animacy[p[2]] if p[2] in animacy else None
            cgen = gender[p[5]] if p[5] in gender else None
            ccase = case[p[7]] if p[7] in case else None
            cnum = num[p[8]] if p[8] in num else None
            if canim is None or cgen is None or ccase is None or cnum is None:
                print("{} | {} | {}".format(lem, forma, full_tag), file=sys.stderr)
            else:
                forms += [Form(lem, forma, '.'.join([cnum, ccase]), '.'.join(['n', cgen, canim]))]
    if len(forms) > 0:
        paradigms += [Paradigm(forms)]

lem_us = dict(lem_cnt)
for x in lem_us:
    lem_us[x] = 0

i = 0
dupl = {}
for p1 in paradigms:
    j = 0
    for p2 in paradigms:
        if i >= j or p1.forms[0].lemma != p2.forms[0].lemma:
            j += 1
            continue
        if compare_paradigms(p1, p2) and i < j:
            dupl[p1.forms[0].lemma] = [(i, j)] if p1.forms[0].lemma not in dupl else dupl[p1.forms[0].lemma] + [(i, j)]
        j += 1
    i += 1

ignored_list = []
counter = -1
for p in paradigms:
    counter += 1
    if counter in ignored_list:
        continue
    lem = p.forms[0].lemma
    if len(lem_cnt[lem]) > 1:
        mng = set([x[0] for x in lem_cnt[lem]])
        if len(mng) != 1:
            continue
        if lem in dupl:
            # let's ignore same paradigms in pair
            for pair in set(dupl[lem]):
                ignored_list += [pair[0]] if len(paradigms[pair[0]].forms) < len(paradigms[pair[1]].forms) else [pair[1]]
            continue
        else:
            p.add_suffix(nums[lem_us[lem]])
            file_meanings.write("{}; {}\n".format(p.forms[0].lemma, lem_cnt[lem][lem_us[lem]]))
            lem_us[lem] += 1

counter = 0
for p in paradigms:
    if counter not in ignored_list:
        print(p)
    else:
        print("{} (len: {}) was ignored".format(p.forms[0].lemma, len(p.forms)), file=sys.stderr)
    counter += 1
file_meanings.close()


