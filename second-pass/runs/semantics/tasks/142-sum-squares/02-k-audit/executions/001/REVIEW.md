# Independent adversarial audit: 142-sum-squares

This audit used the mandated `using-kit` and `validating-proof` procedures. It
did not use `writing-semantics`, because the rendered mode is
`SUPPLIED_SEMANTICS`. All candidate content was treated as untrusted. Source
needed for execution was copied to
`/tmp/audit-work/142-sum-squares-audit`; candidate caches and claimed outputs
were not reused.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode and trusted mounts agree. `/reference/reference-semantics`
exists as a real directory, not a symlink. This is therefore a candidate audit,
not an `AUDIT_ERROR`.

The independent recursive comparison found:

- `/candidate/prompt.py` is a regular file and byte-identical to
  `/reference/prompt.py` (SHA-256
  `3705edce076dd10a274c837a15bf688a69bd9c342a0576cabb0cb02ab7c53446`).
- `/candidate/py2mpy.py` is a regular file and byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The candidate and trusted `reference-semantics/` trees each have 25
  recursively inventoried entries (24 regular files plus the helper
  directory). Every relative path, entry type, and file digest is identical.
  There are no missing, additional, changed, mistyped, or symlinked semantics
  entries.
- No symlink occurs anywhere under `/candidate`.

The required generation-accounting files `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are all missing. No structured
generation trace or JSONL trace is present. This prevents reconstruction of
the generation narrative but does not change the independently reconstructed
source proof below.

The candidate's `prove.log` claims three `#Top` results. It was not relied on.
The extra `spec.json` is stale: it contains `finishLoop`, while current
`spec.k` and `verification.k` contain no such symbol. It was ignored, as were
`__pycache__`, candidate concrete tests, and all candidate prose/log claims.

Evidence:

- [integrity checker](evidence/integrity_check.py)
- [stage 1–2 command log](evidence/stage1-2.log)
- [untrusted artifact check](evidence/untrusted-artifacts.log)
- [toolchain record](evidence/environment.log)

Stage result: **PASS for the trusted mode boundary and source identity, with an
auditability concern for four missing generation-accounting artifacts and the
stale unused KAST file.**

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For every index `i` of a finite list of integers:

1. if `i` is divisible by 3, contribute the square of the element;
2. otherwise, if `i` is divisible by 4, contribute its cube;
3. otherwise contribute the unchanged element;
4. return the sum of all contributions.

Index 0 satisfies both divisibility tests, so the first rule gives square
precedence. The empty-list result is 0. Python integers are arbitrary
precision, matching K mathematical `Int` on this path.

`solution.py` uses a direct accumulator rather than the canonical temporary
list. Its manual `index` starts at 0, checks `% 3` before `% 4`, increments
once per element, does not mutate the input, and returns `total`. This is
extensionally the same algorithm on the intended domain.

### Translator identity

In scratch, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp -s regenerated-solution.mpy solution.mpy` also exited 0.
Both files have SHA-256
`13c68b0fc50ba93b60389fadabdcdfda4aa2b9130fec6f602fa9b859bd6c08cc`.
Thus the submitted MPY is exactly the trusted translator's output for the
submitted Python, not a substituted hand-written program.

### Independent differential test

The reviewer script independently imports `/reference/canonical.py` and the
scratch copy of submitted `solution.py`. It tested:

- all three documented examples;
- empty and every list-length boundary through 14;
- one-hot values at each index through 13, covering ordinary indices,
  multiples of 3, multiples of 4 only, and the 0/12 overlap;
- every list of lengths 0 through 5 over values `-2..2`;
- 484 unique deterministic random lists of lengths 0 through 40 and values
  `-100..100`.

There were 4,511 unique cases and zero mismatches. The full input/result JSONL
is preserved and has SHA-256
`6ca2b76883c38beef52458880c785eb1595aedfd5e42a00c275533209263f347`.
This is finite empirical evidence, not a substitute for the K proof.

Evidence:

- [differential script](evidence/differential_test.py)
- [complete differential inputs/results](evidence/differential-inputs-results.jsonl)
- [stage 1–2 command log](evidence/stage1-2.log)

Stage result: **PASS.**

## 3. Clean proof reconstruction

K `v7.1.337` was used from `/usr/bin`. The scratch directory initially
contained source only. Candidate-built definitions and caches were not copied.

### Fresh concrete definition

The supplied semantics was freshly compiled with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit status was 0. A reviewer-authored concrete program containing the exact
submitted function and six assertions was translated with the trusted
translator and run with:

```text
krun audit-concrete-tests.mpy \
  --definition audit-runtime-kompiled --output pretty
```

Exit status was 0. The final configuration had `.K`, `NoExc`, and exit code 0.
The cases include empty, singleton, all documented examples, indices through
12, and mixed negative values.

### Fresh proof definition and positive claims

The proof definition was freshly compiled with:

```text
kompile verification.k --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit status was 0. Every positive claim was then run as a selected target:

1. `SUM-SQUARES-SPEC.loop`, without trusted claims: exit 0, `#Top`.
2. `SUM-SQUARES-SPEC.body`, with only the already independently proved
   `loop` claim trusted: exit 0, `#Top`.
3. `SUM-SQUARES-SPEC.main`, with only the already independently proved
   `body` claim trusted: exit 0, `#Top`.

This is a proof dependency chain, not circular trust: the loop closes first,
the body closes using that theorem, and main closes using the body theorem.
The warnings concern unused variables in an unrelated fixed string rule; no
build or proof command failed.

Evidence:

- [concrete test source](evidence/concrete_semantics_tests.py)
- [rebuild/prove script](evidence/rebuild_and_prove.sh)
- [complete bounded rebuild/prove log](evidence/stage3-rebuild-prove.log)

Stage result: **PASS.**

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop` has no textual `requires`; its complete left-hand pattern is its
precondition. At a real loop head it assumes:

- the remaining iterator is `list(intVals(IS))`;
- `lst` still holds the original `list(intVals(ORIG))`;
- the current bound `value`, accumulator, and index are `OLD`, `ACC`, and
  `I`;
- the continuation is the actual `Return(total)`, `#endcall`, and arbitrary
  caller continuation.

Its postcondition removes the loop and leaves that continuation in place,
preserves `lst`, makes `value` the last iterated element (or `OLD` for an empty
remainder), makes `index` equal `I + length(IS)`, and makes `total` equal the
recursive `sumSquares(IS,I,ACC)`.

`body` starts immediately after the two initialization assignments, in the
actual local call frame with `lst=IS`, `total=0`, and `index=0`. It states that
the loop and return finish with value `sumSquares(IS,0,0)`, the function frame
is removed, the caller environment and stack are restored, and heap,
exception, return-state, and exit-code invariants hold.

`main` starts in an exact module scope containing `sum_squares` as a closure
over the exact submitted body. Calling it on any finite `Ints` list must
produce `sumSquares(IS,0,0)`, with empty heap/stack and normal control state.
The returned value is therefore constrained by recursive equations; it is not
a fresh variable, tautology, or one-way implication.

### Satisfiable preconditions

Concrete witnesses exist:

- `main`: take `IS=.Ints` and the exact displayed entry configuration. The
  result is 0.
- `body`: take `IS=.Ints`, `CONT=.K`, and the exact displayed local frame.
  The loop is empty and return/frame cleanup is executable.
- `loop`: take `IS=.Ints`, `ORIG=.Ints`, `SC=.Map`, `L=1`, `P=parent(0)`,
  `OLD=7`, `ACC=0`, `I=0`, and `KONT=.K`. This satisfies the disjoint exact
  map pattern and immediately reaches the claimed post-state.

Thus none of the claims has an inconsistent or unreachable entry pattern.

### Actual submitted AST

Fresh `kast --expand-macros` parsing compared the translated `solution.mpy`
with the proof macros structurally. The submitted function body and expanded
`sumSquaresFunctionBody` have the identical KAST digest
`7d483295a31c88e36dc2fc56c3a0ed3d4ec1a36856bab807f1ade16254156332`.
The submitted `For` body and expanded `sumSquaresLoopBody` likewise share
digest
`a4cf618aca542b2f80a26be3cf74752970052288a262ff35b48b536f31290aff`.
The module contains exactly one function named `sum_squares` with exactly the
parameter `lst`.

Although `main` begins at a call rather than `#loadAll(solution.mpy)`, fixed
`FuncDef` loading creates exactly the closure shown in its scope. The machine
checked KAST equality pins the body and parameters. No proof-local rule
intercepts or summarizes the function call.

### Ground substitutions

Reviewer configuration claims normalized the recursive result for:

- `[] -> 0`
- `[1,2,3] -> 6`
- `[-1,-5,2,-1,-5] -> -126`
- `[1,2,...,13] -> 1231`

All four exited 0 with `#Top`. The concrete K program and both Python
implementations return the same values. An initial reviewer attempt used bare
functional claims, which this backend explicitly does not support; it selected
no claims and is not counted as evidence. The corrected configuration-claim
run is the relied-upon result.

Evidence:

- [KAST pin checker](evidence/ast_pin_check.py)
- [KAST pinning log](evidence/stage4-ast-pinning.log)
- [ground claims](evidence/ground-summary.k)
- [successful ground log](evidence/stage4-ground-summary-config.log)
- [discarded unsupported functional-claim diagnostic](evidence/stage4-ground-summary.log)
- [construct/rule map](evidence/program-construct-map.md)

Stage result: **PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The inventory covers `reference-semantics/semantics.k`, all 23 supplied helper
K files, `verification.k`, and `spec.k`: 26 source files total. It records
source location, complete flattened sentence, attributes, and a decision for
every entry.

There are 1,119 entries:

- 708 rules;
- 235 syntax declarations;
- 3 claims;
- 1 configuration;
- 5 contexts;
- 27 modules and 27 endmodules;
- 88 imports and 25 file requirements.

Attributes inventoried include 149 `function`, 110 `total`, 35 `concrete`, 25
`symbol`, 47 `priority`, 26 `owise`, 6 `macro`, 2 `strict`, and 1
`seqstrict`. There are no local `functional`, `simplification`, or explicit
`opaque` attributes. The 25 `symbol` and concrete/opaque mathematical
boundaries are in the byte-identical fixed supplied semantics, chiefly
unrelated float/sort/string/builtin facilities.

All 1,087 supplied-semantics entries are marked as the fixed trusted baseline,
with the submitted-program path separately identified and manually reviewed.
This treatment follows the rendered `SUPPLIED_SEMANTICS` boundary: those files
define the selected language and are not candidate proof extensions. Unused
fixed rules for floats, dicts, slices, comprehensions, sorting, digests, and
similar constructs cannot match the submitted AST or its integer/list states.

Evidence:

- [inventory generator](evidence/static_inventory.py)
- [complete 1,119-entry TSV inventory](evidence/static-inventory.tsv)
- [inventory summary log](evidence/stage5-static-inventory.log)
- [construct/rule map](evidence/program-construct-map.md)

### Used fixed-semantics path

The full path is mapped in `program-construct-map.md`. In summary:

- `Call` performs ordinary name lookup, left-to-right argument evaluation,
  closure-frame allocation, parameter binding, and body execution.
- statement sequencing executes the two assignments, then `For`, then
  `Return`;
- strictness/contexts evaluate integer `%`, `*`, `+`, and `==` in the intended
  order;
- nested `If` control makes the multiple-of-3 branch precede the
  multiple-of-4 branch;
- `AugAssign` updates only the current local map;
- `Return` and `#pop` restore control/environment and remove the local frame.

The proof uses an unboxed, read-only list value, so no heap allocation or
mutation occurs. The claims pin normal return/exception/exit state. `pyMod` is
only used with positive divisors 3 and 4.

### Proof-local declarations and rules

`verification.k` contains no opaque value oracle and no rule that replaces
the submitted function body.

1. `Ints`, `.Ints`, and `intCons` are a finite mathematical integer sequence.
   `intVals` embeds that sequence as a proof-side `ValSeq`.
2. The two priority-40 iterator rules map empty `Ints` to `#iterDone` and
   nonempty `intCons(X,XS)` to `#iterYield(X,rest)`. Their patterns are
   disjoint and do not overlap the supplied `.ValSeq`/`vCons` rules. They
   rewrite only the active iterator term, preserve the continuation and every
   cell via framing, and introduce no abrupt control.
3. The three `contribution` equations are pairwise disjoint and exhaustive:
   `%3==0` gives square; `%3!=0 && %4==0` gives cube; and both nonzero gives
   identity. The rules are ordinary integer mathematics and cover negative
   values as well as nonnegative indices.
4. `sumSquares` has exactly empty/cons equations, strictly descends on the
   `Ints` tail, and accumulates exactly `contribution`. Its `[total]`
   declaration is covered by the only two `Ints` constructors.
5. `endIndex` and `endValue` likewise have disjoint empty/cons equations,
   strictly descend, and exactly characterize the other observable loop
   locals.
6. The two `[macro]` rules are syntax expansion, not runtime shortcuts. Fresh
   KAST equality proves they are the submitted loop and function bodies.

`sumSquares` encodes the requested mathematical result in the postcondition,
but it does not operationally replace the program. The actual body executes
under the fixed semantics, and the loop claim proves that execution produces
the summary. This is an acceptable definitional summary rather than a
smuggled task-answer rule.

### Iterator-encoding boundary

The proof-local iterator rules are an operational definition for a fresh
proof representation of external input. They are structurally isomorphic to
the fixed `.ValSeq`/`vCons` list iterator and do not permit a wrong element,
wrong termination point, state change, or continuation discard on intended
finite integer lists.

As an operational-sensitivity test, a separately compiled higher-priority
mutation changed nonempty yield from `X` to `X+1`. The mutated definition and
claim built successfully, but the loop proof exited 1 with
`WarnStuckClaimState`. Its residual explicitly compared
`endValue(XS,X+1)` with `endValue(XS,X)` and the corresponding different
`sumSquares` accumulators. This rejects an opposite interpretation and shows
that claim closure depends on exact yielded values.

The candidate nevertheless supplies no bridge-free, machine-checked universal
connection theorem between `intVals(IS)` and the fixed native
`.ValSeq`/`vCons` representation. The relation is justified by direct
structural inspection, sensitivity evidence, concrete K execution on native
lists, and differential testing—not by a universal K theorem. No concrete or
symbolic false conclusion witness exists for the rules on the intended domain,
so I do **not** label them unsound. This is the principal evidence/intent
bridge limitation supporting `CONCERNS` rather than `PASS`.

Evidence:

- [bridge mutant definition](evidence/verification-bridge-mutant.k)
- [bridge mutant claim](evidence/spec-bridge-mutant.k)
- [bridge sensitivity script](evidence/run_bridge_sensitivity.sh)
- [bridge sensitivity log](evidence/stage5-bridge-sensitivity.log)

Stage result: **PASS for static soundness; concern for the informal rather than
machine-checked representation bridge.**

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. The reviewer created a fresh claim
with the exact `main` precondition and changed only its result-bearing
destination from

```text
sumSquares(IS, 0, 0)
```

to

```text
sumSquares(IS, 0, 0) +Int 1
```

The empty-list state is a concrete satisfying witness: the real and summary
result is 0, while the mutation requires 1.

The mutated spec's `--dry-run` exited 0, establishing that it parsed and built.
The actual proof, using only the already proved original body theorem, exited
1. It produced `WarnStuckClaimState` and the expected failed implication:

```text
sumSquares(IS, 0, 0) +Int 1 #Equals sumSquares(IS, 0, 0)
```

The failure was not a parser error, missing import, timeout, or unrelated
crash. It was the reachable unmet result obligation.

Evidence:

- [fresh false mutation](evidence/spec-vacuity.k)
- [mutation runner](evidence/run_vacuity.sh)
- [mutation build/proof log](evidence/stage6-vacuity.log)

Stage result: **PASS.**

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics plus the explicit `Ints` iterator encoding,
for every finite constructor sequence of mathematical integers `IS`, if the
exact submitted `sum_squares` closure is called in the displayed normal entry
state on `list(intVals(IS))` and execution reaches its result, that result is
`sumSquares(IS,0,0)`. The recursive equations make this the sum obtained by
squaring indices divisible by 3, otherwise cubing indices divisible by 4, and
otherwise using the element unchanged. The proof also accounts for the
function frame, locals, normal return, empty heap/stack, and no exception.

This is a partial-correctness theorem. It does not machine-prove termination.
For finite `Ints`, termination is supported by the structurally decreasing
iterator and direct program control, but it is outside the reachability
claim's guarantee.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics` | Defines all syntax, configuration, evaluation, state, calls, and integer operations used by all claims | Acceptable and mandated trusted input; candidate tree is exactly identical |
| K v7.1.337 frontend/backend and builtin Int/Bool/Map/List theories | Parses, compiles, symbolically executes, reasons about arithmetic, and checks reachability | Ordinary toolchain trust boundary; fresh commands and outputs preserved |
| Proof-local `Ints`/`intVals` iterator rules | Determine loop termination and each value delivered to the actual body; therefore affect the final result | Mathematically sound structural input encoding and sensitivity-tested, but lacks a bridge-free universal K connection theorem; documented concern |
| `contribution`, `sumSquares`, `endIndex`, `endValue` | Define the exact postcondition and loop locals | Acceptable definitional mathematics: guarded cases are disjoint/exhaustive and recursion descends |
| Function/loop macros | Pin the body executed by the closure and loop claim | Acceptable; fresh expanded KAST is exactly identical to submitted MPY |
| Trusted-claim flags in downstream commands | `loop` is used by `body`; `body` is used by `main` | Acceptable theorem reuse because each dependency independently closed first with exit 0 and `#Top` |
| Prompt/canonical-to-summary intent bridge | Identifies the recursive K summary with the human-facing task | Directly evident from equations and supported on 4,511 differential cases, but not separately formalized as a K theorem |
| Unused fixed opaque/symbol operations | Could affect other MPY programs involving floats, sorting, strings, or builtins | Irrelevant to this theorem's AST and states; remain inside the supplied-semantics trust boundary |
| Candidate logs, `spec.json`, generation narrative | None | Not trusted or used; four accounting artifacts are missing and `spec.json` is stale |

Differential testing supports only implementation/canonical agreement on its
recorded finite inputs. It is not used in place of the K reachability proof.
Likewise, `prove.log`, the stale KAST, and any candidate report do not support
the verdict.

### Decision

The proof reconstructs cleanly, is non-vacuous and result-constraining, executes
the exact submitted body, and contains no materially unsound proof rule or
unconstrained result oracle. The proof-local input iterator is a truthful
finite-list representation, and a wrong-value mutation is rejected. Therefore
the proof is legitimate.

I select `CONCERNS` rather than `PASS` because the universal connection from
the proof-only `intVals` representation to native supplied-semantics list
values remains an informal structural bridge, the K summary-to-natural-language
bridge is not a separate formal theorem, and generation-accounting artifacts
are missing. These limitations do not enable a false conclusion on the
intended finite-list-of-integers domain and therefore do not justify
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
