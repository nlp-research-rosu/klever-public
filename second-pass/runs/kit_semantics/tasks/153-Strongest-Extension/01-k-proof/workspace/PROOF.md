VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the exact translated body of
`Strongest_Extension` has been proved partially correct for:

- every finite `class_name` represented by `str(CLASS:IntSeq)`;
- the empty extension list; and
- every nonempty finite `list(ValSeq)` whose elements are finite `Str` values.

For each extension, the score is the number of uppercase characters minus the
number of lowercase characters. The result is the class name, `"."`, and the
first extension with maximal score. Strict `>` in the scan retains the earlier
extension on ties. The implementation additionally defines the empty-list
result as `class_name + "."`.

This is a partial-correctness theorem: it constrains every terminating execution
covered by the claims. It is not a separate liveness theorem.

## Formal claim

`spec.k` contains four claims:

1. `SPEC.inner-loop` describes the complete character loop over an arbitrary
   finite `Str`, including the exact final `strength` and `character` locals.
2. `SPEC.outer-loop` describes the complete extension-list loop over an
   arbitrary finite all-string `ValSeq`, including every local changed by the
   loop.
3. `SPEC.entry-empty` loads the exact `FuncDef`, resolves and calls the exact
   `Strongest_Extension` binding, and proves the empty-list return value.
4. `SPEC.entry-nonempty` does the same for
   `vCons(str(FIRST), RESTEXTS)` with `allStrings(RESTEXTS)`.

The two entry claims collectively cover all finite extension-list lengths. The
nonempty theorem is symbolic in both the number of extensions and the length
of every extension; no fixed-size or bounded-unrolling restriction is used.

The result function uses the same association as the two source-level string
additions:

```text
seqConcat(seqConcat(CLASS, "."), strongest-extension)
```

`bestCodes` and `bestScore` are exact left-to-right scan summaries. Their two
step cases are guarded by `score > bestScore` and
`(score > bestScore) ==Bool false`, respectively.

## Proof-extension inventory

The inventory below was reconstructed from `verification.k` and the proof
specifications after the successful run.

| Extension | Class and semantic role | Complete domain/context and state footprint | Value justification, dependents, and validation |
|---|---|---|---|
| `INNER-BODY`, `OUTER-BODY`, `STRONGEST-BODY` | Definitional syntax macros; they name source AST blocks and add no runtime rewrite. | Compile-time only. `STRONGEST-BODY` is the body translated in `solution.mpy`; it includes every assignment, both loops, branch, and return. | Used by all program and connection claims. Body sensitivity is demonstrated by `MUTATED-BODY`, whose proof fails. |
| `charStrength`, `extensionStrength`, `lastCharacter` | Definitional summaries; they describe values without replacing execution. | All `Int` codes and all finite `IntSeq`. Uppercase (`65..90`), lowercase (`97..122`), and neither are exhaustive and pairwise disjoint. Recursion descends structurally. | `CONNECTION-SPEC.inner-loop` executes fixed semantics and proves the exact score and final character universally. The `+1` mutation is rejected. |
| `isStringVal`, `allStrings`, `definedProjectStr` | Definitional domain predicates. | Every `Val`/finite `ValSeq`; equations cover empty/cons and string/non-string values. No state. | `allStrings` is the exact outer-claim precondition. It is preserved on the symbolic tail. |
| `projectStrTotal`, its cast orientations, `#Ceil` characterization, and projection equality simplifiers | Derived datatype projection lemmas; they expose the static `Str` view of a dynamically sorted `Val`. They do not execute program code. | Uses are guarded by `isStringVal(V)`. `Str` has the sole constructor `str(IntSeq)`. On strings the projection is identity; on non-strings its opaque total value is never used by a target claim. No control or state effects. | The equality characterizations follow by complete `Val` constructor cases: for `str(CS)`, `codesProject(str(CS)) = CS` and both equalities are true; for every other constructor, equality with a `Str` constructor and `isStringVal` are both false. `CONNECTION-SPEC.projection-identity` prints `#Top`. |
| `codesOf`, `codesProject`, and guarded reconstruction `projectStrTotal(V) => str(codesProject(V))` | Definitional projections. `codesProject` is result-bearing only on the guarded string domain. | `codesOf` covers every `Str`. `codesProject` collapses on `str(CS)`; it is opaque outside the string guard. It reads no state. | `V = str(codesProject(V))` under `isStringVal(V)` is fixed by the datatype equality lemma and checked through the projection/yield connection claims. The wrong concrete projection of `"A"` to `""` is rejected. |
| `bestCodes`, `bestScore` | Definitional left-fold summaries, with the same equations also oriented as simplifiers. | Empty sequences and string-headed cons sequences. The true/false comparison guards are exhaustive and disjoint; recursive calls descend on the tail. | `OUTER-CONNECTION-SPEC.outer-loop` executes the scan for arbitrary `allStrings(VS)` and proves both summaries. These functions state scan behavior, not an assumed maximality postcondition. |
| `lastExtension`, `lastStrength`, `lastCharacterAcross` | Definitional summaries of otherwise unobserved but live Python locals. | Empty/string-headed finite sequences; all target uses satisfy `allStrings`. Structural descent is strict. | Included so the outer transition preserves the entire exact local frame rather than hiding changed locals. Proved by the outer connection theorem. |
| `expectedResult` | Definitional whole-result expression. | Empty input and nonempty string-headed input, exactly matching the two entry-claim domains. | It concatenates the class, dot, and `bestCodes`; no operational step is replaced. Both entry claims constrain the returned `Str`. |
| Guarded `#iterYield ... #loopStep` rule in `VERIFICATION` | Operational bridge/static-sort dispatch twin. | Exact target `Name("extension")`, exact `OUTER-BODY`, `list(VS)` rest, guard `isStringVal(V)`, and an arbitrary trailing continuation identical to the fixed rule's frame. It changes no cell itself. | `CONNECTION-SPEC.yield-connection`, compiled under `VERIFICATION-BASE` without this bridge, proves the complete transition and identity-projected value. The concrete wrong-value probe is rejected. |
| Inner `#loop(STRING, Name("character"), INNER-BODY)` rule in `VERIFICATION` | Operational bridge. | Exact closed seven-binding plain function frame with `parent(0)`, arbitrary trailing continuation, and all omitted top cells framed. It changes only `strength` and `character`; it preserves bindings, environment, heap, stack, return, exception, and exit state. | `CONNECTION-SPEC.inner-loop`, compiled under bridge-free `VERIFICATION-BASE`, proves this complete match domain with `#Top`. The off-by-one summary probe fails. |
| Outer `#loop(list(VS), Name("extension"), OUTER-BODY)` rule in `TARGET-VERIFICATION` | Operational bridge. | Exact closed function frame, exact loop target/body, guard `allStrings(VS)`, arbitrary trailing continuation, and all omitted top cells framed. It updates `strongest`, `best_strength`, `extension`, `character`, and `strength`; all other state is preserved. | `OUTER-CONNECTION-SPEC.outer-loop`, compiled under `VERIFICATION` before this bridge is imported, proves the complete unbounded domain. Its dependencies are only the already-connected yield and inner bridges. |

No bridge admits a wider continuation, binding, frame shape, or input domain
than its supporting connection theorem.

## Exact commands and actual outputs

The complete executable record is `prove.sh`; the captured output is
`prove.log`. The end-to-end command was:

```bash
bash -o pipefail -c './prove.sh 2>&1 | tee prove.log'
```

It exited `0`. The positive proof commands in that script were:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
# Output: #Top   Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition outer-connection-kompiled
kprove outer-connection-spec.k \
  --definition outer-connection-kompiled \
  --spec-module OUTER-CONNECTION-SPEC
# Output: #Top   Exit: 0

kompile --backend haskell verification.k \
  --main-module TARGET-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top   Exit: 0
```

The required LLVM build and concrete execution were:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual final concrete state: `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The compiler emitted warnings from the supplied
semantics, but compilation and execution exited `0`.

The four negative probes all exited `1` as expected:

```text
EXPECTED FAILURE: false-result (exit 1)
EXPECTED FAILURE: inner-wrong-value (exit 1)
EXPECTED FAILURE: yield-wrong-value (exit 1)
EXPECTED FAILURE: changed-body (exit 1)
```

The false-result residual contained the actual `"."` result instead of the
mutated `"X"`. The inner mutation residual contained the impossible condition
`S == S +Int 1`. The changed-body residual contained the concrete string
`"wrong"`.

## Gate results

### Gate A — PASS

- **A1 program identity/body sensitivity:** both entry claims load the exact
  `FuncDef` body represented by `STRONGEST-BODY`, resolve its module binding,
  and call that closure. `solution.mpy` was regenerated from `solution.py`.
  Replacing the body by `Return(Str("wrong"))` makes the original result claim
  fail.
- **A2 operational-state preservation:** every bridge has an exact state
  footprint and a connection theorem. Inner and outer bridges constrain all
  changed locals in a closed plain frame; other top cells are framed equally
  in bridge and theorem.
- **A3 binding/evaluation/control fidelity:** the yield twin matches the exact
  target and body; loop bridges match exact loop terms and preserve arbitrary
  continuations. Each supporting theorem has the same continuation
  generality. Projection identity and wrong-value rejection establish value
  fidelity.
- **A4 consistency/rule validity:** score cases are disjoint, scan branches are
  true/false complements, recursive summaries descend, and total functions
  cover their stated sorts. `codesProject` is opaque outside the guarded string
  domain and no target use observes that region.
- **A5 result constraint/non-vacuity:** the realizable empty/empty input returns
  `"."`; mutating the result to `"X"` produces a stuck claim and exit `1`.

### Gate B — PASS

The formal domain is not length-bounded: it covers every finite class-name
string and every finite list of finite extension strings in the fixed model.
Empty lists are handled rather than excluded. Non-string extension elements
are outside the prompt's extension-name domain and would make the specified
character-method computation undefined.

There is one explicit fixed-model boundary. CPython string case predicates are
Unicode-aware, while the supplied semantics' `isUpperC`/`isLowerC` recognize
ASCII ranges only, and source string literal loading is ASCII-only. The proof
covers every `IntSeq` value represented by the fixed model and the implementation
faithfully calls Python's `str.isupper`/`str.islower`; no theorem-side length or
constructor restriction is introduced. Therefore this is a recorded language
model boundary under Gate B2, not candidate domain narrowing. For example,
CPython treats Greek `Ω` as uppercase, while the fixed predicate does not.

The scan summary-to-property bridge is formal: its strict-update recursive
equations select the first maximum, and the unbounded outer connection theorem
proves the program implements those equations.

### Gate C — PASS

All named assumptions, connection definitions, proof commands, concrete tests,
and mutations are present in the workspace and reproduced by `prove.sh`.
Formal facts, conditional model adequacy, and finite empirical evidence are
separated in this report.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  fixed execution model.
- K's kompilers, Haskell/LLVM backends, SMT reasoning, and host toolchain are
  trusted.
- The datatype projection lemmas are proof-local derived facts. Their
  derivation uses the complete `Val` constructor split and the sole
  `Str ::= str(IntSeq)` constructor; all result-bearing program uses are
  connected by machine-checked claims.
- Unicode case classification is conditional on the fixed model boundary
  described under Gate B. No claim is made that the supplied ASCII predicates
  equal CPython's Unicode database.
- `codesProject` is intentionally opaque for non-string `Val` inputs. That
  region affects no target claim because every use is under `isStringVal` or
  `allStrings`.

## Empirically supported facts

- `python3 differential_test.py` compared the implementation with an
  independently structured oracle using `sum` and `max` over 5 directed cases
  plus 2,000 deterministic random cases. Actual output:
  `differential_cases=2005 mismatches=0`.
- `concrete_tests.mpy` ran five directed cases through the supplied LLVM
  semantics: both prompt examples, a different winner, an empty list, and a
  first-on-tie case. It terminated with `.K`, `NoExc`, and exit code `0`.
- Unicode directed cases passed against the CPython oracle. This supports the
  Python implementation but does not erase the supplied semantics' ASCII model
  boundary.
- Negative mutation evidence is finite validation evidence; the universal
  execution facts come from the connection and target `#Top` proofs.

## Excluded behavior

- Values outside the prompt's string `class_name` and list-of-string extension
  domain are not covered.
- CPython Unicode classification equivalence is not proved by the supplied
  ASCII-oriented semantics.
- Termination is not separately claimed beyond the reachability proof's
  partial-correctness interpretation.
