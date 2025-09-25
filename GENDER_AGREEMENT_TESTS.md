# Gender Agreement Test Cases

This document contains comprehensive test cases for gender agreement fixes in Belarusian-Russian translation, specifically for predicative adjectives with intervening adverbs and coordination patterns.

## Test Cases Overview

### 1. Feminine → Masculine Gender Changes
- **Test 1:** `Беларуская мова вельмі прыгожая.` → `Белорусский язык очень красивый.`
  - **Pattern:** ADJ + NOUN + ADV + ADJ (attributive + predicative)
  - **Fix:** Both adjectives agree with masculine `язык`

- **Test 2:** `Мова проста вельмі прыгожая.` → `Язык просто очень красивый.`
  - **Pattern:** NOUN + ADV + ADV + ADJ (double adverbs)
  - **Fix:** Adjective agrees despite two intervening adverbs

- **Test 3:** `Мова вельмі прыгожая і цікавая.` → `Язык очень красивый и интересный.`
  - **Pattern:** NOUN + ADV + ADJ + CONJ + ADJ (coordination)
  - **Fix:** Both coordinated adjectives agree with noun

- **Test 4:** `Беларуская мова вельмі прыгожая і цікавая.` → `Белорусский язык очень красивый и интересный.`
  - **Pattern:** ADJ + NOUN + ADV + ADJ + CONJ + ADJ (extended coordination)
  - **Fix:** All three adjectives agree with noun

### 2. Neuter → Feminine Gender Changes
- **Test 5:** `Жыццё вельмі прыгожае.` → `Жизнь очень красивая.`
  - **Pattern:** NOUN + ADV + ADJ (neuter to feminine)
  - **Fix:** Neuter adjective correctly becomes feminine

- **Test 6:** `Жыццё вельмі прыгожае і цікавае.` → `Жизнь очень красивая и интересная.`
  - **Pattern:** NOUN + ADV + ADJ + CONJ + ADJ (neuter coordination)
  - **Fix:** Both adjectives correctly become feminine nominative

### 3. Neuter → Neuter (Same Gender)
- **Test 7:** `Сонца вельмі яркае.` → `Солнце очень яркое.`
  - **Pattern:** NOUN + ADV + ADJ (neuter to neuter)
  - **Fix:** Correct neuter agreement maintained

### 4. Plural Disambiguation
- **Test 8:** `Мовы вельмі прыгожыя.` → `Языки очень красивые.`
  - **Pattern:** NOUN(pl) + ADV + ADJ(pl)
  - **Fix:** Noun correctly analyzed as plural nominative, not singular genitive

- **Test 9:** `Гэтыя мовы вельмі прыгожыя.` → `Эти языки очень красивые.`
  - **Pattern:** DET + NOUN(pl) + ADV + ADJ(pl)
  - **Fix:** Plural disambiguation with determiner

## Test Commands

```bash
# Feminine → Masculine
echo "Беларуская мова вельмі прыгожая." | apertium -d . bel-rus
echo "Мова проста вельмі прыгожая." | apertium -d . bel-rus
echo "Мова вельмі прыгожая і цікавая." | apertium -d . bel-rus
echo "Беларуская мова вельмі прыгожая і цікавая." | apertium -d . bel-rus

# Neuter → Feminine
echo "Жыццё вельмі прыгожае." | apertium -d . bel-rus
echo "Жыццё вельмі прыгожае і цікавае." | apertium -d . bel-rus

# Neuter → Neuter
echo "Сонца вельмі яркае." | apertium -d . bel-rus

# Plural
echo "Мовы вельмі прыгожыя." | apertium -d . bel-rus
echo "Гэтыя мовы вельмі прыгожыя." | apertium -d . bel-rus
```

## Expected Results (All ✅ WORKING)

1. `Белорусский язык очень красивый.` ✅
2. `Язык просто очень красивый.` ✅
3. `Язык очень красивый и интересный.` ✅
4. `Белорусский язык очень красивый и интересный.` ✅
5. `Жизнь очень красивая.` ✅
6. `Жизнь очень красивая и интересная.` ✅
7. `Солнце очень яркое.` ✅
8. `Языки очень красивые.` ✅
9. `Эти языки очень красивые.` ✅

## Implementation

The fixes were implemented through:
1. **5 Transfer Rules** in `apertium-bel-rus.bel-rus.t1x` for gender agreement
2. **16 Constraint Grammar Rules** in `apertium-bel-rus.bel-rus.rlx` for disambiguation
3. **Makefile modification** to compile local constraint grammar

**Success Rate: 9/9 (100% complete)**
