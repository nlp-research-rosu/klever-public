# Independent adversarial review: 129-minPath

The candidate does not contain a proof of the full HumanEval contract. Fresh
reconstruction confirms that its eleven submitted claims are honest,
result-constraining proofs of the exact generated program for a finite set of
inputs. However, the formal scope is only three fixed 3x3 executions and all
2x2 permutations at the single path length `k = 5`. The task contract ranges
over every square permutation grid with `N >= 2` and every positive `k`.
Neither a general entry claim nor loop invariants/summary claims bridge that
material gap. The successful differential tests are finite evidence about the
implementation and cannot substitute for the absent K theorem.

All candidate material, including prior `#Top` reports and compiled
definitions, was treated as untrusted. Execution used source copied to
`/tmp/audit-work/candidate-src`; fresh definitions were written only there.
Reviewer-authored tests and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the three expected files:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` is absent, including as a symlink. This is
consistent with the rendered mode, so there is no infrastructure breach. See
`evidence/stage1-provenance.txt`.

### Required artifacts and file types

The following candidate inputs are present as ordinary regular files, not
directories, devices, or symlinks:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`
- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`, `prove.sh`

The structured generation trace is one regular JSONL file. It contains 198
valid JSON records and no malformed record. The trace and reports claim that
eleven claims proved, but those claims were not used as proof evidence; see
`evidence/stage1-trace-summary.txt`,
`evidence/stage1-untrusted-json.txt`, and
`evidence/stage1-untrusted-reports.txt`.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, a Python bytecode cache, and generation logs. These
are additional untrusted build/report artifacts, not source integrity
failures. None was copied into or used by the fresh reconstruction.

### Prompt and translator identity

Byte comparisons against the trusted mounts passed:

- Candidate and trusted `prompt.py` both have SHA-256
  `417c9ed701884d14aff5ce42047f77711731af279eeeba3d3b685b92a8f29adb`.
- Candidate and trusted `py2mpy.py` both have SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Both `cmp` commands exited 0.

No required source artifact was missing, changed, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a square `N x N` grid, `N >= 2`, whose cells are a permutation of
`1..N^2`, and a positive integer `k`, return the lexicographically least
sequence of values obtained by visiting exactly `k` cells, starting anywhere
and moving across a shared edge at each step. Cells may be revisited.

Because `1` is unique and globally least, every minimum path starts at its
cell. For `k > 1`, its second value is the least orthogonal neighbor `m` of
that cell. From `m`, returning to `1` is lexicographically optimal, so the
minimum sequence alternates `1, m, 1, m, ...`. The trusted canonical
implementation computes that neighbor and constructs this alternating result.

### Candidate implementation

`/candidate/solution.py` implements the same algorithm:

1. It scans the square grid for the unique cell containing `1`.
2. It computes the minimum of the in-bounds orthogonal neighbors.
3. It appends `1` at even result indices and that minimum neighbor at odd
   indices until the result has length `k`.

Within the stated domain, each scan terminates, the cell containing `1` is
found exactly once, that cell has at least two neighbors because `N >= 2`,
and every subscript is guarded in bounds.

### Translator fidelity

The trusted translator was run on the scratch copy:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
```

It exited 0. Submitted and regenerated MPY files have the same SHA-256
`85540afa4175c713b59b8a6c9a85f05dadabb04a4bf032f90ea2b6b8772b610b`,
and `cmp` exited 0. See `evidence/stage2-mpy-regeneration.txt` and the
preserved `evidence/solution.regenerated.mpy`.

### Independent differential reconstruction

`evidence/differential_test.py` imports the trusted and generated entry
points by exact path. Its third oracle is an independently written
lexicographic dynamic program over paths ending at each cell; it does not
reuse either implementation or any K equation.

The test covered 855 valid inputs:

- both documented examples and a long-path version of the interior example;
- all 24 permutations of a 2x2 grid for every `k` from 1 through 9;
- every one of the nine possible positions of `1` in a directed 3x3 branch
  suite, at four path lengths;
- 250 deterministic random 3x3 grids, 250 4x4 grids, and 100 5x5 grids, with
  `k` from 1 through 18.

There were zero candidate-versus-canonical mismatches, zero
candidate-versus-independent-oracle mismatches, and no example failure. The
test also recorded out-of-domain behavior. In particular, at `N = 1` the
canonical raises `ValueError` while the candidate returns `[1]`; this is not
an intended-domain divergence because the contract requires `N >= 2`. See
`evidence/stage2-differential.txt`.

This establishes strong finite evidence that the Python rewrite is faithful.
It does not establish universal correctness and is not counted as a K proof.

## 3. Clean proof reconstruction

### Fresh builds

The scratch source directory initially contained only copied source artifacts.
It did not contain either candidate-provided compiled directory. K version
`v7.1.293` was used.

The generated semantics was freshly compiled with:

```text
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled-fresh
```

The command exited 0. The proof definition was freshly compiled with:

```text
kompile verification.k \
  --main-module MINPATH-VERIFICATION \
  --syntax-module MINPATH-VERIFICATION \
  --backend haskell \
  --output-definition verification-kompiled-fresh
```

That command also exited 0. The warnings in both logs concern deprecated
surface notation for `.K`; they do not report missing rules, parse failures,
or backend failures. See `evidence/stage3-build-semantics.txt` and
`evidence/stage3-build-proof.txt`.

### Positive proof reconstruction

The submitted aggregate target was rerun exactly:

```text
kprove spec.k \
  --definition verification-kompiled-fresh \
  --spec-module MINPATH-SPEC
```

It exited 0 and printed `#Top`; see
`evidence/stage3-kprove-all.txt`.

Because the candidate claims are unlabeled, the reviewer script
`evidence/split_claims.py` copied each of the eleven claims verbatim into a
distinct module. The generated claim artifacts are preserved in
`evidence/isolated-claims/`. Each was run independently with a command of the
form:

```text
kprove isolated-claims/spec-claim-NN.k \
  --definition verification-kompiled-fresh \
  --spec-module MINPATH-SPEC-NN
```

Every one of the eleven commands exited 0 and printed exactly one `#Top`.
The exact command and bounded output for each claim are in
`evidence/stage3-kprove-claim-01.txt` through
`evidence/stage3-kprove-claim-11.txt`.

### Fresh generated-semantics execution

`evidence/concrete_semantics_compare.py` ran the fresh LLVM definition on:

- both prompt examples;
- the interior example at `k = 6`;
- all four placements of `1` in a 2x2 grid at `k = 5`;
- the zero-iteration result loop at `k = 0`;
- the out-of-domain `N = 1` and empty-grid boundaries.

Every `krun` invocation exited 0. All ten K result cells exactly matched
direct execution of `solution.py`; see
`evidence/stage3-concrete-semantics.txt`. The valid cases exercise true and
false outcomes of all four neighbor-bound guards. The `k = 0` case exercises
the zero-iteration answer loop.

Thus clean reconstruction succeeds for the theorem the candidate actually
submitted.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

All claims begin from empty environment/function maps and result `none`. They
execute `solutionProgram`, then invoke the stored `minPath` body through
`start(grid, k)`. Every postcondition requires an empty `<k>` cell and an
exact `some(vList(...))` result. Final environment and function maps are
existentially framed and do not weaken the result equality.

| Claims | Precondition in plain language | Exact postcondition |
|---|---|---|
| 1 | First prompt grid, `k = 3` | result is `[1,2,1]` |
| 2 | Second prompt grid, `k = 1` | result is `[1]` |
| 3 | Second prompt grid, `k = 6` | result is `[1,4,1,4,1,4]` |
| 4–5 | A 2x2 grid with `1` top-left; the other entries are a permutation of `2,3,4`; split on the order of its two neighbors; `k = 5` | alternating path using the lesser neighbor |
| 6–7 | Same conditions with `1` top-right | alternating path using the lesser neighbor |
| 8–9 | Same conditions with `1` bottom-left | alternating path using the lesser neighbor |
| 10–11 | Same conditions with `1` bottom-right | alternating path using the lesser neighbor |

For claims 4–11, `validTail(A,B,C)` requires all three values to be distinct
members of `2..4`, hence exactly a permutation of `2,3,4`. Its conjunction
with either `A < B` or `B < A` is satisfiable and exhaustive because
`A != B`.

`evidence/adequacy_witnesses.py` supplies one ground satisfying assignment for
every claim. For example, `A=2,B=3,C=4` satisfies each `A<B` branch and
`A=3,B=2,C=4` satisfies each `B<A` branch. Both Python implementations return
the exact claimed value for all eleven witnesses. See
`evidence/stage4-adequacy-witnesses.txt`.

### Real-program identity

`solutionProgram` is a proof-definition constant whose sole rule expands into
the full constructor term in submitted `solution.mpy`. It does not summarize
or replace execution after expansion.

The static source comparison finds the same AST constructor tree; explicit
`.Stmts`/`.Exprs` tokens in `verification.k` are merely the parsed empty list
forms omitted by the MPY pretty-printer. A dynamic sensitivity check confirms
this identity. Under the fresh proof definition:

- submitted `solution.mpy` at depth 1, and
- `solutionProgram` at depth 2 (one extra step for its expansion)

produce byte-identical pretty-printed configurations, with SHA-256
`a3366567d28622cf089d31a9773bedb122fdc541f173aff9498a4eccc9f9f11f`.
The `diff` exited 0. See `evidence/program_pinning.sh`,
`evidence/solutionProgram.mpy`, and
`evidence/stage4-program-pinning.txt`.

There are no helper or loop claims. The fixed-size claims close by executing
the real nested scan loops and result-construction loop under `semantic.k`.

### Material adequacy failure

The formal theorem's domain is the union of:

- three fixed 3x3 `(grid,k)` executions; and
- all 24 valid 2x2 grids, but only at `k = 5`.

There is no claim quantified over:

- arbitrary `N >= 2`;
- arbitrary valid grid contents/shape at that `N`; or
- arbitrary positive `k`.

There is also no general invariant/summary claim for either nested grid scan
or the answer-building loop. The semantics can run other concrete inputs, but
executability is not a reachability theorem about them.

A simple intended-domain witness outside the formal theorem is
`grid=[[1,2],[3,4]], k=2`. Both Python implementations and the fresh
semantics return `[1,2]`, but none of the eleven claims has that precondition.
Likewise, almost every valid 3x3 grid and every valid `N >= 4` input is outside
the claims. The missing theorem is therefore material, not a cosmetic
restriction or a thin intent bridge.

The postconditions that do exist are exact and non-tautological. The failure is
not vacuity or result freedom; it is absence of the general entry theorem
needed by the problem.

## 5. Rule-by-rule static soundness review

### Source universe and declaration inventory

The candidate has exactly two K definition source files and one spec:
`semantic.k`, `verification.k`, and `spec.k`. There are no additional
proof-local helper K files.

Local syntax declarations are:

- `semantic.k:8-12`: `Program`, statement lists, parameter/string lists, and
  expression lists.
- `semantic.k:14-19`: `FuncDef`, `Assign`, `While`, `If`, expression
  statements, and `Return`.
- `semantic.k:21-29`: integer/name/binary/comparison/subscript/call/attribute/
  list expressions and comparison operators.
- `semantic.k:40-46`: runtime integer, Boolean, list, and `None` values;
  expression injection; stored functions; optional result.
- `semantic.k:48-62`: internal control items for sequencing, entry startup,
  evaluation continuations, and result setting.
- `semantic.k:64,68`: the local functions `listLength` and `getVal`.
- `verification.k:8-14`: the function symbols `grid2`, `grid3`, `path1`,
  `path3`, `path5`, and `path6`.
- `verification.k:35`: the Boolean function `validTail`.
- `verification.k:46`: the program constant `solutionProgram`.

The configuration at `semantic.k:73-79` has exactly the state used by this
program: `<k>`, variable environment, function map, and optional result.
There is no unused heap, output, exception, or call-stack cell.

There are nine local symbols declared `[function]`: `listLength`, `getVal`,
the six grid/path constructors, and `validTail`. There are no local
`[total]`, `[functional]`, `[simplification]`, `[anywhere]`, `[owise]`,
priority, or opaque declarations. The declaration scan is preserved in
`evidence/stage5-declaration-scan.txt`.

### Construct-to-semantics mapping

Every construct in `solution.mpy` is mapped:

| Used constructor | Declaration | Execution rules |
|---|---|---|
| `Module`, statement sequence | `semantic.k:8-9` | 81–83 |
| `FuncDef`, `Params` | 10–11, 14 | 85–90 |
| `Assign(Name(...),...)` | 15, 22 | 92–94 |
| `While` | 16 | 107–110 |
| `If` | 17 | 103–105 |
| `Expr` | 18 | 96–97 |
| `Return` | 19 | 99–101 |
| `Int`, `Name`, empty `ListExpr` | 21–22, 28 | 112–115 |
| `BinOp` with `+,-,*,%` | 23 | 117–122 |
| `Compare`/`CmpOp` with `<,>,==` | 24, 29 | 124–128 |
| nested `Subscript` | 25 | 130–132 plus 69–71 |
| `len` call | 26 | 134–135 plus 65–66 |
| named-list `append` call | 26–27 | 137–139 |

The continuation rules evaluate binary operands, comparison operands, and
subscript base/index left-to-right. `If` evaluates only the selected branch.
`While` returns to a stable condition/continuation shape. Assignments update
only `<env>`, append updates the named list binding, function definition
updates only `<functions>`, and return updates only `<result>`.

### Exhaustive semantic rule inventory

Every local rule in `semantic.k` is listed below. “Sound” is scoped to the
generated subset and the reachable uses in the submitted program, as required
for generated minimal semantics.

| ID | Line(s) | Rule and decision |
|---|---:|---|
| S01 | 65 | `listLength(.List) => 0`: sound empty-list base case. |
| S02 | 66 | `listLength(ListItem(_) REST)`: sound structural recursion; strictly removes one item. |
| S03 | 69 | `getVal(ListItem(V) _,0) => V`: sound zero-index lookup. |
| S04 | 70–71 | Positive-index `getVal` recursion: sound and decreasing under `I > 0`; negative/out-of-range accesses remain visibly stuck. |
| S05 | 81 | `Module(SS) => exec(SS)`: sound entry sequencing. |
| S06 | 82 | Empty `exec` disappears: sound sequence base case. |
| S07 | 83 | Head statement followed by remaining `exec`: sound ordered sequencing. |
| S08 | 85–86 | `FuncDef` stores its exact parameters/body under its textual name: sound for the module's single function. |
| S09 | 88–90 | `start` selects the exact stored `minPath` binding, installs `grid,k`, and executes that body: acceptable explicit entry-harness primitive; it does not manufacture a result. |
| S10 | 92 | Named assignment evaluates its RHS first: sound. |
| S11 | 93–94 | Evaluated assignment updates the named environment entry: sound. |
| S12 | 96 | Expression statement evaluates before discard: sound. |
| S13 | 97 | Discarding an evaluated value has no modeled state effect: sound. |
| S14 | 99 | Return evaluates its expression first: sound on the submitted final return. |
| S15 | 100–101 | `setResult` stores the exact value: sound on the submitted final return and exact `none` initial result. |
| S16 | 103 | `If` evaluates the guard first: sound. |
| S17 | 104 | True guard executes exactly the then-list: sound. |
| S18 | 105 | False guard executes exactly the else-list: sound. |
| S19 | 107 | `While` evaluates the condition: sound. |
| S20 | 108–109 | True condition executes the body then the same loop: sound recurring control. |
| S21 | 110 | False condition exits the loop: sound. |
| S22 | 112 | Integer literal becomes the same unbounded integer value: sound. |
| S23 | 113–114 | Name lookup returns the map-bound value: sound for all reachable candidate names. |
| S24 | 115 | Empty list expression becomes an empty runtime list: sound; nonempty literal syntax is deliberately unmodeled and unused. |
| S25 | 117 | Binary operation starts by evaluating the left operand: sound. |
| S26 | 118 | It then evaluates the right operand while retaining the left value: sound left-to-right order. |
| S27 | 119 | Integer addition: sound for Python's unbounded integers. |
| S28 | 120 | Integer subtraction: sound for Python's unbounded integers. |
| S29 | 121 | Integer multiplication: sound for Python's unbounded integers. |
| S30 | 122 | Integer remainder: sound on reachable nonnegative indices with divisor `2`; no conclusion is drawn for Python/K sign differences outside that use. |
| S31 | 124 | Comparison starts with the left operand: sound. |
| S32 | 125 | Comparison then evaluates its right operand: sound. |
| S33 | 126 | Integer `<`: sound. |
| S34 | 127 | Integer `>`: sound. |
| S35 | 128 | Integer equality: sound. |
| S36 | 130 | Subscript evaluates the base first: sound. |
| S37 | 131 | Subscript evaluates the index second: sound. |
| S38 | 132 | Integer list lookup delegates to `getVal`: sound for the guarded in-bounds candidate accesses. |
| S39 | 134 | Exact one-argument `len` call evaluates its argument: sound for `len(grid)`. |
| S40 | 135 | List length delegates to the truthful structural function: sound. |
| S41 | 137 | Exact `Name(X).append(E)` form evaluates `E` before update: sound for `answer.append(...)`. |
| S42 | 138–139 | Append extends the named list binding and yields `None`: sound for the non-aliased local `answer` list used here. |

The semantic function equations have no conflicting overlap: empty and
nonempty list-length cases are disjoint; index zero and positive-index
`getVal` cases are disjoint. Operator rules are separated by literal operator
strings. The valid program guards keep all used list indices in range.

This is intentionally not a reusable full Python semantics. In particular,
return does not model abrupt unwinding through an arbitrary suffix,
`append` does not model receiver evaluation/aliasing beyond a named local
list, nonempty list literals are unmodeled, and ordinary user-function calls
are replaced by the explicit `start` harness. Those are narrower coverage
limitations. They do not justify labeling a rule unsound here because the
submitted program reaches only a final return, appends only to the unaliased
local `answer`, constructs only an empty literal, and is invoked only through
`start`. No intended-domain input supplies a false-conclusion witness for
those excluded contexts.

### Exhaustive verification-rule inventory

| ID | Line(s) | Rule and decision |
|---|---:|---|
| V01 | 16–18 | `grid2`: truthful row-major 2x2 nested-list constructor; unconditional and terminating. |
| V02 | 20–23 | `grid3`: truthful row-major 3x3 nested-list constructor; unconditional and terminating. |
| V03 | 25 | `path1`: truthful one-element `[1]`; ignoring its readability argument is harmless and explicit. |
| V04 | 26–27 | `path3(M)`: truthful `[1,M,1]`. |
| V05 | 28–30 | `path5(M)`: truthful `[1,M,1,M,1]`. |
| V06 | 31–33 | `path6(M)`: truthful `[1,M,1,M,1,M]`. |
| V07 | 36–40 | `validTail`: truthful range and pairwise-distinct predicate; over `2..4` it is exactly the permutation condition. |
| V08 | 47–122 | `solutionProgram`: exact definitional expansion to submitted MPY; execution continues through all fixed semantic rules. |

Each verification function has one unconditional, terminating equation for
its constructor, so coverage is complete and there is no same-symbol rule
overlap. `solutionProgram` is not an oracle or task-answer rule: it only
introduces the actual source term. The depth-sensitive pinning test confirms
that it does not bypass or alter control/state.

### Static soundness conclusion

No local rule encodes the requested answer, replaces a program-derived value
with an unconstrained symbol, fabricates a result, or preempts an implemented
construct. There are no opaque symbols or proof-local operational bridges.
Accordingly, this review makes no claim that a local rule is unsound and does
not invent a false-conclusion witness. The candidate's decisive defect is
theorem scope, not an unsound semantic shortcut.

## 6. Fresh non-vacuity test

The reviewer-authored `evidence/spec-vacuity.k` contains one reachable
mutation of claim 1. On the prompt grid whose real result is `[1,2,1]`, it
changes the required result from `path3(2)` to `path3(3)`, i.e. `[1,3,1]`.
The precondition is ground and satisfiable.

First, the mutation was compiled without executing the proof:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled-fresh \
  --spec-module MINPATH-SPEC-VACUITY \
  --dry-run
```

This exited 0, proving the mutation has valid imports, syntax, and generated
KORE; see `evidence/stage6-mutation-dry-run.txt`.

The actual proof command omitted `--dry-run`. It exited 1 and emitted
`WarnStuckClaimState`. The residual terminal configuration has empty `<k>` and
the concrete result `[1,2,1]`, which cannot unify with the mutated
postcondition `[1,3,1]`. This is the expected unmet result obligation, not a
parser error, missing import, timeout, or unrelated crash. See
`evidence/stage6-mutation-proof.txt`.

The finite submitted claims therefore pass non-vacuity.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the generated semantics and K built-ins, the fresh `#Top` results
establish:

- the exact submitted MPY program terminates with the claimed list on the
  three fixed 3x3 invocations;
- for every `A,B,C` satisfying the stated finite 2x2 preconditions, the exact
  program terminates at `k = 5` with the stated alternating list;
- the result is constrained exactly, not left free;
- the submitted program body, nested loops, guards, lookups, assignments, and
  appends are executed rather than replaced by a summary.

For the eight symbolic 2x2 claims, the preconditions together cover every
valid 2x2 permutation. Therefore those claims amount to a proof of all valid
2x2 grids specifically at `k = 5`.

They do not establish the HumanEval function for arbitrary valid `(grid,k)`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, LLVM/Haskell backends, and reachability prover | All builds and proofs | Ordinary unavoidable toolchain trust; acceptable. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, and `LIST` primitives | Arithmetic, comparison, environments, and list operations | Ordinary low-level K trust boundary; acceptable. |
| Trusted CPython-AST translator | Identity of Python source and MPY term | Byte identity was independently reconstructed; acceptable syntactic bridge. |
| Generated `semantic.k` as a model of the used Python subset | Meaning of MPY execution | Audited rule by rule and tested concretely. Faithful for every reachable used construct; explicitly not a full Python semantics. |
| `start` entry harness | Binding `grid,k` and executing `minPath` | Acceptable operational harness because it selects the exact stored body and does not affect the computed result except through execution. |
| `solutionProgram` definitional constant | Every formal claim | Exact source expansion, statically and depth-sensitively pinned; acceptable. |
| Trusted canonical implementation and independent DP oracle | Python fidelity/intent evidence | Finite empirical support only; not part of or a substitute for the K proof. |
| Mathematical argument that the minimum path alternates `1` and its least neighbor | Natural-language interpretation of exact lists | Sound informal argument and independently tested, but only relevant to inputs actually covered by a formal claim. |
| Generalization from the finite claims/tests to every `N >= 2, k > 0` | The requested full correctness result | Illegitimate: no K claim or proof supplies this generalization. This is the material failure. |

### Gate accounting and verdict rationale

- Clean verification of the submitted claims: **pass**. Aggregate and all
  isolated positive targets exit 0 with `#Top`.
- Real-program soundness and non-vacuity for those claims: **pass**. The
  program is pinned, no shortcut/oracle exists, all preconditions are
  satisfiable, and the false result mutation is rejected.
- Intent adequacy for problem 129: **fail**. The theorem omits arbitrary grid
  size, grid contents, and positive `k`; this is the central requested domain,
  not a minor evidence limitation.
- Reproducibility/trust accounting: **pass**, subject to the stated ordinary
  toolchain and generated-semantics boundaries.

The candidate contains legitimate proofs of the eleven narrow claims, but it
does not contain a legitimate partial-correctness proof of the real generated
program over the problem's intended domain. A prior aggregate `#Top` and the
855 successful differential cases cannot repair the missing universal K
theorem. Under the supplied decision boundary, this material adequacy gap is
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
