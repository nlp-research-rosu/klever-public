VALIDATED

## What is proven

Under the supplied MPY semantics, `check_dict_case` terminates for every finite
symbolic dictionary key sequence with no heap-reference key and returns:

```text
nonempty(keys)
and
(every key is a string satisfying islower
 or every key is a string satisfying isupper)
```

The key sequence is not size-bounded. `KS:ValSeq` and `VALUES:ValSeq` remain
symbolic in the target claim. Dictionary values are arbitrary and unused.
Reference-valued keys are excluded by `notBool hasRefVS(KS)`: in the target's
initial empty heap such references are dangling, and the supplied semantics uses
references for mutable list objects, which are not valid Python dictionary keys.
All direct non-reference `Val` constructors are included, so the formal domain
is a superset of the ordinary hashable values represented by MPY.

## Formal claims

`SPEC.loop` is an all-path coinductive invariant over an arbitrary finite
`KS:ValSeq` and arbitrary current Boolean accumulators. It executes the literal
translated loop body and computes `foldLowerKeys`, `foldUpperKeys`, and
`hasAnyKey` over the entire unprocessed suffix.

`SPEC.target` starts from the initial MPY configuration, loads the literal
translated `FuncDef`, calls it with `dictV(KS, VALUES)`, and proves that the
module variable `result` is:

```text
checkCaseSummary(true, true, false, KS)
```

The target proof uses `SPEC.loop` as an auxiliary theorem. It is marked trusted
only in the composition command after a separate untrusted `kprove` invocation
has proved `SPEC.loop` with `#Top`.

## Proof-extension inventory

- `checkDictLoopBody`, `checkDictReturn`, and `checkDictBody` are total
  definitional AST aliases. They expand to the exact translated statements.
- `isStringKey` is an attribute-complete evaluator twin of frozen `isStrV`.
  Both have the same `str(_) => true` and `Val => false [owise]` equations.
  The simplification equation from `isStrV` to `isStringKey` changes no value;
  it supplies the `[total]` information missing from the frozen declaration.
- `stringCodes` is a guarded constructor destructor. Its only observed domain
  is `isStringKey(V) == true`, where `V` is necessarily `str(CS)` and the rule
  `stringCodes(str(CS)) => CS` fixes its result. Its arbitrary total
  interpretation on non-strings cannot affect control, state, or the result.
- `lowerKeyCodes` and `upperKeyCodes` are exact names for the frozen method
  formulas `hasLower and not hasUpper` and `hasUpper and not hasLower`.
- The two guarded `applyMethod` simplification twins duplicate those frozen
  formulas on the complete string-constructor domain. They do not alter
  lookup, argument evaluation, continuation order, heap, stack, or exceptions.
- The one priority bridge matches only the exact post-evaluation
  `#applyK(toCall(builtinV("isinstance")), (V,typeV("str"),.Vals))` redex and
  returns `isStringKey(V)`. Its `notBool isRefV(V)` guard leaves the frozen
  heap-dereference path untouched.
- `lowerKey`, `upperKey`, the folds, `hasAnyKey`, and `checkCaseSummary` are
  terminating mathematical definitions over `ValSeq`. Their constructor cases
  are disjoint and exhaustive.
- There are no proof-local rules that return from the function, pop a frame,
  skip a loop, suppress an exception, allocate memory, or directly write the
  claimed result.

`CONNECTION-SPEC` is compiled without importing `VERIFICATION`, so it contains
none of the operational dispatch rules. Its three universal claims prove:

1. the exact frozen `isinstance` redex produces `isStringKey(V)` for every
   non-reference `V` and every following `CONT:K`;
2. frozen `islower` produces the copied formula for every `str(CS)` and every
   following computation;
3. frozen `isupper` does likewise.

## Commands and actual results

The complete replay is:

```bash
./prove.sh
```

Actual final result: exit 0. The script contains the exact individual commands.
The relevant command results were:

```text
python3 test_solution.py
checks = 4374
mismatches = 0
Exit: 0

diff -u <fixed LLVM krun output> <bridge-enabled Haskell krun output>
Output: empty
Exit: 0

kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
#Top
Exit: 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop
#Top
Exit: 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop,SPEC.target \
  --trusted SPEC.loop
#Top
Exit: 0
```

The frozen LLVM and bridge-enabled Haskell executions both terminated with
`.K`, an empty stack, `NoExc`, exit code 0, identical heaps/allocation counters,
and:

```text
empty_result      = false
lower_result      = true
upper_result      = true
mixed_case_result = false
mixed_type_result = false
uncased_result    = false
```

The A5 mutation command was:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual completed the
exact program with `"result" |-> false`, while the deliberate mutation required
`"result" |-> true`. `prove.sh` checks this as an expected failure.

## Gate results

### Gate A — PASS

- A1: `SPEC.target` loads and executes the literal translated body; the loop
  theorem uses exact definitional aliases of that same body and continuation.
- A2/A3: the bridge-free connection claims retain an arbitrary continuation.
  The `isinstance` bridge was narrowed after a probe exposed the reference
  dereference boundary; reference arguments now remain on the fixed path.
- A4: evaluator twins have exhaustive, non-overlapping equations. The sole
  opaque destructor is value-determined on every reachable observation domain.
  No fresh result can select an unconstrained final outcome.
- A5: the satisfiable empty-dictionary false-postcondition mutation failed and
  displayed the actual false result.
- Fixed and bridge-enabled ground executions were byte-identical.

### Gate B — PASS

The theorem covers arbitrary finite symbolic key sequences, not examples,
fixed sizes, or bounded unrollings. The postcondition directly formalizes the
prompt's nonempty/all-lower-or-all-upper contract, including rejection of
non-string and uncased string keys. The no-reference premise removes values
that cannot be well-formed keys in the supplied model's empty initial heap; it
does not bound the material dictionary domain.

The intended execution model for this benchmark is the supplied MPY semantics.
Its string case predicates are ASCII-oriented. The Python implementation itself
was additionally checked against CPython on Unicode examples, but universal
equivalence between MPY's character model and CPython Unicode is not claimed.

### Gate C — PASS

All named artifacts and commands exist in the workspace. The bridge-free
connection proofs, positive proofs, negative mutation, LLVM/Haskell execution
differential, prompt examples, and independent CPython differential corpus all
ran in the final replay. No mismatch was hidden or converted into an
assumption.

## Trust boundary

Trusted components are the supplied read-only MPY semantics, K's parser and
LLVM/Haskell backends, the K logical kernel, and the stated interpretation of
MPY constructors as the benchmark's Python subset. `py2mpy.py` is trusted only
for the source-to-constructor translation; `solution.mpy` was regenerated in
the replay, and the target embeds the same constructor body.

`SPEC.loop` is not an external trust assumption: it has its own positive proof
command. The shared proof theory contains no externally trusted primitive and
no unconstrained result-bearing oracle.

## Empirical support and excluded behavior

`test_solution.py` uses an independently written CPython contract oracle. It
checked the five prompt examples and every key sequence of length zero through
three over a 16-element boundary pool: lowercase, uppercase, cased-plus-digit,
uncased, mixed-case, Unicode, integers, `True`, `None`, and a tuple. There were
4,374 comparisons and zero mismatches. This is finite evidence, not the formal
unbounded proof.

Excluded from the formal claim are non-dictionary arguments, dangling or
mutable heap-reference keys, and claims that the supplied ASCII case model is a
complete model of CPython Unicode. These exclusions do not hide a finite-size
bound on dictionaries or strings.
