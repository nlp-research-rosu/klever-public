# Independent adversarial audit: 87-get-row

The candidate's source, logs, compiled definitions, and reports were treated as
untrusted. All executable sources were copied to
`/tmp/audit-work/87-get-row/source`; the candidate's compiled definitions and
caches were never used. K version v7.1.293 was available independently.

Headline finding: the submitted program is faithful to the HumanEval task, the
generated semantics is sound for every construct the program uses, the actual
translated program is pinned exactly, all eleven submitted claims reconstruct,
and a false-result mutation is rejected. However, those eleven claims prove only
three concrete examples and the fixed matrix shape `[[A, B], [C]]`. There is no
entry claim quantified over an arbitrary finite ragged matrix. This is a
material missing theorem, not a thin intent bridge, so the candidate is not a
legitimate proof of the full task contract.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent as required (including a
non-following symlink check). The trusted files `/reference/canonical.py`,
`/reference/prompt.py`, and `/reference/py2mpy.py` are regular files. There is no
mount contradiction and therefore no infrastructure breach.

Evidence:
`evidence/stage01_integrity.sh`,
`evidence/stage01_integrity.log`.

### Required artifacts and identity

The following candidate artifacts are present as regular files:

- provenance: `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL trace;
- identity inputs: `prompt.py`, `py2mpy.py`;
- proof sources: `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, `prove.sh`.

There are no symlinks in the top-level candidate source/provenance scope or the
trace tree. There are no additional helper K source files. Every scratch
execution source compares byte-for-byte with its read-only candidate or trusted
origin.

The candidate prompt and translator are byte-identical to the trusted mounts:

- prompt SHA-256:
  `8de3ecf44a0ece8d4e372c37aa51439548bd77398c179f009834d5b5d1ea34fb`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

No required artifact is missing, changed, mistyped, or symlinked. The candidate
also contains extra build byproducts `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`; these were deliberately excluded
from scratch. The provenance logs and trace are additional untrusted evidence,
not proof sources. No candidate `PROOF.md` or `spec-vacuity.k` is present;
neither was a required generation deliverable.

### Untrusted generation claims

`run-input.json` identifies problem `87-get-row`, the bare condition, and hashes
matching the trusted prompt/translator. `metrics.json` claims a successful,
non-timeout generation. `codex-last.txt` and `codex-output.log` claim eleven
successful claims and randomized tests. The structured trace parses as 488
JSONL records. None of these success claims was accepted without reconstruction.

Evidence:
`evidence/stage01_untrusted_provenance_claims.sh`,
`evidence/stage01_untrusted_provenance_claims.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite ragged nested list `lst` and integer `x`, `get_row(lst, x)` must
return the zero-based `(row, column)` coordinate of every occurrence of `x`.
Rows must appear in ascending order; within each row, columns must appear in
descending order. Empty outer lists and empty rows are valid.

The trusted canonical implementation enumerates all coordinates and performs a
stable column-descending sort followed by a row-ascending sort. Stability
preserves descending column order within equal row keys.

The candidate implementation iterates rows in ascending order, scans each row
from `len(row)-1` down to zero, and appends a coordinate on equality. This is a
different but contract-equivalent algorithm on the intended integer-matrix
domain.

### Trusted translation

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/87-get-row/source/solution.py
```

regenerated `solution.mpy` with SHA-256
`e50e32702d53dc6c6eed4320d309dab83171d3a30d300d027d5b77e8596f5f8d`,
byte-identical to the submitted `solution.mpy`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch candidate `solution.py`. It checks:

- all three documented examples;
- explicit empty-row, singleton hit/miss, first/last-column, multiple-match,
  ragged, and negative-integer boundaries;
- every ragged matrix with 0 to 3 rows, each row length 0 to 3, values in
  `{-1,0,1}`, for `x` in `{-2,-1,0,1,2}`;
- 3,000 deterministic larger random cases using seed 870087.

There were 331,216 comparisons and zero mismatches. The recorded result digest
is `2003daa8a63e5dc2772ea87d4a310af27a1a561473742e14d13c329b291c1a89`.
This is strong finite evidence for implementation fidelity, not a universal K
proof.

Evidence:
`evidence/stage02_program_fidelity.sh`,
`evidence/stage02_program_fidelity.log`,
`evidence/regenerated_solution.mpy`.

## 3. Clean proof reconstruction

### Fresh builds

Fresh source-only builds were made at:

- `/tmp/audit-work/87-get-row/semantic-audit-kompiled` using LLVM;
- `/tmp/audit-work/87-get-row/verification-audit-kompiled` using Haskell.

Both `kompile` commands exited 0, and their fresh backend markers report `llvm`
and `haskell`, respectively. No file from either candidate-provided kompiled
directory was copied or read as build input.

Evidence:
`evidence/stage03_fresh_build.sh`,
`evidence/stage03_fresh_build.log`.

### Concrete generated-semantics reconstruction

The freshly translated `solution.mpy` was executed with the fresh LLVM
definition on seven inputs: a normal multiple-match case, the main documented
example, empty outer list, empty rows plus a later match, singleton hit,
singleton miss, and a ragged negative-integer case. Every `krun` exited 0,
finished with `<k> .K </k>`, and produced an exact encoded result equal to both
Python implementations.

Evidence:
`evidence/generated_semantics_compare.py`,
`evidence/stage03_semantics_execution.log`.

### Independent positive claims

The three originally unlabeled claims were given labels only in a scratch copy,
`evidence/spec-labeled.k`, so each unchanged claim body could be selected
independently. The following eleven independent commands each exited 0 and
printed exactly one `#Top`:

```text
SPEC.example-prompt
SPEC.example-empty
SPEC.example-third
SPEC.symbolic-000
SPEC.symbolic-001
SPEC.symbolic-010
SPEC.symbolic-011
SPEC.symbolic-100
SPEC.symbolic-101
SPEC.symbolic-110
SPEC.symbolic-111
```

The original submitted `spec.k` was then proved as a whole against the same
fresh definition; it also exited 0 and printed `#Top`.

Evidence:
`evidence/stage03_individual_proofs.sh`,
`evidence/stage03_individual_proofs.log`.

This stage passes reconstruction. `#Top` establishes closure of these eleven
claims under the reconstructed theory; it does not enlarge their preconditions.

## 4. Adequacy and real-program pinning

### Exact real-program identity

The regenerated `solution.mpy` was parsed to KORE with the fresh verification
definition. Separately, `solutionProgram` from `verification.k` was macro
expanded to KORE. `cmp` reports byte identity; both terms have SHA-256
`26754746c5f7419e3fe9097ca1e87e1d2418fb821dc5558ca273a2e5a89e375f`.
Thus the claims execute the submitted translated program, not a substituted
program.

Evidence:
`evidence/stage04_pinning_and_witnesses.sh`,
`evidence/stage04_pinning_and_witnesses.log`,
`evidence/translated-program.kore`,
`evidence/proof-program.kore`.

### Plain-language claim inventory

The first three claims have exact initial configurations: the actual program
followed by `start`, one named concrete argument pair, empty environment and
function map, and `noResult`. Their postconditions require complete execution
to `.K`, cleanup of those maps, and an exact returned list:

1. the main documented matrix at `x=1`, with
   `matrixCoords(promptMatrix,1,0)`;
2. the empty matrix at `x=1`, with `matrixCoords(mnil,1,0)`;
3. `[[],[1],[1,2,3]]` at `x=3`, with
   `matrixCoords(thirdMatrix,3,0)`.

The eight symbolic claims all have the exact input shape `[[A,B],[C]]` for
arbitrary mathematical integers `A,B,C,X`. Each precondition chooses one of the
eight equality/non-equality patterns against `X`. Each postcondition requires
the exact corresponding coordinate list built by `expectedFlags`. Collectively,
the eight conditions cover all element-value patterns for that one fixed shape.

There are no helper or loop reachability claims. The reconstructed prover
symbolically executes and finitely unrolls the real `for` and `while` loops for
the three concrete matrices and the fixed three-element symbolic matrix.

Every postcondition rewrites `noResult` to a fully determined `returned(pyList(
...))`; there is no free result variable, tautology, or one-way implication.

### Satisfying states and ground substitution

`evidence/claim_witnesses.py` exhibits one satisfying state for every claim.
The three exact examples satisfy their implicit exact preconditions. For each
symbolic bit pattern it uses `X=0`, matching elements equal to zero, and
nonmatching elements 11, 12, or 13. All eleven claimed results equal both
Python implementations; witness count 11, failure count 0.

### Material adequacy failure

`verification.k` defines a general `Matrix` datatype and a truthful general
`matrixCoords` function, but `spec.k` contains no claim of the necessary form
"for arbitrary `M:Matrix` and `X:Int`, executing the program on
`pyList(encodeMatrix(M))` returns `pyList(matrixCoords(M,X,0))`." Merely defining
that mathematical result function proves no connection to arbitrary program
execution.

Inputs such as `lst=[[1]]`, `x=1` satisfy the natural-language domain and return
`[(0,0)]`, yet they satisfy none of the eleven entry preconditions. More
generally, arbitrary row counts and row lengths are absent. The eight symbolic
claims vary element values but not shape. Consequently the K proof does not
establish the task contract for the intended domain.

This is a material theorem-scope gap. It is not repaired by the correct source
algorithm, the concrete claims, the 331,216 differential comparisons, or the
universally defined but unconnected `matrixCoords` equations.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule inventory is
`evidence/rule_inventory.md`; the mechanically reproduced declaration scan is
`evidence/stage05_inventory_scan.log`.

### Inventory totals and sensitive attributes

- `semantic.k`: 50 local rules;
- `verification.k`: 19 local rules;
- `spec.k`: 11 reachability claims and no local semantic rules;
- ten local `[function]` symbols;
- four `[total]` functions: `rowCoords`, `coordStep`, `addCoord`,
  `expectedFlags`;
- six macro symbols;
- no local `[functional]`, simplification, concrete, owise, anywhere, priority,
  trusted, or opaque declaration/rule.

The evidence inventory enumerates every syntax/configuration declaration and
decides all 69 rules individually.

### Generated semantics

The configuration contains exactly the state needed by the program: control,
two arguments, an environment, a function registry, and a result. There is no
unused heap, allocation counter, I/O, or exception cell.

The submitted constructor tree is completely covered:

- module and statement sequencing;
- function registration and the exact two-argument `get_row` entry harness;
- assignment;
- list `for`, integer-controlled `while`, and Boolean `if`;
- abrupt top-level return;
- names, integers, lists, tuples, expression-list evaluation;
- integer subtraction/addition and list concatenation;
- integer `>=` and `==`;
- list subscript;
- list `len`.

The manual continuation terms enforce left-to-right evaluation. Loop rules
re-evaluate the while guard, iterate the for-list in source order, and preserve
environment updates. Return records the evaluated value and discards the
remaining function continuation. The program does not mutate its iterated input
list, so the stored for-tail matches its Python behavior.

`vlen` and `vconcat` are disjoint, structurally descending equations. `vnth` is
intentionally partial: zero and positive indices are covered, while negative or
out-of-range indices get stuck. On every submitted program path, `col` starts
at `len(row)-1`, indexing happens only under `col >= 0`, and each iteration
decrements it; therefore every actual index is within bounds. Missing exception
semantics for invalid external programs is unused coverage, which is acceptable
in generated-semantics mode.

The generated semantics is a deliberately small model rather than full Python,
but it does not silently fabricate a result for any used construct.

### Verification equations

The program macros are exact by the KORE identity check and do not bypass
execution. `encodeInts` and `encodeMatrix` are disjoint structural
representation maps.

`rowCoords` recurses on the tail before appending a current match, producing
descending columns. `matrixCoords` concatenates a current row before later
rows, producing ascending rows. `coordStep` and `addCoord` split on disjoint,
exhaustive Boolean constructors. `expectedFlags` builds the correct `B,A,C`
coordinate order for `[[A,B],[C]]`. All recursive calls descend structurally.
All `[total]` declarations have exhaustive equations, and overlaps either do
not exist or have disjoint constructor/guard domains.

These result helpers occur in postconditions and encodings; no rule rewrites
`exec`, `eval`, a loop, return, or another operational computation into one of
them. There is no operational bridge, unconstrained oracle, or circular
program-derived abstraction.

### Static decision

No local rule was found unsound, so no unsoundness label or false-conclusion
witness is asserted. The narrower established defect is missing theorem
coverage, documented in Stage 4. Concrete semantics evidence is finite; the
rule-by-rule argument supplies the non-empirical justification for the modeled
constructs.

## 6. Fresh non-vacuity test

No candidate mutation was available. A fresh mutation was created at
`evidence/spec-vacuity-audit.k`. It retains the exact satisfiable empty-input
precondition but changes the required result from `[]` to the demonstrably false
`[(0,0)]`.

The mutation's parse/build-only command (`kprove --dry-run`) exited 0. The real
proof command exited 1 and emitted one `WarnStuckClaimState`. Its terminal
configuration contains

```text
<result> returned ( pyList ( vnil ) ) </result>
```

which cannot unify with the mutated nonempty destination. This is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation.

Evidence:
`evidence/stage06_nonvacuity.sh`,
`evidence/stage06_nonvacuity.log`.

The submitted claims are non-vacuous and result-constraining.

## 7. Proven versus assumed accounting

### Precisely proven

Under the submitted generated semantics and proof equations, the actual
translated `solution.mpy` reaches the exact returned coordinate lists for:

- the three documented concrete inputs in `spec.k`; and
- all integer values `A,B,C,X` for the single input shape `[[A,B],[C]]`, split
  across eight exhaustive equality-pattern claims.

The claims also require the stated final `.K`, empty environment/function maps,
and returned-result cell. The fresh mutation shows the result cannot be changed
arbitrarily.

No K reachability theorem establishes the requested result for an arbitrary
finite ragged `Matrix`.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, and reachability engine | Builds and checks every K execution/claim | Conventional unavoidable toolchain trust; fresh builds and exact exit/output records reduce provenance risk. |
| Imported K `INT`, `BOOL`, and `MAP` modules | Integer arithmetic/comparison, Boolean guards, environment/function maps | Acceptable low-level trusted primitives. No task answer is encoded in them. |
| Trusted `/reference/py2mpy.py` | Maps `solution.py` to `solution.mpy` | Authority supplied by the audit. Byte regeneration pins the submitted MPY artifact, but translator correctness itself is outside the K theorem. |
| Candidate-generated `semantic.k` | Defines all program execution | Not independently supplied. It was audited rule by rule and tested concretely on seven normal/boundary inputs. Its alignment with Python remains a reviewer-justified modeling bridge rather than a theorem about CPython, but no used-rule discrepancy was found. |
| `rowCoords`, `matrixCoords`, `expectedFlags` equations | Fix the K postcondition values | Fully transparent, terminating mathematical definitions; no opaque result-bearing symbol. Their ordering meaning is justified by structural inspection. |
| Trusted canonical Python function | Oracle for program/semantics comparisons | Supports only the tested cases. It does not substitute for K reachability. |
| 331,216 Python comparisons and seven K/Python comparisons | Empirical implementation and generated-semantics bridges | Reproducible finite evidence only; explicitly not universal. |
| Source-level reasoning that the candidate scans rows forward and columns backward | Connects the implementation to the English order contract | Informal but persuasive; it cannot compensate for the absent all-matrix K claim. |

There are no local opaque symbols, external result oracles, proof-local
simplifications, priority rules, trusted attributes, or operational shortcuts.

### Gate accounting and verdict rationale

- Real-program soundness for the eleven claims: pass. The exact program
  executes, equations are sound, results are constrained, satisfying witnesses
  exist, and the false mutation is rejected.
- Natural-language intent adequacy: fail materially. The intended domain is all
  finite ragged integer matrices, while the theorem domain consists of three
  points plus one fixed shape.
- Evidence auditability: pass for the claims actually made. Commands, source
  mutations, exact statuses, and bounded outputs are preserved under
  `/audit-output/evidence/`.

The candidate therefore contains sound limited reachability proofs, but not the
requested partial-correctness proof over the real task's intended input domain.
The absent universal entry theorem is a missing proof obligation, so this
cannot be downgraded to a mere concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
