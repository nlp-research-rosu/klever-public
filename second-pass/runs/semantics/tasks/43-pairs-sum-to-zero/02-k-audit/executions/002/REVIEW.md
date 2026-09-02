# Independent adversarial review: 43-pairs-sum-to-zero

## Executive finding

The candidate's positive K commands are reproducible, its Python implementation is
extensionally correct on the tested intended domain, and the entry claims execute the
submitted function body. Those facts do not make the proof legitimate.

The arbitrary-list theorem imports a priority-40 operational bridge at
`/candidate/verification.k:115`:

```k
rule <k> #applyK(toList, .Vals)
      => #alloc(list(intValues(.IntSeq))) ... </k>
  [priority(40)]
```

This is not equivalent to the supplied list-literal rule. The supplied semantics
allocates `list(.ValSeq)`, whose truthiness is false. The bridge allocates
`list(intValues(.IntSeq))`; the supplied `truthy(list(VS))` equation tests whether
`VS ==K .ValSeq`, so this new representation is truthy. I established all of the
following with fresh artifacts:

- CPython and the bridge-free K definition accept an assertion that `if []` takes
  the false branch.
- The lemma definition reaches `AssertionError` and exit code 1 for the same
  translated program.
- The bridge-free definition proves the correct result `false` with `#Top`.
- The lemma definition proves the Python-false result `true` with `#Top`.

The witness is in
[`empty-list-bridge-witness.py`](evidence/empty-list-bridge-witness.py) and
[`empty-list-bridge-claims.k`](evidence/empty-list-bridge-claims.k). The bounded
execution logs are
[`stage5-empty-bridge-base-krun.log`](evidence/stage5-empty-bridge-base-krun.log),
[`stage5-empty-bridge-lemmas-krun.log`](evidence/stage5-empty-bridge-lemmas-krun.log),
[`stage5-empty-bridge-base-claim.log`](evidence/stage5-empty-bridge-base-claim.log),
and
[`stage5-empty-bridge-false-claim.log`](evidence/stage5-empty-bridge-false-claim.log).
Thus the main proof relies on a materially unsound proof rule that can prove a
concrete false conclusion.

There is also a real-input-domain gap: the universal claim ranges over the new
term `list(intValues(INPUT))`, not the supplied semantics' concrete
`.ValSeq`/`vCons` list representation. No bridge-free universal connection theorem
relates whole-function execution on those two representations. The only entry
claims over actual `vCons` lists cover lengths zero, one, and two. Under the
benchmark's decision rule, that cannot prove the unrestricted list domain.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `43-pairs-sum-to-zero`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and the required legacy-selected-stage1
records:

- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the complete structured trace under `/generation-evidence/codex-trace/`

`runtime-metrics.json` is absent. This is not an integrity defect for
`legacy-selected-stage1`; the prompt expressly says not to reconstruct historical
runtime metrics that were never recorded.

The audit campaign object equals `/audit-campaign-lock.json` exactly, and the
lock's actual SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-declared container path is present, readable, and nonsymlinked.
All recorded single-file SHA-256 values match the mounted bytes. The one trace
file matches the path/hash map in `/generation-result.json`; all 702 JSONL
records parse, with zero parse failures. See
[`stage1-provenance.log`](evidence/stage1-provenance.log) and
[`stage1-generation-record-inspection.log`](evidence/stage1-generation-record-inspection.log).

The generation log and trace were treated only as untrusted history. They claim
that the candidate's `prove.sh` completed and eventually show positive `#Top`
outputs, but none of those results was reused.

### Supplied-semantics boundary

The trusted `/reference/reference-semantics` mount is present, as required in
`SUPPLIED_SEMANTICS` mode. Recursive, no-dereference comparison against
`/candidate/reference-semantics` exits 0. The two trees have identical entry
types and bytes, and neither contains symlinks or special entries. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to the trusted prompt and
translator. Evidence:

- [`stage1-supplied-semantics-diff.log`](evidence/stage1-supplied-semantics-diff.log)
- [`stage1-prompt-diff.log`](evidence/stage1-prompt-diff.log)
- [`stage1-translator-diff.log`](evidence/stage1-translator-diff.log)

All required candidate proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`) are present. There is no
infrastructure breach, so a candidate verdict is appropriate.

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For every finite Python list of integers, `pairs_sum_to_zero(l)` must return a
Boolean that is true exactly when there are distinct indices `i != j` whose
values sum to zero. One zero is insufficient; two zeros form a valid pair. The
trusted canonical implementation enumerates each pair with `i < j`.

The submitted implementation keeps the already visited prefix in `seen`. Before
appending each current value, it returns true exactly when the current value's
negation is in that prefix. This is a different but valid algorithm. It does not
mutate the input.

### Trusted regeneration

Running the trusted translator on the scratch copy of `solution.py` produced a
363-byte `solution.mpy` with SHA-256
`e301c4a2be59c74f263a77fad0f37b88cdf0a27f9e94341fff3e1285afe13475`.
It is byte-identical to the submitted `solution.mpy`. See
[`stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical and submitted functions and also checks a direct
two-index mathematical oracle. Its deterministic scope was:

- all five documented examples;
- empty, singleton, zero, duplicate, early-match, late-match, and large-integer
  boundary cases;
- every list of lengths 0 through 6 over `{-3,-2,-1,0,1,2,3}`: 137,257 cases;
- 5,000 seed-fixed random lists of lengths 0 through 30, including deliberately
  injected pairs.

All 142,278 cases agreed, with zero mismatches. See
[`stage2-differential.log`](evidence/stage2-differential.log).

Differential testing is finite evidence of implementation fidelity, not a
substitute for the K theorem.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`, used the trusted translator
and trusted supplied-semantics tree, and did not copy or use any candidate-built
definition or cache. K reports version 7.1.293; tool evidence is in
[`stage3-tool-versions.log`](evidence/stage3-tool-versions.log).

### Concrete definition

The LLVM definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. Warnings concern non-exhaustive functions in supplied, unused
constructs such as floats, `map(str, ...)`, joins, and out-of-bounds subscripting;
none is on this integer-list program's execution path. The reviewer-authored
concrete program tests empty, singleton, zero-pair, early/late pair, and no-pair
cases. `krun` reached `.K`, `NoExc`, and exit code 0. Evidence:

- [`concrete_semantics_tests.py`](evidence/concrete_semantics_tests.py)
- [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`stage3-krun-concrete.log`](evidence/stage3-krun-concrete.log)

### Proof definitions and positive claims

Both Haskell definitions were rebuilt from source:

- base `PAIRS-VERIFICATION`:
  [`stage3-kompile-base.log`](evidence/stage3-kompile-base.log);
- promoted-lemma `PAIRS-VERIFICATION-LEMMAS`:
  [`stage3-kompile-lemmas.log`](evidence/stage3-kompile-lemmas.log).

Every positive claim was rerun. Each command exited 0 and printed `#Top`:

| Claim | Definition / proof mode | Evidence |
|---|---|---|
| `bounded-empty` | base, direct symbolic execution | [`stage3-kprove-bounded-empty.log`](evidence/stage3-kprove-bounded-empty.log) |
| `bounded-one` | base, direct symbolic execution | [`stage3-kprove-bounded-one.log`](evidence/stage3-kprove-bounded-one.log) |
| `bounded-two` | base, direct symbolic execution | [`stage3-kprove-bounded-two.log`](evidence/stage3-kprove-bounded-two.log) |
| `membership-summary` | base, independently proved | [`stage3-kprove-membership.log`](evidence/stage3-kprove-membership.log) |
| `loop-summary` | base, using the separately proved membership claim as a trusted modular lemma | [`stage3-kprove-loop.log`](evidence/stage3-kprove-loop.log) |
| `all-integer-lists` | promoted-lemma definition | [`stage3-kprove-main.log`](evidence/stage3-kprove-main.log) |

This establishes verification under the candidate-extended theory. It does not
validate that theory.

**Stage 3 result: PASS as reconstruction; no soundness conclusion follows yet.**

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

- `bounded-empty` starts a direct call to the submitted closure on an actual
  `list(.ValSeq)`, requires the standard initial cells, and says it returns
  `false`; it also constrains the allocated `seen` object.
- `bounded-one` and `bounded-two` do the same for actual one- and two-element
  integer `vCons` lists. Their result is the recursively defined `pairsSpec`,
  and their final heap is constrained by `seenAfter`.
- `membership-summary` says the supplied membership machine over the new
  `intValues(INPUT)` representation returns `memberIS(V, INPUT)` while preserving
  any continuation. The membership machine touches only `<k>`.
- `loop-summary` says that, from the precise function-frame loop head,
  processing suffix `REM` with prefix `SEEN` returns `scanIS(REM, SEEN)`, removes
  the local frame, restores environment/scope location, and leaves exactly the
  processed-prefix heap specified by `seenAfterIS`.
- `all-integer-lists` starts the submitted closure on
  `list(intValues(INPUT))` for arbitrary `INPUT:IntSeq` and requires the return
  to be exactly `pairsIS(INPUT)`, with all principal cells and the final heap
  constrained.

These are result-bearing equalities, not one-way implications or free-result
postconditions.

### Program term identity

The trusted regeneration produced the sole function binding
`FuncDef("pairs_sum_to_zero", Params("l"), BODY)`. The supplied `FuncDef` rule
binds exactly `closureVal(("l", .ParamNames), BODY, 0)` in the initial module
environment. Every entry claim calls
`closureVal(("l", .ParamNames), pairsBody, 0)`.

[`constructor_compare.py`](evidence/constructor_compare.py) asks the trusted
compiled parser for both complete constructor trees: the regenerated module and
the same module with the `pairsBody` equation's RHS. Their KAST SHA-256 values
are both
`487aba2ea6a104bce44bc91b3a81f3b07281a8c2c4f71cdf3d8b91d27d2a7242`;
the trees compare equal. A K claim checking the alias normalization also prints
`#Top`; see
[`stage4-constructor-compare.log`](evidence/stage4-constructor-compare.log) and
[`stage4-body-pinning-proof.log`](evidence/stage4-body-pinning-proof.log).
Thus the executed closure body is the real submitted body. Bypassing the
top-level name lookup does not substitute a different body or binding.

### Satisfying states and ground substitutions

The standard initial configuration with empty module scope, builtins at `-1`,
scope location 1, empty heap, empty stack, `noRet`, `NoExc`, and exit code 0
satisfies each entry precondition. For the loop claim, choose for example
`REM=.IntSeq`, `SEEN=.IntSeq`, heap location `H=0`, `NEXT=1`, and the exact local
scope/frame shown in the claim.

Fresh K reductions and both Python implementations agree on these concrete
substitutions:

| Formal `INPUT` | Python list | Claimed/Python result |
|---|---|---|
| `.IntSeq` | `[]` | `false` |
| `iCons(0,.IntSeq)` | `[0]` | `false` |
| `iCons(5,iCons(-5,.IntSeq))` | `[5,-5]` | `true` |
| `iCons(2,iCons(4,iCons(-5,iCons(3,iCons(5,iCons(7,.IntSeq))))))` | `[2,4,-5,3,5,7]` | `true` |
| `iCons(1,iCons(2,iCons(3,.IntSeq)))` | `[1,2,3]` | `false` |

See [`stage4-witness-k.log`](evidence/stage4-witness-k.log) and
[`stage4-witness-python.log`](evidence/stage4-witness-python.log).

### Body sensitivity

I changed the actual `pairsBody` terminal return from `false` to `true`, rebuilt
the lemma definition successfully, and reran the universal theorem. The prover
exited 1 with `WarnStuckClaimState`; the residual fixes
`INPUT = .IntSeq` and contains the incorrect returned `true`. Evidence:

- [`body-sensitivity-verification.k`](evidence/body-sensitivity-verification.k)
- [`stage4-body-sensitivity-diff.log`](evidence/stage4-body-sensitivity-diff.log)
- [`stage4-body-sensitivity-kompile.log`](evidence/stage4-body-sensitivity-kompile.log)
- [`stage4-body-sensitivity-kprove.log`](evidence/stage4-body-sensitivity-kprove.log)

This shows that the theorem depends on the executed body.

### Material real-input representation gap

The universal claim's precondition does not contain an actual supplied-semantics
integer list. `ValSeq` in the supplied semantics has the concrete constructors
`.ValSeq` and `vCons(Val, ValSeq)`. The proof adds the distinct constructor
`intValues(IntSeq)` and quantifies only lists containing that constructor.

The candidate supplies iterator and append equations for this new constructor,
but no bridge-free universal theorem establishes that executing the submitted
function on a concrete `vCons` embedding has the same result, control, state,
and exceptions as executing it on `intValues`. The false empty-list witness in
Stage 5 proves that the representation is not generally observationally
equivalent to concrete `ValSeq`. The actual-representation entry claims stop at
length two.

The body itself is pinned, but the unrestricted real-program input domain is
not. This is a material adequacy failure, not an artifact-maintenance
observation.

**Stage 4 result: FAIL for unrestricted real-program pinning.**

## 5. Rule-by-rule static soundness review

### Complete inventory

[`stage5-rule-inventory.tsv`](evidence/stage5-rule-inventory.tsv) is a
source-derived inventory of every local module/import, configuration, context,
syntax declaration, rule, and claim in the complete supplied semantics,
`verification.k`, and `spec.k`. It contains:

- 1 configuration;
- 5 contexts;
- 239 syntax declarations;
- 719 rules;
- 6 claims;
- 1,143 total source records including modules, imports, and requires.

Of the 719 rules, 695 are in the byte-identical supplied semantics and 24 are
candidate-local. There are no candidate-local simplification rules,
`functional` declarations, `[opaque]` attributes, or proof-side
`[concrete]` rules. Supplied opaque/no-evaluator symbols are confined to unused
features such as float operations, symbolic sorting, and MD5; none can affect
this proof path.

Every supplied rule is listed in the inventory. For the theorem-relevant subset,
the following mapping was checked rule by rule:

| Submitted construct/effect | Declaration and execution rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:53-61`; `core.k:123-127`; `functions.k:14-16` |
| direct closure call, argument order, frame creation | `core.k:183-191`; `call.k:20-21,69-74`; `functions.k:63-90` |
| `Assign`, names, integer/Boolean literals | `syntax.k:9-12,41`; `core.k:129-196`; `controls.k:9-18` |
| empty `ListExpr`, allocation | `syntax.k:17`; `list.k:13-15`; `core.k:117-121` |
| `For`, iterator protocol, target binding | `syntax.k:45`; `controls.k:62-74`; `iter.k:8`; `list.k:9-10`; `tuple.k:31-41` |
| `If`, truthiness, return and frame pop | `syntax.k:49-50`; `core.k:198-205`; `controls.k:50-54`; `functions.k:77-90` |
| unary integer negation | `syntax.k:14`; `operators.k:10,44-46`; `int.k:7` |
| list `in` membership | `syntax.k:30-32`; `operators.k:15-17,38-42`; `list.k:57-67` |
| `Attribute`, `Call`, and `seen.append(value)` | `syntax.k:28-29`; `call.k:15-24,52-74`; `list.k:52-55` |
| discarded expression statement | `syntax.k:52`; `controls.k:46-48` |

Those fixed rules preserve left-to-right evaluation, select the actual closure
binding, allocate and mutate the `seen` heap object, use distinct loop
iterations, unwind returns through the exact stack frame, and compute integer
negation/membership correctly. Other supplied rules are unreachable from this
program and cannot contribute to claim closure. The compiler's totality
warnings are for those unused paths.

### Exhaustive candidate-local rule decisions

| Rule | Classification and decision |
|---|---|
| `verification.k:7` `pairLoopBody` | Definitional alias; exact generated loop body. Sound. |
| `verification.k:19` `pairsBody` | Definitional alias; mechanically equal to regenerated body. Sound. |
| `verification.k:35` `oppositeIn(_, .ValSeq)` | Mathematical base case. Sound. |
| `verification.k:36` `oppositeIn(X,vCons(Y,YS))` | Structural additive-inverse search. Sound on its all-integer use domain. |
| `verification.k:43` `pairsSpec(.ValSeq)` | No distinct pair in an empty sequence. Sound. |
| `verification.k:44` `pairsSpec(vCons(X,XS))` | Searches only the tail, then recurses; exactly the distinct-index property. Sound. |
| `verification.k:50` `seenAfter(.ValSeq,SEEN)` | Exhausted input leaves the entire accumulated prefix. Sound. |
| `verification.k:51` matching `seenAfter` branch | Returns before append when an opposite is already in `SEEN`. Sound. |
| `verification.k:53` nonmatching `seenAfter` branch | Appends and recurses. Guard is the Boolean complement of line 51; no overlap. Sound. |
| `verification.k:64` `snocIS` base | Correct append-to-empty equation. Sound. |
| `verification.k:65` `snocIS` step | Structurally recursive append. Sound and descending. |
| `verification.k:69` `memberIS` base | Correct empty membership. Sound. |
| `verification.k:70` `memberIS` step | Correct equality-or-recursion. Sound and descending. |
| `verification.k:74` `oppositeIS` | Names membership of `-X`; correct integer identity. Sound. |
| `verification.k:79` `scanIS` base | No pair in exhausted suffix. Sound. |
| `verification.k:80` `scanIS` step | Checks current value against the exact prior prefix and then snocs it. Sound and equivalent to distinct-index existence. |
| `verification.k:85` `pairsIS` | Starts `scanIS` with an empty prefix. Sound mathematical definition. |
| `verification.k:88` `seenAfterIS` base | Returns accumulated prefix on exhaustion. Sound. |
| `verification.k:89` `seenAfterIS` step | Its conditional branches exactly match early return versus append/recurse. Sound and descending. |
| `verification.k:97` empty `intValues` iterator | Intended representation base observation; disjoint from fixed `.ValSeq`/`vCons` iterator rules. Locally truthful. |
| `verification.k:98` nonempty `intValues` iterator | Intended head/tail iterator observation; disjoint and structurally descending. Locally truthful. |
| `verification.k:103` `valSeqConcat(intValues(...),vCons(X,.ValSeq))` | Homomorphism to `snocIS`; disjoint from fixed concat rules. Locally truthful for the intended representation. |
| `verification.k:115` empty-list allocation bridge | **Unsound operational bridge.** It preempts the fixed list-literal rule over every continuation and changes observable truthiness. Concrete false witness below. |
| `verification.k:119` promoted loop summary | Operational bridge. The candidate's proved claim was slightly narrower in framed cells, but a fresh bridge-free theorem over the complete promoted match domain closes with `#Top`; accepted conditional on the independently proved membership lemma. |

The `[total]` declarations for `oppositeIn`, `pairsSpec`, and `seenAfter` are
not syntactically exhaustive over the later-added `intValues` constructor or
non-integer `ValSeq` heads. Their uses are restricted to concrete all-integer
chains in the bounded claims, so they produce no false conclusion on those
uses. This is a narrow totality/maintenance defect, not the decisive
unsoundness.

### Promoted loop bridge

The loop bridge matches the exact loop body, terminal
`Return(Bool(false)) ~> #endcall`, frame continuation `.K`, local bindings,
scope locations, `seen` object, and stack. It reads `REM`, `SEEN`, and the local
frame; it removes the local scope/frame, preserves the existing heap outside
`H`, preserves heap location, exception and exit cells, and returns
`scanIS(REM,SEEN)`.

The candidate's `loop-summary` fixes `builtinsScope`, `NoExc`, and exit code 0,
whereas the promoted rule frames arbitrary values for those cells. To test the
full match domain, I wrote a bridge-free connection claim that explicitly
quantifies the arbitrary builtins scope, heap location, exception, and exit
cells and imports no promoted bridge. With only the separately proved
`membership-summary` trusted, it exits 0 and prints `#Top`. See
[`loop-bridge-context-spec.k`](evidence/loop-bridge-context-spec.k) and
[`stage5-loop-bridge-complete-domain.log`](evidence/stage5-loop-bridge-complete-domain.log).
The promoted loop bridge is therefore not the defect.

### Empty-list bridge false-conclusion witness

The fixed rule at `reference-semantics/semantics/list.k:15` gives:

```text
#applyK(toList,.Vals)
=> #alloc(list(vals2valSeq(.Vals)))
=> #alloc(list(.ValSeq))
```

The candidate bridge instead stores `list(intValues(.IntSeq))`. The fixed
truthiness rule at `reference-semantics/semantics/core.k:204` computes:

```text
truthy(list(intValues(.IntSeq)))
= notBool (intValues(.IntSeq) ==K .ValSeq)
= true
```

The satisfiable witness program uses no input outside ordinary Python:

```python
def empty_list_truth():
    if []:
        return True
    return False
```

CPython returns false. Fresh base `krun` stores `list(.ValSeq)` and exits 0.
Fresh lemma `krun` stores `list(intValues(.IntSeq))`, takes the true branch,
fails the assertion, and exits 1. More strongly, the base definition proves
the correct result `false`, while the lemma definition proves the Python-false
result `true`; both K commands print `#Top`. This supplies the required concrete
false-conclusion witness, not merely an unproved suspicion.

The rule has an arbitrary continuation and no guard restricting it to the
candidate's `seen = []` assignment. There is no bridge-free universal
connection theorem over that match domain, and the witness proves no such
theorem can exist. The main theorem depends on the bridge to initialize `seen`
in the `intValues` representation. This is a materially unsound, execution-
replacing proof rule, not an acceptable primitive or harmless normalization.

**Stage 5 result: FAIL.**

## 6. Fresh non-vacuity test

I did not reuse the candidate's mutation. The fresh mutation replaces the
universal result `pairsIS(INPUT)` with its Boolean complement
`notBool pairsIS(INPUT)` while leaving the satisfiable entry state and heap
obligation intact. `INPUT=.IntSeq` is an explicit counterexample: the submitted
program and `pairsIS` both return false, while the mutated destination requires
true.

The mutation is
[`fresh-vacuity-spec.k`](evidence/fresh-vacuity-spec.k). Its dry run compiles
successfully with exit 0
([`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)).
The actual proof exits 1 with `WarnStuckClaimState`; the residual reports the
failed implication between `scanIS(INPUT,.IntSeq)` and
`notBool scanIS(INPUT,.IntSeq)`
([`stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log)).

This is the expected unmet result obligation, not a parse failure, crash,
timeout, or unreachable mutation. The entry theorem is result-constraining and
non-vacuous. Non-vacuity does not cure its unsound theory.

**Stage 6 result: PASS.**

## 7. Proven-versus-assumed accounting and decision

### What the successful reachability proof actually establishes

Under the candidate-extended module `PAIRS-VERIFICATION-LEMMAS`, for every
`INPUT:IntSeq`, a direct call of the exact submitted closure on the extended
value `list(intValues(INPUT))` rewrites to the fully defined Boolean
`pairsIS(INPUT)` and leaves the abstract processed-prefix heap stated by
`seenAfterIS`.

That statement is machine-checked only in a theory containing the false
empty-list bridge. It is not a partial-correctness theorem for the submitted
program over all ordinary supplied-semantics integer lists.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 frontend/backend and builtin integer/Boolean theories | All parsing, rewriting, induction, and unbounded integer mathematics | Normal unavoidable low-level trust boundary. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Acceptable here: regeneration is byte-identical and constructor identity was mechanically checked. |
| Supplied reference semantics | Calls, frames, state, lists, control, membership, allocation | Required fixed semantics. The material used subset was reviewed and concretely exercised. |
| `membership-summary` trusted during the loop proof | Membership result for arbitrary `IntSeq` and arbitrary continuation | Acceptable modular lemma: independently proved with exit 0 and `#Top` before being trusted. |
| Promoted loop rewrite | Result, heap, scope/frame cleanup, control | Acceptable after the fresh bridge-free complete-domain connection theorem. |
| Recursive `memberIS`, `scanIS`, `pairsIS`, `snocIS`, `seenAfterIS` | Final Boolean and final heap | Fully equational, structurally descending, and ordinary mathematics; no opaque oracle. |
| `intValues` representation and its iterator/append rules | Universal input, membership, loop state, final heap | Concerning/result-bearing and not universally connected to concrete `vCons` whole-program execution. This creates a material domain/pinning gap. |
| Priority-40 empty-list bridge | Program allocation, heap representation, downstream observations, main proof closure | Illegitimate. It is observably false and enables a false `#Top` conclusion. |
| Differential tests | Python implementation/canonical bridge on 142,278 inputs | Strong finite evidence only; not a universal proof and not a repair for an unsound K rule. |

No externally trusted opaque value or primitive on the actual proof path
computes the task answer. The failure instead comes from a proof-local
operational rewrite that changes program semantics.

### Gate and benchmark decision

- Real-program soundness (Gate A): **FAIL** because the empty-list bridge is
  false over its complete match domain and the main claim relies on it.
- Intent adequacy (Gate B): **FAIL** independently because the universal claim
  ranges over a distinct unconnected representation; actual `vCons` entry
  claims are bounded to at most two elements.
- Evidence/auditability (Gate C): reviewer evidence is reproducible, but finite
  tests cannot repair Gates A or B.

Clean `#Top` reconstruction and successful non-vacuity are therefore
insufficient. The candidate relies on materially unsound semantics and does not
prove the unrestricted HumanEval source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
