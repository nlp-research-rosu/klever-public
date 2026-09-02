# Independent adversarial review: 122-add-elements

Decision: **CONCERNS / LEGIT**.

The candidate contains a fresh-reconstructible, result-constraining
partial-correctness proof of the exact submitted `solution.py` function body
under the supplied K semantics. It is not, however, a proof that the submitted
program agrees with the trusted canonical over the stated domain of integer
arrays. The material witness is `arr=[-99], k=1`: the proved/submitted function
returns `-99`, while the trusted canonical returns `0`.

The proof is therefore legitimate as a theorem about the real submitted
program, but its bridge to the requested task is materially limited.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is no
mode/mount contradiction, so this is not an infrastructure-error case.

The independent lstat/byte audit in
`evidence/stage1/integrity_check.py` and
`evidence/stage1/integrity_check.log` found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `0e13fa71b137d4f1598346bec0d43a7a97585397568c34e2040e71c198b2acf0`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Every directory and regular file in the candidate
  `reference-semantics/` tree exactly matches the trusted supplied tree.
  There are no missing, additional, mistyped, changed, or symlinked entries.
  The independent recursive `diff --no-dereference` also exits 0
  (`evidence/stage1/semantics_diff.log`).
- The complete candidate manifest records no symlinks
  (`evidence/stage1/candidate_manifest.log`).

The candidate omits `run-input.json`, `metrics.json`, `codex-last.txt`, and
`codex-output.log`, and contains no filename suggesting a structured
generation trace. Those missing artifacts reduce provenance auditability but
do not conceal or substitute for the source proof. There is also no
candidate `PROOF.md` or `spec-vacuity.k` to rely on.

K was available independently as version v7.1.337
(`evidence/stage1/kompile_version.log` and
`evidence/stage1/kprove_version.log`).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks, for a nonempty integer array of length at most 100
and `1 <= k <= len(arr)`, for the sum of elements with at most two digits
among the first `k` elements. The trusted canonical operationalizes that
phrase as:

```python
sum(elem for elem in arr[:k] if len(str(elem)) <= 2)
```

The submitted implementation instead uses:

```python
if abs(element) < 100:
    total += element
```

These are equivalent for nonnegative integers, but not for negative integers
having two decimal digits. The prompt states integers and supplies no
nonnegativity restriction, so those values are in the intended domain.

### Translation fidelity

The trusted translator was run afresh on the scratch copy of
`solution.py`. The regenerated and submitted `.mpy` files are byte-identical,
both with SHA-256
`7b5c94215b395cce642414d4e864a3643404201eabef94b6355fa8b8f264a779`.
The exact command, statuses, and hashes are in
`evidence/stage2/regenerate_and_compare.sh` and
`evidence/stage2/regenerate_compare.log`.

### Independent differential

`evidence/stage2/differential_test.py` independently imports
`/reference/canonical.py:add_elements` and the scratch copy of the submitted
entry point. Its deterministic 510 cases comprise:

- the documented example;
- an empty outside-domain diagnostic;
- lower and upper `k` boundaries and length 100;
- all decision boundaries around `-101`, `-100`, `-99`, `-10`, `-9`, `0`,
  `9`, `10`, `99`, `100`, and `101`;
- every singleton integer from -150 through 150; and
- 200 generated in-domain arrays with seed 122.

The command exits 1 because it finds 205 result mismatches and no execution
errors (`evidence/stage2/differential_test.log`). Examples include:

- `[-99], 1`: canonical `0`, submitted `-99`;
- `[-10], 1`: canonical `0`, submitted `-10`;
- the combined boundary array:
  canonical `109`, submitted `0`.

This is a material implementation-to-canonical discrepancy, not a different
but equivalent algorithm.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/src`; candidate
`__pycache__`, any hypothetical kompiled directories, and candidate caches
were not reused. All build products were created under
`/tmp/audit-work/build`.

Fresh builds:

- LLVM supplied semantics:
  `kompile reference-semantics/semantics.k --backend llvm
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX ...` exits 0
  (`evidence/stage3/kompile_llvm.log`).
- Haskell proof definition:
  `kompile verification.k --backend haskell
  --main-module ADD-ELEMENTS-VERIFICATION
  --syntax-module MPY-SYNTAX ...` exits 0
  (`evidence/stage3/kompile_haskell.log`).

The unmodified two-claim module proves with exit 0 and `#Top`
(`evidence/stage3/kprove_all.log`).

For independent target selection, the scratch-only
`evidence/stage3/spec-labeled.k` adds labels without changing either claim:

- The loop invariant alone exits 0 with `#Top`
  (`evidence/stage3/kprove_loop.log`).
- The entry proof, with the independently proved loop invariant marked
  trusted, exits 0 with `#Top`
  (`evidence/stage3/kprove_entry_trusting_proved_loop.log`).

Selecting only the entry while filtering away its loop circularity caused
unbounded concrete loop unrolling and was auditor-terminated. The two
diagnostic logs explicitly record exit 130
(`evidence/stage3/kprove_entry.log` and
`evidence/stage3/kprove_entry_with_proved_loop.log`); they are not target
failures. The successful proof chain is loop first, then entry using that
proved invariant, exactly as the combined proof does.

Fresh concrete execution under the rebuilt LLVM definition covers the
documented example, comparison boundaries, the `[-99]` divergence witness,
and a length-100/k-100 input. It terminates with `.K`, `NoExc`, exit-code 0,
and process exit 0 (`evidence/stage3/concrete_audit.py`,
`evidence/stage3/run_concrete_audit.sh`, and
`evidence/stage3/krun_concrete_audit.log`). An initial audit test used the
unsupported test-only expression `list(range(100))`; that unrelated test
stuck and is retained, not counted as proof evidence, in
`evidence/stage3/krun_concrete_audit_initial_unmodeled_test.log`.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

Starting at the real loop head over any nonempty `ValSeq` whose head and tail
are integers, with integer accumulator `ACC`, the loop consumes the sequence.
It leaves `total` equal to `qualifyingSumAcc(ACC, sequence)` and consumes the
loop computation. It permits the final `element` binding to be any value,
which is appropriate because the final binding itself is not the result. The
global scope may be symbolic, but the precondition requires that it not
shadow the builtin `abs`.

### Entry claim in plain language

Let the nonempty selected prefix be `HEAD :: PREFIX`, let `SUFFIX` be the
remainder of the input array, and set `k` to the selected prefix length. All
three sequence parts contain integers and total array length is at most 100.
The claim calls a closure containing the submitted body and says that, if the
call terminates, its result is exactly:

```text
qualifyingSumAcc(0, HEAD :: PREFIX)
```

Thus `k >= 1`, `k <= len(arr)`, the input is nonempty, and the returned K
value is constrained; it is not existential, free, tautological, or merely
one side of an implication.

### Program pinning

`evidence/stage4/pinning_check.py` extracts the submitted `.mpy` function
body and checks that the entry closure contains that exact body after only
normalizing K's explicit `.Stmts` empty-list unit. The check exits 0
(`evidence/stage4/pinning_check.log`). The entry does start directly at the
closure call rather than re-executing `Module` and `FuncDef` binding, but it
does not replace, summarize, or skip the function body. For this undecorated,
noncapturing function, direct closure invocation preserves its arguments,
body, defining global scope 0, call frame, return, heap effects, and result.

The entry uses the supplied semantics' permitted unboxed read-only
`list(ValSeq)` claim input instead of allocating an external list reference.
The function does not mutate `arr`; slicing allocates a new list and the
post-heap/heap location are existentially recorded. This is a sound
read-only input abstraction, though it is an informal claim-entry bridge.

### Satisfying states and substitution

`evidence/stage4/precondition_witness.py` and its log exhibit satisfying
states for both claims:

- `HEAD=21`, `PREFIX=[3]`, `SUFFIX=[4000]` gives `arr=[21,3,4000]`,
  `k=2`, claimed/submitted/canonical result `24`.
- `HEAD=-99`, empty prefix and suffix gives `arr=[-99]`, `k=1`. Every
  entry precondition holds. The claimed and submitted result is `-99`, while
  the trusted canonical result is `0`.
- A loop-head witness uses empty globals, `ACC=0`, `V=-99`, empty tail,
  and therefore satisfies the no-shadow and integer-list preconditions.

The second witness proves that the K theorem accurately pins the submitted
program while simultaneously exposing its failure to establish canonical
task behavior.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5/k_inventory.py` generated the complete declaration inventory
in `evidence/stage5/k_inventory.log`. It enumerates each declaration with
source span and normalized text:

- 695 supplied semantic rules: 238 operational and 457 equational;
- 227 supplied syntax declarations, including 146 function declarations and
  107 declarations marked `total`;
- one configuration and five explicit contexts;
- 45 priority rules and 26 `owise` rules;
- 25 `symbol(...)` declarations, 22 also marked `no-evaluators`;
- no `functional` declarations;
- three proof-local function declarations, two marked `total`;
- fourteen proof-local equations, eight marked `simplification`; and
- both reachability claims.

The same log gives per-file counts and row-by-row contents. The candidate
semantics is byte-identical to the selected supplied semantics, so these 695
rules are fixed semantic baseline rather than candidate proof extensions.
All fixed rules were included in the inventory. Rules for unused constructs
are inert for this theorem; they cannot be reached from the submitted AST.

### Used construct map and control/state audit

The submitted constructs map as follows:

| Submitted construct | Declaration and operative fixed rules |
|---|---|
| `Module`, statement list | `syntax.k:56,61`; `core.k:124-127` |
| function/closure call | `syntax.k:53,57`; `functions.k:14-16`; direct entry uses the resulting `closureVal`; `call.k:20-21,69-74` |
| parameters | `functions.k:63-66` |
| `Assign`, `AugAssign` | `syntax.k:41,44`; `controls.k:9-11,20-23` |
| integer/name lookup | `syntax.k:9-12`; `core.k:130-154,194` |
| `arr[:k]` | `syntax.k:22,38-39`; `subscript.k:27-28,31-33,50-65,72-114` |
| list allocation/iteration | `core.k:117-121`; `list.k:9-10`; `controls.k:65-74,106-108`; target binding at `tuple.k:31-41` |
| `if` | strict declaration at `syntax.k:49`; `controls.k:51-54` |
| call to builtin `abs` | `call.k:20-32`; builtin lookup at `core.k:157-181`; `builtins.k:43-44` |
| `< 100` | `operators.k:15-17`; `int.k:22` |
| integer `+` | `int.k:9` |
| `return` | strict declaration at `syntax.k:50`; `functions.k:77-90` |

Evaluation order is preserved: strictness evaluates assignment RHS, loop
iterable, condition, augmented-assignment RHS, and return expression; calls
evaluate callee then arguments left to right. The function call allocates a
fresh local scope and pushes a frame. Slicing allocates a new list, the `for`
rule dereferences it once, each iteration binds `element`, the guarded branch
updates `total`, and return restores the caller and removes the local scope.
No output, exception, or abrupt-control behavior is bypassed. Python and K
integers are unbounded here. The entry's empty module globals ensure builtin
`abs` binding; the loop claim separately guards against shadowing.

The modules/rules for assertions, comprehensions, dictionaries, floats,
methods, ranges, sets, sorting, strings, and concrete keyed sorting have no
reachable redex in this AST. `MPY-CONCRETE` is not imported into the Haskell
proof main module.

### Proof-local rules

Every proof-local rule is individually classified and decided in
`evidence/stage5/proof_extension_review.md`. In summary:

- `intsOnly` is a complete, descending definition over constructor
  `ValSeq`s.
- `qualifyingSumAcc` has disjoint/exhaustive include and skip cases on
  integer heads and descends on the tail.
- `intValue(I:Int) => I` is truthful. Its `[total]` declaration is broader
  than its only equation, but every proof use is guarded by `isInt`; no
  noninteger value can influence the intended-domain result.
- The `abs` and integer-add refinements agree exactly with the fixed rules
  whenever `isInt(V)` holds.
- The four map-update simplifiers are the same-key and distinct-key laws of
  K's `Map`; guards are disjoint and values agree on overlaps.
- The `slAdjust` and `buildVS` prefix/suffix equations are mathematically
  valid for finite constructor sequences: lengths put the stop within bounds,
  and the supplied recursion selects exactly `HEAD :: PREFIX`.

There are no proof-local priority rules, operational `<k>` rewrites, abrupt
returns, state-cell rewrites, or fresh result oracles. No proof rule encodes a
result independently of executed program behavior.

The candidate did not provide bridge-free universal K connection claims for
the two refined-sort rules or the two slice accelerations. An auditor-authored
bridge-free definition builds (`evidence/stage5/connection_kompile.log`), but
the broad symbolic slice connection attempt does not close
(`evidence/stage5/connection_kprove_all.log`); even the generic
concat-length attempt is blocked by the supplied semantics' total/opaque
symbolic `ValSeq` treatment
(`evidence/stage5/connection_concat_length.log`). This is a connection-evidence
gap, not an observed false equation on a satisfying concrete input. Per the
required decision rule, no rule is labeled unsound without a false-conclusion
witness.

The fixed semantics declares the following 25 opaque/named symbols:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. None occurs in the submitted
AST, claims, proof-local summaries, or final result. The fixed semantics also
intentionally leaves `valSeqAt` abstract on opaque/out-of-bounds sequences;
the submitted slice is in bounds on finite input sequences.

Finally, the separate body-sensitivity mutation changes both executed
comparison constants from 100 to 99 while leaving the summary unchanged. It
builds successfully and then exits 1 with `WarnStuckClaimState`
(`evidence/stage5/body_sensitivity_dry_run.log` and
`evidence/stage5/body_sensitivity_proof.log`). Thus the proof is sensitive to
the real body rather than solely to a smuggled summary.

## 6. Fresh non-vacuity test

The fresh mutation in `evidence/stage6/spec-vacuity.k` changes the entry
result from:

```text
qualifyingSumAcc(0, vCons(HEAD, PREFIX))
```

to the deliberately false:

```text
qualifyingSumAcc(0, vCons(HEAD, PREFIX)) +Int 1
```

For the satisfying witness `HEAD=-99`, empty prefix/suffix, the original
result is `-99` and the mutation demands `-98`
(`evidence/stage6/mutation_witness.txt`).

The dry run parses and builds the mutation with exit 0
(`evidence/stage6/vacuity_dry_run.log`). The actual proof exits 1, reports
`WarnStuckClaimState`, and retains the expected unmet condition that
`qualifyingSumAcc(...) +Int 1` is not equal to
`qualifyingSumAcc(...)` (`evidence/stage6/vacuity_proof.log`). This is a
meaningful result-obligation failure, not a parser error, missing import,
timeout, unreachable mutation, or unrelated crash.

## 7. Proven versus assumed accounting

### What is formally established

Under the rebuilt supplied semantics plus the fourteen equations in
`verification.k`, the reachability proof establishes partial correctness of
the exact submitted function body:

> For every nonempty finite integer sequence decomposed as
> `HEAD :: PREFIX ++ SUFFIX`, with total length at most 100 and
> `k = len(HEAD :: PREFIX)`, if the submitted call terminates, it returns the
> accumulator sum of precisely those first-`k` elements whose absolute value
> is less than 100.

It does not prove termination, although all concrete finite inputs in scope
do terminate operationally. It does not prove the trusted canonical's
string-length predicate for all integers.

### Assumptions and trust boundaries

1. **K toolchain and hooks.** K v7.1.337, its reachability prover, and the
   imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, and `K-EQUAL` hooks are
   trusted. Result-dependent primitives used here are `isInt`, `absInt`,
   integer arithmetic/comparison, structural equality, and map
   update/lookup/membership.
2. **Supplied semantics.** The entire trusted supplied semantics is fixed
   outside the candidate proof. Candidate identity was verified byte for
   byte. Its unrelated opaque float/sort/digest symbols are listed above and
   are inert for this theorem.
3. **Translator.** The mounted translator is trusted as the Python-to-MPY
   bridge. Candidate identity and output byte identity were checked, but this
   audit does not formally verify the translator implementation.
4. **Direct closure entry.** Exact-body syntactic pinning, fixed call-frame
   rules, and the absence of decorators/captures justify starting at the
   closure call instead of module loading. This is an informal adequacy
   argument, not a separate reachability theorem for `FuncDef`.
5. **Unboxed read-only input list.** The supplied semantics explicitly
   permits bare list values in claims. Read-only use of `arr`, fresh slice
   allocation, concrete execution, and existential final heap support this
   bridge.
6. **Proof-local pure accelerations.** The refined-sort, map, and slice
   simplifiers are statically justified on concrete finite integer sequences.
   The candidate lacks universal bridge-free K connection theorems; the
   failed broad auditor attempts are retained as a validation limitation.
7. **Empirical evidence.** Fresh concrete K execution supports operational
   fidelity only for the recorded cases. The 510-case Python differential
   supports—and in fact refutes—the canonical bridge on those cases. Neither
   finite test replaces the K reachability proof.

### Gate accounting

- Real-program soundness: **PASS with validation concern**. The proof executes
  the exact body, closes freshly, constrains the result, rejects body/result
  mutations, and no false proof-local equation witness was found. Universal
  K connection claims for pure symbolic accelerations are missing.
- Intent adequacy: **FAIL**. `[-99], 1` satisfies the source domain but the
  proved/submitted result differs from the trusted canonical.
- Trust/evidence auditability: **PASS with provenance concern**. Commands,
  source mutations, statuses, and bounded outputs are preserved, but the four
  requested candidate generation records and structured trace are absent.

The intent failure prevents `PASS`, but because the proof honestly and
non-vacuously establishes the behavior of the real submitted program, it
does not make the K proof itself illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
