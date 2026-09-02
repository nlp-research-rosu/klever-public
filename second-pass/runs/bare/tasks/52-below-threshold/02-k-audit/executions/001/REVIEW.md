# Independent adversarial review: 52-below-threshold

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted `solution.mpy` under its generated semantics. I
rebuilt both definitions from copied source, independently closed both positive
claims, checked that the theorem macro expands to the submitted translated
program, exhaustively reviewed every local rule, and obtained the expected
failure from fresh body-sensitivity and false-result mutations.

The concern is scope, not formal soundness. The prompt speaks of a Python list
of “numbers,” while the theorem and generated semantics cover only finite
`IntSeq` lists of K `Int` values and an `Int` threshold. The representation and
used-subset correspondence to CPython are independently audited and strongly
differentially tested, but are not a machine-checked refinement theorem and do
not cover floats, numeric subclasses, custom comparisons, or exceptional
behavior. Thus the proof is legitimate but soundly limited.

The Kit validation gates are:

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **FAIL (scope limitation only)** because the formal
  domain is narrower than an unrestricted reading of Python “numbers.”
- Gate C, trust/evidence auditability: **PASS**.

This corresponds to `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` does not exist. The trusted mount contains
exactly the expected trusted files:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

All required candidate source and run-record artifacts are regular files.
No candidate symlinks were found. The structured generation trace is a regular
JSONL file with 218 valid JSON records and no parse errors. Candidate-built
`semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`, and their
caches were treated only as untrusted extras and were never copied or used.
There are no generated helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`.

The candidate prompt and translator are byte-identical to the trusted mounts:

| Comparison | SHA-256 | `cmp` |
|---|---|---|
| trusted/candidate `prompt.py` | `b8e47fee4b6fffb27f872307ef74803b1e427e22802413851b9f0c61bb05306e` | 0 |
| trusted/candidate `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | 0 |

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace solely as untrusted claims. They
claim a successful prior run, including `#Top`; none of that result was reused.
`run-input.json` identifies problem `52-below-threshold`, the bare condition,
and no supplied semantics, consistent with the rendered mode.

Evidence:

- `/audit-output/evidence/stage1-inventory.log`
- `/audit-output/evidence/stage1-untrusted-claims.log`
- `/audit-output/evidence/stage1-trace-summary.log`
- `/audit-output/evidence/stage1_inventory.sh`
- `/audit-output/evidence/stage1_untrusted_claims.sh`
- `/audit-output/evidence/trace_summary.py`

There is no infrastructure breach and no missing, changed, mistyped, or
symlinked required artifact.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical implementation, `below_threshold(l, t)`
must return `True` exactly when every element `e` of `l` satisfies `e < t`.
The empty list returns `True`; if any element is equal to or greater than `t`,
the result is `False`. The canonical implementation returns early on the first
violating element.

The candidate `solution.py` has the required signature and implements exactly
that algorithm, with only the loop variable renamed from `e` to `x`.

### Trusted translation identity

I copied the source artifacts, but no compiled artifact, into
`/tmp/audit-work/reconstruction`. Running the trusted mounted translator copy
on the copied `solution.py` produced a file byte-identical to the submitted
`solution.mpy`:

```text
SHA-256 regenerated: ab83d1f82b73af6aa67b6272b8cce230d0a9034553bfa8fd44c9ab3f751a9186
SHA-256 submitted:   ab83d1f82b73af6aa67b6272b8cce230d0a9034553bfa8fd44c9ab3f751a9186
cmp exit: 0
```

Evidence: `/audit-output/evidence/stage2-prepare-and-translator.log` and
`/audit-output/evidence/stage2_prepare_scratch.sh`.

### Independent differential run

`/audit-output/evidence/differential_check.py` independently imports the
trusted canonical entry point and generated entry point and also compares both
with the direct mathematical oracle `all(e < t for e in l)`.

The run covered:

- both documented examples;
- empty lists, including a negative threshold;
- just-below, equality, and just-above boundaries;
- violations in the first, middle, and last position;
- negative values, duplicates, and arbitrary-size Python integers;
- all lists of lengths 0 through 4 over elements `-4..4`, with thresholds
  `-3..3` (51,667 exhaustive cases);
- 2,500 seeded generated lists of lengths 0 through 30 with values and
  thresholds in `[-10^12, 10^12]`.

All 54,183 cases matched; mismatch count was 0 and the script exited 0.
Evidence: `/audit-output/evidence/stage2-differential.log`.

This establishes strong finite support for the integer-domain intent bridge.
It is not substituted for the K proof or treated as a universal theorem.

## 3. Clean proof reconstruction

The live toolchain was K v7.1.293. All work occurred under
`/tmp/audit-work/reconstruction`; candidate-compiled definitions and caches
were not used.

### Concrete generated-semantics rebuild

Exact command:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition audit-semantic-llvm-kompiled
```

It exited 0. Fresh `krun` executions covered the two prompt examples, empty
input, equality, and a negative all-below case. Every run exited 0, reached
`.K`, and produced respectively `true`, `false`, `true`, `false`, and `true`.
The reviewer comparison script extracted each K `<result>` and checked it
against both Python implementations and the mathematical predicate; mismatch
count was 0.

Evidence:

- `/audit-output/evidence/stage3-kompile-concrete-llvm.log`
- `/audit-output/evidence/stage3-krun-prompt-true.log`
- `/audit-output/evidence/stage3-krun-prompt-false.log`
- `/audit-output/evidence/stage3-krun-empty.log`
- `/audit-output/evidence/stage3-krun-equality.log`
- `/audit-output/evidence/stage3-krun-negative-true.log`
- `/audit-output/evidence/stage3-concrete-python-comparison.log`
- `/audit-output/evidence/compare_concrete_results.py`

### Proof rebuild and positive claims

Exact build command:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition audit-verification-haskell-kompiled
```

It exited 0. Both claims were then reconstructed:

| Claim/run | Result |
|---|---|
| `SPEC.loop-invariant` selected directly | `#Top`, exit 0 |
| entry proof with the already independently proved loop claim marked trusted for that composition | `#Top`, exit 0 |
| full `SPEC` with neither claim trusted | `#Top`, exit 0 |

Evidence:

- `/audit-output/evidence/stage3-kompile-proof-haskell.log`
- `/audit-output/evidence/stage3-kprove-loop-invariant.log`
- `/audit-output/evidence/stage3-kprove-entry-with-proved-helper.log`
- `/audit-output/evidence/stage3-kprove-all.log`

One diagnostic run selected only `SPEC.below-threshold-correct`. K’s
`--claims` filtering removed the loop claim that the entry proof uses as its
circularity, so that changed theory made no progress. I interrupted it after
90 seconds (status 130); it is recorded in
`/audit-output/evidence/stage3-kprove-entry.log` and is not used as proof
evidence or as a candidate failure. The separately proved-helper run and the
full untrusted run are the relevant reconstructions.

The required success signal is present: every positive claim closes under the
proper source theory with both exit 0 and `#Top`.

## 4. Adequacy and real-program pinning

### Claim meanings

The auxiliary `loop-invariant` claim says:

- Precondition: for arbitrary remaining `XS:IntSeq`, threshold `T:Int`, full
  original input, and initial loop-variable slot, execution is at the exact
  real loop term and exact trailing `Return(true)` continuation; `l` and `t`
  contain the formal inputs and no result exists yet.
- Postcondition: the whole computation is consumed and the exact Boolean
  result is `allBelow(XS,T)`; only the final internal `x` slot is existential.

The entry `below-threshold-correct` claim says:

- Precondition: for arbitrary `XS:IntSeq,T:Int`, execution begins at `boot`
  with `solutionProgram`, the formal-input slots and `x` are unbound, and the
  result is `noResult`.
- Postcondition: execution consumes `<k>`, binds `l` and `t` to those exact
  inputs, and produces exactly `result(allBelow(XS,T))`; only final `x` is
  existential.

There is no free result variable, tautology, implication-only postcondition,
or omitted observable result cell.

### Program identity

Using the freshly built proof definition, I parsed submitted `solution.mpy` and
separately parsed `solutionProgram` with macro expansion. Their JSON KAST files
were byte-identical (`cmp` exit 0), with identical SHA-256
`03a98ad423b6b745e1371445002663d7995490d199e0bc1a3ce52d94ef27158e`.
Together with trusted-translator byte identity, this establishes:

```text
solution.py --trusted py2mpy.py--> submitted solution.mpy
                                      ==
                         expanded solutionProgram
```

Evidence:

- `/audit-output/evidence/stage4-kast-submitted-program.log`
- `/audit-output/evidence/stage4-kast-solution-macro.log`
- `/audit-output/evidence/stage4-kast-program-identity.log`
- `/audit-output/evidence/stage4-kast-program-hashes.log`

The `<k>` cell executes that program’s `BODY`; no rule replaces the body with
the desired answer.

### Satisfiable witness

A concrete state satisfying the universal entry precondition is:

```text
<k> boot </k>
<program> solutionProgram </program>
<input> cons(5,nil) </input>
<threshold> 5 </threshold>
<l> unbound </l> <t> unbound </t> <x> unbound </x>
<result> noResult </result>
```

Substitution gives `allBelow(cons(5,nil),5) = false`. The trusted canonical,
generated Python function, and fresh K execution all return `False`.
Evidence: `/audit-output/evidence/stage4-entry-precondition-witness.log` and
`/audit-output/evidence/stage3-krun-equality.log`.

## 5. Rule-by-rule static soundness review

The exhaustive production-, configuration-, rule-, claim-, and
used-constructor inventory is preserved in
`/audit-output/evidence/static-rule-inventory.md`. The mechanically extracted
declarations are in
`/audit-output/evidence/stage5-source-declaration-inventory.log`.

### Complete local declaration inventory

There are 14 local syntax/configuration entries:

1. `Pgm` with `Module(Stmts)`;
2. generated `Stmts` list;
3. `Stmt` with `FuncDef`, `For`, `If`, and `Return`;
4. generated comma-separated `ParamItems`;
5. `Params`;
6. `Expr` with `Name`, `Bool`, and `Compare`;
7. `CmpOp`;
8. `IntSeq` with `nil` and `cons`;
9. `Value` with integer, Boolean, and list variants;
10. `Slot`;
11. `Result`;
12. the nine evaluator/control `KItem` alternatives;
13. the complete `<bt>` configuration;
14. verification declarations `allBelow [function,total]` and
    `solutionProgram [macro]`.

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority,
or opaque declarations. There are no other helper K source files.

### Complete local rule inventory and decisions

| IDs | Rules | Static decision |
|---|---|---|
| R1 | Exact module/entry `boot`, parameter binding, and `BODY` dispatch | Sound narrow invocation bridge. It reads the exact name/arity and executes arbitrary matched `BODY`; it does not calculate a result. |
| R2-R3 | Empty and nonempty statement execution | Sound left-to-right sequencing. |
| R4 | Boolean literal evaluation | Exact. |
| R5-R7 | Lookups of `l`, `t`, and `x` | Literal names are disjoint; slots must be initialized. |
| R8-R10 | Left-to-right `>=` evaluation and K integer comparison | Correct operand order (`I1 >=Int I2`); less/equal/greater cases were concretely witnessed. |
| R11-R13 | Condition evaluation and true/false branch selection | Branch heads are disjoint and exactly one branch executes. |
| R14-R15 | Iterable evaluation and `VList` loop entry | Sound representation bridge for the immutable `IntSeq` input used here. |
| R16-R17 | Empty loop and head-binding/tail recursion | Constructors are disjoint; recursion structurally descends and preserves left-to-right order. |
| R18 | `Return(E)` discards the rest of the function computation | Sound for this one-function, no-call-stack language. All available expressions are pure; the submitted false path exercises continuation discard. |
| R19 | Boolean return writes `result(B)` and empties `<k>` | Requires `noResult`; exact observable return. |
| V1-V2 | `allBelow(nil,T)` and `allBelow(cons(I,XS),T)` | True mathematical definition; cases are disjoint and exhaustive for `IntSeq`, with structural descent. `[total]` is justified. |
| V3 | `solutionProgram` macro equation | Exact syntax definition; machine-checked against submitted KAST. |
| C1 | Loop invariant circularity | Matches the real recurring loop state after concrete progress and includes the exact trailing continuation; independently proved. |
| C2 | Entry claim | Executes the actual body and fixes the result exactly. |

Every constructor in submitted `solution.mpy` is covered:

| Construct | Rules |
|---|---|
| `Module`, `FuncDef`, `Params` | R1 |
| statement list / empty list | R2-R3 |
| `For` and `Name("l")` | R5, R14-R17 |
| `If` | R11-R13 |
| `Compare`, `CmpOp(">=")`, names `x,t` | R6-R10 |
| `Return(Bool(false/true))` | R4, R18-R19 |

All configuration cells are used. Evaluation order, loop binding, early return,
and result publication agree with the actual program. Rule overlaps are
constructor- or literal-disjoint. There is no fresh result-bearing symbol,
unconstrained oracle, answer-encoding semantic rule, or execution bypass.

### Operational/body sensitivity

As a distinct Gate A probe, I changed the pinned function body to always
`Return(Bool(true))` while leaving the original `allBelow` obligation in place.
The mutated definition built successfully (exit 0), but proof exited 1 with
`WarnStuckClaimState`; the reached result was `true` and the unmet obligation
was `true == allBelowBodyMutation(XS,T)`. Input `[5], t=5` is a concrete false
witness to that mutation. This confirms that changing the executed body changes
proof validity.

Evidence:

- `/audit-output/evidence/verification-body-mutation.k`
- `/audit-output/evidence/spec-body-mutation.k`
- `/audit-output/evidence/stage5-body-mutation-kompile.log`
- `/audit-output/evidence/stage5-body-mutation-kprove.log`

No local rule was found unsound. Accordingly, this review makes no
unsound-rule allegation requiring a false-conclusion witness. The narrower
Python-domain bridge is recorded as an adequacy limitation, not mislabeled as
a false K rule.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate negative result was
trusted. I created
`/audit-output/evidence/spec-vacuity-audit.k` from the fresh source theory.
It retains the real loop claim and changes the entry result from:

```text
result(allBelow(XS,T))
```

to:

```text
result(false)
```

This mutation is demonstrably false for the satisfiable empty-list state:
`allBelow(nil,T) = true`, and both Python implementations plus the fresh empty
`krun` return `true`.

The mutation’s `kprove --dry-run` exited 0, establishing that it parses and
builds. The real proof run exited 1 with `WarnStuckClaimState`. Its residual
shows the reached `result(allBelow(XS,T))` and failed condition
`false == allBelow(XS,T)`. This is the expected reachable unmet result
obligation, not a parser error, missing import, timeout, or unrelated crash.

Evidence:

- `/audit-output/evidence/stage6-vacuity-dry-run.log`
- `/audit-output/evidence/stage6-vacuity-kprove.log`
- `/audit-output/evidence/stage6-vacuity-artifact-hash.log`
- `/audit-output/evidence/stage3-krun-empty.log`
- `/audit-output/evidence/stage3-concrete-python-comparison.log`

Non-vacuity therefore passes.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

For every finite `XS:IntSeq` and every K integer `T`, if the exact submitted
program starts in the specified `boot` configuration with input `XS`,
threshold `T`, unbound local slots, and no result, then under the candidate’s
generated MPY semantics it reaches an empty computation with:

```text
result(allBelow(XS,T))
```

where `allBelow` is recursively equal to `true` exactly when every integer in
`XS` is strictly less than `T`. This is a partial-correctness statement under
the supplied K theory. The report does not use testing as a substitute for it.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, matcher, reachability engine, and core `INT`/`BOOL`/`STRING`/list/K-sequence operations | All concrete and symbolic results | Ordinary low-level toolchain trust; acceptable and explicitly outside the local proof. |
| Trusted mounted `py2mpy.py` as a faithful AST constructor transliterator | Link from `solution.py` to `solution.mpy` | The exact output identity is checked, but translator correctness itself is trusted by the audit authority. |
| R1 entry-driver bridge | Binding the external input/threshold and starting the submitted body | Acceptable: exact name/arity/module match, explicit state footprint, actual body execution, KAST identity, and body-sensitivity rejection. |
| R15 mapping `VList(IntSeq)` to left-to-right loop consumption | Correspondence between formal `IntSeq` and Python list iteration | Sound for immutable integer-list inputs; statically reviewed and concretely tested. It excludes mutation and non-integer/exceptional iteration. |
| K unbounded `Int` and `>=Int` as the model of Python integer comparison | Guard result and `allBelow` connection | Appropriate for ordinary Python integers, including arbitrary-size witnesses; excludes floats, subclasses, and custom comparison methods. |
| Human argument that the minimal generated semantics matches CPython for the used subset | Natural-language interpretation of the K theorem | Supported by exhaustive local rule review, body sensitivity, five K/Python comparisons, and 54,183 Python differential cases, but not a machine-checked CPython refinement theorem. This is the reason for `CONCERNS`. |
| Trusted canonical implementation as differential oracle | Finite implementation-to-intent evidence | Independent of proof equations and zero mismatches, but only empirical evidence over its recorded sample. |

There are no opaque symbols, unconstrained fresh values, assumed
proof-local lemmas, or task-answer rules. `allBelow` is not assumed: its
equations are transparent, and C1/C2 connect it to actual execution. Marking
C1 trusted in the isolated entry-composition run adds no final assumption
because C1 was separately proved and the full run also proved both claims with
neither trusted.

### Final rationale

The reconstructed K proof is sound, non-vacuous, result-constraining, and
machine-pinned to the real translated candidate. The generated semantics
executes every used construct and contains no illicit correctness shortcut.
The only material limitation is the narrower integer-only formal domain and
the necessarily informal/empirical bridge from this bespoke minimal semantics
to the broader possible readings of Python “numbers.” That supports a
legitimate proof with concerns, not rejection.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
