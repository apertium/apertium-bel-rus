# Gender Agreement Fixes - Changes Summary

## Problem Addressed
Fixed gender agreement issues in Belarusian-Russian translation where predicative adjectives with intervening adverbs had incorrect gender agreement with their subject nouns.

**Example Issue:** `Беларуская мова вельмі прыгожая.` → `Белорусский язык очень красива.` ❌  
**Fixed To:** `Беларуская мова вельмі прыгожая.` → `Белорусский язык очень красивый.` ✅

## Files Modified

### 1. `apertium-bel-rus.bel-rus.t1x` (Transfer Rules)
**Added 5 new transfer rules + 1 category definition:**

1. **New Category:** `<def-cat n="cnjcoo">` for coordinating conjunctions
2. **Rule 1:** `ADJ + NOUN + ADV + ADJ` pattern (attributive + predicative)
3. **Rule 2:** `NOUN + ADV + ADJ` pattern (basic predicative)
4. **Rule 3:** `NOUN + ADV + ADV + ADJ` pattern (double adverbs)
5. **Rule 4:** `NOUN + ADV + ADJ + CONJ + ADJ` pattern (coordination)
6. **Rule 5:** `ADJ + NOUN + ADV + ADJ + CONJ + ADJ` pattern (extended coordination)

**Purpose:** Ensure proper gender transfer from source noun to target adjectives across various syntactic patterns.

### 2. `apertium-bel-rus.bel-rus.rlx` (Constraint Grammar - NEW FILE)
**Added 16 new disambiguation rules in 3 sections:**

#### Section 1: Neuter Adjective Disambiguation (Rules 1-6)
- Select neuter nominative for predicative adjectives after neuter nouns
- Remove incorrect feminine genitive readings
- Handle single and double adverb patterns

#### Section 2: Plural Disambiguation (Rules 7-10)  
- Select plural nominative nouns when followed by plural nominative adjectives
- Remove incorrect singular genitive readings
- Handle determiner + noun patterns

#### Section 3: Coordination Agreement (Rules 11-16)
- Ensure coordinated adjectives match in gender, case, and number
- Handle masculine, feminine, neuter, and plural coordination
- Remove incorrect genitive readings in coordination

**Purpose:** Resolve morphological ambiguities by selecting correct analyses based on syntactic context.

### 3. `GENDER_AGREEMENT_TESTS.md` (NEW FILE)
**Comprehensive test documentation including:**
- 9 test cases covering all patterns
- Expected results (all ✅ working)
- Test commands for verification
- Implementation summary

## Technical Approach

### Transfer Rules Strategy
- Used `case_adapter_n` macro to transfer gender from noun to adjective
- Created specific patterns for different syntactic structures
- Ensured all adjectives in coordination get proper gender agreement

### Constraint Grammar Strategy
- Applied SELECT rules to choose correct morphological analyses
- Applied REMOVE rules to eliminate incorrect analyses
- Used positional context (e.g., `-1 Adv`, `-2 (n nt nom)`) for disambiguation

### Makefile Integration
- Modified compilation to use local constraint grammar file
- Enabled testing and development of new disambiguation rules

## Results Achieved

**Success Rate: 9/9 test cases (100% complete)**

All patterns now correctly handle:
- ✅ Gender agreement across adverbs
- ✅ Multiple adverb patterns  
- ✅ Coordinated adjectives
- ✅ Plural disambiguation
- ✅ Complex syntactic patterns

## Testing
Run the test suite:
```bash
# All test cases
bash -c 'while read line; do echo "$line" | apertium -d . bel-rus; done < <(grep "echo" GENDER_AGREEMENT_TESTS.md | cut -d'"' -f2)'
```

Or see `GENDER_AGREEMENT_TESTS.md` for individual test commands.
