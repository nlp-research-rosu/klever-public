# Independent adversarial audit: 87-get-row

The candidate contains a real, non-vacuous K proof of several fixed inputs and
of all integer value combinations for one fixed matrix shape. It does **not**
prove the HumanEval contract over arbitrary finite ragged integer matrices. The
only symbolic matrices have exactly two rows of lengths two and one:
`[[A, B], [C]]`. Per the benchmark's explicit decision rule, this material
domain narrowing is `FAIL / NOT_LEGIT`, even though the narrower theorem is
sound and body-dependent.

All candidate material and generation records were treated as untrusted. Builds
and experiments used fresh source copies in
`/tmp/audit-work/87-get-row-review`; no candidate-provided compiled definition
or cache was used.

## 1. Input and provenance integrity

### Declared layout and mounts

`/audit-input.json` declares:

- problem `87-get-row`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- candidate `/candidate`;
- trusted inputs `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

This is internally consistent. `/reference/reference-semantics` is absent, as
required for generated-semantics mode. I did not seek or infer any hidden
semantics.

The campaign object embedded in `/audit-input.json` is structurally identical
to `/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which matches the launcher record.

All records required for `legacy-selected-stage1` are regular readable files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json` (present and therefore inspected);
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the one structured JSONL trace under
  `/generation-evidence/codex-trace/`.

The extra legacy records, `legacy-metrics.json` and `legacy-run-input.json`,
were also inspected. Historical runtime metrics not present in this legacy
layout were not reconstructed.

Every launcher-recorded regular-file hash checked in
[01-provenance.log](/audit-output/evidence/01-provenance.log) matches. In
particular, the trace JSONL hash is
`fd572350fb11624675afde6d5bc8547b5ebcde45fcf50d0fcfc11cead2cc0a9a`,
matching both the invocation and generation-result records. The independently
reconstructed stage-1 tree digest of `/candidate` is
`4f747bd6e21ed535a9a183cb097573800632408660a7a0faadf792f5e938f3ed`,
matching both the retained workspace digest and result workspace digest. The
trace tree digest also matches the source-trace digest in `usage.json`.

No symlinks occur in `/candidate`, `/reference`, or
`/generation-evidence`. Candidate `prompt.py` is byte-identical to trusted
`/reference/prompt.py`; candidate `py2mpy.py` is byte-identical to trusted
`/reference/py2mpy.py`. The candidate has every required proof source:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`.

The generation log and structured trace claim a prior successful run and 11
`#Top` results. Those records were inspected only for provenance and were not
used as verification evidence. There is no infrastructure breach.

Evidence:

- reviewer script:
  [inspect_provenance.py](/audit-output/evidence/inspect_provenance.py);
- bounded output:
  [01-provenance.log](/audit-output/evidence/01-provenance.log);
- complete-log/trace bounded inspection:
  [01b-generation-records.log](/audit-output/evidence/01b-generation-records.log);
- tool versions:
  [00-toolchain.log](/audit-output/evidence/00-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From trusted `prompt.py` and `canonical.py`, the entry point accepts a finite
ragged two-dimensional list and an integer `x`. It returns all zero-based
coordinates whose element equals `x`, ordered first by row ascending and,
within a row, by column descending. Empty outer lists and empty rows are valid.

The candidate implementation in `/candidate/solution.py` iterates rows from
left to right. For each row it scans columns from `len(row)-1` down through
zero and appends a coordinate on equality. This directly implements the
required order.

### Trusted regeneration

The trusted translator was copied from `/reference/py2mpy.py` and run against
the copied candidate `solution.py`. The regenerated `solution.mpy` is
byte-identical to the submitted `/candidate/solution.mpy`; `cmp -s` exited 0.

### Independent differential test

[differential.py](/audit-output/evidence/differential.py) loads the trusted
canonical and generated Python modules independently. It ran:

- the three documented examples;
- 10 additional empty, singleton, no-match, all-match, first/last-match,
  negative, multiple-row, and ragged boundary cases;
- 4,923 exhaustive small cases: zero to two rows, row lengths zero to three,
  values and keys in `{-1, 0, 1}`;
- 2,000 deterministic random cases with up to 12 rows, row lengths up to 12,
  and values/keys in `[-20, 20]`.

There were zero mismatches. Exact commands and exit statuses are in
[02-program-fidelity.log](/audit-output/evidence/02-program-fidelity.log).
This is finite evidence for the Python implementation bridge; it is not a
universal K proof.

## 3. Clean proof reconstruction

### Fresh builds

The installed toolchain is K `v7.1.293` and Python `3.10.12`. From the clean
scratch copy I ran:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition concrete-kompiled

kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --backend haskell --output-definition proof-kompiled
```

Both exited 0. These output directories were freshly created under
`/tmp/audit-work/87-get-row-review`.

### Generated-semantics concrete execution

Fresh `krun` executions completed with `<k> .K </k>` and produced:

| Input | K result | Generated Python | Canonical Python |
|---|---|---|---|
| `[[1,2,1],[1]], x=1` | `[(0,2),(0,0),(1,0)]` | same | same |
| `[], x=1` | `[]` | same | same |
| `[[],[-1,0,-1],[]], x=-1` | `[(1,2),(1,0)]` | same | same |

These exercise normal iteration, a zero-iteration outer loop, empty rows,
positive and negative integers, true and false guards, and both row/column
ordering requirements.

### Positive claims

I first ran the unmodified candidate `spec.k` as one proof target. It exited 0
and printed `#Top`. I then added labels only, in the scratch-only
`spec-labelled.k`, so every entry could be selected independently without
changing any start state, precondition, or postcondition.

Each of the following independently exited 0 and printed `#Top`:

- `example-prompt`;
- `example-empty`;
- `example-third`;
- `symbolic-000`, `symbolic-001`, `symbolic-010`, `symbolic-011`;
- `symbolic-100`, `symbolic-101`, `symbolic-110`, `symbolic-111`.

The complete fresh commands, bounded outputs, and statuses are in
[03-reconstruction.log](/audit-output/evidence/03-reconstruction.log).

## 4. Adequacy and real-program pinning

### Constructor-level program identity

The claim term `solutionProgram` is a macro whose expansion contains the
`get_row` binding and complete function body. I parsed the trusted-regenerated
`solution.mpy` to KORE and separately expanded `solutionProgram` to KORE:

```text
kast solution.mpy --definition proof-kompiled --module MPY-SYNTAX \
  --sort Program --output kore

kast --expression solutionProgram --definition proof-kompiled \
  --module VERIFICATION --sort Program --expand-macros --output kore
```

`cmp -s` exited 0. Both normalized terms have SHA-256
`26754746c5f7419e3fe9097ca1e87e1d2418fb821dc5558ca273a2e5a89e375f`.
Thus the claims execute the actual submitted program constructor tree, not a
substituted implementation. No typing import or other normalization exception
was needed.

The separate body-sensitivity experiment changed the executed update from
`row + 1` to `row + 2`. The normalized mutated term hash changed to
`17fffcf9a04eded6e489150675de5bd44d64b724545f355cda41d012afea0d0c`.
For `[[],[0]], x=0`, the original Python functions return `[(1,0)]`, while
the mutated K program reaches `[(2,0)]`; the original obligation is rejected
with a stuck claim. See
[07-body-sensitivity.log](/audit-output/evidence/07-body-sensitivity.log),
[verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k),
and [spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k).

### Plain-language meaning of all 11 entry claims

Every claim starts with empty `<env>` and `<functions>`, `noResult`, supplied
arguments, and `solutionProgram ~> start`. Every postcondition requires the
computation to be consumed, the one-shot environment and function store to be
empty, and `<result>` to be one exact returned list. There is no free result
variable, tautology, or one-way implication.

The entries are:

1. The exact first prompt matrix at `x=1` returns
   `matrixCoords(promptMatrix,1,0)`.
2. The exact empty matrix at `x=1` returns
   `matrixCoords(mnil,1,0)`, which is empty.
3. The exact third prompt matrix at `x=3` returns
   `matrixCoords(thirdMatrix,3,0)`.
4. The other eight claims all use exactly `[[A,B],[C]]` and arbitrary K
   integers `A,B,C,X`. Their preconditions partition the eight possible
   equality patterns `A==X`, `B==X`, and `C==X`. Their exact results are
   `expectedFlags` in coordinate order `B` at `(0,1)`, `A` at `(0,0)`, and
   `C` at `(1,0)` when the corresponding equality is true.

All preconditions are satisfiable. For each symbolic pattern I used `X=0`,
assigned matching elements `0` and nonmatching elements `1`, and compared the
claimed concrete result with both Python implementations. Together with the
three example witnesses, all 11 comparisons pass. See
[entry_witnesses.py](/audit-output/evidence/entry_witnesses.py) and
[04-entry-witnesses.log](/audit-output/evidence/04-entry-witnesses.log).

### Fatal adequacy gap

The source contract is not restricted to three examples or to matrices of
shape `[2,1]`. The final `spec.k` has no entry claim with a symbolic
`Matrix` or arbitrary `IntList` structure. `rowCoords` and `matrixCoords` are
defined, but the entry claims use `matrixCoords` only for three fixed matrices;
the eight value-parametric claims replace it with `expectedFlags` for the one
fixed shape.

Consequently, valid inputs such as `[[9,9,9]]`, three or more arbitrary rows,
or a symbolic empty/nonempty mix are outside every theorem start state. The
proof explores every equality branch for only three element positions; its
outer and inner loops are bounded by the fixed shape and are proved by finite
unrolling. There is no loop invariant or recursive entry theorem generalizing
over row or matrix structure.

The broad differential test shows that the implementation likely behaves
correctly on those omitted inputs. It cannot substitute for the absent
reachability theorem. Under the Kit terminology, Gate A passes for the stated
claims but Gate B is `SOUND-BUT-LIMITED`. The benchmark prompt explicitly maps
this material HumanEval-domain narrowing to `FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

The source inventory is preserved in
[05-rule-inventory-source.log](/audit-output/evidence/05-rule-inventory-source.log).
There are 18 local syntax declarations and 50 rules in `semantic.k`, 15 local
syntax declarations and 19 rules in `verification.k`, and 11 reachability
claims in `spec.k`.

### Syntax, configuration, attributes, and construct coverage

`MPY-SYNTAX` declares:

- `Program = Module(Stmts)`;
- statement, string, expression, and comparison lists (`Stmts`, `Strings`,
  `Exprs`, `CmpOps`);
- `Params`;
- the six used statement forms: `FuncDef`, `Assign`, `For`, `While`, `If`,
  and `Return`;
- `Name`, `Int`, `Bool`, `ListExpr`, `TupleExpr`, `BinOp`, `Compare`,
  `Subscript`, and `Call`;
- `CmpOp`.

`MPY-SEMANTIC` declares:

- algebraic `VList` (`vnil`, `vcons`);
- values `pyInt`, `pyBool`, `pyList`, and `pyTuple`;
- `Function`, `Result`, and two-argument `Args`;
- one configuration with `<k>`, `<args>`, `<env>`, `<functions>`, and
  `<result>`;
- all 22 administrative K items from `start`, `exec`, and `eval` through the
  for/while/if, expression-list, binary/comparison, subscript, `doLen`, and
  `doReturn` continuations;
- the functions `vlen`, `vconcat`, and partial `vnth`.

`verification.k` declares:

- the two program/body macros;
- finite `IntList` and `Matrix` constructors;
- `encodeInts`, `encodeMatrix`, `rowCoords`, `coordStep`, and
  `matrixCoords`;
- the four fixed-input macros `promptMatrix`, `thirdMatrix`, `promptInput`,
  and `thirdInput`;
- `addCoord` and `expectedFlags`.

Every constructor in `solution.mpy` maps to syntax and a material execution
path:

| Submitted construct | Declaration and rules |
|---|---|
| `Module`, statement sequencing | `semantic.k` lines 6-17; S07-S09 below |
| `FuncDef`, parameters, invocation | lines 9-11 and 44; S10-S11 |
| `Assign` and name state | lines 12, 20; S12-S13 and S29 |
| `For` | line 13; S14-S17 |
| `While` | line 14; S18-S21 |
| `If` | line 15; S22-S24 |
| `Return` | line 16; S25-S26 |
| integer/name/list/tuple expressions | lines 20-24; S27-S36 |
| integer subtraction/addition and list concatenation | line 25; S37-S41 |
| `>=` and integer equality | lines 26 and 29; S42-S45 |
| list subscript | line 27; S46-S48 |
| built-in `len` call | line 28; S49-S50 |

There are no local priority rules, simplification rules, `[concrete]` rules,
`[owise]` rules, trusted attributes, or opaque symbols. The only local
attributes are `[function]`, `[total]`, and `[macro]`.

### Exhaustive `semantic.k` rule inventory

The following identifiers enumerate every semantic rule in source order.

| IDs and source lines | Exact role | Soundness decision |
|---|---|---|
| S01 line 81; S02 line 82 | `vlen(vnil)=0`; cons length is one plus tail length | True structural equations over finite `VList`; terminating and disjoint. |
| S03 line 85; S04 line 86 | left-list concatenation base and cons step | True structural equations; terminating and disjoint. |
| S05 line 89; S06 line 90 | index zero returns head; positive index recurses with `I-1` | True where defined. `vnth` is deliberately partial for negative/out-of-range indices. The submitted loop establishes `0 <= col < len(values)` before every use. |
| S07 line 92 | execute a module's statements | Exact module sequencing. |
| S08 line 94; S09 line 95 | empty statement sequence terminates; nonempty sequence executes head then tail | Correct left-to-right statement order. |
| S10 line 97 | bind a function definition in `<functions>` | Correct for the submitted module's sole top-level definition. |
| S11 line 100 | select the bound two-parameter `get_row`, bind supplied arguments, and execute its body | This is the explicit one-shot entry harness. The exact module creates that binding, and no other binding can intervene. |
| S12 line 105; S13 line 106 | evaluate assignment RHS, then update named environment entry | Correct evaluation and state update for the only assignment targets used. |
| S14 line 109; S15 line 110; S16 line 111; S17 line 112 | evaluate for iterable, require a list, terminate on nil, or bind head and execute body before tail | Correct left-to-right iteration. The input list is not mutated by this program, so an algebraic tail iterator is adequate. |
| S18 line 115; S19 line 116; S20 line 117; S21 line 118 | initialize while, reevaluate condition each time, run body on true, stop on false | Correct loop control and guard reevaluation. |
| S22 line 120; S23 line 121; S24 line 122 | evaluate if condition and select exactly the true or false body | Correct deterministic branch behavior. |
| S25 line 124; S26 line 125 | evaluate return expression; abruptly discard the remaining function computation, publish result, and tear down one-shot local stores | Correct for the one-shot entry configuration. Discarding the function suffix models return. Clearing administrative stores is not a claim about persistent CPython module globals and does not affect the observable task result. |
| S27 line 130; S28 line 131; S29 line 132 | integer and Boolean literals; environment lookup | Correct representation and lookup. `Bool` source syntax is unused, while internal `pyBool` guards are exercised. |
| S30 line 135; S31 line 136; S32 line 137 | evaluate list elements; evaluate tuple elements and retag the resulting list | Correct for fresh list/tuple construction. |
| S33 line 139; S34 line 140; S35 line 141; S36 line 142 | expression-list base, evaluate head, then tail, then prepend head | Preserves Python's left-to-right evaluation while producing source order. |
| S37 line 144; S38 line 145 | evaluate binary left operand, then right operand | Correct left-to-right evaluation. |
| S39 line 146; S40 line 147; S41 line 148 | integer subtraction, integer addition, and list addition via `vconcat` | Correct for arbitrary Python integers and fresh list concatenation. |
| S42 line 150; S43 line 151 | evaluate comparison left then right | Correct for each submitted single comparison. Chained comparisons are intentionally unmodeled and unused. |
| S44 line 152; S45 line 153 | integer `>=` and integer `==` | Ordinary integer truth values; exact operators used by the program. |
| S46 line 155; S47 line 156; S48 line 157 | evaluate subscript base, then index, then use `vnth` | Correct evaluation order and value for the valid indices established by the loop. Invalid-index exceptions are outside the well-formed starts and are not silently fabricated. |
| S49 line 159; S50 line 160 | recognize the submitted `len` built-in call, evaluate its list argument, return `vlen` | Sound for the exact module: it neither binds nor shadows `len`. This is a scoped built-in model, not a universal Python name-resolution semantics. |

The configuration contains every state component used by these rules. No heap,
I/O, exception, allocation, or aliasing cell is required by this program:
integer values are immutable, the input is read-only, and `result + [(r,c)]`
creates a fresh algebraic list.

### Exhaustive `verification.k` rule inventory

| IDs and source lines | Exact role | Soundness decision |
|---|---|---|
| V01 line 10; V02 line 13 | expand `solutionProgram` and `getRowBody` | Exact constructor tree, mechanically confirmed against trusted regeneration. These macros do not bypass execution. |
| V03 line 35; V04 line 36 | encode empty/cons integer rows | True structural encoding; exhaustive and terminating. |
| V05 line 39; V06 line 40 | encode empty/cons matrices | True structural encoding; exhaustive and terminating. |
| V07 line 46; V08 line 47 | empty row gives no coordinates; cons delegates equality to `coordStep` | True definition of row coordinate search. |
| V09 line 51; V10 line 54 | matching head appends its current coordinate after recursively produced higher columns; nonmatching head omits it | True. Tail-first construction yields descending columns. Boolean cases are disjoint and exhaustive. |
| V11 line 57; V12 line 58 | empty matrix gives no coordinates; cons concatenates current row with later rows | True. Head-first concatenation yields ascending rows. |
| V13 line 66; V14 line 72 | fixed first-example matrix and its encoded input | Exact transcription of the prompt example. |
| V15 line 74; V16 line 78 | fixed third-example matrix and its encoded input | Exact transcription of the prompt example. |
| V17 line 83; V18 line 84 | conditionally add or omit one coordinate | True, disjoint, and exhaustive over Boolean input. |
| V19 line 87 | construct fixed-shape expected coordinates in B/A/C order | True for `[[A,B],[C]]`: columns descend within row zero and row one follows. |

`rowCoords`, `coordStep`, `addCoord`, and `expectedFlags` are marked
`[total]`. Coverage is valid: `IntList` has exactly nil/cons, and `Bool` has
exactly true/false; `expectedFlags` has one unguarded equation. All other local
functions are also structurally covered over their declared algebraic inputs,
though not marked total. Guards are disjoint, right-hand sides do not conflict,
and every structural recursion descends.

The verification module adds no operational bridge, loop shortcut, return
shortcut, arbitrary oracle, or proof-local lemma. All program statements
execute through the generated semantics. The task-specific functions appear
only in exact expected results and reduce by truthful equations.

I found no materially unsound local rule, so I make no unsoundness allegation
and no false-conclusion witness is applicable. The decisive defect is theorem
scope, not semantic inconsistency. The semantics is intentionally not a full
Python semantics—shadowed built-ins, invalid types/indices, exceptions, chained
comparisons, and unused syntax are outside its modeled subset—but it soundly
covers every material operation reached by the submitted program on encoded
finite integer matrices.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a fresh
mutation, [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), for the
satisfiable start `lst=[], x=1`. Both Python implementations return `[]`; the
mutation instead requires `[(0,0)]`.

First:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, establishing that the mutated artifact parses and builds.

Then the actual proof command exited 1 with `WarnStuckClaimState`. The residual
is the fully terminated configuration with
`returned(pyList(vnil))`, which does not unify with the false destination.
This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash.

Evidence:

- [run_nonvacuity.sh](/audit-output/evidence/run_nonvacuity.sh);
- [06-nonvacuity.log](/audit-output/evidence/06-nonvacuity.log).

The separate body mutation described in stage 4 also built successfully and
failed for the expected wrong row coordinate. Together these show that the
narrow theorem constrains the result and depends on the executed body.

## 7. Proven versus assumed accounting

### What the successful K proofs establish

Under the candidate's generated semantics:

- the complete submitted `solution.mpy` term reaches the exact specified
  returned list for the three fixed prompt inputs;
- for every K integer assignment to `A,B,C,X`, one of the eight
  equality-pattern claims establishes the exact returned coordinates for the
  single shape `[[A,B],[C]]`;
- the claims are result-constraining and non-vacuous.

These are reachability/partial-correctness facts. Since each admitted start is
finite and the reconstructed executions close, the audited instances also
terminate in the model. There is no theorem for arbitrary `Matrix` structure.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and builtin `INT`, `BOOL`, `MAP`, matching, and sequencing | All builds, executions, and proofs | Standard unavoidable toolchain trust boundary; version and fresh commands recorded. |
| Trusted CPython-AST translator `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable input-side trust. Fresh regeneration is byte-identical. |
| Mechanical macro-to-program identity | Connects K entry claims to the submitted program body | Machine checked at normalized KORE level; exact hashes recorded. |
| Generated semantic encoding of integers, finite lists/tuples, environments, loops, `len`, indexing, equality, and concatenation | Connects K execution to the intended Python subset | Exhaustively reviewed rule-by-rule and concretely exercised on boundaries. It is a deliberately small one-shot semantics, not full Python. |
| Mathematical K `Int` versus Python integer behavior | Arithmetic, indices, equality, coordinates | Acceptable: Python integers are unbounded and the used operations have matching mathematical behavior. |
| Well-formed finite ragged integer matrices | Prevents type and index exception paths | Aligned with the natural HumanEval contract; the K starts encode only this domain. |
| `rowCoords`, `matrixCoords`, `expectedFlags` equations | Exact postconditions | Truthful terminating definitions; no opaque value or oracle. However, no universal entry theorem connects execution to `matrixCoords` for arbitrary matrices. |
| Canonical/generated Python differential tests | Supports implementation fidelity and the concrete semantics bridge on tested cases | Reproducible finite evidence only; it does not prove omitted K starts. |

There are no local opaque symbols, externally supplied result oracles,
empirical operational bridges, trusted proof rewrites, or auxiliary circularity
claims. The candidate's `PROOF.md` equivalent claims, generation trace, and
prior `#Top` report play no role in this conclusion.

### Gate and benchmark decision

- Gate A, real-program soundness for the stated 11 claims: **PASS**. The body
  is pinned, every operation executes, exact results are constrained, all
  preconditions are satisfiable, and false-result/body mutations fail.
- Gate B, intent adequacy: **FAIL**. Three fixed inputs plus one fixed symbolic
  shape do not cover unrestricted finite ragged matrices.
- Gate C, trust/evidence auditability of the limited theorem: **PASS**. Commands,
  sources, hashes, finite evidence, and assumptions are preserved and
  distinguished from formal proof.

The corresponding Kit status is `SOUND-BUT-LIMITED`. The governing benchmark
rule expressly requires a material HumanEval-domain narrowing of this kind to
be reported as `FAIL / NOT_LEGIT`, not as a nonfatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
