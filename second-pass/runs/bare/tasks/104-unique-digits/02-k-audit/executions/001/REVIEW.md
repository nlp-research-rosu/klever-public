# Independent adversarial audit: 104-unique-digits

## Executive decision

The candidate's `#Top` is reproducible, and the entry claim constrains an exact
result. It is nevertheless **not a legitimate partial-correctness proof of the
submitted Python program**.

The decisive failure is in `/candidate/semantic.k:119`: the only operational
rule recognizes the complete submitted AST and directly rewrites it to
`uniqueDigitsMeaning(NS)`, a hand-written implementation of the task answer.
There are no semantic rules for `Module`, function definition, lookup,
conditionals, comparisons, arithmetic AST nodes, calls, recursive calls,
returns, list comprehensions, or `sorted`. Consequently, the proof never
executes either function body. The postcondition reduces to the same
filter-and-sort equations used by that operational shortcut. Exact AST matching
pins syntax but does not supply the missing universal connection theorem.

This is also observably false as a model of the real submitted CPython program
on the prompt's unbounded positive-integer domain. For
`D = int("1" * 1200)`, the K shortcut returns `[D]`, while the submitted
recursive Python helper raises `RecursionError`; the trusted canonical function
returns `[D]`. This is a concrete satisfying intended-domain witness where the
bridge changes exceptional control into a normal result.

The audit ran against K v7.1.293. There was no infrastructure breach or
uncertainty.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` does not exist, exactly as required. I did not
search for or use any hidden reference semantics. The complete trusted mount is:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

This is therefore a candidate verdict, not `AUDIT_ERROR`. See
[stage1_integrity.log](evidence/stage1_integrity.log).

### Candidate artifacts and types

All required source deliverables are present as regular files:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and executable `prove.sh`. The requested
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and one
structured JSONL trace are also regular files. No required path is missing,
mistyped, or symlinked, and no symlink occurs in the trace tree.

The candidate also contains `semantic-kompiled/` and
`verification-kompiled/`. Those are additional generated build artifacts, not
source integrity failures. They were treated as untrusted and never copied or
used. There are no helper K source files. There is no candidate `PROOF.md` and
no candidate `spec-vacuity.k`; neither was treated as evidence.

The candidate prompt is byte-identical to `/reference/prompt.py` with SHA-256
`bebe5af48f3614d96f23c19fa6134409f0b3bfe2f759662569f0987e15e0507c`.
The candidate translator is byte-identical to `/reference/py2mpy.py` with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Those hashes also match the corresponding untrusted claims in
`run-input.json`.

### Untrusted provenance claims

I read the run-input, metrics, final agent text, generation output, and
structured trace only as claims. The trace records earlier stuck proofs as well
as the final `#Top`; it describes the semantics as tied to the complete AST and
states that the prompt is unbounded. The final report claims that `prove.sh`
completed all claims. A bounded extraction, including record counts, relevant
commands, outputs, and final claims, is in
[stage1_untrusted_claims.log](evidence/stage1_untrusted_claims.log); the
extractor is [extract_untrusted_claims.py](evidence/extract_untrusted_claims.py).
None of those claims was used instead of reconstruction.

Stage 1 result: **PASS for provenance integrity**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`, the entry point
`unique_digits(x)` accepts a list of positive integers. It must retain every
occurrence of an element if and only if all of that element's decimal digits
are odd, discard elements having any even digit, preserve multiplicity, and
return the retained elements sorted in increasing order. The empty list is
valid. The prompt states no upper bound on list length, integer magnitude, or
decimal digit count.

The candidate implementation uses recursive quotient-by-ten digit inspection,
a list comprehension, and `sorted`. Mathematically this implements the intended
predicate for positive integers while the recursion completes, and it preserves
duplicates.

### Trusted translation

I regenerated `solution.mpy` in scratch with the trusted translator:

```text
python3 /tmp/audit-work/104-unique-digits/reference/py2mpy.py \
  /tmp/audit-work/104-unique-digits/candidate/solution.py \
  > /tmp/audit-work/104-unique-digits/candidate/solution.regenerated.mpy
```

The regenerated and submitted terms are byte-identical, both with SHA-256
`d8d3826e35a2ff49382daa10d55e5efc95ef660c0c28438bc242abd69a136940`.
Command, comparison, hashes, and exit 0 are in
[stage2_translation.log](evidence/stage2_translation.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports
the trusted canonical and copied candidate entry points. Its reproducible input
scope is:

- both documented examples;
- empty, singleton, decimal, even-digit-position, ordering, and duplicate
  cases;
- every singleton integer from 1 through 2000;
- five values around each power of ten from `10^1` through `10^18`;
- 1,000 deterministic random lists, seed 260, lengths 0 through 20, with
  values from 1 through `10^18`;
- positive 1,200-digit and 2,000-digit all-odd integers.

The 3,105 ordinary cases had zero mismatches. Both deep positive boundary cases
diverged: the canonical returned the sole input, while the candidate raised
`RecursionError` at Python's default recursion limit of 1000. The script exits
1 because it correctly reports those two material divergences. Full scope,
outcomes, and status are in
[stage2_differential.log](evidence/stage2_differential.log).

This finite test is evidence, not a proof. The deep cases expose an
implementation-to-contract and K-to-CPython mismatch on the stated domain.

Stage 2 result: **FAIL for full implementation-to-intent fidelity**, although
ordinary finite inputs strongly support the mathematical algorithm.

## 3. Clean proof reconstruction

All execution sources were copied to
`/tmp/audit-work/104-unique-digits/candidate`; trusted inputs were copied to
`/tmp/audit-work/104-unique-digits/reference`. Candidate-built definitions and
caches were not copied. The six core scratch source files remained
byte-identical to `/candidate` throughout the reconstruction, as recorded in
[stage3_scratch_provenance.log](evidence/stage3_scratch_provenance.log).

### Fresh builds

The concrete semantics and proof definition were independently rebuilt with
the Haskell backend:

```text
kompile semantic.k --backend haskell \
  --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Both exited 0. See
[stage3_build_semantics.log](evidence/stage3_build_semantics.log) and
[stage3_build_verification.log](evidence/stage3_build_verification.log).

### Positive claims

The original submitted spec was run as a whole:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`; the two ground digit claims were reported as
trivial. See
[stage3_prove_original_all.log](evidence/stage3_prove_original_all.log).

For independent per-claim evidence, I copied the five claims unchanged except
for adding labels in [spec_labeled.k](evidence/spec_labeled.k), then selected
each label separately. Entry, both digit checks, and both examples all exited 0
and printed `#Top`:

- [entry](evidence/stage3_claim_entry.log)
- [odd true](evidence/stage3_claim_odd_true.log)
- [odd false](evidence/stage3_claim_odd_false.log)
- [example one](evidence/stage3_claim_example_one.log)
- [example two](evidence/stage3_claim_example_two.log)

### Fresh concrete execution

The rebuilt generated semantics was run on empty input, the base/even branches,
both examples, and a duplicate-preservation case. Every `krun` exited 0 and
produced the same finite list as both independent Python implementations. The
commands and K outputs are in
[stage3_concrete_k.sh](evidence/stage3_concrete_k.sh) and its individual
`stage3_krun_*.log` files; matching Python outputs are in
[stage3_python_cases.log](evidence/stage3_python_cases.log).

This establishes that the submitted K theory compiles, that every submitted
positive claim closes, and that its shortcut computes the expected answer on
the tested ordinary inputs. It does not establish that the theory executes the
Python program.

Stage 3 result: **PASS for mechanical reconstruction**.

## 4. Adequacy and real-program pinning

### Claims in plain language

The five entry claims state:

1. For every finite `IntSeq NS` whose elements are all greater than zero,
   executing `solutionProgram` followed by the abstract
   `invoke("unique_digits", pyList(NS))` produces exactly
   `pyList(uniqueDigitsSpec(NS))`.
2. The mathematical alias `allDecimalDigitsOdd` is true at 97531.
3. The same alias is false at 1422.
4. The first prompt input produces `[1, 15, 33]`.
5. The second prompt input produces `[]`.

The entry precondition is satisfiable. For example, `.Ints`, `cons(1,.Ints)`,
and `cons(15,cons(33,cons(1422,cons(1,.Ints))))` all satisfy it. Substituting
the last sequence makes the claimed result `[1,15,33]`, matching both Python
implementations and the rebuilt `krun`. `[1]` is another concrete satisfying
state and produces `[1]` in the K theory and both Python implementations.

The postcondition is exact and result-constraining: it is not a free variable,
tautological implication, or unconstrained existential. The fresh false
mutation in Stage 6 confirms that changing the result alone is rejected.

### Pinning failure

`solutionProgram` expands to the exact submitted AST, and trusted regeneration
confirms that identity. Concrete `krun solution.mpy` also parses that AST.
Therefore the proof is syntactically pinned to the submitted term.

It is not behaviorally pinned. The `<k>` cell never evaluates that AST.
`isUniqueDigitsProgram(P)` performs one structural match, after which the
single operational rule at `/candidate/semantic.k:119` replaces:

```text
P ~> invoke("unique_digits", pyList(NS))
```

with:

```text
pyList(uniqueDigitsMeaning(NS))
```

The two program-defined bodies, parameter binding, recursion, comprehension,
and built-in call do not execute. There are no helper or loop execution claims
that could provide a connection theorem. The entry postcondition then unfolds
`uniqueDigitsSpec` to the same `sortInts(filterOddDigits(NS))` expression used
by `uniqueDigitsMeaning`. Thus the proof is circular as a program-correctness
argument: the hand-written execution answer and hand-written specification are
definitionally identical.

An operational-sensitivity mutation changed the submitted helper's even branch
to return `True`. Python evaluated that mutation and returned `[2]` for `[2]`,
but the rebuilt K semantics left the mutated AST stuck because the recognizer
no longer matched. See
[mutated_solution.py](evidence/mutated_solution.py),
[stage4_mutated_body_python.log](evidence/stage4_mutated_body_python.log), and
[stage4_mutated_body_krun.log](evidence/stage4_mutated_body_krun.log).
`krun` itself exits 0 on that residual; the unreduced AST, not the process
status, is the evidence. This demonstrates exact syntax sensitivity but also
shows there is no construct semantics behind the exact pattern.

For the positive 1,200-digit witness, the K shortcut exits 0 with a normal
singleton result
([stage4_krun_deep_positive.log](evidence/stage4_krun_deep_positive.log)),
whereas the real candidate raises `RecursionError`
([stage2_differential.log](evidence/stage2_differential.log)).

Stage 4 result: **FAIL for real-program pinning**.

## 5. Rule-by-rule static soundness review

The complete inventory, including every local syntax production, configuration
cell, attribute, all 16 `semantic.k` rules, all six `verification.k` rules, all
five claims, construct mapping, coverage, overlap, descent, and rule
classification, is
[rule_inventory.md](evidence/rule_inventory.md). The raw declaration/rule scan
with line numbers is [stage5_raw_inventory.log](evidence/stage5_raw_inventory.log).

### Syntax, configuration, and used constructs

The grammar declares every submitted AST constructor:
`Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`, `CmpOp`, `Int`,
`Return`, `Bool`, `BinOp`, `Call`, `ListComp`, and `CompFor`. It also declares
finite `IntSeq`, `pyList`, unused `pyBool`, and abstract `invoke`.

Declaration is the entire coverage. There are no operational rules for any of
the AST constructs. There are no strictness declarations or other evaluation
contexts. The configuration contains only `<k>`; it has no bindings,
environment, stack/frame, heap, iterator, exception, or built-in namespace
cell. Accordingly, it cannot model evaluation order, name selection, argument
binding, calls and returns, recursive frames, exception propagation, list
allocation/comprehension, or the lookup and behavior of `sorted`.

### Equational functions

The following local functions are declared `[function,total]`:
`solutionProgram`, `oddDigits`, `filterOddDigits`, `insertSorted`, `sortInts`,
`uniqueDigitsMeaning`, `positiveInts`, `allDecimalDigitsOdd`,
`retainAllOddDigitItems`, `inIncreasingOrder`, and `uniqueDigitsSpec`.
`isUniqueDigitsProgram` is `[function]` but intentionally partial.

- `solutionProgram` truthfully expands to the exact regenerated AST.
- The four `oddDigits` equations have disjoint, exhaustive integer guards and
  descend for positive odd inputs. The negative equation is an over-broad
  out-of-contract convention; I do not label it unsound based on an
  out-of-domain witness.
- `filterOddDigits` has complementary keep/drop guards and structural descent.
- `insertSorted` has disjoint/exhaustive `<=` and `>` branches.
- `sortInts`, `positiveInts`, and the sequence functions structurally descend
  over finite `IntSeq`.
- The contract-level functions are truthful aliases for the hand-written
  mathematical summary.

There are no overlaps with disagreeing right-hand sides and no material
totality gaps in these mathematical functions. There are no local priority
rules, simplification rules, `[functional]` declarations, `[opaque]`
attributes, `[concrete]` rules, or proof-local operational rules.

### Materially invalid operational rule

The rule at lines 119-121 is an operational bridge, not a definitional summary,
because it preempts all execution of program-defined code. Its complete local
context is:

- reads the whole `P:Program`, `NS:IntSeq`, and an arbitrary framed `<k>`
  suffix;
- requires only structural recognition of the exact AST;
- consumes the program and abstract invocation;
- writes a result-bearing `pyList(uniqueDigitsMeaning(NS))`;
- has no other cells to read, preserve, or update.

Its justification scope is empty: no fixed construct semantics or auxiliary
reachability claim establishes that executing the bodies has this value and
control effect. Syntactic equality does not establish value equivalence.
Finite differential tests cannot replace the required universal connection
theorem. The bridge directly encodes the task answer and silently fabricates
results for every used construct.

Required false-conclusion witness: with the exact submitted program and
`NS = cons(int("1"*1200),.Ints)`, the rule enables a normal returned singleton
on an input satisfying `positiveInts`. Actual CPython reaches a
`RecursionError`, not that normal result. The K and Python records are
[stage4_krun_deep_positive.log](evidence/stage4_krun_deep_positive.log) and
[stage2_differential.log](evidence/stage2_differential.log). This witnesses a
false control/result conclusion on the intended input domain; the rule is
materially unsound as semantics for the real generated program.

Even if one deliberately abstracted away CPython's finite recursion stack, the
bridge would remain illegitimate under the required proof boundary: it replaces
the very program-defined computation whose property is to be proved and has no
machine-checked connection theorem.

Stage 5 result: **FAIL for static real-program soundness**.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact. I created a fresh mutation in
[spec-vacuity.k](evidence/spec-vacuity.k). Its concrete precondition is
`positiveInts(cons(1,.Ints))`, which is true, while its destination was changed
from the correct `[1]` to the false `[]`.

First, `kprove --dry-run` parsed and built the mutation successfully with exit
0; see [stage6_mutation_dry_run.log](evidence/stage6_mutation_dry_run.log).
Then the actual proof exited 1 with `WarnStuckClaimState`. Its residual was:

```text
<k>
  pyList ( cons ( 1 , .Ints ) ) ~> _DotVar1 ~> .K
</k>
```

That is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. See
[stage6_mutation_proof.log](evidence/stage6_mutation_proof.log).

Stage 6 result: **PASS for result non-vacuity**. This does not repair the
execution-substitution failure.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate's custom rewrite theory and K's imported mathematical
domains:

- for any finite `IntSeq NS` satisfying `positiveInts(NS)`;
- the distinguished exact-AST constant followed by abstract `invoke`;
- rewrites through the whole-program shortcut and equations;
- to the insertion-sorted sequence obtained by filtering `NS` with the
  hand-written quotient/remainder predicate.

It also establishes two ground facts about that mathematical predicate and two
ground outputs through the same shortcut. That is a theorem about the
candidate-authored summary theory. It is not a reachability theorem derived
from evaluation of `solution.mpy`.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 prover/compiler and imported `INT`, `BOOL`, `STRING`, and generated list machinery | All builds, arithmetic equations, and proof closure | Ordinary low-level trusted primitive boundary; acceptable and explicitly versioned. |
| Trusted `/reference/py2mpy.py` | Identity between `solution.py` and `solution.mpy` | Acceptable syntactic bridge; byte identity was independently checked. It provides no semantics. |
| `solutionProgram` expansion and `isUniqueDigitsProgram` | Selection of the submitted AST | Acceptable as syntax pinning only. |
| Mathematical `oddDigits`, filter, insertion, and sort equations | K output and formal postcondition | Equations are sound on positive finite `IntSeq` by ordinary mathematics. Their interpretation as the Python body's execution is not proved. |
| Whole-program rule at `semantic.k:119` | Universal entry claim, both examples, all concrete `krun` results | Illegitimate operational bridge. It replaces program-defined execution with the property-bearing answer, lacks a connection theorem, and has a concrete positive-domain exception/control counterexample. |
| Python recursion, comparison, floor division, name binding, recursive calls, comprehension, allocation, return, exception behavior, and built-in `sorted` | Any claim about the real generated program | Entirely assumed or omitted. No corresponding K semantics or auxiliary claims exist. |
| Independent differential testing | Empirical Python implementation-to-canonical bridge | 3,105 ordinary cases support the algorithm only finitely; two deep cases refute full-domain equivalence. It cannot justify the K operational bridge universally. |
| Informal mathematical argument that repeated quotient/remainder tests characterize decimal odd digits | Natural-language intent bridge on recursion-success cases | Plausible and supported by tests, but not machine-checked against program execution. |

### Gate summary

- **Gate A — real-program soundness: FAIL.** The task-answer operational bridge
  bypasses every used construct and has no connection theorem; the deep
  positive witness also shows false exceptional/normal control.
- **Gate B — intent adequacy: FAIL.** The formal precondition covers all
  positive K integers, but the real recursive CPython implementation does not
  meet the unbounded prompt on sufficiently many-digit positive inputs, and
  the generated language omits exceptions and recursion limits.
- **Gate C — trust and evidence auditability: FAIL in the candidate report.**
  It presented concrete shortcut executions and `#Top` as program proof
  without disclosing the result-bearing bridge as an assumption. The reviewer
  evidence is reproducible, but it demonstrates rather than repairs that trust
  failure.

Mechanical proof closure and a successful false-postcondition rejection are
necessary but not sufficient. Because Gate A fails, the candidate falls
directly under the decision rule for a proof that relies on materially unsound
semantics and bypasses real execution.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
