VALIDATED

## What is proven

Under the supplied MPY semantics, the `sort_numbers` body is proved for an
arbitrary symbolic finite `IntSeq` input `CS`, subject only to:

```k
allNumberWords(splitWS(CS, .IntSeq, .ValSeq))
```

This is an unbounded algebraic input domain. It is not a collection of fixed
sizes: the semantic whitespace split may contain any finite number of tokens,
including duplicates, and every token must be one of `zero` through `nine`.

The reachability theorem is a partial-correctness theorem. It proves that the
call:

```k
Call(Name("sort_numbers"), str(CS))
```

using the exact `_number_key` and `sort_numbers` closure bodies translated in
`solution.mpy`:

- returns `expectedSortNumbers(CS)`;
- restores the module environment and empties the call stack;
- allocates exactly the split list and the newly sorted list at heap locations
  0 and 1;
- leaves `heapLoc` at 2; and
- leaves `NoExc` and exit code 0.

`expectedSortNumbers(CS)` is exactly:

```k
str(joinCodes(
  strToCodes(" "),
  sortKeyVS(
    splitWS(CS, .IntSeq, .ValSeq),
    numberKeyClosure)))
```

Ten additional reachability claims execute `_number_key` under the fixed
semantics and prove the complete valid callback domain:

```text
zero→0, one→1, two→2, three→3, four→4,
five→5, six→6, seven→7, eight→8, nine→9
```

Together with the supplied trusted `sortKeyVS` contract—stable ascending sort
by the values produced by its callable—this is the HumanEval property: all
allowed numeral tokens, with multiplicity preserved, are returned in numeric
order and separated by one space.

## Formal claims

`spec.k` contains:

- `SPEC.sort-numbers`, the unbounded entry claim;
- `SPEC.key-zero` through `SPEC.key-nine`, the complete valid-domain execution
  claims for the program-defined key helper.

The target precondition has a realizable witness, for example
`CS = strToCodes("three one five")`. The LLVM smoke run includes that witness
and reaches `.K`, `NoExc`, and exit code 0 with result `one three five`.

## Proof-extension inventory

### `numberKeyClosure` and `sortNumbersClosure`

- **Class:** Definitional summaries implemented as compile-time macros.
- **Semantic role:** Name the exact translated closure values; they do not
  rewrite or replace runtime execution.
- **Domain and matched context:** Every syntactic occurrence of the respective
  zero-argument macro; no configuration cells or continuation are matched.
- **Justification scope and containment:** The expanded parameter lists,
  bodies, and defining environment 0 are an exact transcription of
  `solution.mpy`. Macro expansion has no wider runtime context.
- **State footprint:** None.
- **Value influence:** They pin name lookup, the executed target body, the key
  callable passed to `sorted`, the heap summary, and the final result.
- **Value justification:** `prove.sh` regenerates `solution.mpy` from
  `solution.py`; the bodies were independently compared with the macro
  expansions. The key-body mutation probe changes the residual callback and
  is rejected.
- **Dependents:** All claims in `spec.k`; `expectedSortNumbers`.
- **Control/value validation:** `spec-body-mutation.k` replaces the helper body
  with `return 9`; `kprove` exits 1 and its residual distinguishes the original
  and mutant closures.

### `isNumberWord`

- **Class:** Definitional summary.
- **Semantic role:** Defines the source-contract token predicate; it does not
  replace execution.
- **Domain:** Every `Val`, with one unconditional equation.
- **Matched context:** Function applications only; no continuation or cells.
- **Justification scope and containment:** Exhaustive equality disjunction over
  exactly the ten literals in `prompt.py`.
- **State footprint:** None.
- **Value influence:** Restricts the entry claim precondition.
- **Value justification:** Ground K equality against the ten ASCII string
  values.
- **Dependents:** `allNumberWords`, hence `SPEC.sort-numbers`.
- **Validation:** The equation is total, has no overlap, and performs no
  recursion.

### `allNumberWords`

- **Class:** Definitional summary.
- **Semantic role:** Lifts `isNumberWord` to arbitrary finite `ValSeq` values;
  it does not replace execution.
- **Domain:** All `ValSeq` values.
- **Matched context:** Function applications only; no continuation or cells.
- **Justification scope and containment:** The disjoint empty and `vCons`
  equations cover the complete constructor domain.
- **State footprint:** None.
- **Value influence:** Restricts the entry claim precondition.
- **Value justification:** Structural conjunction of `isNumberWord` over every
  element.
- **Dependents:** `SPEC.sort-numbers`.
- **Validation:** Disjoint exhaustive cases and strict structural descent.

### `expectedSortNumbers`

- **Class:** Definitional summary.
- **Semantic role:** Names the exact fixed-semantics value reached by the
  program. It does not intercept a Python term or any `<k>` computation.
- **Domain:** Every `IntSeq`, with one unconditional equation.
- **Matched context:** Function applications only; no continuation or cells.
- **Justification scope and containment:** Its right-hand side is exactly the
  composition left after fixed-semantics `split`, trusted keyed sort, and
  `join`.
- **State footprint:** None.
- **Value influence:** Constrains the target result.
- **Value justification:** The entry proof executes the target body to that
  same term. The false-result mutation rejects `noneV`.
- **Dependents:** `SPEC.sort-numbers` and the two negative probes.
- **Validation:** Total, nonrecursive, and nonoverlapping.

### Key-helper auxiliary claims

- **Class:** Derived auxiliary reachability claims.
- **Semantic role:** Execute the exact program-defined helper; they do not
  replace its execution in the target.
- **Domain:** The ten allowed input words, collectively the complete helper
  domain relevant to the source contract.
- **Matched context:** Exact call, module bindings, empty heap and stack,
  environment 0, scope location 1, `NoExc`, and exit code 0.
- **Justification scope and containment:** Each claim starts from the exact
  invocation configuration it establishes.
- **State footprint:** Reads the module binding, creates and removes a call
  scope, returns an integer, and preserves the visible heap, stack, exception,
  and exit cells stated in the claims.
- **Value influence:** Supplies the numeric interpretation used by the trusted
  keyed-sort contract.
- **Value justification:** All ten execute with fixed semantics and are
  included in the all-claims `#Top` run.
- **Dependents:** The HumanEval interpretation of `SPEC.sort-numbers`.
- **Validation:** Complete valid-domain coverage plus the rejected helper-body
  mutation.

No proof-local operational bridge, priority rule, opaque oracle, projection,
cast, or simplification lemma was added.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

Actual result:

```text
prove.sh exit: 0
#Top
#Top
expected vacuity-probe failure: exit 1
expected body-mutation failure: exit 1
```

The fixed semantics emits compiler warnings about unrelated non-exhaustive
dynamic-sort cases and unused `strLt` variables; compilation still exits 0.

The positive build and proof commands executed by `prove.sh` are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled --output none

python3 differential_test.py
python3 py2mpy.py differential_test.py > differential_test.mpy
krun differential_test.mpy --definition runtime-kompiled --output none

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.sort-numbers

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual outputs and exits:

- translation and Python compilation: no stdout, exit 0;
- LLVM compilation: warnings described above, exit 0;
- smoke `krun`: no stdout under `--output none`, exit 0;
- CPython and K differential commands: no assertion failure, exit 0;
- Haskell compilation: only the fixed `strLt` unused-variable warnings,
  exit 0;
- isolated unbounded target: `#Top`, exit 0;
- all eleven claims: `#Top`, exit 0.

The exact negative commands are also in `prove.sh`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

- false result (`noneV`) mutation: exit 1 with
  `WarnStuckClaimState`; `vacuity.out` shows the actual returned
  `str(joinCodes(... sortKeyVS ...))` cannot unify with `noneV`;
- helper body changed to `return 9`: exit 1 with
  `WarnStuckClaimState`; `body-mutation.out` shows the actual result and heap
  contain the mutant callback while the destination requires the original
  callback.

Reproducibility hashes at the audited run:

```text
prompt.py                       61b0d963a0d3797bc5ef83253bf35a531d7e31eedbd18181ff117b0e07e5c940
solution.py                     337cb01ee37a039327568aa39a2e490cf62e9c37784675dbad528eb2ad4a5781
solution.mpy                    bdf82834ab9745e68574560d80f1d29c8b02469bec9b5b692f584d6d7a038eec
verification.k                  b73cb66e355f82c46d6d3c2e6c8c86a06b5f401195ae4e74ebe414ba96ba5731
spec.k                          1bd7531c81319aedfad71d50f4a2a6c9fa7b74f02537aba31542ed113325313c
reference-semantics/semantics.k 57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97
```

## Gate results

### Gate A — PASS

- **A1:** The exact `sort_numbers` body executes under fixed semantics.
  `_number_key` has fixed-semantics auxiliary execution claims for every valid
  input. The scopes pin both program bindings and the builtin `sorted`
  binding. The helper-body mutation is rejected.
- **A2:** No proof-local execution is skipped. The target claim constrains the
  returned value, both allocations, `heapLoc`, restored environment, scope,
  stack, exception, and exit cells. The supplied symbolic sort abstraction
  changes only the content of the newly allocated sorted list.
- **A3:** Fixed call rules perform lookup, left-to-right argument evaluation,
  split allocation, builtin dispatch, join, return, and frame restoration.
  There is no continuation-widening proof rule.
- **A4:** Every local function has exhaustive, nonoverlapping equations.
  `allNumberWords` descends structurally. The closure aliases are compile-time
  expansions.
- **A5:** `three one five` is a concrete valid witness. Replacing the returned
  string by `noneV` is rejected with exit 1 and a stuck residual containing the
  real result.

### Gate B — PASS

- **B1:** `CS:IntSeq` and recursive `allNumberWords(splitWS(CS,...))` cover
  arbitrary finite valid token sequences, not bounded sizes. Duplicates and
  empty sequences are included. ASCII spaces required by the prompt are
  included; the implementation also accepts repeated/leading/trailing MPY
  whitespace.
- **B2:** The ten words and prompt delimiter are ASCII, exactly represented by
  MPY's code-sequence string model. Invalid tokens and their exception behavior
  are outside the prompt and formal precondition.
- **B3:** The K theorem formally establishes the exact
  split/`sortKeyVS`/join result. Its interpretation as numeric ordering is
  conditional on the explicitly named supplied `sortKeyVS` contract, combined
  with the ten machine-checked key claims.
- **B4:** The implementation maps every allowed word to its numeric rank,
  preserves duplicates through stable sorting, and joins with one space,
  matching the prompt and example.

### Gate C — PASS

- The unproved sort contract is named below with its exact dependents and value
  effect.
- All referenced artifacts exist, and all exact commands are in `prove.sh`.
- `differential_test.py` uses a nested counting oracle that does not call
  `sorted`, `_number_key`, or any proof equation. It covers 15 documented
  boundary, ordered, reverse, duplicate, mixed, and whitespace cases.
- Both CPython and the concrete `MPY-KRUN` execution report zero assertion
  failures. This is finite evidence only and is not presented as a universal
  sort theorem.

## Trust boundary

1. **`sortKeyVS(ValSeq, Val)` in `MPY-SORT`:** trusted primitive supplied by
   the read-only semantics. Its contract is stable ascending sorting by the
   result of invoking the callable on each element. It affects the returned
   string and heap location 1 in `SPEC.sort-numbers`. The K symbolic theorem
   does not prove this universal sorting algorithm. Evidence is the concrete
   `MPY-KRUN` callback execution against the independent counting oracle on the
   15 cases in `differential_test.py`; the ten callback values themselves are
   machine-checked for their complete valid domain.
2. **Supplied MPY semantics and K implementation:** the theorem is relative to
   the unchanged files under `reference-semantics/` and the K/Haskell/SMT
   toolchain. Their implementation is foundational and is not reproved here.
3. **Translation identity:** `py2mpy.py` is supplied and unchanged.
   `prove.sh` regenerates `solution.mpy` before every run. The closure macros
   were audited against that generated AST, and the body-sensitivity probe
   demonstrates that changing the helper body changes and invalidates the
   target connection.

## Empirically supported facts

- `smoke.py` checks empty input, the stated example, duplicates, and reverse
  order under concrete LLVM execution.
- `differential_test.py` checks 15 cases against an independent
  counting-by-word oracle in both CPython and MPY-KRUN, with zero failures.

## Excluded behavior

- Inputs containing tokens outside the ten words, non-string arguments, and
  the resulting Python exceptions are outside the HumanEval contract and the
  formal precondition.
- The supplied MPY whitespace model recognizes ASCII space, tab, newline, and
  carriage return. Python behavior for other Unicode whitespace is not modeled;
  the prompt's space-delimited domain is covered.
- The theorem is partial correctness; termination and resource bounds are not
  separate liveness results.
- Universal correctness of the trusted keyed-sort primitive is a named trust
  assumption, not a theorem proved in these artifacts.
