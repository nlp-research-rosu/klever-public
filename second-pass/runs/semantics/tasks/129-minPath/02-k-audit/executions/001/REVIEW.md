# Independent adversarial audit: 129-minPath

## Outcome

The reconstructed K claims are sound, non-vacuous, result-constraining, and
execute the exact submitted `solution.mpy` AST under the unchanged supplied
semantics. The candidate does **not**, however, prove the full natural-language
contract. Its entry claims prove two fixed examples and one symbolic theorem
restricted to every 2x2 permutation at exactly `k = 4`. There is no entry claim
for arbitrary `N >= 2` and arbitrary positive `k`.

That is a material intent-adequacy limitation, but it is not an unsoundness in
the claims that were actually made. No candidate rule can prove a false result
on the formal claim domains, no operational bridge bypasses execution, and the
fresh false-result mutation is rejected. The appropriate pairing is therefore
`CONCERNS / LEGIT`, not `PASS` and not `FAIL`.

Audit workspace: `/tmp/audit-work/129-minPath-audit`.

Reviewer evidence: [`evidence/`](./evidence/).

## 1. Input and provenance integrity

### Mode and trusted mounts

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no mode/mount
contradiction and hence no infrastructure breach.

The candidate and trusted trees were enumerated without following symlinks.
The candidate contains no symlinked entries. See
[`stage1-candidate-tree.log`](./evidence/stage1-candidate-tree.log) and
[`stage1-reference-tree.log`](./evidence/stage1-reference-tree.log).

### Exact integrity checks

All selected source-integrity checks pass:

- `cmp -l /candidate/prompt.py /reference/prompt.py` exited 0:
  [`stage1-prompt-cmp.log`](./evidence/stage1-prompt-cmp.log).
- `cmp -l /candidate/py2mpy.py /reference/py2mpy.py` exited 0:
  [`stage1-translator-cmp.log`](./evidence/stage1-translator-cmp.log).
- `diff -r --no-dereference /candidate/reference-semantics
  /reference/reference-semantics` exited 0:
  [`stage1-semantics-diff.log`](./evidence/stage1-semantics-diff.log).

Thus every file and directory in the candidate's `reference-semantics/` has
the trusted counterpart, type, and bytes. There are no missing, additional,
changed, mistyped, or symlinked entries inside that required semantics tree.
This integrity result does not bless `verification.k`; that file is reviewed
separately below.

### Missing and extra candidate artifacts

The following requested provenance/report artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any of the checked conventional structured generation trace names
  (`generation-trace*.json[l]` or `structured-generation-trace*.json[l]`)
- `PROOF.md`

The bounded existence check is
[`stage1-claims-artifacts.log`](./evidence/stage1-claims-artifacts.log).
Because these files do not exist, there were no corresponding candidate claims
to trust or inspect. Their absence is an auditability concern, not a substitute
for dynamic proof reconstruction and not by itself a proof unsoundness.

The candidate also contains the built cache
`__pycache__/solution.cpython-310.pyc`. It is outside the required supplied
semantics tree, was treated as an extra generated artifact, and was ignored.
The scratch build copied only source artifacts and the trusted semantics tree;
no candidate-provided definition or cache was used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and reference behavior

For a square `N x N` grid with `N >= 2` containing the permutation
`1..N*N`, and a positive integer `k`, the function must return the
lexicographically least sequence of values along a legal orthogonal path that
visits exactly `k` cells. Cells may be revisited.

The trusted canonical implementation finds the unique cell containing `1`,
chooses the minimum-valued orthogonal neighbor `m`, and returns
`[1, m, 1, m, ...]` truncated to length `k`. This is the intended minimum:
the first value must be the globally smallest value `1`; the smallest possible
second value is `m`; returning from `m` to `1` gives the smallest possible
third value; the argument repeats. Uniqueness of grid values fixes the chosen
cell and neighbor.

The submitted `solution.py` implements the same algorithm with explicit
up/down/left/right minimum updates. It scans the full grid, computes
`neighbor = n*n + 1` and lowers it with every in-bounds neighbor of `1`, then
appends `1` on even loop indices and `neighbor` on odd indices.

### Trusted translation identity

The submitted constructor term was regenerated in scratch with:

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
```

The command exited 0, and
`cmp -l solution.mpy regenerated-solution.mpy` exited 0. Exact logs:
[`stage2-regenerate-mpy.log`](./evidence/stage2-regenerate-mpy.log) and
[`stage2-mpy-byte-identity.log`](./evidence/stage2-mpy-byte-identity.log).
The submitted `solution.mpy` is therefore byte-identical to the trusted
translation of `solution.py`.

### Independent differential testing

The reviewer-authored suite
[`differential_test.py`](./evidence/differential_test.py) imports the trusted
canonical entry point and the generated entry point independently. Its complete
deterministic inputs are preserved in
[`differential-inputs.json`](./evidence/differential-inputs.json), SHA-256
`ea59221ea097b68ad0ebd34210a3d48a1fd8dd87fd66afcd6f85c94ad1232628`.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py \
  --candidate /tmp/audit-work/129-minPath-audit/solution.py \
  --canonical /tmp/audit-work/129-minPath-audit/trusted/canonical.py \
  --inputs-out /audit-output/evidence/differential-inputs.json
```

It exited 0 over 3,570 cases:

- both documented examples;
- all 24 valid 2x2 grids at `k` in `{1,2,3,4,5,8}`;
- 1,260 seeded 3x3 cases covering every position of `1`;
- 720 cases each for seeded 4x4, 5x5, and 6x6 grids;
- empty-grid and `k = 0` probes explicitly marked outside the prompt domain.

There were zero candidate/canonical mismatches. An independent exhaustive path
enumerator also checked 1,046 small cases and found zero mismatches. Each of the
four position guards saw both truth values. The nested minimum updates saw all
reachable outcomes on valid inputs; the first executed `up` comparison is
necessarily true because its initial comparator is the `n*n+1` sentinel.
Results and exit status are in
[`stage2-differential.log`](./evidence/stage2-differential.log).

These tests strongly support program/canonical equivalence on the tested
inputs. They do not turn the later narrow K claims into a universal K theorem.

## 3. Clean proof reconstruction

### Toolchain and clean definitions

The independently available toolchain is K `v7.1.337` (build date
2026-06-18). `kup` is absent, but `/usr/bin/kompile`, `/usr/bin/kprove`, and
`/usr/bin/krun` all run. See
[`stage3-tool-versions.log`](./evidence/stage3-tool-versions.log).

The LLVM definition was built from the trusted scratch semantics with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. Its non-exhaustive-match warnings concern supplied functions such
as `mapStrVS`, float conversions, `joinCodes`, and out-of-bounds
`valSeqAt`; none is reached by the audited program claims. Exact output:
[`stage3-kompile-llvm.log`](./evidence/stage3-kompile-llvm.log).

The translated candidate concrete assertion driver then ran with:

```text
krun concrete-tests.mpy --definition runtime-kompiled
```

It exited 0 with final `.K`, `NoExc`, and exit code 0:
[`stage3-krun-concrete-tests.log`](./evidence/stage3-krun-concrete-tests.log).

The Haskell proof definition was built from source with:

```text
kompile verification.k \
  --backend haskell \
  --main-module MINPATH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0:
[`stage3-kompile-haskell.log`](./evidence/stage3-kompile-haskell.log).
The proof definition imports `MPY`, not concrete-only `MPY-CONCRETE`.

### Independent positive-claim runs

The original claims were unlabeled. The reviewer made the semantically inert
label-only copy [`spec-labeled.k`](./evidence/spec-labeled.k) so every claim
could be selected independently. The unchanged source is preserved as
[`original-spec.k`](./evidence/original-spec.k).

Each command below exited 0 and printed `#Top`:

```text
kprove spec-labeled.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC \
  --claims MINPATH-SPEC.loop-invariant

kprove spec-labeled.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC \
  --claims MINPATH-SPEC.example-top-left

kprove spec-labeled.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC \
  --claims MINPATH-SPEC.example-interior

kprove spec-labeled.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC \
  --claims MINPATH-SPEC.symbolic-2x2
```

The individual logs are
[`stage3-kprove-loop-invariant.log`](./evidence/stage3-kprove-loop-invariant.log),
[`stage3-kprove-example-top-left.log`](./evidence/stage3-kprove-example-top-left.log),
[`stage3-kprove-example-interior.log`](./evidence/stage3-kprove-example-interior.log),
and
[`stage3-kprove-symbolic-2x2.log`](./evidence/stage3-kprove-symbolic-2x2.log).

Finally, the untouched complete source was run:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC
```

It also exited 0 and printed `#Top`:
[`stage3-kprove-complete-spec.log`](./evidence/stage3-kprove-complete-spec.log).
Clean reconstruction therefore passes.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

1. **Append-loop invariant.** Given loop state
   `#loop(rangeObj(I,K,1), Name("i"), minPathAppendBody)`, with
   `0 <= I < K`, local `path = ref(H)`, local `neighbor = N`, and heap object
   `H = list(P)`, executing the remaining exact append loop consumes the
   computation, leaves `neighbor` unchanged, sets `i` to `K-1`, and changes
   the same heap object to `minPathBuild(P,I,K,N)`.

2. **First prompt example.** Loading the submitted function and calling it on
   `[[1,2,3],[4,5,6],[7,8,9]], 3` terminates without exception and returns
   `ref(0)`, whose exact heap value is `[1,2,1]`.

3. **Second prompt example.** Loading the submitted function and calling it on
   `[[5,9,3],[4,1,6],[7,8,2]], 1` terminates without exception and returns
   `ref(0)`, whose exact heap value is `[1]`.

4. **Symbolic 2x2 theorem.** For integers `A,B,C,D` that are pairwise distinct
   and each in `1..4`, loading the submitted function and calling it on
   `[[A,B],[C,D]], 4` returns the exact alternating four-element list
   `[1,m,1,m]`, where `m` is the smaller neighbor of the unique cell containing
   `1`.

The returned value is not free or existential. Every entry claim fixes
`<k>` to `ref(0)`, fixes heap location 0 to an exact list expression, fixes the
post-load closure, and constrains the stack, return state, exception state, and
exit code. No one-way implication substitutes for the result equality.

### Satisfiability and ground substitutions

A concrete state satisfying the loop claim is:

```text
I=0, K=4, N=2, P=.ValSeq, L=0, H=0,
scope 0 containing i=OLD, path=ref(0), neighbor=2,
heap 0 containing list(.ValSeq)
```

It satisfies `0 <= 0 < 4`; the claimed post-state has `i=3` and heap list
`[1,2,1,2]`.

The fixed entry claims are their own concrete satisfying states. For the
symbolic claim, `A=1,B=2,C=3,D=4` is a satisfying substitution. The
reviewer check
[`pinning_python_check.py`](./evidence/pinning_python_check.py) shows that the
claimed result, trusted canonical result, and submitted Python result are equal
for one satisfying instance of every entry claim. It exited 0:
[`stage4-python-pinning-witnesses.log`](./evidence/stage4-python-pinning-witnesses.log).

The same three cases were translated with the trusted translator and executed
under the fresh LLVM semantics. All assertions passed with `.K`, `NoExc`, and
exit code 0:
[`pinning-driver.py`](./evidence/pinning-driver.py),
[`stage4-translate-pinning-driver.log`](./evidence/stage4-translate-pinning-driver.log),
and
[`stage4-krun-pinning-witnesses.log`](./evidence/stage4-krun-pinning-witnesses.log).

### Exact real-program pinning

The entry claims use the proof macro `minPathProgram`, so textual similarity
alone was not accepted. The reviewer parsed and macro-expanded both the actual
submitted `solution.mpy` and the expression `minPathProgram` using the fresh
proof definition:

```text
kast --definition verification-kompiled \
  --module MINPATH-VERIFICATION --sort Module --expand-macros \
  --output kore --output-file parsed-solution.kore solution.mpy

kast --definition verification-kompiled \
  --module MINPATH-VERIFICATION --sort Module --expand-macros \
  --output kore --output-file parsed-macro.kore \
  --expression minPathProgram

cmp -l parsed-solution.kore parsed-macro.kore
```

Both parses and the final comparison exited 0:
[`stage4-kast-submitted-program.log`](./evidence/stage4-kast-submitted-program.log),
[`stage4-kast-proof-program.log`](./evidence/stage4-kast-proof-program.log),
and
[`stage4-kast-program-identity.log`](./evidence/stage4-kast-program-identity.log).
The macro-expanded KORE terms are byte-identical. The proof executes the actual
submitted AST, not a substituted algorithm.

### Material adequacy gap

There is no symbolic entry claim for general `N` or general positive `k`.
The append-loop helper is general over a loop that has already been initialized,
but it does not prove the grid scan, neighbor selection, or caller for arbitrary
inputs. The only non-fixed entry theorem has `N=2` and `k=4`.

Therefore the K proof does not establish the prompt contract for, for example,
a symbolic 3x3 grid at arbitrary `k`, even though differential evidence strongly
supports the Python implementation. This is the reason the verdict cannot be
`PASS`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated, line-addressed inventory is
[`rule-inventory.md`](./evidence/rule-inventory.md), produced by
[`inventory_k.py`](./evidence/inventory_k.py). The exact command and exit status
are in
[`stage5-inventory-command.log`](./evidence/stage5-inventory-command.log).

It covers every declaration/rule start in `reference-semantics/semantics.k`,
all 23 supplied helper K files, and `verification.k`:

- 950 total records;
- 235 syntax declarations;
- 709 rules;
- 5 evaluation contexts;
- 1 configuration;
- 25 opaque/concrete-symbol function declarations;
- 45 records carrying `priority(...)`;
- 0 simplification rules.

An independent raw start-count agrees exactly with the inventory totals.
Every record includes source line, attributes, class, audited-path status,
complete normalized text, and an assessment.

### Selected configuration and used-construct mapping

The supplied configuration has the relevant cells `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The entry claims constrain all cells material to loading,
calling, allocation, return, and failure.

The constructs in `solution.mpy` map to fixed rules as follows:

| Submitted construct | Declaration/behavior |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k:124-127` |
| `FuncDef`, closure, frame, return | `functions.k:14-20,63-90`; `call.k:69-75` |
| `Name`, `Call`, argument order | `core.k:130-191`; `call.k:16-32` |
| `len`, `range` | `builtins.k:20-26,177-180`; `range.k:9-24` |
| `Assign`, `If`, nested `For` | `controls.k:9-31,51-74` |
| integer `+`, `-`, `*`, `%`, comparisons | `operators.k:10-46`; `int.k:9-27` |
| list/row indexing | `subscript.k:11-41`, including heap dereference |
| empty list and append | `list.k:13-20,53-55`; call routing in `call.k` |
| loop-target binding | `tuple.k:31-41` |

Evaluation is left-to-right through strictness/contexts and `#evalArgs`.
`For` evaluates its iterable once, uses `#iterNext`, binds the target, executes
the body, and resumes the loop label. Function calls create a fresh scope,
bind parameters, push a frame, execute the real body, and pop on return.
List construction allocates a fresh heap object; `append` updates that object
in place. The entry claims' exact heap/scopes/stack post-states therefore cover
the observable allocation and state changes used by this program.

### Supplied-semantics rules

The entire supplied tree is byte-identical to the trusted selected semantics.
No candidate-local semantic rule was inserted into it. The fixed semantics is
the declared execution level for this audit; the inventory nevertheless
separates rules reachable from the claims from unused language features.

All 45 priority-bearing rules are in the unchanged supplied tree. On the used
path, priority selects heap dereference, cell-aware writes, or allocation-aware
list handling before generic value dispatch. Those matches preserve the
complete relevant state footprint. `verification.k` adds no priority rule.

The 25 opaque/concrete symbols are:

```text
intFloatDiv divII floatMod floatLt absF floorFI toF ceilF
subF divF addF mulF powF gtF eqF decStrToF divFloatIntV intToF
truncF roundF roundFN sqrtF md5hexCodes sortVS sortKeyVS
```

They concern floats, hashes, or sorting. None occurs in `solution.mpy`, any
claim, any postcondition helper, or a reachable claim path. No result in this
audit depends on an opaque interpretation. The proof definition also excludes
the concrete-only module.

The LLVM compiler notes narrower fixed-semantics coverage gaps in unused
functions, and `valSeqAt` is intentionally total but underspecified
out-of-bounds. All subscript operations in the formal entry claims are
in-bounds: the two examples are concrete valid grids, and the symbolic claim
constructs exactly two rows of length two while the unique-`1` scan fixes row
and column to `{0,1}`. Without a false conclusion witness on the formal domain,
these are recorded as unused/narrower evidence boundaries, not mislabeled as
unsound rules.

### Proof-local declarations and rules

`verification.k` has 8 syntax declarations and 14 rules:

- Four macro declarations/equations:
  `minPathAppendBody`, `minPathBody`, `minPathProgram`, and
  `minPathClosure`. They are compile-time aliases, not operational bridges.
  Macro-expanded program identity is established in Stage 4.
- `minPathMin` has the disjoint, exhaustive guards `A <= B` and `A > B` and
  returns the ordinary integer minimum.
- `minPathNeighbor2` has four mutually exclusive cases selected by the
  location of `1` in `A`, then `B`, then `C`, else `D`. The cases are
  exhaustive over all integers. Under the entry precondition, exactly one
  argument is `1`, and each RHS is the minimum of the two actual orthogonal
  neighbors.
- `minPathFour(M)` constructs exactly `[1,M,1,M]`.
- `minPathBuild` has the base case `I >= K` and two `I < K` parity cases.
  The cases are disjoint and exhaustive because `pyMod(I,2)` is either zero
  or nonzero. Recursion increases `I` by one and exactly models the loop's
  append-in-place behavior.

There is no proof-local `<k>` operational rewrite, opaque symbol,
`[simplification]`, `[concrete]`, `[owise]`, or priority rule. The helpers
name mathematical results but do not replace program execution. Their guards
cover every declared use, overlaps are either absent or impossible, and no
task answer is injected through an unconstrained oracle.

No unsound rule is identified. Accordingly, there is no false-conclusion
witness to report for a supposedly unsound rule; the narrower issue is theorem
coverage, not rule validity.

## 6. Fresh non-vacuity test

The reviewer created
[`spec-vacuity.k`](./evidence/spec-vacuity.k), a distinct module containing the
first prompt-example entry claim but changing its exact result heap from the
true `[1,2,1]` to the false `[1,3,1]`. The input is a reachable satisfying
state and its true result is independently shown by both Python
implementations and fresh K execution.

First, the mutation was parsed and compiled to KORE:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC-VACUITY --dry-run
```

This exited 0:
[`stage6-vacuity-dry-run.log`](./evidence/stage6-vacuity-dry-run.log).

Then the actual proof was run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module MINPATH-SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The residual is the fully executed
reachable final state with `<k> ref(0) ~> .K </k>` and heap location 0 equal to
the actual list `[1,2,1]`, which cannot unify with the mutated `[1,3,1]`.
The failure is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash. Full bounded evidence:
[`stage6-vacuity-proof.log`](./evidence/stage6-vacuity-proof.log).

The proof is non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the selected supplied MPY semantics and K's reachability logic:

- the exact submitted append-loop body satisfies the stated accumulator
  invariant for every state matching its precondition;
- the exact submitted program terminates with `[1,2,1]` on the first prompt
  example;
- it terminates with `[1]` on the second prompt example;
- for all 24 permutations of `1..4` in a 2x2 grid, at `k=4`, it terminates
  without exception and returns the exact lexicographic-minimum sequence
  `[1,m,1,m]`.

The proof also fixes the post-load closure, result reference, heap allocation,
empty stack, cleared return state, absence of exception, and zero exit code.

It does **not** formally establish:

- the entry theorem for arbitrary `N >= 2`;
- the entry theorem for arbitrary positive `k`;
- universal equivalence between the submitted Python implementation and the
  trusted canonical implementation;
- universal equivalence between the supplied MPY subset and all CPython
  behavior;
- correctness of any unused float, hash, sort, dict, string, or other
  fixed-semantics feature.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell/LLVM backends, reachability engine | All build, execution, and proof results | Necessary low-level trust boundary; independently rebuilt and exercised. |
| K integer, Boolean, map, list, and equality hooks | Used MPY rules and helper mathematics | Acceptable ordinary mathematical/runtime primitive boundary. |
| Byte-identical trusted supplied MPY semantics | Every formal claim | Required selected semantics level; used constructs were statically mapped and dynamically executed. |
| `pyMod` and list/range/call primitives in the supplied semantics | Append invariant and all entries | Used only on guarded ordinary integer/list cases; no opaque result. |
| Proof-local macro aliases | All entries | Acceptable because expanded KORE is byte-identical to submitted `solution.mpy`. |
| `minPathMin`, `minPathNeighbor2`, `minPathFour`, `minPathBuild` | Symbolic result and loop claim | Truthful, total, guarded mathematical definitions; no execution replacement. |
| 25 fixed opaque/concrete symbols | None of the audited claims | Inert for this program; listed explicitly in Stage 5. |
| Trusted prompt, canonical implementation, and translator mounts | Intent restatement and differential oracle | Authorized trusted inputs. The translator identity is exact; canonical-to-intent meaning remains an informal mathematical bridge plus finite testing. |
| Reviewer differential suite | General program/canonical evidence | 3,570 finite cases with zero mismatches; supportive only, not a universal K proof. |
| Alternating-path argument | Natural-language meaning of the 2x2 result and broader algorithm | Straightforward informal mathematics, not encoded as a general K theorem. |
| Missing candidate provenance files and `PROOF.md` | Candidate auditability only | Concerning omission, but not used as proof evidence and not allowed to replace reconstruction. |

### Gate summary and verdict rationale

- **Real-program soundness:** pass. The proof runs the exact AST, all positive
  claims reconstruct, local extensions are sound and non-operational, concrete
  witnesses exist, and the false result is rejected.
- **Intent adequacy:** limited. The formal entry domain omits essentially all
  grids larger than 2x2 and all symbolic path lengths other than the fixed
  examples/`k=4`.
- **Trust/evidence auditability:** reviewer evidence is reproducible and
  bounded, but the candidate supplied none of the requested generation
  provenance or proof report files.

The formal claims are legitimate proofs about the real generated program.
Their substantial under-coverage of the requested input domain and the missing
candidate audit trail require `CONCERNS`, while the absence of any false,
vacuous, substituted, or oracle-backed proof justifies `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
