# Adversarial audit: 73-smallest-change

The candidate does not contain a legitimate partial-correctness proof of the
submitted program. Fresh reconstruction confirms that all candidate claims do
print `#Top`, the submitted Python implementation agrees with the canonical
implementation on extensive finite testing, and the proof macros contain the
exact submitted constructor bodies. The fatal issue is after that point:
priority rules replace both exact closure calls with a separately hand-written
`#targetCall` machine. The only “bridge” claims close by those same rules; there
is no bridge-free execution theorem. Fixed call dispatch, binding, body
evaluation, indexing/equality, recursion, return, and frame control are not
proved.

This is not merely a documentation limitation. A public-body sensitivity
mutation changes the closure actually matched by the claim to `return 999`, yet
the bridge theory still proves result `0` for the valid empty-list input. The
unmodified local rules also prove a concrete false result on their declared
formal `mainCall` domain: fixed Python and freshly rebuilt fixed K return `0`
for `[[5], [5]]` by structural equality, while the candidate theory proves `1`
because its target machine compares the two distinct inner references using
raw `==K`.

## 1. Input and provenance integrity

Status: **PASS (audit infrastructure intact).**

`/audit-input.json` declares:

- problem `73-smallest-change`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- mounted paths under `/candidate`, `/reference`, and
  `/generation-evidence`.

I read the launcher envelope, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and every required generation record
for this layout: `invocation.json`, `metrics.json`, `usage.json` (present),
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete structured
trace. The trace contains one 798,609-byte/422-line JSONL file; every line
parsed. The generation records claim `KPROVE_PASSED`, but that claim was not
used as proof evidence.

The campaign block is structurally identical to the campaign lock, and the
lock SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All launcher-recorded hashes for the run/task/result manifests, generation
records, canonical source, prompt, and translator match the mounted bytes. The
embedded task block in the audit envelope has one launcher-added top-level
`config` field; all shared fields match `/task.json`, whose recorded file hash
also matches.

The supplied-semantics boundary is consistent: trusted
`/reference/reference-semantics` exists. A recursive type-and-byte comparison
of its 25 entries against `/candidate/reference-semantics` found no missing,
additional, changed, mistyped, or symlinked entry. No symlink exists anywhere
in the inspected provenance, reference, generation, or candidate mounts. The
candidate prompt and translator are byte-identical to their trusted versions.

Evidence:

- [stage1 integrity checker](evidence/stage1_integrity.py)
- [complete integrity result and hashes](evidence/stage1-integrity.log)

There is no infrastructure contradiction, so a candidate verdict is
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS for implementation fidelity.**

The trusted contract asks for the minimum number of individual element changes
needed to make a finite array of integers palindromic. Each unequal mirrored
pair requires exactly one change and each equal pair requires none, so the
answer is the number of unequal mirrored pairs. Empty and singleton arrays have
answer zero. The source contract contains no finite size bound.

The canonical implementation iterates over the first half and counts unequal
mirrored pairs. The candidate implements the same recurrence:

- return zero when `left >= right`;
- compare `arr[left]` and `arr[right]`;
- recurse on `(left + 1, right - 1)`, adding one exactly for a mismatch;
- call the helper initially at `(0, len(arr) - 1)`.

Using the trusted `/reference/py2mpy.py` in scratch regenerated
`solution.mpy` with exact byte identity. Both submitted and regenerated files
have SHA-256
`3149f2b775bce3cf3815542741c6b54072b1e070bbd9af809d6f9d01da78b06f`.

The independent differential test compares the trusted canonical entry point,
the candidate entry point, and a third mirrored-pair oracle. It covers:

- all three documented examples;
- empty, singleton, even/odd, equal/mismatching boundary cases;
- negative and arbitrary-precision integers;
- every list of length 0 through 7 over `{-2,-1,0,1,2}` (97,656 cases);
- 1,000 deterministic random lists of lengths 0 through 100.

All 98,670 cases agree, with zero mismatches.

Evidence:

- [scratch-copy log](evidence/stage2-prepare.log)
- [trusted regeneration and byte comparison](evidence/stage2-fidelity.log)
- [differential script](evidence/differential_test.py)
- [differential results](evidence/stage2-differential.log)

These tests support source equivalence only on their finite sample. They are
not a K proof and are not used as a universal execution bridge.

## 3. Clean proof reconstruction

Status: **PASS mechanically under the candidate theory.**

All builds and execution occurred in
`/tmp/audit-work/73-smallest-change`, copied from source artifacts only.
Candidate compiled definitions and caches were not copied or reused. The live
toolchain reports K `v7.1.293`.

Fresh commands and outcomes:

1. LLVM compilation of the supplied semantics with main module `MPY-KRUN` and
   syntax module `MPY-SYNTAX`: exit 0.
2. Concrete execution of the candidate’s translated assertion program: exit
   0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0.
3. Haskell compilation of `verification.k` with main module `VERIFICATION`:
   exit 0.
4. Full `SPEC` proof: `#Top`, exit 0.
5. Each claim independently selected:
   `SPEC.public-entry-bridge`, `SPEC.helper-entry-bridge`, and
   `SPEC.smallest-change-correct` each printed `#Top` and exited 0.

Evidence:

- [LLVM build](evidence/stage3-kompile-llvm.log)
- [concrete run](evidence/stage3-krun-concrete.log)
- [Haskell build](evidence/stage3-kompile-haskell.log)
- [all claims together](evidence/stage3-kprove-all.log)
- [public bridge](evidence/stage3-kprove-public-entry-bridge.log)
- [helper bridge](evidence/stage3-kprove-helper-entry-bridge.log)
- [correctness claim](evidence/stage3-kprove-smallest-change-correct.log)

This establishes closure under the supplied semantics plus the candidate’s
proof-local rules. It does not establish that those added rules are valid.

## 4. Adequacy and real-program pinning

Status: **FAIL.**

### Plain-language claims and satisfiable states

`public-entry-bridge` has no explicit precondition. It says that applying the
exact public closure to `ref(H)` under any continuation may become
`#targetCall(mainCall, ref(H), 0, 0)`, while omitting every non-`<k>` cell.

`helper-entry-bridge` likewise has no explicit precondition. It says that
applying the exact helper closure to any `ref(H), L, R` and any continuation may
become `#targetCall(helperCall, ref(H), L, R)`.

`smallest-change-correct` starts from the proof-local `#targetCall`, not either
closure or function body. For `mainCall`, `targetValid` is always true and the
postcondition is `changeRange(VS, 0, len(VS)-1)`. For `helperCall`, it requires
`0 <= L <= len(VS)` and `-1 <= R < len(VS)`, then returns
`changeRange(VS,L,R)`. It preserves arbitrary caller environment, scopes,
allocation counters, heap remainder, and stack, while requiring `noRet`,
`NoExc`, and exit code 0.

The entry preconditions are satisfiable. Examples include:

- main: `H=0`, `VS=.ValSeq`, `L=0`, `R=0`, empty heap remainder, `noRet`,
  `NoExc`; `targetValid` is true and the claimed result is 0;
- helper: `H=0`, `VS=[1,2]`, `L=0`, `R=1`; the bounds hold and the claimed
  result is 1.

Ground substitutions for empty input, both documented nontrivial examples,
and a valid helper interval all prove `#Top`; their results agree with both
Python implementations. See [ground spec](evidence/spec-ground.k) and
[ground proof log](evidence/stage4-ground-substitution.log).

### Constructor identity is present

This audit did not reject the proof merely because the source module is not
automatically loaded by the claim. Parsing both submitted functions and
expanding the proof macros with the rebuilt definition gives exact KAST
identity for parameters and bodies. The closures also use defining scope 0.
See [constructor comparison](evidence/constructor_compare.py) and its
[result](evidence/stage4-constructor-compare.log).

### Execution identity is absent

Constructor identity is not an execution theorem. At
`verification.k:73-86`, priority-40 rules match the exact closures and replace
them before the fixed closure-call rule at `semantics/call.k:69-74` can run.
They skip:

- parameter binding and local-scope creation;
- the public body’s `len` lookup/call and helper lookup;
- both `If` conditions and all source `Subscript`, `Compare`, and `BinOp`
  evaluation;
- recursive closure calls;
- return, frame pop, continuation restoration, and affected cells.

The two bridge claims are circular evidence: each closes because the
corresponding operational bridge already states its transition. Neither is a
bridge-free universal connection theorem over the rule’s complete match
domain.

A body-sensitivity mutation changes the actual `#mainClosure` body in both the
claim term and matched rule to `Return(Int(999))`. Python and rebuilt fixed K
confirm result 999 on `[]`. Nevertheless, the candidate theory still proves
all original positive claims and additionally proves the explicit false claim
that applying that mutated closure to the empty list returns 0.

Evidence:

- [mutated verification](evidence/verification-body-mutant.k)
- [fixed Python/K mutation run](evidence/stage4-body-mutant-concrete.log)
- [mutated build](evidence/stage4-body-mutant-kompile.log)
- [unchanged positive claims still close](evidence/stage4-body-mutant-positive-claims.log)
- [explicit false result still closes](evidence/spec-body-mutant-false.k)
- [false result proof](evidence/stage4-body-mutant-false-result.log)

This mutation changes the constructor term actually applied by the claim; it
does not merely edit an external source file. The successful proof is
therefore insensitive to the program-defined public computation. The
`smallest-change-correct` claim proves the substituted target machine.

## 5. Rule-by-rule static soundness review

Status: **FAIL.**

The exhaustive inventory covers 26 K files and contains every configuration,
context, syntax declaration, function/total declaration, macro, opaque symbol,
priority, ordinary rule, and claim. It records:

- 695 fixed supplied-semantics rules and 16 proof-local rules;
- 237 syntax declarations, including 148 functions and 110 total functions;
- 47 priority rules and 54 concrete-only rules;
- 22 explicit `no-evaluators` opaque symbols;
- 3 reachability claims.

See the [exhaustive source-positioned inventory](evidence/static-rule-inventory.md),
[used-construct map](evidence/stage5-used-construct-map.md), and
[per-local-rule decisions](evidence/proof-local-rule-review.md).

The candidate semantics tree is exactly the trusted fixed baseline. At this
selected semantics level, its rules are the fixed trust boundary. All 22
explicit opaque symbols concern MD5, floating-point operations/conversions, or
sorting; none is reached by this integer-list program. The used fixed rules do
model left-to-right calls, frames, integer comparison/arithmetic, negative-index
normalization, list dereference/structural comparison, and return control. The
candidate proof bypasses those material rules rather than exposing a missing
fixed-semantics construct.

### Proof-local rules

The four body/closure macros are exact. The `changeRange`, `targetAnswer`, and
`#addMismatch` equations are ordinary descending arithmetic definitions for
the invented target machine. They do not connect that machine to execution.

The two priority closure rewrites are operational bridges with no connection
theorem. The main-to-helper and helper-recursion rules then hand-code the
expected computation. In particular, helper recursion uses
`valSeqAt(VS,L) ==K valSeqAt(VS,R)` directly. Fixed source execution instead
performs `Subscript` (including negative-index normalization and heap
dereference) followed by `Compare` (including structural list equality).

Two independent sensitivity witnesses make the gap concrete:

1. **Integer-list helper witness.** For the exact helper on `[5], L=-1, R=0`,
   Python and rebuilt fixed K normalize `-1` and return 0. The candidate bridge
   produces a target term containing unconstrained raw
   `valSeqAt([5],-1)`. The unmodified bridge-to-1 attempt gets stuck on exactly
   the missing equality, not on parsing or setup. A disjoint ground completion
   of that candidate-left-undefined total-function case is accepted by K and
   makes the bridge prove the false result 1. This is a symbolic false
   conclusion witness over the unrestricted helper bridge’s own declared
   domain, using a valid integer list. See
   [fixed run](evidence/stage5-negative-index-fixed.log),
   [unmodified residual](evidence/stage5-negative-index-bridge-proof.log),
   [model completion](evidence/verification-negative-model.k), and
   [completed false proof](evidence/stage5-negative-model-proof.log).

2. **Unmodified formal-main witness.** The `mainCall` precondition accepts
   every `ValSeq`, not just integer elements. On the satisfying heap state for
   `[[5],[5]]`, the two inner lists are different references with equal
   structure. Python and rebuilt fixed K return 0. The unmodified candidate
   target machine compares the references with raw `==K` and proves 1 with
   `#Top`. See [witness program](evidence/nested-list-witness.py),
   [fixed run](evidence/stage5-nested-list-fixed.log),
   [false claim](evidence/spec-nested-list-witness.k), and
   [candidate-theory proof](evidence/stage5-nested-list-bridge-proof.log).

The nested-list example is outside the narrower source contract of integer
elements, but it is inside the candidate claim’s explicit formal precondition
and the local rule’s complete match domain. It is therefore a concrete witness
for the global proof-rule unsoundness. On the narrower public integer-list
domain, finite testing found no value mismatch; the fatal finding there is the
separate real-program pinning failure: the property-bearing computation is
replaced, not executed or connected by proof.

No candidate rule was labeled false merely because of an untested possibility.
The complete local decisions and witnesses are recorded in the cited
rule-review artifact.

## 6. Fresh non-vacuity test

Status: **PASS for result discrimination; it does not cure Stage 4/5.**

No candidate vacuity file was trusted. The fresh mutation uses the fully ground
satisfying state:

```k
<k> #targetCall(mainCall, ref(0), 0, 0) => 1 </k>
<heap> 0 |-> list(.ValSeq) </heap>
```

The correct target-machine result is 0. `kprove --dry-run` exits 0, establishing
that the mutation parses and builds. The real proof exits 1 with
`WarnStuckClaimState`; the residual `<k>` cell contains `0` and does not unify
with destination `1`. This is the expected unmet result obligation, not a
parser error, timeout, unrelated hook, or unreachable mutation.

Evidence:

- [fresh mutation](evidence/spec-vacuity.k)
- [successful dry run](evidence/stage6-vacuity-dry-run.log)
- [expected stuck proof](evidence/stage6-vacuity-proof.log)

Thus the induction over `#targetCall` constrains its own result. Non-vacuity of
the substitute does not validate the substitute-to-program bridge.

## 7. Proven-versus-assumed accounting and decision

### What the successful reachability proof establishes

Under the supplied semantics **augmented with all candidate local rules**, the
proof establishes:

- `#targetCall(mainCall, ref(H),...)` rewrites to the raw mirrored-pair count
  for the heap list;
- `#targetCall(helperCall,ref(H),L,R)` rewrites to the corresponding interval
  count under `targetValid`;
- exact closure applications may be replaced by those target calls because
  the proof-local priority bridge rules say so.

Only the first two bullets are proved by the target-machine induction. The
third is assumed operationally and repeated as bridge claims; it is not
derived from fixed execution.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compilers, LLVM/Haskell backends, built-in integer/Boolean/map/list theories | All dynamic evidence and symbolic closure | Ordinary toolchain trust; acceptable for this benchmark. |
| Launcher-selected supplied semantics | Defines the fixed `.mpy` execution model | Integrity verified exactly. It is an accepted semantics-level trust boundary, not support for `verification.k`. |
| Trusted translator | Connects `solution.py` to `solution.mpy` | Byte regeneration verified; acceptable. |
| Mechanical KAST constructor comparison | Connects `solution.mpy` function bodies to the closure macros | Verified exactly; supports syntax/binding identity only. |
| Priority bridges at `verification.k:73-86` | Connect exact program closures to every target proof | Illegitimate. They replace program-defined execution, have no bridge-free universal connection theorem, accept broad contexts, and fail body/value sensitivity. |
| Target main/helper operational rewrites | Supply the result used by `smallest-change-correct` | Illegitimate as a program proof. They encode the property-bearing algorithm independently; the helper rewrite also differs from fixed indexing/equality on its full domain. |
| `changeRange`, `targetAnswer`, `targetValid` | State the target-machine result and domain | `changeRange` arithmetic is acceptable for in-bounds integer lists. `targetValid` is over-broad and admits a concrete false formal-main result. None connects the source body. |
| Fixed-semantics opaque symbols | Potential empirical/trusted primitives | The 22 explicit opaque symbols are unreachable here. `valSeqAt` is total but undefined out of bounds; the helper bridge improperly exposes that case by omitting fixed normalization. |
| Differential and ground tests | Support implementation/canonical agreement and concrete bridges | Reproducible finite evidence only; cannot replace the missing universal K connection theorem. |

Gate A (real-program soundness) fails. Gate B’s mathematical mirrored-pair
summary matches the integer-list source contract without a finite-size bound,
but that does not rescue a theorem about a substituted machine. Gate C evidence
is reproducible and clearly delimited; the missing connection is a Gate A
failure, not a minor evidence limitation.

The candidate therefore satisfies the positive `#Top` runner condition but
does not contain a sound, result-constraining proof that pins and executes the
real submitted program. Under the benchmark decision boundary, an
execution-bypassing substituted program is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
