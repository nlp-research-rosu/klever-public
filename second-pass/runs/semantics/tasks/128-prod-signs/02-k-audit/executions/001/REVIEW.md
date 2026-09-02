# Independent adversarial audit: 128-prod-signs

## Executive decision

The candidate reconstructs to `#Top`, the submitted Python program matches the
trusted canonical implementation on extensive finite testing, and the claims
are result-constraining. It is nevertheless **not a legitimate proof** under
the supplied semantics.

The decisive defect is the priority-40 loop rule at
`/candidate/verification.k:74`. It is an operational bridge whose match domain
is broader than the fixed-semantics transition it claims to replace. On the
valid integer list `[5]`, in a well-formed frame where the loop target `value`
is a closure cell, the rule concludes that the scope binding becomes the
integer `5` while the heap cell remains `99`. Fixed semantics instead preserves
the `cellRef(0)` binding and updates heap cell 0 to `5`.

This is a machine-checked false-conclusion witness:

- With the candidate bridge, the false transition proves `#Top`, exit 0:
  [cell-witness-bridge-spec.k](evidence/cell-witness-bridge-spec.k) and
  [cell-witness-bridge.log](evidence/cell-witness-bridge.log).
- With the bridge removed and only supplied semantics present, the identical
  claimed transition is rejected, exit 1. The residual displays the actual
  fixed result—`"value" |-> cellRef(0)` and `0 |-> cellV(5)`:
  [cell-witness-fixed-spec.k](evidence/cell-witness-fixed-spec.k) and
  [cell-witness-fixed.log](evidence/cell-witness-fixed.log).

The submitted function itself reaches a plain, non-cell frame, but that does
not validate a globally false ordinary rewrite. The Kit extension-soundness
contract specifically requires equivalence over the bridge's complete match
domain; an off-path false rule must be narrowed before its `#Top` can be used.

All audit execution occurred in
`/tmp/audit-work/128-prod-signs.HMXf22`. Nothing from a
candidate-provided compiled definition or cache was copied or reused.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`SUPPLIED_SEMANTICS` was requested and
`/reference/reference-semantics` is present. There is no infrastructure breach.

The recursive, no-dereference comparison of
`/candidate/reference-semantics` against the trusted tree returned exit 0.
There are no symlinks in either semantics tree and no missing, added, or
changed entries. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted mounted versions. `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are regular files, not symlinks.

Four requested generation-provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present at candidate top level. These
omissions limit provenance review but are not an infrastructure contradiction.
The complete checks, source SHA-256 values, command, and status are in
[stage1_integrity.sh](evidence/stage1_integrity.sh) and
[stage1-integrity.log](evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for a nonempty integer array, add the magnitudes of
all elements and multiply that sum by the product of their signs, where each
sign is `-1`, `0`, or `1`; return `None` for the empty array.

The trusted canonical function computes the same value using `abs`, negative
parity, and a zero-membership test. Candidate `solution.py` uses a single loop:
negative elements add `-value` and flip `sign`; nonnegative elements add
`value`, with zero setting `sign` to zero. The branches cover all Python
integers and preserve the contract.

The submitted `solution.mpy` was independently regenerated using
`/reference/py2mpy.py`. `cmp` returned exit 0, establishing byte identity; see
[translate.log](evidence/translate.log).

The independent differential test imported the trusted canonical entry point
and the scratch copy of the candidate entry point. Its scope was:

- 16 named documented, empty, branch-boundary, large-integer, and long-list
  cases;
- every array of lengths 0 through 5 over integers `[-3,3]`—19,608 cases;
- 1,000 seeded generated arrays of lengths 0 through 20 and values in
  `[-1,000,000,1,000,000]`.

All 20,624 cases also went through a separately written contract oracle.
There were zero result mismatches and zero input mutations. The exact script,
all JSONL inputs, empty mismatch file, summary, and command/status are
[differential_test.py](evidence/differential_test.py),
[differential-inputs.jsonl](evidence/differential-inputs.jsonl),
[differential-mismatches.jsonl](evidence/differential-mismatches.jsonl),
[differential-summary.json](evidence/differential-summary.json), and
[differential.log](evidence/differential.log). This is finite implementation
evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

The live toolchain was K v7.1.337; exact binaries and versions are recorded in
[toolchain.log](evidence/toolchain.log).

Fresh source builds were performed with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

kompile verification.k --backend haskell \
  --main-module PROD-SIGNS-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exited 0. Logs are
[kompile-runtime.log](evidence/kompile-runtime.log) and
[kompile-verification.log](evidence/kompile-verification.log).
The runtime build reported fixed-semantics non-exhaustiveness warnings for
several unused helpers; the proof build reported only unused-variable warnings.

Every positive entry claim was then run independently:

| Target | Result | Evidence |
|---|---:|---|
| All claims together | `#Top`, exit 0 | [kprove-all.log](evidence/kprove-all.log) |
| `PROD-SIGNS-SPEC.prod-signs-empty` | `#Top`, exit 0 | [kprove-empty.log](evidence/kprove-empty.log) |
| `PROD-SIGNS-SPEC.prod-signs-nonempty` | `#Top`, exit 0 | [kprove-nonempty.log](evidence/kprove-nonempty.log) |

Concrete execution of the actual submitted `solution.mpy` also exited 0 and
loaded `prod_signs` as the expected closure in module scope:
[krun-solution-load.log](evidence/krun-solution-load.log). These successful
runs establish closure only under the compiled theory; Stage 5 shows that the
candidate extension in that theory is invalid.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`prod-signs-empty` begins from the normal module/builtins configuration with no
heap objects, calls the submitted closure on the bare empty list, and requires
the call to finish as `noneV`. It also pins the expected allocation of the
empty list constructed by `arr == []`, the heap counter, restored environment,
empty call stack, no return marker, no exception, and exit code zero.

`prod-signs-nonempty` begins from the same configuration on
`vCons(I:Int, VS)` and requires `allInts(VS)`. Thus it covers every nonempty
finite integer list. It requires the call to finish as the exact integer
`magnitudeSum(vCons(I,VS)) *Int signProduct(vCons(I,VS))` and pins the same
configuration effects. The result is not a free variable, tautology, or
one-way implication.

### Satisfying states and concrete substitution

The empty initial configuration written in the claim with input `.ValSeq`
satisfies the empty precondition, which has no `requires` clause. For the
nonempty claim, `I = 1` and
`VS = vCons(2,vCons(2,vCons(-4,.ValSeq)))` satisfy `allInts(VS) = true`.
Substitution yields magnitude `9`, sign product `-1`, and result `-9`.

Additional satisfying witnesses cover zero and positive outcomes. Every
instantiated formal result equals both Python implementations:
[ground_witnesses.py](evidence/ground_witnesses.py) and
[ground-witnesses.log](evidence/ground-witnesses.log).

### Pinning to the submitted program

The `<k>` cell calls `prodSignsFunction`, a macro for a closure rather than
loading the module file during proof. This does not substitute a different
algorithm here: the trusted translation reproduced `solution.mpy`
byte-for-byte, and the closure printed by concrete loading of that exact file
matches the macro's parameters, statement sequence, docstring expression,
defining environment 0, and return. The proof therefore pins the submitted
function body, subject to the invalid loop bridge assessed next.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and used-construct map

The machine-generated inventory covers `semantics.k`, all 23 files under
`reference-semantics/semantics/`, and `verification.k`: 25 files, 1,086
declaration records, including 711 ordinary rules, 232 syntax declarations,
five contexts, one configuration, 149 function declarations, 111 total
attributes, 46 priority rules, 35 concrete rules, 25 named symbols, and 22
`no-evaluators` opaque symbols. The exact file/line/text/attribute inventory
and generation command are
[rule-inventory.tsv](evidence/rule-inventory.tsv),
[rule-inventory-summary.json](evidence/rule-inventory-summary.json),
[rule_inventory.py](evidence/rule_inventory.py), and
[rule-inventory.log](evidence/rule-inventory.log).

The 1,062 supplied-semantics records are the selected fixed semantics and were
confirmed byte-identical to the trusted baseline. Rules outside the import
closure or constructs unused by this program cannot contribute to the target
claims. The constructs that do contribute map as follows:

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module sequencing in `core.k`; closure creation in `functions.k` |
| `Call`, argument evaluation | `call.k` plus the left-to-right `#evalArgs` loop in `core.k` |
| Function frame, parameter, return | `call.k` frame entry; `functions.k` binding, `Return`, `#pop` |
| Docstring `Expr(Str(...))` | `str.k` literal; discarded-expression rule in `controls.k` |
| `Name`, `Assign` | scope lookup in `core.k`; plain and cell-aware assignment in `controls.k` |
| `ListExpr`, list equality | allocation/iteration/equality in `list.k`; comparison dispatch and reference dereference in `operators.k` |
| `If`, truthiness | strict syntax; `#branch` and list dereference in `controls.k`; `truthy` in `core.k` |
| `For` and loop target | `#loop` protocol in `controls.k`; list `#iterNext` in `list.k`; `#bindTgt` plain/cell rules in `tuple.k` |
| Integer literals, `+`, `-`, `*`, `<`, `==` | dispatch in `operators.k`; exact unbounded-integer equations in `int.k` |

Configuration cells, evaluation order, frame allocation/restoration,
environment lookup, the one list allocation caused by the empty-list
comparison, normal control completion, and returned value all align on the
actual path.

### Candidate-local extensions

Every local declaration and equation is assessed individually in
[candidate-extension-review.tsv](evidence/candidate-extension-review.tsv).
The main findings are:

- `allInts` is exhaustive and sound.
- `magnitudeAcc` and `signAcc` use disjoint, descending integer cases and
  truthfully compute the magnitude and sign folds on the entry domain.
- `magnitudeSum`, `signProduct`, and `lastInt` are truthful on their uses.
  Their `[total]` annotations are broader than their equations: non-integer
  sequences are not covered by the folds, and `lastInt` has no empty or
  non-integer case. This is a narrower off-domain coverage defect, not the
  false-conclusion witness used for the verdict.
- `prodSignsFunction` is an exact macro alias for the submitted closure.
- There are no candidate-local simplification rules, explicit `functional`
  declarations, or opaque symbols.

### Materially unsound operational bridge

The rule at `verification.k:74-105` preempts ordinary `For` execution and
updates `M["total"]`, `M["sign"]`, and `M["value"]` directly. Its guards require
integer list elements and integer accumulator bindings, but do **not** exclude
a `$cells` frame or require that `value` is an ordinary binding.

Concrete false-conclusion witness:

```text
input list: [5]
scope before:
  "$cells" |-> cellsMark("value")
  "value"  |-> cellRef(0)
  "total"  |-> 0
  "sign"   |-> 1
heap before: 0 |-> cellV(99)

candidate bridge conclusion:
  "value" |-> 5, "total" |-> 5, "sign" |-> 1
  heap remains 0 |-> cellV(99)

fixed-semantics conclusion:
  "value" |-> cellRef(0), "total" |-> 5, "sign" |-> 1
  heap becomes 0 |-> cellV(5)
```

The bridge-enabled false claim closes with `#Top`; the bridge-free claim fails
and prints the fixed conclusion. This is not merely an absent proof or an
informal concern: it is a demonstrated false transition enabled by the rule on
an intended-domain integer list.

A separate bridge-free ground run on the plain-frame list `[-2,0,3]`, including
an observable continuation assignment, reaches `#Top`:
[loop-continuation-plain-spec.k](evidence/loop-continuation-plain-spec.k) and
[loop-continuation-plain.log](evidence/loop-continuation-plain.log). That
supports the arithmetic summary on one actual-style state, but finite ground
agreement cannot establish the required universal connection over the
candidate rule's broader match domain. The attempted complete bridge-free
connection exposes the cell branch in its residual:
[loop-connection-spec.k](evidence/loop-connection-spec.k) and
[loop-connection.log](evidence/loop-connection.log).

The priority bridge is therefore materially unsound and blocks real-program
proof validation.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. A fresh spec changed the
nonempty result obligation to:

```text
(magnitudeSum(input) *Int signProduct(input)) +Int 1
```

Input `[1]` satisfies the original entry precondition; both Python functions
and the original formal expression return `1`, while the mutation demands `2`.

The mutated spec successfully parsed and built through `kprove --dry-run`,
exit 0: [vacuity-dry-run.log](evidence/vacuity-dry-run.log). The real proof run
then exited 1 with `WarnStuckClaimState`; its residual is precisely the failed
implication `result +Int 1 = result`:
[spec-vacuity.k](evidence/spec-vacuity.k) and
[vacuity-proof.log](evidence/vacuity-proof.log).

This establishes non-vacuity of the result obligation. It does not cure the
unsound operational rule.

## 7. Proven versus assumed accounting

The successful reachability runs establish the following only **inside the
candidate-extended theory**:

- the exact submitted closure returns `noneV` on the empty list; and
- on a nonempty integer list, it returns the product of the two recursively
  defined fold summaries.

Because the nonempty symbolic execution is accelerated by a false ordinary
rewrite, that theory result is not a sound partial-correctness proof under the
selected fixed semantics.

Trust and assumption ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical function, and translator | Natural-language intent and source-to-`.mpy` bridge | Acceptable trusted inputs; byte identity and finite differential evidence recorded |
| Supplied MPY semantics tree | All program execution | Acceptable selected fixed semantics; candidate copy is exact and unsymlinked |
| K v7.1.337, Haskell/LLVM backends, K integer/map theories | Compilation, concrete execution, and reachability | Necessary toolchain trust; exact versions and statuses recorded |
| `allInts`, magnitude/sign folds, `lastInt` | Formal domain and claimed mathematical result | Equations are valid on every target use; totality attributes have documented off-domain coverage gaps |
| Direct closure macro | Pinning the call to `solution.mpy` | Acceptable here because trusted regeneration and concrete closure loading establish exact syntax and environment |
| Priority loop-summary rule | Skips the property-bearing loop and supplies all final accumulator values | **Illegitimate**: no bridge-free theorem covers its complete domain, and the cell witness proves a false transition |
| Supplied opaque symbols `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `md5hexCodes` | Potential symbolic results in other programs | None occurs in this program, its claims, or their proof path; therefore none supports the result |
| Differential and ground tests | Python-to-contract and selected fixed-execution evidence | Empirical only; explicitly not treated as a universal theorem |
| Missing generation metadata | Provenance auditability | Concerning but not the basis of the soundness verdict |

The proof is result-constraining and non-vacuous, and it pins the submitted
function body. It fails the more fundamental soundness gate because a
proof-contributing operational rule can prove a concrete false state
transition.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
