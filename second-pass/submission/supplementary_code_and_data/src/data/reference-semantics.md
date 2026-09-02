# Reference semantics — scope and validation notes

The frozen K reference semantics for the modeled Python subset is
installed at `data/reference/src` (tree sha256
`4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`).
These notes document the comparator breadth of the builtin fold/sort
semantics, its validation, and one documented residual boundary.

## Comparator breadth

CPython's `max`, `min`, and `sorted` operate over any mutually-orderable
values (mixed int/float, bool, str). The semantics decides all of these
through its own `applyCmp` dispatch:

1. `builtins.k` iterable folds `#maxCont*` / `#minCont*` fold general
   `Val` accumulators (not an Int-only seed).
2. `builtins.k` variadic `maxVals` / `minVals` accept the same breadth.
3. `concrete.k` keyed-sort comparator `kLt` and `sort.k` concrete
   `sortVS` insertion compare through the shared bridges
   (`ltIF`/`ltFI`, bool-to-int promotion, `strLt`).

Strict comparison is used so the first maximal/minimal element survives
(the CPython tie rule). Unordered pairs (int-vs-str, `None`) remain
stuck, matching the model's unmodeled-exception convention where CPython
raises.

## Validation

Validated in the frozen runner image against a CPython 3.10.12 oracle:
71/71 machine witnesses (59 type-exact value checks, 7 stuck-convention
checks, 5 byte-diff regressions), the full prior regression harness
green, and the Haskell proof-module kompile succeeding.

## Documented residual (deliberate)

The keyed concrete sort's `reverse=True` reverses equal-key runs, while
CPython keeps stable order (e.g. `sorted([1, 1.0], key=idf,
reverse=True)`: model `[1.0, 1]`, CPython `[1, 1.0]`). The non-keyed
`reverse=True` path is exact via a krun-only `priority(40)` override.
Candidates touching keyed descending sorts must record this boundary in
the trust ledger.
