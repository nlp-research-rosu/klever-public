# Reference semantics v3 — comparator-breadth Class-B one-fix

Date: 2026-07-30. Tree sha256:
`4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`
(installed at `data/reference/src`; v2 `e017e7dd…` preserved at
`data/semantic-archive/v2/src`; registry:
`data/reference-semantics-versions.json`).

## Defect class

CPython's `max`, `min`, and `sorted` operate over any mutually-orderable
values (mixed int/float, bool, str). The v2 model represents all of these
values and its `applyCmp` dispatch can compare them, but three builtin
implementations were arbitrarily narrower, producing concrete stuck states
on CPython-valid inputs (machine witnesses: `max([1, 2.5])`,
`max([True, 2])`, `max(["a", "b"])`, keyed `sorted` over mixed-numeric
keys — stuck at `#maxCont0` / `#maxCont(1)` / `kLt`):

1. `builtins.k` iterable folds `#maxCont*` / `#minCont*`: Int-typed seed
   and accumulator, `maxInt`/`minInt` steps.
2. `builtins.k` variadic `maxVals` / `minVals`: Int-only.
3. `concrete.k` keyed-sort comparator `kLt` and `sort.k` concrete
   `sortVS` insertion: Int-Int / Float-Float / Str-Str legs only.

## Fix (strict widening; +104/−10 lines)

General `Val` folds decided by the semantics' own `applyCmp` dispatch —
reusing the exact v2 bridges (`ltIF`/`ltFI`, bool→int promotion,
`strLt`) with strict comparison so the first maximal/minimal element
survives (CPython tie rule). Crossover rules hand the old Int and Float
folds over on a mixed yield; the pre-existing Int/Float/Str rules are
textually untouched, and homogeneous-domain outputs are byte-identical
to v2. Unordered pairs (int-vs-str, None) remain stuck, matching the
model's unmodeled-exception convention where CPython raises.

## Validation

Frozen image `humaneval-codex-runner:frozen-0.144.6-k7.1.293-actual-report`,
CPython 3.10.12 oracle: 71/71 witnesses (59 type-exact value checks, 7
stuck-convention checks, 5 v2-vs-v3 byte-diff regressions), full v2
harness re-run green under v3 (FIX1 32, FIX2 18 004, FIX3 2 010, smoke
tasks), Haskell proof-module kompile succeeds. Harness and logs:
scratchpad `semv3val/` (witness.log, validate-full.log, v2-to-v3.diff).

## Documented residual (deliberately not fixed)

The keyed concrete sort's `reverse=True` reverses equal-key runs; CPython
keeps stable order. This flaw pre-exists in v2 on its working domain
(`sorted(["aa","bb"], key=len, reverse=True)`: model `["bb","aa"]`, both
versions byte-identical) and fixing it would change old-domain outputs.
With `kLt` widened it is now also reachable for equal mixed-numeric keys
(`sorted([1, 1.0], key=idf, reverse=True)`: model `[1.0, 1]`, CPython
`[1, 1.0]`). The non-keyed `reverse=True` path is exact via a krun-only
`priority(40)` override. Candidates touching keyed descending sorts must
record this boundary in the trust ledger.

## Impact statement

No completed audit is affected: audits mount the semantics version the
candidate recorded (`inputs.reference_semantics_sha256`), and every
completed execution recorded v1 or v2. v3 governs only launches made
after this installation.
