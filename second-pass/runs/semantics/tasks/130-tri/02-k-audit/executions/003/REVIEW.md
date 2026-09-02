# Independent adversarial review: HumanEval 130 `tri`

This audit was performed from source in `/tmp/audit-work/130-tri-audit`. No
candidate-compiled definition, cache, prior `#Top`, prose report, or generation
trace was trusted. The required `using-kit` and `validating-proof` procedures
were applied. Because the rendered mode is `SUPPLIED_SEMANTICS`,
`writing-semantics` was intentionally not used.

The proof is legitimate but has a non-fatal specification/auditability
limitation: its universal postcondition describes the returned list through an
underdefined, non-injective `prefixIndex` certificate rather than a structural
equality or a proved equivalence to the recurrence sequence. The certificate is
not vacuous—it is exercised by the real body, a changed computed value breaks
the proof, and an off-by-one result mutation is rejected—but the final
certificate-to-English-contract direction remains informal. A second,
non-material discrepancy is that the rewrite returns integer elements whereas
the trusted CPython canonical happens to produce equal-valued floats after
index 1.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `130-tri`, condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I read the launcher-owned audit input and campaign lock, `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, both legacy
records present in the evidence bundle, and the structured JSONL trace. Runtime
metrics are not required for this legacy-selected layout. The generation
records were treated only as untrusted historical claims.

The independent integrity script and complete output are
[`stage1_integrity.py`](evidence/stage1_integrity.py) and
[`stage1_integrity.log`](evidence/stage1_integrity.log). Results:

- the campaign lock JSON exactly equals the `audit_campaign` block;
- its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the launcher-recorded value;
- all launcher-recorded hashes for the run/task/result/invocation, generation
  prompt/metrics/usage/output/last message, canonical, trusted prompt, and
  translator match the mounted bytes;
- all evidence hashes repeated in `invocation.json` and
  `generation-result.json` match;
- the sole trace file has its declared hash, and all 584 JSONL records parse;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts;
- all five required proof deliverables are regular, readable files; their
  independent hashes are recorded in the log;
- the full candidate mount and supplied-semantics subtrees contain no symlink.

The required trusted `/reference/reference-semantics` is present. A recursive
name/type/content manifest over every candidate and trusted entry is identical:
25 entries, zero missing, extra, changed, mistyped, or symlinked entries. The
reviewer-defined manifest digest is
`787e8f4a6abd5bff9e8cdcde0d26ceff912311986b52bd8a67d2b45279f58b37`
on both trees. This independently confirms the launcher’s supplied-semantics
integrity assertion; proof-specific rules remain separately audited below.

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires, for every non-negative integer `n`, a list of
values at indices `0..n`. The bases are `T(0)=1`, `T(1)=3`; even indices use
`T(i)=1+i/2`; odd indices use
`T(i)=T(i-1)+T(i-2)+T(i+1)`. The documented example is
`tri(3) = [1,3,2,8]`.

The candidate implements the same recurrence with a `while` loop and scalar
locals holding the previous two values. For odd `i`,
`1 + (i+1)//2` is exactly the following even value `T(i+1)` on this domain.
The use of `//` is exact because all divisions are by 2 at non-negative even
arguments.

The scratch preparation record is
[`prepare_scratch.log`](evidence/prepare_scratch.log). It copies candidate
source/proof files, the trusted canonical/prompt/translator, and the trusted
supplied semantics, but no compiled definition or cache.

Trusted regeneration is recorded in
[`stage2_fidelity.log`](evidence/stage2_fidelity.log). The submitted and
regenerated `solution.mpy` are byte-identical, both with SHA-256
`981dfdba56e992c7f3c332501505f3eccf7c04c752418534a06c9ce2874544e6`.

The independent differential oracle is
[`differential_test.py`](evidence/differential_test.py). It imports the trusted
canonical and candidate independently and checks:

- `n=0`, no-loop `n=1`, first even `n=2`, first odd `n=3`;
- subsequent even/odd boundaries and the documented example;
- fixed medium boundaries through 256;
- 120 seeded generated values in `0..1000`.

There were 134 distinct inputs, zero value mismatches, and zero direct
recurrence/length failures. There were 132 element-type-shape differences:
for `n=3`, canonical gives `[1,3,2.0,8.0]`, while the candidate gives
`[1,3,2,8]`. Python list equality and the mathematical/prompt values agree;
the prompt does not require floating element types, so this is a representation
limitation rather than a material result divergence.

## 3. Clean proof reconstruction

Before building, the scratch tree contained no `*-kompiled`, KORE, or temporary
kompile artifact. K version `7.1.293` was independently available.

The exact build/proof commands, statuses, bounded output, and paths to full logs
are in [`stage3_reconstruction.log`](evidence/stage3_reconstruction.log):

1. Fresh LLVM build of trusted `reference-semantics/semantics.k`, main module
   `MPY-KRUN`, syntax module `MPY-SYNTAX`: exit 0.
2. Fresh Haskell build of copied `verification.k`, main module
   `TRI-VERIFICATION`, syntax module `MPY-SYNTAX`: exit 0.
3. `kprove` of `TRI-LOOP-SPEC`: exit 0, exactly one `#Top`.
4. `kprove` of `TRI-CORRECT-SPEC`: exit 0, exactly one `#Top`.

The complete positive outputs are
[`stage3_loop_claim.full.log`](evidence/stage3_loop_claim.full.log) and
[`stage3_entry_claim.full.log`](evidence/stage3_entry_claim.full.log).
Thus every positive target claim independently closes under a fresh definition.

The first reviewer-authored concrete assertion file used the wrong constructor
shape for `Compare` and failed in parsing. That failed attempt remains visible
in the reconstruction log and is not candidate evidence. After correcting only
the reviewer test syntax, the same fresh LLVM definition executed assertions at
`n=0,1,2,3,4,5,10,25` with exit 0; see
[`runtime_checks.mpy`](evidence/runtime_checks.mpy) and
[`stage3_concrete_retry.log`](evidence/stage3_concrete_retry.log). These cover
zero iteration, initialization, and both branches.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim starts immediately before iteration `I`, with:

- `I >= 2`, `R >= 0`, and `n = I+R-1`, hence exactly `R` remaining iterations;
- `a=T(I-2)`, `b=value=T(I-1)`;
- the heap list satisfying `prefixIndex(VS)=I-1`.

It executes the real `#while` guard/body, preserves the caller continuation and
non-target cells, and concludes `i=I+R` with the resulting list certified
through `I+R-1`.

The entry claim starts from the exact module-level environment, builtins frame,
empty heap, empty stack, normal return/exception/exit state, and arbitrary
`N >= 0`. It calls a closure with parameter `n`, the exact submitted function
body, and defining scope 0. It concludes that the call returns `ref(0)`, the
heap contains a list at 0, allocation advances once, and
`prefixIndex(result)=N`.

Both preconditions are realizable. For the entry claim, `N=0` and `N=3` are
concrete examples. For the loop claim, take `I=2`, `R=1`, `n=2`,
`VS=[1,3]`, `a=1`, `b=value=3`, and `i=2`; all conditions hold and the even
branch is reachable.

### Mechanical program identity

The claim is allowed to call the exact closure directly rather than execute the
whole module load. I mechanically removed only the `Module(FuncDef(...))`
wrapper from trusted-regenerated `solution.mpy`, parsed that body and
`TriFunctionBody` with the fresh definition, expanded macros, and compared KAST
JSON. The files are byte-identical, both SHA-256
`ee788cb77842288a7d80ded1945ca0ba5992ca206bd642d278556f36a7f4fe30`.
The closure parameter list `("n", .ParamNames)` and defining scope 0 also match
the submitted `FuncDef`. Commands and artifacts are in
[`stage4_body_pinning.log`](evidence/stage4_body_pinning.log).

This constructor comparison covers the condition, both branch expressions,
append call, scalar updates, increment, early return, and final return. No
material source construct is omitted.

### Concrete substitution and sensitivity

Independent finite K claims substitute `N=0` and `N=3` and demand the exact
heap lists `[1]` and `[1,3,2,8]`; both close together with `#Top`:
[`stage4_concrete_substitution.k`](evidence/stage4_concrete_substitution.k) and
[`stage4_concrete_substitution.log`](evidence/stage4_concrete_substitution.log).
Those lists equal both Python implementations by value.

A body-sensitivity mutation changed the constructor actually executed by the
claim, from even `1+i//2` to `2+i//2`. Its expanded body hash differs, the
mutated definition builds, and the loop proof exits 1 with
`WarnStuckClaimState` on the appended `I/2+2` value. The valid retry is
[`stage5_body_sensitivity_retry.log`](evidence/stage5_body_sensitivity_retry.log).
The earlier malformed reviewer script attempt is preserved separately and was
not counted.

The remaining limitation is not program pinning but result description.
`prefixIndex(result)=N` is a sufficient inductive certificate generated only
from correct bases and correct appends in this proof, but the candidate supplies
no converse theorem saying every sequence with that index is structurally the
unique recurrence prefix. Because `prefixIndex` is total and underdefined on
other sequences, the final formula itself is not an injective characterization.
The dynamic, concrete-K, and sensitivity results support the informal bridge;
they do not turn it into a universal equivalence theorem.

## 5. Rule-by-rule static soundness review

The exhaustive raw inventory is
[`k_declaration_rule_inventory.txt`](evidence/k_declaration_rule_inventory.txt);
per-file counts are
[`k_inventory_summary.tsv`](evidence/k_inventory_summary.tsv); and every file
and every one of the 16 proof-local rules is classified in
[`static_rule_ledger.md`](evidence/static_rule_ledger.md). The inventory covers
695 supplied rules, all syntax/configuration/context/priority/total/function/
opaque declarations, the 16 local rules, and both claims.

The used semantic path is:

```text
closure call / parameter binding
  -> exact If and scalar initialization
  -> fresh list allocation
  -> exact while guard
  -> integer %, //, + and comparisons
  -> in-place heap append
  -> scalar assignments and increment
  -> loop circularity
  -> exact return / frame pop
```

The fixed rules enforce left-to-right argument/list evaluation, current-scope
lookup and writes, monotonic heap allocation, one-location append mutation,
guard re-evaluation, and proper call/return control. Every material cell is
present in the claims. There is no proof-local call interception, priority
rule, abrupt control bridge, fabricated allocation, or unmodeled used
construct.

The proof-local findings are:

- `triAt` is a definitional mathematical summary. The base, even, and odd
  equations are true on every guard. Duplicate backend-normalized equations
  agree on overlap and cover every reached non-negative index.
- `prefixIndex` has true base and append-certificate equations. It does not
  replace append execution; it summarizes the resulting symbolic list.
- `triPrefix` and its three related rewrites are dead scaffolding. A fresh
  definition deleting the constructor and every related rule still proves both
  target modules with `#Top`; see
  [`stage5_minimal_dependency.log`](evidence/stage5_minimal_dependency.log).
- A proposed false-state witness demanding that `n=0` return the synthetic
  `triPrefix(0)` heap was rejected with the concrete `[1]` residual by both the
  candidate and a bridge-free definition. This is recorded in
  [`stage5_bridge_witness.log`](evidence/stage5_bridge_witness.log). Therefore
  I do not misclassify the dead `vCons -> triPrefix` rule as a contributing
  unsound operational bridge.
- Opaque float, sorting, digest, and other supplied primitives are unused and
  have no target dependents.

No rule was labeled unsound: I found no concrete or symbolic false conclusion
witness enabled by a rule on the intended domain. The concern is narrower:
the `prefixIndex` equations are sufficient but not a formal converse, leaving
the human meaning of the postcondition less auditable than a structural
sequence predicate.

## 6. Fresh non-vacuity test

The fresh mutation changes only the entry result obligation from
`prefixIndex(result)=N` to the false
`prefixIndex(result)=N+1`. `N=0` is a satisfying input and returns `[1]`, whose
base summary is 0.

Artifact and record:

- mutated spec: [`spec_vacuity.k`](evidence/spec_vacuity.k);
- exact commands and bounded outputs:
  [`stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log);
- full mutation proof output:
  [`stage6_vacuity_proof.full.log`](evidence/stage6_vacuity_proof.full.log).

`kprove --dry-run` exits 0, so the mutation parses and builds. The actual proof
exits 1 with `WarnStuckClaimState`; the residual is the normal returned heap
`0 |-> list(vCons(1,.ValSeq))` under `N=0`, and the implication to the
off-by-one obligation fails. There is no parse failure, missing import, timeout,
or unrelated backend crash. The target proof is non-vacuous.

## 7. Proven versus assumed accounting

### What the machine proof establishes

Under the supplied MPY semantics plus the audited local equations, for every
mathematical integer `N >= 0`, partial correctness of the exact submitted
closure is established: if execution reaches its return, it returns the sole
fresh list reference, leaves normal return/exception/exit state, and the actual
heap sequence has the inductive certificate `prefixIndex=N`. The independently
proved loop circularity covers an unbounded number of iterations; there is no
fixed-size unrolling or domain narrowing.

The proof also formally checks that the program appends `triAt(I)` at each
iteration, where `triAt` obeys the required base/even/odd equations. It does
not formally state a universal structural equality between the returned
`ValSeq` and a recursively constructed canonical `ValSeq`.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover and builtin Int/Bool/Map/List theories | All machine results | Ordinary toolchain trust; fresh builds and exact exits/outputs are preserved. |
| Trusted supplied MPY semantics | Program execution | Integrity is exact. The complete inventory was reviewed; the used slice models every material operation. |
| Trusted translator | Program-to-constructor bridge | Byte regeneration and expanded constructor comparison discharge this mechanically for the immutable candidate. |
| `triAt` proof-local function | Loop values and append certificate | Acceptable definitional summary: guarded exhaustive equations on every reached index, mathematically checked for truth and overlap. |
| `prefixIndex` proof-local total function | Loop invariant and final postcondition | Concerning but not illegitimate: matched equations provide a discriminating inductive certificate, but no converse/injectivity theorem makes it equivalent to exact list contents. |
| `triPrefix` constructor/rules | None after dependency test | Dead scaffolding; no target proof dependency and no successful false-state witness. |
| Opaque float/sort/digest primitives in supplied modules | None | Irrelevant to both target claims. |
| Differential and concrete tests | Python equivalence and intent bridge only | Finite evidence over the recorded scope, never substituted for the universal K proof. |
| Canonical float versus candidate integer representation | Source-intent alignment | Equal mathematical/list values, but different element types after index 1; prompt examples support integer values. Non-fatal limitation. |

Gate A (real-program soundness) passes: fixed execution is used, body identity
is mechanical, helper and entry proofs close independently, body sensitivity
holds, and the false result is rejected. Gate B covers the full source domain
and recurrence, with the documented non-fatal `prefixIndex` intent bridge and
numeric representation caveat. Gate C passes: all commands, mutations, source
artifacts, and bounded/full outputs are present.

Under the benchmark decision boundary, those limitations prevent an
unqualified `PASS` but do not make a false conclusion provable, substitute a
program, narrow the HumanEval domain, or render the theorem vacuous.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
