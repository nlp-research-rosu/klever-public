# Canonical-solution gap analysis — what the rewrites simplified away

The proven proofs use *rewritten* solutions that deliberately avoid hard constructs
(comprehensions → explicit loops, `len` → folds, `.split` → scans, early-`return` →
flags, …). This file diffs the **unmodified canonical solutions**
(`questions/<problem>/canonical.py`, the dataset originals) of the proven problems against
the reference — i.e. what a ZERO-DRIFT reference would have to cover.

Counts = number of the **62 proven** canonicals using the feature (Python `ast` walk; type
annotations + docstrings excluded). Per-feature problem lists are the *sources* — that is
where each construct actually appears.

## Already covered — no gap

The language core is done: `+ - * % // **`, `< <= > >= == !=`, unary `-` / `not`,
int / bool / **str** / **None** literals, `and` / `or`, ternary `if-else`, `is` / `is not`,
**subscript** `x[i]`, **slice** `x[a:b:c]`, **tuple**, `for` / `while` / `if` / assign /
`break` / `continue` / functions / `return`. (This subsumes the old Tier-1/Tier-2 bundles
A–G *and* the cheap one-liners `not` / `**` / `is None` / `None`, all now shipped.)

What's left is **comprehensions** and **method dispatch**; the builtin-call family
(Tier A) is now shipped.

## Remaining gaps, ranked by (low effort × high frequency)

### Tier A — ✓ DONE: the builtin-call family ([`mpy-builtins.k`](src/mpy-builtins.k))

Shipped: **builtin-call dispatch** — a rule that recognizes `Call(Name(f), args)` for a
known builtin `f` (the generic user-call rule is `[owise]`, so it defers to this) — plus
`len` / `sum` / `abs` / `min` / `max` / `ord` / `chr` / `str`, each 1–3 rules over helpers
the reference already had (`vsLen` / `isLen`, INT's `absInt` / `maxInt` / `minInt`,
`str(IntSeq)`). Tested in [`tests/semantics/builtins/`](tests/semantics/builtins/). The
counts + sources are kept below as the record of what this retired:

| builtin | count | effort | note / existing building block |
| --- | --: | --- | --- |
| `len` | 22 | trivial | wrap `vsLen` (list/tuple) / `isLen` (str) — already in `mpy-core.k` |
| `sum` | 9 | low | fold a `ValSeq` of `Int` |
| `max` | 4 | low | fold (≥2-arg and iterable forms) |
| `ord` | 4 | low | single-char `str(iCons(c,.))` → `c` (done per-problem in 50/66/93/134) |
| `abs` | 3 | trivial | `absInt` |
| `chr` | 2 | low | `Int` → `str(iCons(c,.))` (done per-problem in 50/93) |
| `min` | 2 | low | fold |
| `str` | 2 | medium | int→str needs digit→char-code (the one non-trivial one here) |

Sources (each problem's `questions/<name>/canonical.py`):

- **`len` ×22** — 12-longest, 14-all-prefixes, 18-how-many-times, 23-strlen, 38-decode-cyclic,
  48-is-palindrome, 72-will-it-fly, 73-smallest-change, 74-total-match, 78-hex-key, 80-is-happy,
  85-add, 98-count-upper, 117-select-words, 118-get-closest-vowel, 122-add-elements,
  128-prod-signs, 134-check-if-last-char-is-a-letter, 135-can-arrange, 140-fix-spaces,
  142-sum-squares, 161-solve
- **`sum` ×9** — 64-vowels-count, 66-digitsum, 72-will-it-fly, 85-add, 121-solution,
  122-add-elements, 128-prod-signs, 142-sum-squares, 151-double-the-difference
- **`max` ×4** — 9-rolling-max, 12-longest, 114-minSubArraySum, 136-largest-smallest-integers
- **`ord` ×4** — 50-decode-shift, 66-digitsum, 93-encode, 134-check-if-last-char-is-a-letter
- **`abs` ×3** — 97-multiply, 128-prod-signs, 152-compare
- **`chr` ×2** — 50-decode-shift, 93-encode · **`min` ×2** — 38-decode-cyclic,
  136-largest-smallest-integers · **`str` ×2** — 122-add-elements, 151-double-the-difference

### Tier B — high reach, medium effort

| feature | count | effort | sources (`questions/<name>/canonical.py`) |
| --- | --: | --- | --- |
| list comprehension | 15 | medium | 7-filter-by-substring, 29-filter-by-prefix, 30-get-positive, 38-decode-cyclic, 42-incr-list, 50-decode-shift, 51-remove-vowels, 62-derivative, 85-add, 93-encode, 112-reverse-delete, 121-solution, 128-prod-signs, 151-double-the-difference, 152-compare |
| `range` | 12 | ✓ **execution done** | 14-all-prefixes, 18-how-many-times, 38-decode-cyclic, 48-is-palindrome, 73-smallest-change, 78-hex-key, 80-is-happy, 85-add, 98-count-upper, 117-select-words, 118-get-closest-vowel, 142-sum-squares |
| `.join` | 9 | medium | 1-separate-paren-groups, 11-string-xor, 28-concatenate, 38-decode-cyclic, 50-decode-shift, 51-remove-vowels, 93-encode, 101-words-string, 112-reverse-delete |
| generator expr | 6 | medium | 11-string-xor, 12-longest, 64-vowels-count, 66-digitsum, 114-minSubArraySum, 122-add-elements |

- **`range`** is a **lazy `rangeObj`** value iterated by the unified `#loop` (RV's `__next__`
  protocol — `for x in obj` over list/str/tuple/range all share one loop; `len`/`sum` consume
  the same per-kind "next", so nothing materializes). `mpy-core.k` (value + `inRange`/`rangeLen`),
  `mpy-statements.k` (`#loop`), `mpy-builtins.k` (`range`/`len`/`sum`); tested in
  [`tests/semantics/range/`](tests/semantics/range/). Because the counter stays an int in the
  term, `for i in range(N)` over a *symbolic* N is **provable** (induction on the bound, à la
  K's `sum-spec`): [`tests/verification/range-loop/`](tests/verification/range-loop/) proves
  `result = N*(N-1)/2` (`#Top`). (A range loop that also indexes a symbolic list —
  `range(len(xs))` + `xs[i]` — combines counter induction with symbolic indexing; the proven
  corpus sidesteps it via direct element-iteration, NOTES §"Position-dependent folds".)
- **list comprehension / genexpr** desugar to an accumulator loop building a `list(ValSeq)` —
  all the pieces exist (for-loop + list build); it needs a `#comp` continuation.
- **`.join`** is a fold over a `list(ValSeq)` of `str` with a separator.

### Tier C — defer: needs a model the reference doesn't have

| feature | count | why it's hard | sources |
| --- | --: | --- | --- |
| `.append` | 7 | **list mutation** — our lists are immutable values; needs a reference/object model | 1-separate-paren-groups, 5-intersperse, 9-rolling-max, 14-all-prefixes, 101-words-string, 117-select-words, 142-sum-squares |
| `.split` / `.lower` / `.swapcase` | 3 / 3 / 3 | char-seq scans (doable but per-method) | split: 101,117,134 · lower: 51,117,134 · swapcase: 27,93,161 |
| `lambda` | 2 | first-class function values as args | 128-prod-signs, 136-largest-smallest-integers |
| `filter` / `zip` / `enumerate` / `list` | 2 / 2 / 2 / 3 | higher-order / iterator protocol | filter: 128,136 · zip: 11,152 · enumerate: 62,121 · list: 128,136,161 |
| `sorted` | 0 | sort is a known blocker (absent from every proven canonical) | — |
| long tail | 1 each | `.index`(148,89), `.clear`(1), `.isalpha`(161), `.startswith`(29), `.isupper`(66), `dict`(93) | — |

## Recommendation

Tier A (builtins) and `range` (execution) are done. The next high-leverage item is
**list comprehension** (×15) — it desugars to an accumulator loop building a `list(ValSeq)`
via a `#comp` continuation. `.append` (×7) is the one common-looking construct
that is genuinely hard — it forces list mutation — so it, and the rest of Tier C, stay
rewritten-around until there's a reason to take on a mutable-object model. This file makes
the choice deliberate, not accidental.
