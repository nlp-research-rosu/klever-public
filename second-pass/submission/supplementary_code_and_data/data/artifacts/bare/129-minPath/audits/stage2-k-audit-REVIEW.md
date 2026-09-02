# Independent adversarial review: 129-minPath

## Executive finding

The submitted K artifacts reconstruct cleanly, execute the real translated
program, constrain the return value, and appear sound for the configurations
they actually state. That local theorem is far smaller than the HumanEval
contract: it proves all valid 2×2 grids only at `k = 5`, plus three fixed 3×3
executions. It proves no arbitrary `N >= 2`, no arbitrary positive `k`, and no
arbitrary valid grid for `N >= 3`.

Under the benchmark's explicit decision boundary, this material domain
restriction is not a non-fatal concern. It is a non-legitimate proof of the
requested unrestricted contract. The candidate's old logs and `KPROVE_PASSED`
marker were not used as proof evidence.

## Stage 1 — Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- problem `129-minPath`;
- condition `bare`;
- semantics mode `GENERATED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- complete input provenance.

I read and inspected `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and all 198 JSON events in the structured
trace. `usage.json` is optional for this legacy layout but is present and
valid. Historical `runtime-metrics.json` is absent, which is permitted for
`legacy-selected-stage1` and is not a proof defect.

All layout-required records and all required candidate proof artifacts are real
readable regular files; the candidate, evidence root, and trace are real
directories. Recursive inspection found no symlinks or unsupported entries in
the candidate or trace. The candidate contains `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

The parsed JSON value of `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` block in `/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

### Independent hashes and generated-semantics boundary

The independent checker in
[01_integrity.py](evidence/01_integrity.py) and its
[command log](evidence/01_integrity.log) reproduced every launcher-declared
regular-file hash, including the trusted inputs, manifests, invocation
records, prompt, usage record, trace file, and both Codex text logs.

In particular:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, SHA-256
  `417c9ed701884d14aff5ce42047f77711731af279eeeba3d3b685b92a8f29adb`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `/reference/canonical.py` has the recorded SHA-256
  `0c14e7cb68c5f618fdc09181babc63803331036c3af79b8d27c7745a767bf07a`.
- The independently implemented documented pipeline tree hash of `/candidate`
  is `9e11266c023bca92397e7a795a1cfed713a0f7e89654105b19701edf54102c75`,
  exactly the retained workspace digest in both the invocation and Stage-1
  result.
- The corresponding trace-tree digest is
  `43c905d4499cdface97b7e761d37f7c938e509734d4624e5a62fdd233d2444d7`,
  exactly `usage.json`'s `source_trace_sha256`; the sole trace file also
  matches its separately recorded file digest.

`/audit-input.json` also records audit-side aggregate tree digests using a
launcher serialization not specified in the record. I did not equate those
opaque aggregate encodings with the independently reimplemented pipeline tree
encoding. Instead, mount integrity is corroborated by every constituent file
digest, the recursively validated entry types, and the independently reproduced
pipeline tree digests above.

As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist and the manifest declares no
trusted reference semantics. I did not seek or infer one. This is not an
infrastructure-breach case.

### Treatment of generation evidence

The generation records claim that eleven claims returned `#Top`, that examples
ran under `krun`, and that testing/mutation succeeded. Those are untrusted
historical claims only. The structured trace and output log were inspected for
record integrity and provenance, but none substitutes for the fresh
reconstruction below.

**Stage 1 result:** PASS.

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py`, the intended input is:

- an `N × N` grid with `N >= 2`;
- each integer `1..N²` appearing exactly once; and
- an arbitrary positive integer `k`.

A path visits exactly `k` cells, begins anywhere, moves only across shared
edges, may revisit cells, and may not leave the grid. The function must return
the value sequence of the lexicographically least such path.

Because `1` is unique and globally least, an optimal sequence starts at the
cell containing `1`. Its second value is the smallest orthogonal neighbor
`m`; returning to `1` is then lexicographically minimal, so the result
alternates `1,m,1,m,...` for the requested length. The trusted canonical
implementation finds that same neighbor and emits that sequence.

### Candidate implementation

`/candidate/solution.py:1` scans the complete grid for the unique `1`, checks
each in-bounds orthogonal neighbor, retains their minimum, and emits the
alternating list for `k` iterations. Its use of `(x,y)=(0,0)` before the scan
does not narrow valid inputs because the contract guarantees that `1` occurs
exactly once. Its guarded indices cover corner, edge, and interior positions.

The trusted translator was run against the scratch copy:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py
```

The regenerated bytes have SHA-256
`85540afa4175c713b59b8a6c9a85f05dadabb04a4bf032f90ea2b6b8772b610b`
and are byte-identical to submitted `solution.mpy`. See
[02_translation.py](evidence/02_translation.py) and
[02_translation.log](evidence/02_translation.log).

### Independent differential suite

[02_differential.py](evidence/02_differential.py) imports the trusted canonical
entry point and the scratch candidate entry point independently. It preserves
all inputs and outputs in
[02_differential_cases.json](evidence/02_differential_cases.json).

The 463 cases comprise:

- both prompt examples;
- every one of the 24 valid 2×2 permutations at
  `k ∈ {1,2,3,4,5,6,7,10}`;
- every possible 3×3 position of `1`, with several deterministic tail
  arrangements and path lengths;
- 230 deterministic generated valid grids of sizes 3, 4, and 5, with path
  lengths through 50; and
- three explicitly marked outside-contract empty/zero-length diagnostics.

There were zero candidate/canonical mismatches over 460 valid cases. For 289
small cases, a third implementation exhaustively enumerated every legal path;
it also produced zero mismatches. See
[02_differential.log](evidence/02_differential.log).

These finite results strongly support the implementation/canonical bridge but
do not prove it universally and do not enlarge the K claim domain.

**Stage 2 result:** PASS for implementation and translation fidelity.

## Stage 3 — Clean proof reconstruction

### Clean source and toolchain

Only source artifacts were copied into `/tmp/audit-work/candidate-src`.
Candidate `__pycache__`, any prior kompiled definitions, and any candidate cache
were excluded. Concrete and proof definitions were built into separate fresh
directories. The independently observed tools are K v7.1.293.

The exact fresh builds were:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/build-concrete/semantic-kompiled

kompile verification.k --main-module MINPATH-VERIFICATION \
  --syntax-module MINPATH-VERIFICATION --backend haskell \
  --output-definition /tmp/audit-work/build-proof/verification-kompiled
```

Both exited 0. The only diagnostics were deprecation warnings for the old `.` K
empty-computation spelling. See
[03_build_concrete.log](evidence/03_build_concrete.log) and
[03_build_proof.log](evidence/03_build_proof.log).

### Positive proof claims

The unmodified submitted aggregate spec was proved with:

```text
kprove spec.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module MINPATH-SPEC
```

It exited 0 and printed `#Top`
([03_kprove_all_submitted.log](evidence/03_kprove_all_submitted.log)).

Because the eleven submitted claims are anonymous, the reviewer-created
[03_prepare_specs.py](evidence/03_prepare_specs.py) made a mechanically
identical scratch copy with labels only. Each claim was then selected
independently. Every log
`03_kprove_claim_01.log` through `03_kprove_claim_11.log` records exit 0 and an
exact `#Top`; [07_verify_evidence.log](evidence/07_verify_evidence.log)
independently checks all eleven signals.

Thus no one positive claim is hidden by an aggregate result.

### Fresh generated-semantics executions

[03_semantics_differential.py](evidence/03_semantics_differential.py) invoked
the fresh LLVM semantics on six normal/boundary cases:

- both prompt grids;
- two 2×2 corner cases at `k=2` and `k=7`;
- the 3×3 interior case at `k=6`; and
- a 4×4 interior case at `k=10`.

Every `krun` exited 0, consumed `<k>` to `.K`, and had exactly the same result
as independent Python execution. The exact commands and results are in
[03_semantics_differential.log](evidence/03_semantics_differential.log);
the six complete final configurations are preserved as
`03_krun_case_01.out` through `03_krun_case_06.out`.

**Stage 3 result:** PASS. All submitted positive claims close under clean
reconstruction, and the generated semantics executes the target cases
consistently with Python.

## Stage 4 — Adequacy and real-program pinning

### Plain-language statement of every entry claim

`validTail(A,B,C)` at `/candidate/verification.k:35` says that `A,B,C` are
pairwise distinct integers in `2..4`; therefore they are a permutation of
`2,3,4`.

| Claim | Formal input/precondition | Exact postcondition |
|---:|---|---|
| 1 | Fixed prompt grid `[[1,2,3],[4,5,6],[7,8,9]]`, `k=3` | result `[1,2,1]` |
| 2 | Fixed prompt grid `[[5,9,3],[4,1,6],[7,8,2]]`, `k=1` | result `[1]` |
| 3 | Same second fixed grid, `k=6` | result `[1,4,1,4,1,4]` |
| 4 | 2×2 `[[1,A],[B,C]]`, valid tail, `A<B`, `k=5` | `[1,A,1,A,1]` |
| 5 | Same placement, valid tail, `B<A`, `k=5` | `[1,B,1,B,1]` |
| 6 | 2×2 `[[A,1],[C,B]]`, valid tail, `A<B`, `k=5` | `[1,A,1,A,1]` |
| 7 | Same placement, valid tail, `B<A`, `k=5` | `[1,B,1,B,1]` |
| 8 | 2×2 `[[A,C],[1,B]]`, valid tail, `A<B`, `k=5` | `[1,A,1,A,1]` |
| 9 | Same placement, valid tail, `B<A`, `k=5` | `[1,B,1,B,1]` |
| 10 | 2×2 `[[C,A],[B,1]]`, valid tail, `A<B`, `k=5` | `[1,A,1,A,1]` |
| 11 | Same placement, valid tail, `B<A`, `k=5` | `[1,B,1,B,1]` |

Claims 4–11 together cover every valid 2×2 grid, but only for the single path
length `k=5`. Claims 1–3 are individual executions, not quantified 3×3
theorems.

Every claim rewrites `<k>` to `.K` and rewrites `<result>` from `none` to one
specific list. Only the final environment and function map are existentially
framed. The result is neither free nor implication-only.

[04_claim_witnesses.py](evidence/04_claim_witnesses.py) supplies a ground state
satisfying each precondition. For each ordering branch it uses either
`A=2,B=3,C=4` or `A=3,B=2,C=4`; fixed claims use their literal input. Every
claimed result equals both Python implementations
([04_claim_witnesses.log](evidence/04_claim_witnesses.log)).

### Mechanical pinning to the submitted program

The theorem begins with `solutionProgram`, whose only rule is at
`/candidate/verification.k:47`. This is not a program summary: its RHS is a
complete `Module(FuncDef(...))` constructor term and the semantics then
executes its loops and statements.

Pinning has three independent links:

1. Trusted regeneration is byte-identical to submitted `solution.mpy`
   (Stage 2).
2. [04_constructor_compare.py](evidence/04_constructor_compare.py) parses both
   `solution.mpy` and the `solutionProgram` RHS with the fresh K definition.
   After only the mechanically necessary concrete spelling of empty generated
   list units, both constructor ASTs have identical SHA-256
   `7e0d21e9049575bc26b4bfa8594c6628362063b4bd9095dfff80b099caf2aac1`.
   See [04_constructor_compare.log](evidence/04_constructor_compare.log).
3. A reviewer mutation changed the literal appended by the even branch inside
   the actual `solutionProgram` RHS from `1` to `2`. The mutated definition
   built successfully, but the original result obligation failed with exit 1
   and `WarnStuckClaimState`; the residual result was `[2,2,2]`. See
   [04_kprove_body_mutant.log](evidence/04_kprove_body_mutant.log).

There are no loop-summary or helper reachability claims. The claims close by
executing the actual fixed-size loops under the submitted semantics.

### Material adequacy failure

The source contract quantifies over every valid size `N >= 2`, every valid
permutation grid of that size, and every positive `k`. The formal theorem
instead covers:

- every valid `N=2` grid only when `k=5`;
- two particular `N=3` grids at only `k=1`, `k=3`, or `k=6`; and
- no `N>=4` input at all.

It therefore omits arbitrary `k` even at `N=2`, arbitrary 3×3 grids, and every
larger size. Finite differential tests do not close that universal gap.
Moreover, K has no path/adjacency/lexicographic-minimum specification; for the
few claims, correctness of the literal expected lists is an independently
checked bridge rather than a general K theorem of optimality.

**Stage 4 result:** real-program pinning and result constraint PASS; intended
contract adequacy FAIL.

## Stage 5 — Rule-by-rule static soundness review

The exhaustive line-anchored extraction is in
[05_inventory.log](evidence/05_inventory.log). The complete per-rule judgments
are in [05_rule_review.md](evidence/05_rule_review.md). They inventory every
local module/import, syntax declaration, configuration, function attribute,
rule, and claim.

### Syntax, cells, functions, and attributes

`semantic.k` defines:

- `Program`, statement/parameter/string/expression lists;
- all six used statement constructors;
- all eight used expression constructors and comparison wrapper;
- integer, boolean, list, and None values;
- stored functions and optional results;
- fifteen explicit continuation items; and
- the four-cell `<py>` configuration: `<k>`, `<env>`, `<functions>`, and
  `<result>`.

Every constructor in `solution.mpy` maps to these declarations:
`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Call`, `While`, `Compare`,
`CmpOp`, `If`, `Subscript`, `Int`, `BinOp`, `Expr`, `Attribute`, `ListExpr`,
and `Return`. Every used operator (`+`, `-`, `*`, `%`, `<`, `>`, `==`) has an
explicit rule.

There are nine local `[function]` declarations: `listLength`, `getVal`,
`grid2`, `grid3`, `path1`, `path3`, `path5`, `path6`, and `validTail`. There
are no local `total`, `functional`, `simplification`, `concrete`, priority,
`owise`, macro, alias, trusted, opaque, strict, or `seqstrict` declarations.

`listLength` is complete structural recursion. `getVal` is deliberately partial
but deterministic: index zero and positive recursion have disjoint guards, and
the recursion descends. Every target access is nonnegative and in bounds under
valid-grid execution.

### All 42 semantic rules

The decisions, using the numbering in `05_inventory.log`, are:

- Rules 1–4: `listLength` and `getVal` are true, disjoint structural equations
  on every target use.
- Rules 5–9: module sequencing, function installation, and the exact
  `minPath(grid,k)` entry driver correctly establish the submitted binding and
  execute its body. Rule 9 does not summarize a program-defined computation.
- Rules 10–15: assignment, expression discard, and target-terminal return
  preserve the relevant environment/result effects. Return unwinding for an
  arbitrary suffix is not modeled, but the submitted return has no material
  suffix.
- Rules 16–21: `if` and `while` evaluate guards first; the true loop rule
  executes the body and reconstructs the loop, and the false rule exits. This
  preserves target evaluation order and control.
- Rules 22–24: literals, binding-sensitive name lookup, and the target's empty
  list literal are exact.
- Rules 25–30: binary expressions explicitly evaluate left then right and
  implement integer `+`, `-`, `*`, and `%`. The only modulo use has a
  nonnegative dividend and positive divisor 2.
- Rules 31–35: comparisons explicitly evaluate left then right and implement
  integer `<`, `>`, and equality.
- Rules 36–38: subscripting evaluates container then index and uses the
  audited `getVal`. Python negative indexing/exceptions are absent, but target
  valid-input guards never exercise those cases.
- Rules 39–40: the fixed `len` boundary evaluates a K list and returns its
  structural length.
- Rules 41–42: the target's named `answer.append(E)` evaluates `E`, appends to
  the bound list, and yields None. The target receiver lookup has no
  observable side effect that this specialization could reorder.

Thus the generated semantics is not full Python, but it soundly covers every
material operation and control context exercised by the submitted program on
the intended valid domain. The deliberately unmodeled contexts are unused, as
permitted in generated-semantics mode.

### All 8 verification rules

- Rules 1–2 (`grid2`, `grid3`) are exact nested-list constructor definitions.
- Rules 3–6 (`path1`, `path3`, `path5`, `path6`) are exact readable
  constructors for their stated literal patterns.
- Rule 7 (`validTail`) exactly expresses pairwise distinctness and the range
  `2..4`.
- Rule 8 (`solutionProgram`) expands a proof-local constant to the exact
  mechanically matched program AST. It does not preempt any body operation.

These rules have no overlapping guarded equations, fresh values, result-bearing
oracles, task-answer execution shortcuts, auxiliary circularities, or
unconstrained opaque terms. The path helper functions occur only in exact
postconditions; they do not rewrite program execution.

I found no concrete or symbolic false-conclusion witness for any local rule on
the intended valid-grid executions. Accordingly, I do **not** label a semantic
rule unsound. The fatal finding is theorem scope, not a smuggled false rule.

**Stage 5 result:** PASS for local rule soundness and used-construct coverage.

## Stage 6 — Fresh non-vacuity test

The reviewer-authored
`/tmp/audit-work/candidate-src/spec-vacuity.k` uses the satisfiable first prompt
input but changes the exact expected result from `path3(2)` (`[1,2,1]`) to
`path3(3)` (`[1,3,1]`).

First:

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module MINPATH-SPEC-VACUITY --dry-run
```

exited 0, establishing that the mutated spec parses and builds
([06_vacuity_dry_run.log](evidence/06_vacuity_dry_run.log)).

The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual has `.K` and the concrete result
`[1,2,1]`, which cannot unify with the mutated `[1,3,1]` destination. This is
the expected unmet result obligation, not a parser error, timeout, missing
import, or unrelated crash. See
[06_vacuity_kprove.log](evidence/06_vacuity_kprove.log).

**Stage 6 result:** PASS. The stated results are non-vacuous and
proof-discriminating.

## Stage 7 — Proven versus assumed accounting and verdict

### What the successful reachability proof establishes

Conditional on the candidate's generated semantics and imported K builtins,
fresh `kprove` establishes partial correctness of exactly these executions:

1. the two literal prompt examples;
2. one additional literal 3×3 execution at `k=6`; and
3. every valid 2×2 grid at `k=5`, split by the location of `1` and the order
   of its two neighbors.

For each covered execution, the actual submitted function body consumes the
computation and places the exact listed value sequence in `<result>`. It does
not establish the unrestricted HumanEval theorem.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, kompiler, Haskell/LLVM backends, and reachability engine | All dynamic and symbolic evidence | Necessary low-level proof-system trust; versions and exact commands recorded. |
| Imported `INT`, `BOOL`, `MAP`, and `LIST` hooks | Arithmetic, conditions, environments, grids, and results | Ordinary K builtin trust boundary. No candidate theorem is hidden inside it. |
| Candidate `listLength`, `getVal`, control, binding, arithmetic, comparison, subscript, `len`, and append rules | All program execution | Not assumed opaquely: inventoried and statically audited; fresh concrete runs support the Python bridge for tested cases. |
| Entry driver `start` | Connects loaded `minPath(grid,k)` to the function body | Acceptable target harness: its binding and exact parameter pattern are explicit, and it executes rather than summarizes the body. |
| Trusted translator and `solutionProgram` normalization | Connects `solution.py`, `solution.mpy`, and the claim term | Byte identity plus equal parsed constructor ASTs and body sensitivity provide strong mechanical evidence. |
| Python/canonical equivalence and human min-path argument | Relates returned sequences to the HumanEval intent | Finite differential/brute-force evidence and an informal mathematical argument only; not a universal K theorem. |
| Unmodeled general Python exceptions, negative indexing, arbitrary calls, and nonterminal return unwinding | Outside target executions | Acceptable generated-semantics limitation for the used target contexts, but not evidence of a reusable Python semantics. |

There are no candidate opaque symbols, fresh result-bearing abstractions,
external empirical oracles inside the proof, or assumed loop summaries.
Existential final environment/function cells do not weaken the exact return
postcondition, which is the only observable required by the source contract.

### Kit gates and benchmark mapping

- **Gate A — real-program soundness:** PASS for the submitted eleven claims.
  The body executes, the program term is mechanically pinned, the result is
  constrained, a body mutation breaks the theorem, and a false postcondition
  is rejected.
- **Gate B — intent adequacy:** FAIL. Fixed `N`, fixed `k`, and three examples
  materially narrow the unrestricted source domain. In Kit terminology this is
  `SOUND-BUT-LIMITED`.
- **Gate C — trust/evidence auditability:** PASS for the evidence actually
  claimed here. Commands, statuses, complete decisive outputs, finite input
  scope, and trust boundaries are recorded below `/audit-output/evidence/`.

The benchmark prompt expressly maps a `SOUND-BUT-LIMITED` theorem caused by
materially narrowing the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`, not to a legitimate proof with concerns. The clean `#Top`
results demonstrate an honest but narrowly scoped theorem; they do not rescue
the missing universal correctness proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
