# BelarusianTagsAnalyzer
# The code was ported from Java code, originally part of the Korpus - Corpus Linguistics Software
# Home page: https://sourceforge.net/projects/korpus/
# Usage: see example.py
import sys, copy

class OneLetterInfo:
    group_name = ""
    letter = ""
    description = ""
    next_letters = None

    def __init__(self, group_name, letter, description, next_letters):
        self.group_name = group_name
        self.letter = letter
        self.description = description
        self.next_letters = next_letters

class TagLetter:
    letters = None
    is_latest_in_paradigm = False
    pos_in_tree = -1

    def __init__(self, pos):
        self.pos_in_tree = pos

    def add(self, tree, text, is_latest=False):
        """Add descriptions for letters."""
        pos = text.find("=>")
        if pos <= 0:
            raise Exception("Error in add: {}".format(text))
        group_name = text[0:pos].strip()
        values = text[(pos + 2):].strip()

        tree.append(copy.deepcopy(tree[0]))
        c = len(tree) - 1
        tree[c].letters = list([])
        tree[c].pos_in_tree = c
        for v in values.split(';'):
            code = v[0]
            if (not ('A' <= code <= 'Z')) and (not ('0' <= code <= '9')):
                raise Exception("Error in letters: {}".format(values))
            if v[1] != ':':
                raise Exception("Error in letters: {}".format(values))
            new_letter = OneLetterInfo(group_name, code, v[2:], c)
            for li in tree[self.pos_in_tree].letters:
                if li.letter == new_letter.letter:
                    raise Exception("Already exists in letters: {} for {}".format(values, new_letter.letter))
            tree[self.pos_in_tree].letters.append(new_letter)
        if is_latest:
            tree[self.pos_in_tree].latest_in_paradigm()
        return c

    def latest_in_paradigm(self):
        """Mark letter as last."""
        self.is_latest_in_paradigm = True
        return self

    def get_letter_description(self, c):
        """Get letter description."""
        for li in self.letters:
            if li.letter == c:
                return li.description
        return None

    def is_finish(self):
        """Check end of current letters-list."""
        return (self.letters is None) or (len(self.letters) == 0)

    def next(self, c):
        """Get next letter (index in Analyzer.tree)."""
        for li in self.letters:
            if li.letter == c:
                return li.next_letters
        return None

class Analyzer:
    root = None
    tree = []

    def __init__(self):
        self.root = 0
        self.tree.append(TagLetter(0))
        self.tree[0].letters = list([])
        self.create_noun_tags(self.root)
        self.create_adjective_tags(self.root)
        self.create_numeral_tags(self.root)
        self.create_pronoun_tags(self.root)
        self.create_participle_tags(self.root)
        self.create_adverb_tags(self.root)
        self.create_verb_tags(self.root)
        self.create_conjunction_tags(self.root)
        self.create_preposition_tags(self.root)
        self.create_interjection_tags(self.root)
        self.create_particle_tags(self.root)
        self.create_predicative_tags(self.root)

    def describe(self, code):
        """Return list with descriptions for each letter in tag."""
        result = []
        tags_pointer = self.root
        for c in code:
            description = self.tree[tags_pointer].get_letter_description(c)
            if description == None:
                raise Exception("Error (invalid description) in code: {}".format(code))
            tags_pointer = self.tree[tags_pointer].next(c)
            if self.tree[tags_pointer] == None:
                raise Exception("Error (unexpected finish) in code: {}".format(code))
            result += [description]
        return result

    def create_noun_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => N:Назоўнік")
        t = self.tree[t].add(self.tree, "Уласнасць => C:агульны;P:уласны")
        t = self.tree[t].add(self.tree, "Адушаўлёнасць => A:адушаўлёны;I:неадушаўлёны;X:???????")
        t = self.tree[t].add(self.tree, "Асабовасць => P:асабовы;I:неасабовы;X:???????")
        t = self.tree[t].add(self.tree, "Скарот => B:скарот;N:нескарот")

        z = self.tree[t].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;C:агульны;X:???????")
        z = self.tree[z].add(self.tree, "Скланенне => 1:1 скланенне;2:2 скланенне;3:3 скланенне;0:нескланяльны;4:рознаскланяльны;6:змешаны;X:???????", True)
        z = self.tree[z].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны")
        z = self.tree[z].add(self.tree, "Лік => S:адзіночны;P:множны")

        p = self.tree[t].add(self.tree, "Множналікавыя => P:множны лік")
        p = self.tree[p].add(self.tree, "Скланенне => 0:нескланяльныя;7:множналікавыя", True)
        p = self.tree[p].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны")
        p = self.tree[p].add(self.tree, "Лік => S:адзіночны;P:множны")

        su = self.tree[t].add(self.tree, "Субстантываванасць => S:субстантываваны;U:субстантываваныя множналікавыя")
        su = self.tree[su].add(self.tree, "Скланенне => 5:ад’ектыўнае", True)
        su = self.tree[su].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;P:адсутнасьць роду ў множным ліку;X:???????")
        su = self.tree[su].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны")
        su = self.tree[su].add(self.tree, "Лік => S:адзіночны;P:множны")

    def create_numeral_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => M:Лічэбнік")
        t = self.tree[t].add(self.tree, "Словазмяненне => N:як у назоўніка;A:як у прыметніка;X:???????")
        t = self.tree[t].add(self.tree, "Значэнне => C:колькасны;O:парадкавы;K:зборны;F:дробавы")
        t = self.tree[t].add(self.tree, "Форма => S:просты;C:складаны", True)

        z = self.tree[t].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;P:няма;X:???????")
        self.tree[t].add(self.tree, "Незмяняльны => 0:незмяняльны")
        z = self.tree[z].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны;X:???????")
        z = self.tree[z].add(self.tree, "Лік => S:адзіночны;P:множны;X:???????")

    def create_pronoun_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => S:Займеннік")
        t = self.tree[t].add(self.tree, "Словазмяненне => N:як у назоўніка;A:як у прыметніка;M:як у займенніка")
        t = self.tree[t].add(self.tree, "Разрад => P:асабовы;R:зваротны;S:прыналежны;D:указальны;E:азначальны;L:пытальна–адносны;N:адмоўны;F:няпэўны")
        t = self.tree[t].add(self.tree, "Асоба => 1:першая;2:другая;3:трэцяя;0:безасабовы;X:???????", True)
        z = self.tree[t].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;P:няма;X:???????")
        self.tree[t].add(self.tree, "Незмяняльны => 0:незмяняльны")
        z = self.tree[z].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны;X:???????")
        z = self.tree[z].add(self.tree, "Лік => S:адзіночны;P:множны;X:???????")

    def create_adjective_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => A:Прыметнік")
        self.tree[t].add(self.tree, "Тып => 0:нескланяльны", True)
        t = self.tree[t].add(self.tree, "Тып => Q:якасны;R:адносны;P:прыналежны;X:???????")
        t = self.tree[t].add(self.tree, "Ступень параўнання => P:станоўчая;C:вышэйшая;S:найвышэйшая", True)
        t = self.tree[t].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;P:множны лік;X:???????")
        t = self.tree[t].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны")
        t = self.tree[t].add(self.tree, "Лік => S:адзіночны;P:множны")

    def create_verb_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => V:Дзеяслоў")
        t = self.tree[t].add(self.tree, "Пераходнасць => T:пераходны;I:непераходны;D:пераходны/непераходны;X:???????")
        t = self.tree[t].add(self.tree, "Трыванне => P:закончанае;M:незакончанае")
        t = self.tree[t].add(self.tree, "Зваротнасць => R:зваротны;N:незваротны")
        t = self.tree[t].add(self.tree, "Спражэнне => 1:першае;2:другое;3:рознаспрагальны", True)

        casR = self.tree[t].add(self.tree, "Час => R:цяперашні")
        casM = self.tree[t].add(self.tree, "Час => P:мінулы")
        casO = self.tree[t].add(self.tree, "Час => F:будучы;Q:перадмінулы")
        zah = self.tree[t].add(self.tree, "Загадны лад => I:загадны лад")
        self.tree[t].add(self.tree, "Інфінітыў => 0:Інфінітыў")
        self.tree[self.tree[self.tree[self.tree[t].add(self.tree, "Невядома => X:невядома")].add(self.tree, "Невядома => X:невядома")].add(self.tree, "Невядома => X:невядома")].add(self.tree, "Невядома => X:невядома")

        casRL = self.tree[casR].add(self.tree, "Асоба => 1:першая;2:другая;3:трэцяя;0:безасабовы")
        self.tree[casR].add(self.tree, "Дзеепрыслоўе => G:дзеепрыслоўе")
        casML = self.tree[casM].add(self.tree, "Асоба => 1:першая;2:другая;3:трэцяя;0:безасабовы;X:???????")
        self.tree[casM].add(self.tree, "Дзеепрыслоўе => G:дзеепрыслоўе")
        casOL = self.tree[casO].add(self.tree, "Асоба => 1:першая;2:другая;3:трэцяя;0:безасабовы")
        self.tree[casO].add(self.tree, "Дзеепрыслоўе => G:дзеепрыслоўе")
        zah = self.tree[zah].add(self.tree, "Асоба => 1:першая;2:другая;3:трэцяя;0:безасабовы")
        self.tree[zah].add(self.tree, "Дзеепрыслоўе => G:дзеепрыслоўе")

        casRL = self.tree[casRL].add(self.tree, "Лік => S:адзіночны;P:множны")
        casML = self.tree[casML].add(self.tree, "Лік => S:адзіночны;P:множны")
        casOL = self.tree[casOL].add(self.tree, "Лік => S:адзіночны;P:множны")
        zah = self.tree[zah].add(self.tree, "Лік => S:адзіночны;P:множны")
        casML = self.tree[casML].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;X:???????")

    def create_participle_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => P:Дзеепрыметнік")
        t = self.tree[t].add(self.tree, "Стан => A:незалежны;P:залежны")
        t = self.tree[t].add(self.tree, "Час => R:цяперашні;P:мінулы")
        t = self.tree[t].add(self.tree, "Трыванне => P:закончанае;M:незакончанае;D:закончанае/незакончанае;X:???????", True)

        t = self.tree[t].add(self.tree, "Род => M:мужчынскі;F:жаночы;N:ніякі;P:множны лік;X:???????")
        t = self.tree[t].add(self.tree, "Склон => N:назоўны;G:родны;D:давальны;A:вінавальны;I:творны;L:месны;V:клічны;H:???????")
        t = self.tree[t].add(self.tree, "Лік => S:адзіночны;P:множны;X:???????")

    def create_adverb_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => R:Прыслоўе")
        t = self.tree[t].add(self.tree, "Утварэнне => N:ад назоўнікаў;A:прыметнікаў;M:лічэбнікаў;S:займеннікаў;G:дзеепрыслоўяў;V:дзеясловаў;E:часціц;I:прыназоўнікаў;X:???????", True)
        t = self.tree[t].add(self.tree, "Ступень параўнання => P:станоўчая;C:вышэйшая;S:найвышэйшая")

    def create_conjunction_tags(self, t):
        t = self.tree[t].add(self.tree, "Часціна => C:Злучнік")
        s = self.tree[t].add(self.tree, "Тып => S:падпарадкавальны")
        k = self.tree[t].add(self.tree, "Тып => K:злучальны")
        self.tree[t].add(self.tree, "Тып => P:паясняльны", True)
        self.tree[s].add(self.tree, "Падпарадкавальны => B:прычынны;C:часавы;D:умоўны;F:мэтавы;G:уступальны;H:параўнальны;K:следства;X:???????", True)
        self.tree[k].add(self.tree, "Злучальны => A:спалучальны;E:супастаўляльны;O:пералічальна-размеркавальны;L:далучальны;U:градацыйны;X:???????", True)

    def create_preposition_tags(self, t):
        self.tree[t].add(self.tree, "Часціна => I:Прыназоўнік", True)

    def create_particle_tags(self, t):
        self.tree[t].add(self.tree, "Часціна => E:Часціца", True)

    def create_interjection_tags(self, t):
        self.tree[t].add(self.tree, "Часціна => Y:Выклічнік", True)

    def create_predicative_tags(self, t):
        self.tree[t].add(self.tree, "Часціна => W:Прэдыкатыў", True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python BelarusianTagsAnalyzer.py <paradigm_tag_from_grammar_db>")
    else:
        analyzer = Analyzer()
        print(analyzer.describe(sys.argv[1]))

if __name__ == "__main__":
    main()
