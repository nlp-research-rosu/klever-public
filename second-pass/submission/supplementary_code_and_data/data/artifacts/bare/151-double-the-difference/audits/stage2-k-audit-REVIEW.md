# Independent adversarial audit: 151-double-the-difference

The candidate contains a legitimate partial-correctness proof of its real
generated program. I reconstructed the definitions from source, obtained
`#Top` on the original two-claim target spec, mechanically pinned the proof
term to trusted-regenerated `solution.mpy`, reviewed every local K declaration
and rule, and obtained the expected stuck obligation from a fresh false result
mutation. The generated semantics is small and task-scoped, but it faithfully
covers every construct and built-in value tag materially used by this program.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: GENERATED_SEMANTICS`, condition `bare`, and problem
`151-double-the-difference`. These agree with `/run.json`, `/task.json`, and
`/generation-result.json`. The trusted boundary is internally consistent:
`/reference/reference-semantics` is absent, as generated-semantics mode
requires.

I read and structurally checked all required pipeline-v3 records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt` under
  `/generation-evidence`;
- the complete structured trace, one JSONL file containing 274 valid records.

All required mounts and records are real directories or regular files. No
symlink or special entry occurs below `/candidate`, `/generation-evidence`, or
`/reference`. The campaign lock is JSON-identical to the campaign block in
`/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every individually recorded SHA-256 checked in the audit input and generation
result matches its mounted file.

Using an independent reimplementation of the pipeline-v3 tree encoding, the
mounted candidate hashes to
`3c153940251af71a81e568dd1f20dcf6b2d42de1de92ab47c7ee7b454e6e6c94`,
exactly the workspace digest in both the invocation and generation result. The
structured trace hashes to
`04ec3d5360d051695f50a642188d6dcb142b4dcaf44fc8c5f5c4f7a5aa5ada63`,
exactly `usage.json`'s source-trace digest, and its sole file independently
matches the generation-result file hash. The additional launcher-owned
aggregate identifiers in `audit-input.json` use no declared serialization and
therefore were recorded but not conflated with the pipeline-v3 encoding.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounted versions. Candidate proof sources and required deliverables are all
present. Candidate-provided compiled definitions, logs, and final prose were
not reused.

Evidence:
[provenance checker](/audit-output/evidence/provenance_check.py),
[integrity log](/audit-output/evidence/01-provenance.log).

Stage 1: PASS. No infrastructure breach or provenance defect was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `double_the_difference(lst)` to return the sum of
the squares of nonnegative odd integers in the input list, ignoring negative
values and non-integers, with 0 for an empty list. Zero's inclusion in the
nonnegative test is immaterial because its square contributes zero.

The candidate program initializes `total = 0`, iterates in list order, checks
`isinstance(value, int)`, then `value >= 0`, then `value % 2 == 1`, and adds
`value * value`. It returns `total`. This directly implements the stated
contract for ordinary built-in integer/float inputs. As in CPython, `bool` is
an `int` subclass, so `True` contributes 1 and `False` contributes 0.

I regenerated the submitted constructor program with the trusted translator:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0. `cmp` exited 0, and both submitted and regenerated files
have SHA-256
`08c0fbd5bc503b676d8896b54af5b1c0e7e8aa6e9c12209a64c060457117e752`.

The independent differential test imports `/reference/canonical.py` and the
scratch copy of candidate `solution.py`. It covered:

- all five documented/empty examples;
- 21 explicit empty, sign, parity, type, Boolean, and large-integer branch
  boundaries;
- every list of length 0 through 4 over a 14-value finite built-in pool
  (41,371 cases);
- 10,000 seeded lists of length 0 through 25 over large/small integers, finite
  floats, and Booleans.

There were zero mismatches in all 51,397 core cases.

Separate extension probes intentionally exposed limitations of the trusted
canonical oracle rather than hiding them. It squares positive infinity even
though infinity is not an integer, and it squares `Fraction(3,2)` even though
that value is non-integral. It also differs from the candidate on some
`Decimal` and `Fraction` objects. Those classes are not imported or mentioned
by the HumanEval prompt, and the canonical behavior on `Fraction(3,2)`
contradicts the natural-language contract. They are not a material narrowing
of the intended ordinary built-in numeric domain. The proof does not claim
behavior for arbitrary user-defined numeric classes.

Evidence:
[differential script](/audit-output/evidence/differential_test.py),
[fidelity runner](/audit-output/evidence/run_fidelity.sh),
[complete results](/audit-output/evidence/02-fidelity-differential.log).

Stage 2: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/candidate-src` and built
new definitions at `/tmp/audit-work/build-verified`; no
`/candidate/*-kompiled` directory or cache was used. The live toolchain reports
K v7.1.293.

The exact fresh positive pipeline was:

```text
timeout 300 kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build-verified/semantic-kompiled
# exit 0

timeout 300 kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build-verified/verification-kompiled
# exit 0

timeout 300 kprove spec.k \
  --definition /tmp/audit-work/build-verified/verification-kompiled \
  --spec-module SPEC
# #Top
# exit 0
```

The original command proves both claims in `SPEC`. I additionally made a
label-only copy and selected the loop claim independently; it also printed
`#Top` and exited 0. A diagnostic that excluded the loop helper made the entry
claim fail, as expected: the entry proof genuinely depends on the invariant
rather than closing by a shortcut.

For generated-semantics validation, I ran the fresh definition against 19
normal and boundary inputs: all prompt examples, empty input, sign/parity
boundaries, all runtime tags, mixed and nested lists, and unbounded large
integers. Every `krun` exited 0, the computation ended at `.K`, all modeled
locals were cleared, and the K result equaled independent Python execution.
There were zero mismatches.

Evidence:
[clean runner](/audit-output/evidence/run_clean_reconstruction.sh),
[successful build/proof log](/audit-output/evidence/03-clean-reconstruction.log),
[dynamic comparison script](/audit-output/evidence/semantics_dynamic_test.py).
The expected entry-without-helper diagnostic is preserved separately in
[its log](/audit-output/evidence/03-clean-reconstruction-entry-isolation-diagnostic.log).

Stage 3: PASS.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

The loop claim has no extra `requires` restriction. For arbitrary finite
`VS:Vals`, accumulator `ACC:Int`, old `value`, input, `lst`, and function
cells, it starts at the actual loop control term followed by the real return.
It consumes the loop and return, clears the local/function cells, and sets the
result to `pyInt(oddSquareFold(VS, ACC))`.

A concrete satisfying loop state is:

```text
VS = intCons(3, intCons(2, nil))
ACC = 1
<k> loop("value", pyList(VS), loopBody)
    ~> Return(Name("total")) .Stmts </k>
<input> pyList(intCons(1, VS)) </input>
<lst> pyList(intCons(1, VS)) </lst>
<total> pyInt(1) </total>
<value> pyInt(1) </value>
<function> function(Params("lst"), BODY) </function>
<result> noResult </result>
```

The claimed result is
`oddSquareFold(intCons(3,intCons(2,nil)),1) = 10`, matching both Python
implementations on `[1,3,2]`.

The entry claim starts from the exact initialized configuration with
`solutionProgram` and an arbitrary `pyList(VS)`. It consumes the whole module
and call, clears locals, and requires the result—not an existential or free
value—to be exactly `pyInt(oddSquareFold(VS,0))`.

For the concrete satisfying entry input
`VS = intCons(1,intCons(3,intCons(2,intCons(0,nil))))`, the formal result
reduces to 10, and both Python implementations return 10.

### Exact program pinning

`solutionProgram` and `loopBody` are constructor abbreviations, not execution
summaries. A reviewer script extracted both equation RHSs, expanded the sole
`loopBody` occurrence, normalized only whitespace and the explicit
empty-list spelling `.Stmts`, and compared the result with trusted-regenerated
`solution.mpy`. Both normalized terms have length 388 and SHA-256
`bd5455c6af6f8b9c71866deaf7dcf3acb88743563db54970bb5761f8a0bcc3ba`.
They are constructor-identical.

A body-sensitivity mutation changed the term actually executed by the claim:
each selected element added `value*value + 1`. The mutated K program returned
2 on `[1]`; the original required result is 1. Its spec built successfully,
and `kprove` exited 1 with `WarnStuckClaimState` at the final
`<result> pyInt(2) </result>`. Thus proof success is sensitive to the
submitted body, not merely to an external source filename.

Evidence:
[mechanical pinning script](/audit-output/evidence/pinning_check.py),
[pinning log](/audit-output/evidence/04-pinning.log),
[body mutation](/audit-output/evidence/verification-body-mutation.k),
[body mutation spec](/audit-output/evidence/spec-body-mutation.k),
[body-sensitivity log](/audit-output/evidence/04-body-sensitivity.log).

The formal `Vals` domain contains every finite list built from unbounded K
integers, K floats, Booleans, and recursively nested lists. It therefore covers
the material source-contract domain of finite lists of ordinary built-in
integers/floats; the extra nested-list cases are handled soundly by ignoring
them. Valid-list input is exactly the source precondition. There is no finite
size bound or bounded unrolling.

Stage 4: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[05-rule-inventory.md](/audit-output/evidence/05-rule-inventory.md). It
enumerates 53 local syntax/function declarations, all 44 rules in
`semantic.k`, all 10 equations in `verification.k`, and both claims.

### Construct and state coverage

Every constructor in `solution.mpy` maps to declared syntax and behavior:

- `Module`, statement sequencing, `FuncDef`, and `start` load and invoke the
  exact one-parameter function;
- `Assign`, `For`, `If`, and `Return` have explicit control rules;
- `Int`, `Name`, `BinOp` for `+`, `*`, `%`, `Compare` for `>=` and `==`, and
  the exact `isinstance(...,int)` call have expression equations;
- `pyInt`, `pyFloat`, `pyBool`, and `pyList` preserve the runtime tag needed by
  `isinstance`; `nil` and every cons constructor have loop and fold cases, with
  Booleans split into true and false cases.

The configuration contains exactly the material state: computation, immutable
input, three local slots, selected function, and result. Expression evaluation
is pure in this submitted program, so recursive function evaluation preserves
Python's observable evaluation order. Loop rules bind before the body, execute
the body before the tail, and preserve the accumulator. Return rules set the
exact value, discard the remaining function continuation as Python return
does, and clear every modeled local/function cell. The with-suffix and
no-suffix return rules have identical observable effects on their possible
overlap.

The arithmetic helpers are intentionally partial outside int/bool operands.
They do not fabricate unsupported results: an out-of-scope use retains an
unreduced `asInt`. Every reached use is int/bool typed. The `[owise]`
`isIntVal` rule is disjoint from the explicit int and bool cases.

### Proof extensions

`loopBody` and `solutionProgram` merely expose exact constructor trees.
`selectedSquare` has two complementary, non-overlapping guards and is total
over `Int`; its SMT hook states the same conditional expression. For negative
integers the nonnegative conjunct is false, so any distinction between
remainder conventions is immaterial; for nonnegative integers remainder by 2
has the intended parity meaning.

`oddSquareFold` is structurally descending and covers `nil` plus every cons
constructor, splitting the Boolean constructor into true and false equations.
Its bool cases agree with CPython's bool-as-int behavior.
Neither `selectedSquare` nor `oddSquareFold` occurs on the operational side of
the language semantics. The real body executes, and the fold appears only in
the invariant/postcondition. Consequently:

- there is no operational bridge;
- there is no fresh or opaque result-bearing oracle;
- there is no circular use of one unconstrained symbol in execution and the
  postcondition;
- there is no local priority, simplification, or concrete rule;
- there is no proof-local ordinary rewrite that preempts real execution.

All inventoried local rules are sound on their complete used domain. I found
no unsound rule, so there is no false-conclusion witness to report. The
inventory identifies the narrower partial-function boundary instead of
mislabeling it unsound.

Stage 5 / validating-proof Gate A static portion: PASS.

## 6. Fresh non-vacuity test

I created a new spec that retains the genuine loop helper and changes only the
entry result obligation from:

```text
pyInt(oddSquareFold(VS, 0))
```

to the false:

```text
pyInt(oddSquareFold(VS, 0) +Int 1)
```

The satisfiable witness `VS = nil` has candidate result 0, canonical result 0,
and mutated required result 1.

`kprove --dry-run` exited 0, establishing that the mutation parsed and built.
The live proof then exited 1 with `WarnStuckClaimState`; its residual says the
configuration unifies with the destination but the implication check fails,
and explicitly retains:

```text
oddSquareFold(VS, 0) +Int 1
#Equals
oddSquareFold(VS, 0)
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:
[false mutation](/audit-output/evidence/spec-vacuity-audit.k),
[runner](/audit-output/evidence/run_nonvacuity.sh),
[proof log](/audit-output/evidence/06-nonvacuity.log).

Stage 6 / validating-proof Gate A5: PASS.

## 7. Proven versus assumed accounting

### Machine-checked result

Under the fresh `MPY` semantics and `VERIFICATION` equations, for every finite
`VS:Vals`, execution of the constructor-identical submitted program from the
initialized configuration reaches `.K`, clears the modeled local/function
cells, and returns:

```text
pyInt(oddSquareFold(VS, 0))
```

The helper claim establishes the stronger accumulator-parametric loop result
for arbitrary finite suffixes and arbitrary integer accumulators. The theorem
is result-constraining and is not conditional on an opaque value.

As a partial-correctness statement, this establishes the postcondition for
terminating executions. The represented finite-list loop in fact structurally
descends, but no claim about arbitrary Python objects or non-list invocation is
made.

### Trust ledger

1. **K toolchain and built-ins.** K v7.1.293, the Haskell backend, reachability
   logic implementation, parser, and imported `INT`, `BOOL`, `FLOAT`,
   `STRING`, and `K-EQUAL` modules are trusted. These are ordinary low-level
   verification foundations, not task-answer axioms.

2. **SMT hook for `selectedSquare`.** The hook maps the locally defined total
   function to the same guarded square-or-zero expression. It affects the
   mathematical postcondition simplification, not program execution. Its
   agreement with the complementary operational equations was checked
   statically.

3. **Trusted translator.** The mounted translator is a trusted input.
   Regeneration was byte-identical, and mechanical expansion pins the proof
   program to its output. The proof does not establish the translator's
   general correctness for all Python ASTs; only this exact generated term is
   needed.

4. **Generated-semantics-to-CPython bridge.** The K semantics is not a
   universal Python semantics. Its correspondence for this program's exact
   constructors, bindings, tag tests, integer/bool arithmetic, loop order,
   return control, and state effects was reviewed rule by rule and tested
   against Python on normal/boundary inputs. This is an intentionally narrow
   but complete language subset, permitted in generated-semantics mode.
   Differential testing is finite evidence for this bridge, not a replacement
   for the K proof.

5. **Runtime input representation.** `Vals` represents finite lists of
   built-in ints, floats, bools, and nested lists. Arbitrary user-defined
   numeric objects, custom `int` subclasses with overridden behavior, complex
   values, and non-list arguments are excluded. They are not part of the
   prompt's material ordinary built-in list domain; the trusted canonical is
   itself not contract-correct on some such extension probes.

There are no other opaque symbols, external primitives, empirical result
oracles, or assumed proof-local lemmas.

Validating-proof gates:

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS.
- Gate C, trust and reproducible evidence: PASS.

The clean proof is sound, pins the real generated program, covers the material
unrestricted HumanEval source domain rather than fixed examples or sizes, and
has no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
