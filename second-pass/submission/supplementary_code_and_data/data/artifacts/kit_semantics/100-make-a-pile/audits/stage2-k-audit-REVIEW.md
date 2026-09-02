# Independent adversarial audit: HumanEval/100 `make_a_pile`

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program over the full source-contract domain of
positive integers. I reconstructed the definitions from source, proved the
claims without candidate caches, mechanically pinned the entry claim to the
translated program, reviewed every local K item, and rejected fresh false
result and changed-body mutations for the expected semantic reasons.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem
`100-make-a-pile`, and condition `kit-semantics`.
`/reference/reference-semantics` is present, as this mode requires.

The read-only checker
[`evidence/provenance_check.py`](evidence/provenance_check.py) inspected the
launcher records, mounted file types, hashes, recursive trees, and all 386
structured trace records. Its exact command and results are in
[`evidence/stage1-provenance.log`](evidence/stage1-provenance.log).
It established:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files. The campaign object in the former equals the latter exactly, and the
  lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  as recorded.
- Every `pipeline-v3` record required by the prompt is a regular file:
  `/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
  runtime metrics, usage, last message, output log, generation prompt, and the
  structured trace. All launcher-declared per-file hashes match.
- The independently recomputed pipeline content-tree hashes match the
  generation records: candidate
  `fb740952960c2e23b6dbe3395a5b503ceef905b9445f1944a5dcd7185d97c60b`,
  reference semantics
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  and trace
  `df6f158f3fe5b2cf849c3faa98e339427413c9f6f6f435e91bbf9e42138491af`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Candidate `reference-semantics/` and trusted
  `/reference/reference-semantics/` have identical names, types, modes, and
  contents for all 25 entries. Neither contains a symlink, extra entry,
  missing entry, or changed entry.
- The candidate tree contains only directories and regular files. All six
  required proof artifacts are present, regular, and nonempty.

I read the generation records only as claims. They report a prior `#Top` and
`VALIDATED`, but neither is used below. There is no provenance or
semantics-mode infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires, for every positive integer `n`, a list describing
`n` levels. The first level is `n`; each next level is the next integer with
the same parity. Equivalently, the result is
`[n + 2*i for i in range(n)]`.
The trusted canonical implementation states exactly that comprehension.

Candidate `solution.py` initializes an empty list and `i = 0`, repeatedly
appends `n + 2*i` while `i < n`, increments `i`, and returns the list. Thus it
uses a different control structure but the same mathematical algorithm.

I copied only source artifacts to `/tmp/audit-work/reconstruction`, ran the
trusted translator there, and compared its output with the submitted
`solution.mpy`. The files are byte-identical and have SHA-256
`b0140b14af8003350564627569171a07a199c5ffe5ecbb851a2948e97ec0f426`;
see
[`evidence/stage2-source-copy-and-translation.log`](evidence/stage2-source-copy-and-translation.log).

The independent differential harness
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and candidate implementations from the scratch copy. It
tested:

- the documented `n = 3` example;
- the out-of-contract empty-result boundary `n = 0` and negative probes;
- the loop boundary `n = 1`;
- both parity classes at `n = 2, 3, 4, 5`;
- larger boundaries `10`, `100`, and `1000`; and
- 1,000 seeded values in `1..10000`.

All 1,012 comparisons matched. The script, complete input-generation rule,
samples, exact command, and exit 0 are preserved in
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).
The finite differential evidence supports fidelity; it is not used as the
universal proof.

## 3. Clean proof reconstruction

I did not use `/candidate/runtime-kompiled`,
`/candidate/verification-kompiled`, candidate caches, or candidate proof logs.
The scratch setup test confirmed that neither output definition existed before
the builds. The clean reconstruction commands are preserved in
[`evidence/clean_reconstruction.sh`](evidence/clean_reconstruction.sh) and
[`evidence/stage3-clean-reconstruction.log`](evidence/stage3-clean-reconstruction.log).

The installed tools report K and `kprove` v7.1.293. From the source-only
scratch tree I ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. An independently authored K smoke program checked `n = 0, 1, 2,
3, 5`; `krun` exited 0 with `.K`, `NoExc`, exit code 0, and heaps containing
`[]`, `[1]`, `[2,4]`, `[3,5,7]`, and `[5,7,9,11,13]`. See
[`evidence/k_smoke.py`](evidence/k_smoke.py),
[`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log), and
[`evidence/stage3-krun-smoke.log`](evidence/stage3-krun-smoke.log).

I then ran:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; output is in
[`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log).
The positive proofs were:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.pile-loop
```

This independently proved the loop claim and printed exact `#Top` with exit 0.
The complete submitted spec was then run with:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It proved both claims, printed exact `#Top`, and exited 0. Finally, I checked
the modular dependency by selecting both claims and marking only the already
proved loop claim trusted:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  --claims SPEC.pile-loop,SPEC.make-a-pile \
  --trusted SPEC.pile-loop
```

The entry proof again printed exact `#Top` and exited 0. Evidence is in
[`evidence/stage3-kprove-pile-loop.log`](evidence/stage3-kprove-pile-loop.log),
[`evidence/stage3-kprove-all.log`](evidence/stage3-kprove-all.log), and
[`evidence/stage3-kprove-make-a-pile-modular.log`](evidence/stage3-kprove-make-a-pile-modular.log).

An entry-only `--claims SPEC.make-a-pile` diagnostic was interrupted after it
excluded the loop circularity and began symbolic unrolling; it is visible at
the end of the reconstruction transcript. It is not a target-proof failure:
the unfiltered submitted proof and the sound modular sequence above both close.

Compiler warnings concern unused variables and incomplete off-path helpers in
the fixed supplied semantics. None names a constructor, function, or
obligation reached by this program. There was no parse failure, backend
failure, timeout, or infrastructure uncertainty in a required command.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.pile-loop` starts at the exact internal `#while` head for the submitted
condition and body. Its precondition says:

- `N >= 0`;
- `0 <= I <= N`;
- the current frame binds `n = N`, `i = I`, and `pile = ref(H)`; and
- heap object `H` initially contains arbitrary sequence `A`.

It consumes the loop, changes `i` to `N`, and changes that heap object to
`finishPile(A,N,I)`. The continuation and unrelated configuration entries are
framed and preserved.

`SPEC.make-a-pile` starts from the standard empty module configuration, loads
one `make_a_pile` binding with the complete function body, calls it with
symbolic integer `N`, and requires `N > 0`. It returns `ref(0)`. Heap object 0
is constrained to `list(finishPile(.ValSeq,N,0))`; heap allocation advances
once; the module closure remains; the callee frame is removed; the stack and
return state are clean; no exception is present; and exit code is 0.

The result is not a free variable, tautology, or one-way implication.
`finishPile` is defined by two exhaustive equations:

```text
finishPile(A,N,I) = A                                  when I >= N
finishPile(A,N,I) =
  finishPile(A ++ [N + 2*I], N, I+1)                  when I < N
```

The guards are disjoint and cover all integer pairs. In the recursive case
`N-I` is a positive integer and decreases by one. The definition therefore
terminates and states precisely the required list contents.

### Mechanical program identity

[`evidence/extract_claim_program.py`](evidence/extract_claim_program.py)
extracts the balanced `Module(FuncDef(...))` term from the first `#loadAll` in
the entry claim. It normalizes only `ListExpr(.Exprs)` to the concrete parser's
equivalent empty-list spelling `ListExpr()`. Both the extracted term and
submitted `solution.mpy` were parsed by `kast` as sort `Module` and emitted as
KORE. `cmp` found byte identity; both KORE files have SHA-256
`0ec9525608acd47e9e991685ccbd900e92da037ceb4645283e5ff41098bf4aea`.
See
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).
The initial failed comparison, which exposed the concrete/internal list-unit
spelling difference, is retained in
[`evidence/stage4-program-pinning-initial.log`](evidence/stage4-program-pinning-initial.log).

Ground satisfying witnesses `N = 1, 2, 3, 5` meet `N > 0`.
For each, the claimed `finishPile` result equals both Python implementations;
the exact results are in the same pinning log and generated by
[`evidence/claim_witness.py`](evidence/claim_witness.py).

### Control-flow and body sensitivity

The helper claim starts at the real `#while` control point produced by the
fixed `While` rule and contains the exact comparison, `append`, arithmetic,
and increment body. The entry claim executes definition binding, lookup,
argument binding, list allocation, every loop operation, return, and frame
cleanup. No ordinary proof rule skips any operation.

For an independent body-sensitivity test, I changed the executed body term
from `n + 2*i` to `n + 4*i` at `n = 2` while retaining the original `[2,4]`
postcondition. The mutation dry-run compiled successfully. Its proof exited 1
with `WarnStuckClaimState` and the concrete residual heap `[2,6]`. This proves
that changing the actual term executed by the claim changes the obligation;
see
[`evidence/body-sensitivity-mutation.k`](evidence/body-sensitivity-mutation.k)
and
[`evidence/stage4-body-sensitivity.log`](evidence/stage4-body-sensitivity.log).

The entry domain `N > 0` exactly matches the prompt's unrestricted
positive-integer domain. There is no finite-size restriction or bounded
unrolling.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md), generated by
[`evidence/rule_inventory.py`](evidence/rule_inventory.py). It line-anchors,
hashes, classifies, and assigns a disposition to every local item in trusted
`semantics.k`, all `semantics/*.k` helpers, candidate `verification.k`, and
positive `spec.k`:

- 933 total items;
- 228 syntax declarations;
- 697 ordinary rules;
- five contexts;
- one configuration; and
- two claims.

Attribute counts are 146 `function`, 108 `total`, 25 `symbol`, 22
`no-evaluators`, 45 priority, 35 concrete, 26 `owise`, two strict, one
`seqstrict`, four macro, and one recursive macro. There are no local
`functional` declarations and no simplification rules. Exact inventory
generation command, count, hash, and status are in
[`evidence/stage5-inventory-command.log`](evidence/stage5-inventory-command.log).

Every off-path row is constructor-, sort-, guard-, or exact-state-disjoint
from the submitted execution. Its operational truth is therefore immaterial
to this theorem, but it was still checked for proof-answer smuggling, overlap
with used symbols, and result-bearing influence. No off-path item can affect
this claim's computation or postcondition.

The complete used-path mapping is:

| Program construct | Fixed declarations and rules reviewed | Effect |
|---|---|---|
| Module and statement sequence | `syntax.k`; `core.k` `#loadAll` and `Stmts` rules | Loads and executes statements in order |
| Function binding and call | `functions.k` `FuncDef`, parameter binding, return/pop; `call.k` callee/argument and closure rules | Selects the loaded binding, creates/restores the callee frame, and preserves return control |
| Assignment and literals | strict statement syntax; `controls.k` plain assignment; `core.k` integer literal | Evaluates RHS first and updates the current plain scope |
| Empty list allocation | `list.k` `ListExpr`/`toList`; `core.k` argument fold and `#alloc` | Allocates fresh heap object 0 and returns `ref(0)` |
| Loop | `controls.k` `While`, `#while`, `#whileCond`, `#loopLbl`; `core.k` `truthy(Int)` | Re-evaluates `i < n`, runs the body only when true, and returns to the exact loop head |
| Arithmetic and comparison | `operators.k` contexts/dispatch; `int.k` integer `<`, `+`, `*` | Left-to-right evaluation and ordinary unbounded-integer operations |
| `pile.append` | `call.k` `Attribute`, bound-method routing, `isMutMethod`; `list.k` priority-40 append rule and `valSeqConcat` | Preserves the heap reference and appends exactly one evaluated integer in place |
| `i += 1` | strict `AugAssign`; `controls.k` plain integer update | Updates only local `i` to `i+1` |
| Result summary | `verification.k` `finishPile` declaration and two equations | Pure mathematical sequence summary; matches no cell and replaces no execution |
| Auxiliary theorem | `SPEC.pile-loop` | Machine-checked circularity over the real recurring control state |

Evaluation order is faithful: `BinOp` is `seqstrict(2,3)`, statement RHSs and
`Attribute` receivers are strict, comparison contexts evaluate left then
right, and the call layer evaluates the callee followed by arguments from
left to right. The loop reads `n`, `i`, and `pile`; append writes only heap
object `H`; increment writes only `i`; list allocation advances `heapLoc`;
call/return push and pop the stack and callee scope. The entry postcondition
pins all of those material effects.

Relevant priority overlaps are safe. Cell-assignment and cell-parameter rules
require a `"$cells"` marker absent from this plain function. The ref-valued
`AugAssign` route is inapplicable because `i` is an integer. The append
priority rule exactly handles the mutating receiver and preempts the generic
pure-method route; `isMutMethod("append")` prevents receiver dereference and
preserves identity. All other priority rules are off-path.

The 25 opaque supplied symbols are exactly enumerated in
[`evidence/stage5-special-attributes.log`](evidence/stage5-special-attributes.log):
22 float operations plus `sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs
in the program, claims, `finishPile`, or reachable residuals. The proof has no
proof-local opaque term. Compiler non-exhaustiveness warnings similarly name
off-path helpers only.

No inventoried rule encodes this task's answer, fabricates a used result,
introduces an unconstrained oracle on the path, or bypasses real execution.
I found no unsound rule contributing to either claim, so there is no
unsoundness allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
[`evidence/fresh-false-mutation.k`](evidence/fresh-false-mutation.k) executes
the exact submitted function at the satisfying input `N = 1` but demands heap
list `[2]` instead of `[1]`.

The independent commands were:

```text
kprove fresh-false-mutation.k --definition verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE --dry-run --output none

kprove fresh-false-mutation.k --definition verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE
```

The dry-run exited 0, proving that the mutation parses and builds. The proof
exited 1 with `WarnStuckClaimState`; its residual has `ref(0)` and heap
`0 |-> list(vCons(1,.ValSeq))`, while the destination demands `[2]`. The
failure is the intended unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. Exact commands, statuses, and residual
are in
[`evidence/stage6-fresh-nonvacuity.log`](evidence/stage6-fresh-nonvacuity.log).

## 7. Proven versus assumed accounting

The successful reachability proof establishes the following under the fixed
supplied K semantics:

> For every K integer `N > 0`, starting from the standard fresh module
> configuration, loading the exact submitted `make_a_pile` function and
> calling it with `N` reaches a clean final configuration returning `ref(0)`.
> That reference denotes a freshly allocated list whose sequence is
> `finishPile(.ValSeq,N,0)`, i.e. exactly
> `[N, N+2, ..., N+2*(N-1)]`. No exception is present and exit code is 0.

The accounting is:

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Trusted supplied `reference-semantics/` | Defines all modeled execution, state, control, and arithmetic for both claims | Acceptable by the rendered `SUPPLIED_SEMANTICS` condition; candidate copy is exactly the trusted tree and every used rule was statically reviewed |
| K builtin `INT`, `BOOL`, `MAP`, `LIST`, equality, strictness generation | Implements mathematical integers, collections, matching, and generated heat/cool rules | Standard low-level semantics/toolchain boundary; used operations are ordinary mathematics and were concretely exercised |
| K v7.1.293 compiler and Haskell prover | Compiles the theory and validates reachability closure | Necessary proof-engine trust; fresh build, exact `#Top`, exit statuses, and meaningful rejected mutations provide reproducible evidence |
| Trusted `py2mpy.py` | Connects candidate Python AST to submitted `.mpy` constructors | Acceptable trusted input; fresh translation is byte-identical and the claim term is parser-level KORE-identical |
| `finishPile` equations | Names the final program-derived list and appears in both claims | Not an opaque assumption or bridge: exhaustive, disjoint, terminating equations directly mirror one fixed-semantics loop iteration |
| `SPEC.pile-loop` | Supplies the circularity used by the entry proof | Proven separately with `#Top`; not assumed in the final unfiltered proof |
| 25 supplied opaque symbols | Float, sorting, and MD5 facilities | No dependent claim or reachable term; inert for this theorem |
| Trusted prompt and canonical Python | State source intent and provide an independent executable oracle | Used for adequacy and finite differential evidence, not to close K claims |
| CPython differential and LLVM smoke tests | Empirical source/model bridge over recorded ground inputs | Finite support only; explicitly not a substitute for the universal K proof |

The remaining informal interpretation is that successive values `N + 2*i`
are the prompt's successive odd numbers when `N` is odd and successive even
numbers when `N` is even. This follows directly because adding two preserves
parity and advances to the next integer of that parity; it is not an empirical
or opaque correctness oracle.

Gate A passes: real execution is pinned, proof extensions are sound, the
result is constrained, body sensitivity holds, and the fresh false result is
rejected. Gate B passes: `N > 0` is the complete source domain and the
postcondition is the requested sequence. Gate C passes: commands, sources,
input scope, outputs, hashes, and trust boundaries are reproducible and
preserved.

VERDICT: PASS
LEGITIMACY: LEGIT
