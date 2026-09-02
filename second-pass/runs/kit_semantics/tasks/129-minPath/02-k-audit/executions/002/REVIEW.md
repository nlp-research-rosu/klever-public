# Independent adversarial audit: 129-minPath

This is a completed seven-stage audit of the immutable candidate in
`/candidate`, under `SUPPLIED_SEMANTICS`. I used the required `using-kit` and
`validating-proof` procedures, rebuilt from source in
`/tmp/audit-work/minpath-129`, and did not use either candidate-provided
kompiled definition.

Decision: **CONDITIONAL CONCERNS / LEGIT** under the registered
129-minPath provision. The exact condition is that the frozen Haskell backend
does not replay the independently proved `result-loop-tail` cut (and does not
symbolically normalize the next `snocVS` instance) while composing the full
unbounded call theorem. All seven constituent claims are freshly machine
proved, no unsound rule or operational bridge was found, and the candidate
reported the incomplete composition honestly. This is not a `PASS`: the
single `minpath-full-contract` composition command still does not produce
`#Top`.

## 1. Input and provenance integrity

### Launcher records

`/audit-input.json` declares `record_layout: pipeline-v3`, problem
`129-minPath`, condition `kit-semantics`, and
`semantics_mode: SUPPLIED_SEMANTICS`. The trusted supplied semantics is
present at `/reference/reference-semantics`, as required. All launcher-required
pipeline-v3 records are readable regular files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- one structured JSONL trace below `/generation-evidence/codex-trace`.

I independently hashed each mounted file. Every recorded per-file hash
matches. In particular, the campaign lock's actual SHA-256 is
`d332998734dca432d9c0f99fafcf5ab5680ec8245bf820a8b19599581dedf16b`,
exactly the value in `/audit-input.json`, and its parsed JSON object exactly
equals the embedded `audit_campaign` block. The canonical, trusted prompt,
translator, run/task/result manifests, invocation, metrics, usage, runtime
metrics, generation prompt, final text, output log, and trace file all match
their launcher-recorded hashes. See
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log).

The 5,661-line structured trace parses as JSON on every line. Its mounted
SHA-256 is
`c2658a044ec865d7927f9f419be7c524d916a6a65c1d64392b35179b82a9ad1a`,
which matches the invocation manifest. I inventoried its event types, 497
shell-command records, plain messages, and flagged failure outputs in
[stage1-trace-summary.log](/audit-output/evidence/stage1-trace-summary.log).
The untrusted generation records consistently say `FAILED`/partial: auxiliary
claims closed but the full target did not. This is an honest historical claim,
not proof evidence.

### Trusted-input and supplied-semantics comparison

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The candidate and trusted
semantics trees each have the same 25 recursively inventoried entries (24
regular K files plus the subdirectory), identical file hashes and entry types,
and no symlinks. There are no missing, additional, changed, mistyped, or
symlinked semantics entries. The candidate tree as mounted has 776 recursively
inventoried entries and no symlinks. Candidate kompiled directories were
therefore untrusted but not an integrity defect; they were excluded from the
scratch reconstruction.

Result of stage 1: **PASS**. There is no infrastructure breach and no reason to
omit a candidate verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Docstring contract

The contract in `/reference/prompt.py` is:

- `grid` has `N` rows and `N` columns, with `N >= 2`;
- its cells contain every integer from `1` through `N*N` exactly once;
- `k` is positive;
- a path visits exactly `k` cells and moves only across shared edges; and
- the function returns the unique lexicographically least value sequence among
  all such paths.

The candidate scans the grid to locate the unique `1`, computes the minimum of
its in-bounds orthogonal neighbors, and returns an alternating sequence of `1`
and that neighbor, truncated to length `k`. This is correct: every least path
must start at the globally least value `1`; its least possible next value is
the least neighbor `M`; from `M`, the globally least adjacent value is the same
cell `1`; induction repeats this unique two-cell path.

The implementation uses no behavior outside the declared permutation-grid
domain to establish that result. Its row/column scan overwrites the coordinates
on equality with `1`, but uniqueness guarantees exactly one such write.

### Trusted regeneration

From the scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

Both MPY files have SHA-256
`c3b09307afd6be7a2e9fb5e23300f303e9899d6d7c3f1a8991dc83074f10112e`;
`cmp` exits 0. Exact command and status are in
[stage2-translation-identity.log](/audit-output/evidence/stage2-translation-identity.log).

### Independent differential

[differential.py](/audit-output/evidence/differential.py) imports the trusted
canonical and candidate entry points independently. It covers both documented
examples, all 24 `N=2` permutations with `k=1..10`, every `1` position in
structured `N=3` grids, odd/even and large `k` values, and deterministic random
permutations for `N=3..8`. It also uses a separately implemented move-enumerating
oracle rather than the alternating-path formula.

The result in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log) is:

- 5,205 valid-domain candidate/canonical comparisons, zero mismatches;
- 384 independent brute-force path comparisons, zero mismatches;
- zero output-length or output-range errors; and
- documented example results `[1,2,1]` and `[1]`.

The script records observations for `N < 2`, nonpositive `k`, and a duplicate
grid. Candidate/canonical differences there do not violate the docstring because
those inputs are expressly outside its preconditions. There is no
canonical/docstring contradiction and no material supplied-model representation
gap in the intended domain.

Result of stage 2: **PASS**.

## 3. Clean proof reconstruction

### Fresh builds and concrete execution

The toolchain is K `v7.1.293` and Python `3.10.12`; see
[toolchain.log](/audit-output/evidence/toolchain.log). Only source files and the
trusted reference semantics were copied to scratch.

I built the concrete definition with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

This exits 0. The warnings concern supplied, unused/non-exhaustive functions;
none is reached by this integer/list program. The exact output is in
[stage3-kompile-llvm.log](/audit-output/evidence/stage3-kompile-llvm.log).
Fresh `krun` executions also exit 0 and end with `.K`, `NoExc`, and exit code 0:

- `[[1,2],[3,4]], k=3` creates result heap list `[1,2,1]` in
  [stage3-krun-odd.log](/audit-output/evidence/stage3-krun-odd.log);
- `[[5,9,3],[4,1,6],[7,8,2]], k=4` creates `[1,4,1,4]` in
  [stage3-krun-even.log](/audit-output/evidence/stage3-krun-even.log).

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exits 0; see
[stage3-kompile-haskell.log](/audit-output/evidence/stage3-kompile-haskell.log).

### Constituent proofs

The exact scan command selects the mutually supporting scan invariants and the
scan cut together:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC \
  --claims SPEC.inner-one-ahead,SPEC.inner-no-one,SPEC.outer-one-ahead,SPEC.outer-one-past,SPEC.scan-finish \
  --depth 240
```

It exits 0 and prints `#Top`; see
[stage3-proof-scan-constituents.log](/audit-output/evidence/stage3-proof-scan-constituents.log).
The selection proves all five reachability claims as a mutually inductive
group under K's guarded circularity mechanism. Diagnostic isolated runs confirm
the dependency: `inner-no-one` closes alone, while `inner-one-ahead` and the two
outer claims need the companion invariant. Those isolated failures are not
claimed as successful proof commands; their logs are retained as dependency
evidence.

The remaining constituents close independently:

| Constituent | Command suffix | Result | Evidence |
|---|---|---:|---|
| `neighbor-finish` | `--claims SPEC.neighbor-finish --depth 400` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-proof-neighbor-finish.log) |
| `result-loop-tail` | `--claims SPEC.result-loop-tail --depth 110` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-proof-result-loop-tail.log) |

`result-loop-tail` emits only `WarnIfLowProductivity` (90%), explicitly a
backend performance warning, before `#Top`.

Thus the seven verified constituent claims are:

1. `inner-one-ahead`;
2. `inner-no-one`;
3. `outer-one-ahead`;
4. `outer-one-past`;
5. `scan-finish`;
6. `neighbor-finish`; and
7. `result-loop-tail`.

None of those successful commands uses `--trusted`.

### Full composed target and registered provision

I reproduced the candidate's recorded full composition exactly, substituting
only the fresh definition name:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC \
  --claims SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail,SPEC.minpath-full-contract \
  --trusted SPEC.scan-finish,SPEC.neighbor-finish,SPEC.result-loop-tail \
  --depth 240
```

It exits 1, does not print `#Top`, and reports `WarnStuckClaimState` plus two
unexplored symbolic-count branches. The state has already returned `ref(0)`
with the correct four-element alternating heap. The failed condition is the
structurally valid equality

```text
snocVS(vCons(1, vCons(M, vCons(1, .ValSeq))), M)
= vCons(1, vCons(M, vCons(1, vCons(M, .ValSeq))))
```

where `M` is the expanded `neighborMin`. This equality follows directly from
the recursive `snocVS` definition, but that general equation is `[concrete]`,
so the frozen symbolic backend neither normalizes this next prefix nor replays
the independently proved generalized result-loop cut. The complete bounded
residual is in
[stage3-proof-full-composed.log](/audit-output/evidence/stage3-proof-full-composed.log).

Under the ordinary decision rule, this missing target `#Top` would be
`FAIL / NOT_LEGIT`. The registered task-specific provision applies only after
the remaining stages show that all constituent content is derived and sound,
the theorem is fully adequate and pinned, and this composition limitation is
the sole defect. Stages 4–7 establish those conditions. The candidate's own
`PROOF.md`, `NOTES.md`, `prove.sh`, generation result, and final generation
message all state the limitation rather than claiming a completed proof.

Result of stage 3: **CONDITIONAL under the registered provision**; all seven
constituents pass, while the one full composition command reproducibly fails
at the frozen backend's cut-replay/term-normalization boundary.

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Precondition and postcondition |
|---|---|
| `inner-one-ahead` | On a valid grid, scan columns `J..N-1` of row `I` when this suffix contains the unique `1`. Finish with `j=N` and set `row,col` to the unique coordinates. |
| `inner-no-one` | Scan the same suffix when it does not contain `1`. Finish with `j=N` and preserve `row,col`. |
| `outer-one-ahead` | Scan rows `I..N-1` when `I` has not passed the row containing `1`. Finish with `i=j=N` and the unique coordinates. |
| `outer-one-past` | Scan after the `1` row has already passed. Finish with `i=j=N` and preserve the previously established coordinates. The `I=N` case requires `j=N`, preventing a false post-state for a loop that performs no iteration. |
| `scan-finish` | From the actual initialized local map (`row=col=i=0`), execute the exact submitted nested loops, preserve the arbitrary following statement tail, and finish with the coordinates and `i=j=N`. |
| `neighbor-finish` | Execute the four actual guarded conditionals in order and change sentinel `N*N+1` to the least in-bounds orthogonal neighbor. Preserve the following statement tail. |
| `result-loop-tail` | From the exact evaluated while-condition state with positive remaining pair count `R`, execute list appends, decrements, loop back-edges, the odd tail, and stop immediately before the actual return. The heap output must satisfy `finishRel`. |
| `minpath-full-contract` | Call the exact `minPath` closure on every represented valid `N>=2` permutation grid and every `K>0`; return fresh reference 0 whose heap sequence satisfies the exact alternating-output relation. |

The inner/outer and neighbor claims frame only cells they do not change. Their
ellipsis admits arbitrary continuations, but the summarized regions contain no
return, exception, break, allocation, or other abrupt control. Their exact
state footprint is the local scope map. `result-loop-tail` instead pins the
complete continuation, call frame, heap location, return state, exception state,
and exit code because it allocates/mutates the result list and approaches a
return.

### Full-domain adequacy

`validPerm(P,N*N)` means length exactly `N*N`, all elements in `1..N*N`, and
pairwise uniqueness. With exactly `N*N` values drawn from a set of size `N*N`,
this is precisely a permutation and necessarily contains one `1`.
`gridRows(P,N)` is the row-major `N` by `N` representation. Conversely, every
docstring-valid Python grid has such a flattened `P`. The extra `oneRow` and
`oneCol` bounds in the target precondition are consequences of `validPerm` and
`N>=2`; they do not narrow the source domain. K integers cover every positive
Python integer `k`, and no size or loop-unrolling bound occurs in the theorem.

For `K>0`, `pyMod(K,2)` is 0 or 1 and the initial `finishRel` counter is
`floor(K/2)`. Its equations force exactly `(1,M)` repeated that many times,
plus a final `1` exactly when `K` is odd. Therefore `?OUT` is not a free result:
the returned `ref(0)`, fresh heap binding, and `finishRel` jointly determine the
unique intended list.

### Mechanical program identity

[constructor_compare.py](/audit-output/evidence/constructor_compare.py) asks
K's own parser to expand all claim macros, then compares the complete submitted
`FuncDef("minPath", Params("grid","k"), ...)` constructor tree with the
closure term used by the claims. Both normalized constructor trees have
SHA-256
`04d681332cee328b08fc0a0f09dcea3888ce3fce5b686c98541f9b7394a5841d`
and compare equal; see
[stage4-constructor-compare.log](/audit-output/evidence/stage4-constructor-compare.log).
This comparison covers the binding, parameters, entire body, and operation
order, not merely an external source filename.

The fixed semantics executes every material construct: closure lookup and
calls, parameter binding and frame restoration, name reads/writes, integer
arithmetic and comparisons, both while loops, all conditionals, nested list
subscripts, empty-list allocation, bound `append` calls with in-place heap
writes, and return. There is no program-level call interception or answer
rewrite.

### Satisfiability and concrete substitution

The common witness `P=[1,2,3,4], N=2, K=3` has `oneRow=0`, `oneCol=0`, and
`neighborMin=2`. Concrete assignments satisfying every auxiliary precondition
are recorded in
[stage4-precondition-witness.log](/audit-output/evidence/stage4-precondition-witness.log):
for example `(I,J)=(0,0)` for `inner-one-ahead`, `(0,1)` for
`inner-no-one`, `I=0` for `outer-one-ahead`, `(I,J)=(1,0)` for
`outer-one-past`, and `R=1,A=[]` for `result-loop-tail`.
The formal output, candidate output, and canonical output are all `[1,2,1]`.

A reviewer-authored ground claim executes the actual closure and requires that
exact heap. It prints `#Top` and exits 0; see
[spec-ground-witness.k](/audit-output/evidence/spec-ground-witness.k) and
[stage4-ground-kproof.log](/audit-output/evidence/stage4-ground-kproof.log).

### Body sensitivity

As a separate operational sensitivity check, I changed the second loop append
inside the claim's executed `minPathBody` from `neighbor` to `99`, rebuilt a
fresh proof definition, and kept the expected `[1,2,1]` post-state. The mutated
constructor hash becomes
`1381440980335292ebaaf2d63c0529f6d4825d804f62789e09952e5dda97dab7`,
different from the submitted program. K executes it to `[1,99,1]` and rejects
the original post-state with `WarnStuckClaimState`. See
[verification-body-mutation.k](/audit-output/evidence/verification-body-mutation.k),
[stage4-body-mutation-constructor.log](/audit-output/evidence/stage4-body-mutation-constructor.log),
and [stage4-body-mutation-proof.log](/audit-output/evidence/stage4-body-mutation-proof.log).

Result of stage 4: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.py](/audit-output/evidence/rule_inventory.py) indexes every
local `requires`, module/import, syntax declaration, configuration, context,
rule, claim, attribute, and source location from the 24 supplied semantics
files, `verification.k`, and `spec.k`. The complete 396 KB inventory is
[stage5-rule-inventory.log](/audit-output/evidence/stage5-rule-inventory.log).
Its exact declaration counts are:

- supplied semantics: 227 syntax declarations, 695 rules, five contexts, and
  one configuration;
- proof-local `verification.k`: 43 syntax declarations and 71 rules;
- `spec.k`: eight reachability claims; and
- across all sources: no `[trusted]` attribute and no `functional` declaration.

The proof-local file has 28 total-function declarations, of which 15 use
`symbol(...), no-evaluators` to remain compact on symbolic inputs; 15 further
syntax declarations are macros. It contains 19 `[simplification]` rules, 16
`[concrete]` equations, no priority rule, and no `<k>` operational rule.

### Proof-local equations and declarations

I reviewed all 71 proof-local rules, grouped below by their complete source
ranges. These groups partition the inventory; none is omitted.

| Lines in `verification.k` | Inventory and soundness conclusion |
|---|---|
| 12–31 | `intMember`, `allInRange`, `uniqueInts`, and `validPerm`: disjoint, structurally decreasing definitions of membership, bounds, uniqueness, and permutation validity. |
| 33–74 | `gridRows*`, `gridRow*`, `pAtTotal`, and `gridAt`: total row-major construction/access. Base and recursive guards cover all integer indices and decrease toward a base. |
| 76–101 | `findOne`, `oneIndex`, `oneRow`, `oneCol`: first-occurrence search and quotient/remainder coordinates. `N>0` and `N<=0` branches are disjoint; all theorem uses have `N>=2`. |
| 105–134 | Five guarded fixed-selector lemmas: row count, row access, cell access, unique-`1` characterization, and cell upper bound. Under `validPerm` and in-bounds indices each is ordinary finite-sequence mathematics. These are the candidate-declared downstream Lean obligations permitted by the task provision. |
| 140–190 | `chooseMin`, four `after*` helpers, three `best*` helpers, and `neighborMin`: disjoint Boolean/minimum equations. `neighborMin` expands to the exact four source conditionals in source order. Out-of-bounds `gridAt` terms occur only in the ignored argument of a false `chooseMin` branch and have no state/control effect. |
| 195–213 | `snocVS` and singleton `valSeqConcat`: exact append. The singleton/two-element simplifications overlap the general concrete recursion but have identical normal forms. |
| 215–267 | `pairDone`, `oddDone`, `finishRel`, and `pathRel`: decreasing recursion on positive `R`; disjoint nonpositive/parity bases. The extra `oddDone(...,snocVS(P,1),...)` equation is append injectivity/induction and agrees with the ordinary recursion on every overlap. |
| 273–409 | Fifteen syntax-macro rules for the exact scan, neighbor, result, and full body constructors. K macro expansion mechanically matches the submitted `FuncDef`; they add no operational behavior. |

The five selector/range lemmas do influence scan branching and the returned
neighbor, so they are not dismissed as inert. Their guards are exactly the
full target's valid-grid and in-bounds facts. There is no broader false case to
which they apply. The derivations are: `gridRows` creates exactly `N` rows;
`gridRow` creates exactly `N` cells; flattening maps `(I,J)` to `I*N+J`;
permutation uniqueness makes `gridAt==1` equivalent to the quotient/remainder
coordinates of the sole `1`; and the range predicate gives every cell
`<=N*N`, hence `<N*N+1`.

[extension_checks.py](/audit-output/evidence/extension_checks.py) supplies
finite corroboration, not a universal substitute: all 24 `N=2` permutations
and 1,200 deterministic `N=3..8` permutations produced zero failures across
39,896 selector checks, 1,224 neighbor summaries, 36 append-overlap checks,
288 finish-relation checks, and 432 odd/pair bridge checks. See
[stage5-extension-checks.log](/audit-output/evidence/stage5-extension-checks.log).

### Used fixed-semantics rule map

The supplied semantics is the fixed trust boundary, but I also mapped every
construct the submitted body uses to its concrete rules:

| Program construct | Fixed declarations/rules and audited effect |
|---|---|
| Module/function binding | `syntax.k` `Module`/`FuncDef`; `core.k` load/sequencing; `functions.k` binds the exact closure. |
| Call and binding | `call.k` evaluates the callee then arguments left-to-right, selects the actual closure value, pushes a frame, and `functions.k` binds `grid,k`; no name-based shortcut exists. |
| Literals/names/assignments | `core.k` integer literals and scope-chain lookup; `controls.k` strict RHS assignment to the current plain scope. Cell-write priority rules are refuted because this frame has no `$cells`. |
| Integer operations | `operators.k` dispatch plus `int.k` exact `+`, `-`, `*`, `//`, `%`, equality, and order rules. Divisors are fixed positive `2`, so no zero-divisor gap is reachable. |
| While/if/control | `controls.k` `While -> #while`, condition evaluation, guarded body/back-edge, and truth-valued branch rules. There is no break, exception, or return inside summarized scan/neighbor regions. |
| Nested subscript | `subscript.k` evaluates base before index and uses `valSeqAt`; the proof guards establish every access in bounds. The fixed total function's unspecified out-of-bounds cases cannot influence this domain. |
| Empty list and append | `list.k` allocates `ListExpr`, call routing preserves the mutating receiver reference, and the priority-40 append rule updates exactly that heap entry via `valSeqConcat`. |
| Return | `functions.k` stores the returned reference, pops/restores the exact frame and environment, preserves escaped heap allocation, and leaves no exception. |

Configuration and allocation are pinned: initial heap and stack are empty,
`scopeLoc=1`, the call allocates frame 1, the result list allocates fresh heap
location 0, `heapLoc` advances to 1, and return restores environment 0 while
keeping the list. Claims that do not mention a cell frame it unchanged.

The supplied tree contains unrelated opaque float, sorting, string-order, and
MD5 primitives. None is reachable from this program or any postcondition, so
none can select a branch, fabricate this result, or close these claims. The
only reachable fixed total abstraction that might otherwise be concerning is
`valSeqAt`; every use is covered by the true guarded selector lemmas above.

### Reachability claims as extensions

The inner/outer claims are guarded loop invariants, not operational rewrite
rules. Their matched continuation and framed-cell domains are sound because
the scan body has only scope updates and normal fall-through. `scan-finish` and
`neighbor-finish` preserve arbitrary statement tails, but both execute regions
that cannot discard or unwind those tails. `result-loop-tail` uses a fixed
continuation, stack frame, heap object, return state, exception state, and exit
code; it does not justify an arbitrary return context. The full claim starts
from the actual closure binding and body.

No rule replaces a program-defined computation with a summary, introduces an
answer-bearing oracle, changes evaluation order, fabricates state, or preempts
fixed operational semantics. The CLI `--trusted` in the failed full composition
names only three constituents first proved without trust; it is not source
`[trusted]` content and does not produce a successful target proof.

I found no unsound rule, so there is no false-conclusion witness to report.
The only evidence gap is the absence of separately submitted Lean derivations
for the five guarded selector/range lemmas; the registered provision expressly
permits exactly these candidate-declared downstream functional obligations,
and the static derivations above establish that they are dischargeable.

Result of stage 5: **PASS** for soundness; no operational bridge, trusted
content, or false rule was found.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation. The fresh
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) uses the satisfying
`P=[1,2,3,4], N=2, K=3` state and changes only the result-bearing heap obligation
from the true `[1,2,1]` to the false `[1,3,1]`.

The parser/backend command

```text
kprove spec-vacuity.k --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exits 0, proving the mutation is well formed; see
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).
The actual proof command, with `--depth 1000`, exits 1 with
`WarnStuckClaimState`. Its terminal state is normal return `ref(0)` with heap
`[1,2,1]`, which fails to unify with the deliberately required `[1,3,1]`.
There is no parser failure, timeout, unrelated crash, or unreachable mutation.
See [stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).

Result of stage 6: **PASS**.

## 7. Proven versus assumed accounting

### What the machine-checked constituents establish

Conditional on the fixed semantics and the sound proof-local functional
equations, K machine-checks all of the following for arbitrary `N>=2`, every
row-major permutation `P` of `1..N*N`, and every positive `K`:

- the nested scan finds the unique coordinates of `1`;
- the four source conditionals compute the least orthogonal neighbor `M`;
- the result loop and odd tail build the exact alternating relation for an
  arbitrary positive remaining pair count; and
- on concrete instances, the exact submitted closure returns the constrained
  heap list.

The seven general constituent claims are machine checked with `#Top`. The
single top-level composition from the function call to that relation is not
machine checked as one `#Top`; its residual is confined to cut replay and a
true `snocVS` normalization equality after correct execution.

### Trust ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| Fixed supplied MPY semantics and K built-in Int/Bool/Map/List/String theories | Binding, order, control, heap, calls, return, arithmetic | Every claim | Required supplied-model trust boundary; recursively integrity-checked. Used-rule map above and fresh concrete execution support it. |
| K `kompile`/Haskell reachability backend | Claim compilation and closure | Every `#Top` | Standard machine-checking boundary, version pinned in `toolchain.log`. The known composition limitation is explicitly retained, not treated as success. |
| Trusted `py2mpy.py` translation | Source-to-MPY bridge | Program identity | Byte-identical trusted regeneration plus constructor-level K comparison. Differential evidence is finite support, not proof. |
| Five guarded selector/range simplifications at `verification.k:105–134` | Length, subscript results, unique-1 branch, cell upper bound | Scan and neighbor constituents, hence target | Candidate-declared downstream Lean obligations permitted by the registered provision. True on the complete guarded domain by finite-sequence/permutation mathematics; 39,896 finite checks add corroboration. |
| Symbolic `validPerm`, `gridRows*`, `gridAt`, `one*`, `neighborMin`, `snocVS`, `pairDone`, `oddDone`, `finishRel`, `pathRel` | Input representation and exact result relation | Claims/postcondition | Not unconstrained oracles: each has terminating/disjoint equations or guarded exact lemmas inventoried above. No operational term rewrites to them. |
| Alternating-sequence to lexicographic-minimum argument | Human-facing intent | Gate B | Ordinary mathematical induction from unique global minimum `1`, least neighbor `M`, and the edge back to `1`. The K postcondition fixes the sequence; it does not merely name “minimum path.” |
| Differential and brute-force scripts | CPython fidelity on tested inputs | Validation only | 5,205 canonical and 384 independent brute-force cases with zero mismatch. Explicitly finite; not substituted for the K proof. |
| Partial-correctness scope | Termination is not the reachability theorem's stated guarantee | Final interpretation | Acceptable for the requested partial-correctness audit. On valid finite inputs both scans and pair counter have obvious decreasing finite bounds, and all tested executions terminate. |

Unrelated supplied opaque primitives (`sortVS`, keyed sort, float operations,
string order, `md5hexCodes`) have no path to the program, control decisions,
heap output, or postcondition and therefore add no task-specific assumption.
There is no external I/O, mutation of the input grid, exception behavior, or
numeric-representation gap on the intended integer domain.

### Gate and decision summary

- Soundness/Gate A content: **PASS** for every constituent and every
  proof-local rule; non-vacuity and body sensitivity pass. The ordinary single
  composed target command remains unclosed.
- Adequacy/Gate B: **PASS**. The target domain is the full unrestricted
  docstring domain, redundant coordinate bounds do not narrow it, and the
  output relation is the unique lexicographic minimum.
- Auditability/Gate C: **PASS**. Exact source mutations, commands, statuses,
  outputs, hashes, inventories, and finite-test scopes are preserved below
  `/audit-output/evidence`.

The registered provision therefore applies. The explicit **CONDITIONAL**
annotation is: the frozen K 7.1.293 Haskell backend fails only to consume the
proved `result-loop-tail` cut / normalize the next symbolic `snocVS` prefix in
`SPEC.minpath-full-contract`; the verified constituents are
`inner-one-ahead`, `inner-no-one`, `outer-one-ahead`, `outer-one-past`,
`scan-finish`, `neighbor-finish`, and `result-loop-tail`. No unsoundness or
unproved reachability constituent was found.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
