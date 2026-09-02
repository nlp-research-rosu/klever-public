# Independent adversarial audit: 0-has-close-elements

The candidate's five submitted proof targets all reconstruct and print `#Top`,
the translated Python rewrite agrees strongly with the trusted canonical
implementation, and a fresh false-result mutation is rejected. Nevertheless,
the proof is not legitimate. Four operational summary rules are
machine-demonstrably false over their declared match domains, and a fifth
arbitrary-body rule is likewise unsupported and false. The staged claims prove
only exact program contexts; the candidate generalizes them to arbitrary loop
bodies, arbitrary closures, arbitrary continuations, or unchecked bindings.
The final proof imports and relies on this modified execution theory.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted directory
`/reference/reference-semantics` exists and is a directory, so there is no
rendered-mode/mount contradiction and no infrastructure breach.

I recursively compared `/candidate/reference-semantics` against the trusted
tree with `diff -qr --no-dereference`. There are no missing, additional,
changed, mistyped, or symlinked entries. Neither tree contains symlinks. The
path-independent recursive file digest is
`06160f82a2076306c4a3074692c5615b898a13fa1c7c888b1dc7cb20944fff1e`
for both trees. See `evidence/01-integrity.log`.

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`, and
its `py2mpy.py` is byte-identical to `/reference/py2mpy.py`. All proof-relevant
candidate sources are regular files.

### Missing provenance artifacts

The following requested candidate artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any structured generation trace matching the requested trace/log forms

There is also no `PROOF.md` and no candidate `spec-vacuity.k`; the latter was
not required to exist because a fresh reviewer mutation was created in stage
6. The missing generation metadata is a provenance defect, not an audit
infrastructure failure.

Candidate-generated `.kproof.97LHgK`, `__pycache__`, and
`kore-exec.tar.gz` artifacts were not trusted or reused. Candidate auxiliary
`smoke.*`, `testsort.*`, and `prove.sh` were read only as untrusted context.

All source required for execution was copied into
`/tmp/audit-work/0-has-close-elements`. The semantics copy came from the
trusted tree after the equality check. Every build in this review was made
there from source. Reviewer evidence is under `evidence/`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a list of floats and a float threshold, return `True` iff there are two
different list positions whose absolute value difference is strictly less
than the threshold. Thus:

- empty and singleton lists return `False`;
- equality with the threshold is not close enough;
- duplicate values are close exactly when the threshold is positive; and
- a non-positive threshold cannot produce `True`.

The trusted canonical implementation checks every ordered pair of distinct
indices. The candidate uses a helper and an increasing `start` index, checking
each unordered pair once. The extra resets of `index`, `other`, `start`, and
`number` do not alter the returned Boolean. The candidate does not mutate the
input list.

### Trusted translation

I regenerated `solution.mpy` from `solution.py` using the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0. `cmp -s` exited 0, and both files have SHA-256
`fdcfe6fa45a3f0c3095f26e402bb739c403800bc3412df619a41bdb449c33307`.
See `evidence/02-translation-and-differential.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and candidate
modules under distinct module names and does not reuse the proof equations. Its
reproducible input description is in
`evidence/differential-input-manifest.json`. It covered:

- 22 explicit cases: both documented examples, empty/singleton, duplicates,
  strict exact-threshold boundaries, `nextafter` values on both sides,
  negative and zero thresholds, signed zero, early and late true branches,
  nonadjacent pairs, infinities, NaNs, and overflowing subtraction;
- 19,530 exhaustive cases over all lists of length 0 through 5 from five small
  float values and five thresholds; and
- 3,000 deterministic random cases with seed `20260724`.

The run checked 22,552 inputs, exited 0, and found zero mismatches. This is
strong finite evidence that `solution.py` implements the trusted contract; it
is not a universal proof.

## 3. Clean proof reconstruction

The live tools are `/usr/bin/kompile` and `/usr/bin/kprove`, K version
7.1.337, build date 2026-06-18. `kup` is absent, but the independently
installed K toolchain is operational.

I first built the supplied semantics with the LLVM backend from trusted source.
The reviewer-authored `evidence/concrete_semantics_test.py` was translated
with the trusted translator. Both Python execution and K execution of its 11
normal/boundary assertions exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-build/runtime-kompiled
krun reviewer-concrete.mpy \
  --definition audit-build/runtime-kompiled --output none
```

See `evidence/03a-translate-concrete.log` through
`evidence/03d-krun-concrete.log`.

I then independently rebuilt every staged Haskell definition and ran every
positive target module:

| Definition main module | Target module | Build | Proof |
|---|---|---:|---:|
| `VERIFICATION-BASE` | `SPEC-INNER` (3 claims) | exit 0 | exit 0, `#Top` |
| `VERIFICATION-WITH-INNER` | `SPEC-HELPER` | exit 0 | exit 0, `#Top` |
| `VERIFICATION-WITH-HELPER` | `SPEC-OUTER` (2 claims) | exit 0 | exit 0, `#Top` |
| `VERIFICATION-WITH-OUTER` | `SPEC-ENTRY` | exit 0 | exit 0, `#Top` |
| `VERIFICATION-WITH-ENTRY` | `SPEC` | exit 0 | exit 0, `#Top` |

Exact commands, statuses, and bounded outputs are in
`evidence/04a-kompile-base.log` through
`evidence/04j-kprove-final.log`. No candidate-compiled definition or cache was
used.

This stage establishes that all submitted claims close under the submitted
theory. It does not establish that the proof-local theory is a sound extension
of the supplied semantics.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

The formal domain is every finite proof-representation `FloatSeq` and every K
`Float` threshold. The public claims have no additional `requires`
precondition.

| Claim | Preconditions and postcondition |
|---|---|
| `SPEC-INNER`, empty | At the helper loop head with an empty remaining list, `env=2`, the exact helper locals, an active call frame, and `noRet`, execute the exact reset/return suffix. It returns the existing `found=false` and resets `index=0`, `other=number`. |
| `SPEC-INNER`, `I < START` | At the exact helper loop head with a nonempty remainder and `found=false`, skip the head as out of range and return `closeSkip(A,R,T,I+1,START)`, with reset locals. |
| `SPEC-INNER`, `I >= START` | At the same exact loop head, include the head comparison and return `near(A,F,T) orBool closeSkip(A,R,T,I+1,START)`. |
| `SPEC-HELPER` | Apply the exact `helperClosure()` to `(A,list(ALL),T,START)` in the stated scopes and return `closeSkip(A,ALL,T,0,START)`. |
| `SPEC-OUTER`, empty | At the exact outer loop head with no remaining elements and `found=false`, execute the reset/return suffix and return `false`. |
| `SPEC-OUTER`, nonempty | At the exact outer loop head, return the current helper result or the remaining-pair result: `closeSkip(A,ALL,T,0,START) orBool hasPairs(ALL,R,T,START+1)`. |
| `SPEC-ENTRY` | Apply the exact `entryClosure()` and return `hasPairs(ALL,ALL,T,1)`. |
| `SPEC` | Load `solutionModule()`, call `has_close_elements` on `list(ALL),T`, and return `hasPairs(ALL,ALL,T,1)`. |

Each entry precondition is satisfiable. For example, use empty heap, `noRet`,
the scopes shown in the claims, `.List` for framed remainders, and:

- inner-empty: `ALL=.FloatSeq`, `A=1.0`, `T=0.1`, `I=0`, `START=1`;
- inner-skip: a nonempty remainder, `I=0`, `START=1`;
- inner-compare: a nonempty remainder, `I=1`, `START=1`;
- helper: `A=1.0`, `ALL=[1.0,1.0]`, `T=0.1`, `START=1`;
- outer-empty: `ALL=.FloatSeq`;
- outer-nonempty, entry, and final: `ALL=[1.0,1.0]`, `T=0.1`.

The result is not a free variable, tautology, or implication: it is the
specific Boolean function `hasPairs`. The fresh negated-result mutation in
stage 6 is rejected.

### Program identity

The final claim does not read a filename at runtime; it loads the proof-local
term `solutionModule()`. I therefore checked this pin independently.
`evidence/program-pinning.k` expands `solutionModule()` and all body helpers
against the full constructor tree emitted in `solution.mpy`. It proves
definitionally with exit 0 and `#Top`; see
`evidence/04k-program-pinning.log`. Together with the trusted translator's
byte-identity result, this pins the loaded AST to the submitted
`solution.mpy`.

For the satisfying public input `[1.0,1.0]`, threshold `0.1`, the formal
summary reduces by its list equations to the pair comparison
`abs(1.0-1.0) < 0.1`, hence `true`. The trusted canonical implementation and
candidate implementation both return `True`; see
`evidence/satisfying_witness.py` and
`evidence/04l-satisfying-witness.log`.

These are genuine adequacy strengths. They do not validate the operational
bridges used to obtain the final `#Top`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and supplied-semantics boundary

`evidence/inventory_k.py` inventories every source-level `syntax`, `rule`,
`claim`, `context`, `configuration`, `macro`, and `alias` sentence across the
24 supplied K files, `verification.k`, and `spec.k`. The resulting
`evidence/rule-inventory.tsv` has a source path, line, module, attributes,
classification, decision, and normalized full sentence for each of 972
entries:

- 717 rules;
- 241 syntax declarations;
- 8 claims;
- 5 contexts; and
- 1 configuration.

This includes every source `[function]`, `[total]`, `[symbol]`,
`[no-evaluators]`, `[concrete]`, `[priority]`, and `[owise]` attribute.
There are no proof-local simplification rules. Counts and the exact generation
command are in `evidence/rule-inventory-summary.txt`.

The supplied rules are the fixed selected semantics and exactly match the
trusted mount. The inventory marks 105 declarations/rules as reached by this
program or the reviewer concrete test and 823 as not reached. Unreached
construct families (dicts, sets, sorting, comprehensions, string methods,
subscripts, ranges, and similar operations) cannot match this program's AST or
its reached internal terms. They are accepted at the mandated supplied
semantics level, not reinterpreted as candidate proof axioms.

### Used-construct map

| `solution.mpy` construct | Declaration/effect rules |
|---|---|
| `Module`, `ImportFrom`, `FuncDef`, `Params`, `Stmts` | `syntax.k`; module sequencing in `core.k:124-127`; function binding in `functions.k:14-16`; non-math import no-op in `controls.k:35-44` |
| `Name`, local/global lookup | `syntax.k:12`; scope-chain rules `core.k:130-154` |
| `Bool`, `Int`, `Float` | `syntax.k:9-13`; literal rules `core.k:194-196` and `float.k:20-21` |
| `Assign`, `AugAssign` | `controls.k:9-31`; integer `+` in `int.k:9`; map update in current scope |
| `For` and list iteration | `controls.k:62-75`; supplied `list.k:9-10`; proof representation rules `verification.k:89-95` |
| `If` and truth | `controls.k:50-54`; Boolean truth in `core.k:199-205` |
| integer `>=` | compare contexts/dispatch in `operators.k:14-17`; integer case `int.k:25` |
| float subtraction, `abs`, and strict `<` | call/dispatch through `call.k`, `operators.k`, `builtins.k:44`, and `float.k:50-56,103-105` |
| helper and entry calls | callee lookup and argument evaluation in `call.k:18-32`; frame allocation/binding/return/pop in `call.k:69-75` and `functions.k:62-90` |
| `Break` | loop labels and unwinding in `controls.k:84-91` |
| `Return` | strict result evaluation and frame pop in `functions.k:77-90` |

The supplied configuration tracks `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.
The fixed rules give left-to-right call argument evaluation, lexical name
lookup, separate function frames, local state changes, and explicit loop
control. For the used subset, the relevant rule guards and priorities are
disjoint or agree on overlaps.

### Sound proof-local definitions

The following proof-local material is sound:

- `nearBody`, `helperLoopBody`, `helperBody`, `outerLoopBody`, `entryBody`,
  the two closures, `solutionModule`, and `solutionScope`
  (`verification.k:7-85`) are definitional abbreviations for the exact emitted
  AST and bindings.
- `FloatSeq`, `.FloatSeq`, and `fCons` form a typed proof-only representation
  of every finite float list. Its two iterator rules
  (`verification.k:89-95`) are exhaustive and disjoint from the supplied
  `.ValSeq`/`vCons` list rules.
- `near` uses exactly the fixed opaque terms produced by float subtraction,
  `abs`, and strict comparison. `closeSkip` has disjoint `I<START` and
  `I>=START` cases covering all integers and structurally descends its list.
  `hasPairs` has exhaustive empty/cons cases and structurally descends its
  current list (`verification.k:97-120`). Their totality declarations are
  justified.
- `#proofDone` is an inert marker and does not determine a result.

The float operations `subF`, `absF`, and `floatLt` are fixed-semantics opaque
symbols for symbolic proof and have supplied `[concrete]` LLVM equations. The
formal result keeps precisely those terms; it does not assume an extra
proof-local equation for their values.

### Rejected operational bridges

The following five rules are not consequences of the exact claims proved in
the preceding rung:

| Rule | Unsupported generalization | False conclusion witness |
|---|---|---|
| `verification.k:130-145` | Replaces `For(Name("other"), list(ALL), _B)` for **any body** and any continuation. The preceding claim covers only `helperLoopBody()` followed by the exact reset/return suffix and exact call-frame shape. | Give the closure an empty loop body, valid public data `[1.0,1.0]`, `T=0.1`, and real initial `START=1`. Fixed semantics returns `false`; the bridge writes `closeSkip(1.0,[1.0,1.0],0.1,0,1)=true`. Both symbolic transition characterizations prove `#Top` in the fixed/extended witness modules. |
| `verification.k:151-161` | Replaces the helper `Call` before callee lookup, checks argument variables but not the selected binding, and accepts an arbitrary continuation. | Put a same-signature closure returning `false` in the current scope under `is_close_to_any`, with `[1.0,1.0]`, `T=0.1`, `START=1`. Fixed lookup/call returns `false`; the bridge returns the same true `closeSkip` summary. Both claims prove `#Top`. |
| `verification.k:163-172` | Matches a closure with the right parameter names but **arbitrary `_BODY`**, skips frame allocation, binding, execution, state, return control, and accepts arbitrary `K`. The only preceding theorem uses exact `helperClosure()` and `#proofDone`. | Let `_BODY = Return(Bool(false))`, input `[1.0,1.0]`, `T=0.1`, `START=1`. Fixed execution returns `false`, while the rule's RHS is the true ground `closeSkip` summary. The fixed claim proves `#Top`; the attempted universal summary in the extended definition fails with residual `false` versus the proximity atom, confirming no connection theorem. |
| `verification.k:178-191` | Replaces the outer `For` for **any body** and continuation. The preceding claims cover only `outerLoopBody()` plus the exact suffix and frame. | Use an empty outer body with `[1.0,1.0]`, `T=0.1`. Fixed semantics leaves `found=false`; the bridge writes `hasPairs(...)=true`. Both fixed and bridge-enabled characterizations prove `#Top`. |
| `verification.k:197-203` | Replaces the public `Call` before lookup without checking the module-scope binding and accepts arbitrary continuation/scopes. | Bind `has_close_elements` to a same-signature closure returning `false` and use `[1.0,1.0]`, `T=0.1`. Fixed execution returns `false`; the bridge returns true `hasPairs`. Both claims prove `#Top`. |

The complete witness source is `evidence/bridge-witness.k`. Exact commands and
the eight successful fixed-versus-bridge proof runs are in
`evidence/05-bridge-witnesses.log`. The arbitrary-closure check is in
`evidence/05b-apply-bridge-check.log`. The ordinary ground value of both
summaries is corroborated by `evidence/04l-satisfying-witness.log` and the
fresh LLVM concrete execution.

The altered bodies and shadowed bindings are operational-sensitivity
witnesses, not claims that `solution.py` itself diverges on those inputs. They
show that each submitted rule's *declared match domain* exceeds its
justification domain and admits a false conclusion on ordinary float/list
inputs. Rule priority does not supply the missing equivalence.

These rules also omit or frame cells whose transitions they skip:

- the loop rules discard arbitrary body effects, exceptions, heap changes, and
  control actions, while directly fabricating local results;
- the direct-call rules skip lookup and binding selection; and
- the arbitrary-closure rule skips call-frame allocation, parameter binding,
  body execution, state changes, return, and frame cleanup.

There is no bridge-free universal connection theorem over any broadened match
domain. The exact prior claims cannot justify arbitrary `_B`, `_BODY`,
continuations, scopes, or bindings. Because the staged positive definitions
import these bridges at the helper, outer, entry, and final rungs, their
`#Top` results are proofs in an unsound proof-local theory, not legitimate
proofs of the fixed supplied execution.

## 6. Fresh non-vacuity test

I created `evidence/spec-vacuity-audit.k`, which keeps the exact final
program-load-and-call configuration but changes the result obligation to:

```text
notBool hasPairs(ALL, ALL, T, 1)
```

This is false for the satisfying input `[1.0,1.0]`, threshold `0.1`, where the
original result is `true`.

The dry run parsed and generated KORE successfully with exit 0:

```text
kprove spec-vacuity-audit.k \
  --definition audit-build/entry-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

The actual proof exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet implication:

```text
hasPairs(ALL, ALL, T, 1)
  #Equals
notBool hasPairs(ALL, ALL, T, 1)
```

See `evidence/06a-vacuity-dry-run.log`,
`evidence/06b-vacuity-proof.log`, and
`evidence/06c-vacuity-witness.txt`. This is valid non-vacuity evidence. It does
not repair the unsound operational bridges.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the candidate-extended K theory, the staged symbolic configurations
close and the final exact AST-load/call configuration reaches the term
`hasPairs(ALL,ALL,T,1)`. The theorem is partial correctness: it does not make a
separate total-termination claim.

Because the extended theory contains false, execution-replacing rules with
broader domains than their proved claims, that statement cannot be projected
back to a sound theorem about the real submitted program under only the fixed
supplied semantics.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical implementation, and translator | Intent oracle and source-to-`.mpy` bridge | Acceptable trusted inputs; byte comparisons and differential evidence recorded |
| Exact supplied semantics tree and K built-ins | All operational behavior and proof mechanics | Required fixed trust boundary; candidate copy has exact integrity |
| `subF`, `absF`, `floatLt` | Every proximity atom and final Boolean | Acceptable fixed opaque primitives for a term-parametric proof; LLVM concrete equations and finite Python comparisons support, but do not universally prove, the Python-float bridge |
| `FloatSeq` representation and iterator equations | Symbolic finite-list inputs | Acceptable: exhaustive, disjoint structural representation covering every finite K-Float list |
| `near`, `closeSkip`, `hasPairs` equations | Final result | Acceptable mathematical definitions; structural descent and guard coverage checked |
| Informal statement that `hasPairs(ALL,ALL,T,1)` denotes all distinct index pairs | Natural-language adequacy | Strongly supported by direct equation review and 22,552 differential cases, but finite testing is not the K proof |
| Five proof-local operational bridges | Loop/call execution, binding, control, state, final result | Illegitimate: no full-domain connection theorem and explicit false-conclusion witnesses |
| Missing generation metadata | Provenance and reproducibility of the original generation | Concerning, but not the source of the soundness verdict |

Gate A (real-program soundness) fails. Gate B evidence strongly supports that
the Python rewrite and result summary match the natural-language task. Gate C
has reproducible source, build, differential, witness, and mutation evidence,
subject to the explicitly named fixed float primitives and missing generation
metadata. Passing the later adequacy and non-vacuity checks cannot override the
Gate A failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
