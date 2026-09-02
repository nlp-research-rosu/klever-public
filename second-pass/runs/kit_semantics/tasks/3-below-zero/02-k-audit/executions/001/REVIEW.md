# Independent adversarial audit: HumanEval/3 `below_zero`

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program for every finite list of mathematical integers. I rebuilt the supplied
semantics and both proof definitions from trusted/source artifacts in a clean
scratch directory, proved each positive connection and target claim
individually, mechanically pinned the claim and operational bridge to the
regenerated program term, reviewed every local K declaration/rule through an
exhaustive inventory, and rejected a fresh reachable false postcondition.

No candidate rule supplies an unconstrained task answer. The one operational
call shortcut is justified by bridge-free reachability claims over its complete
match domain. The source contract has no material uncovered case under the
ordinary `List[int]` reading, and there is no canonical/docstring conflict or
material supplied-model representation gap.

The exact command ledger is
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md). All generated
definitions and mutation execution occurred under
`/tmp/audit-work/3-below-zero-audit`; no candidate-provided compiled definition
or cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`, condition
`kit-semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as this mode requires.

I read the launcher manifest and all required pipeline-v3 records:
`/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
runtime metrics, usage, prompt, last message, full Codex output, and the full
structured trace. The trace parser consumed all 1,093 JSONL records; the output
scanner consumed all 3,107,349 characters. These generation records were used
only as provenance claims, never as proof evidence.

The independent integrity script
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) established:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files; the lock object exactly equals `audit_input["audit_campaign"]`, and
  the lock's actual SHA-256 is the recorded
  `70a42badf03d18428c314dd9376cf48e0e0947ec0227de06f02994ad675d46d5`.
- Every required pipeline-v3 record is regular and readable. Every recorded
  per-file SHA-256 checked by the script matches, including prompt, translator,
  canonical, run/task/result manifests, all generation JSON/text/log files,
  and the single trace JSONL file.
- The independent pipeline tree digest of the trace is
  `5cc3076ba1c65e7458747f40dda7e9cb85aa859d3108da87d0e05f260795e518`,
  matching `usage.json`; the candidate workspace digest is
  `a6bf772bffd470e92984ff88d72b9f8ab1edae492a3d45cb539a2708c788d704`,
  matching `generation-result.json`.
- The candidate prompt and translator are byte-identical to their trusted
  mounts.
- A recursive path/type/content comparison found the candidate and trusted
  supplied-semantics trees identical across all 25 entries. Their independent
  pipeline tree digest is the manifest-recorded
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
  Neither tree contains a symlink or unsupported entry; there are no missing,
  extra, mistyped, or changed entries.
- The required candidate deliverables are regular files. The candidate tree,
  generation tree, trace tree, and both semantics roots are real directories,
  not symlinks.

The full result and hashes are preserved in
[01-stage1-integrity-final.log](/audit-output/evidence/01-stage1-integrity-final.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The docstring in [prompt.py](/reference/prompt.py) gives a bank account starting
at zero and a finite `List[int]` of deposits/withdrawals. The required result is
`True` exactly if the balance is negative after some processed operation, and
`False` otherwise. The examples require `[1,2,3] -> False` and
`[1,2,-4,5] -> True`. Equivalently, the result is true exactly when a nonempty
prefix sum is below zero.

The trusted [canonical.py](/reference/canonical.py) is a witness for that
contract: it updates a running balance and returns at the first negative
prefix. The submitted [solution.py](/candidate/solution.py) implements the same
algorithm. Its extra initialization `operation = 0` is overwritten by every
nonempty loop iteration and is unobservable for the empty case; it does not
change the result or input.

Running the trusted translator over the scratch copy and piping its output to
`cmp` against submitted `solution.mpy` exited 0 with no output. Thus the
submitted constructor term is byte-identical to trusted regeneration; see
[02-regenerate-mpy-byte-identity.log](/audit-output/evidence/02-regenerate-mpy-byte-identity.log).

### Independent differential

The reviewer-authored
[differential.py](/audit-output/evidence/differential.py) separately imports the
trusted canonical function and submitted function and compares both with a
third, independently written running-prefix oracle. Its deterministic input
scope is recorded in
[differential-inputs.txt](/audit-output/evidence/differential-inputs.txt):

- both documented examples;
- empty, zero, immediate-negative, exact-zero, just-below-zero, later-deficit,
  and very-large-integer boundaries;
- every list of lengths 0 through 6 over `[-3,3]`;
- 5,000 seeded lists of lengths 0 through 80 with values in
  `[-10^12,10^12]`.

All 142,270 cases agreed, with zero mismatches and exit 0
([02-python-differential.log](/audit-output/evidence/02-python-differential.log)).
This is finite fidelity evidence, not a substitute for the K theorem.

## 3. Clean proof reconstruction

The observed toolchain was K 7.1.293 and Python 3.10.12. I copied only source
artifacts and the trusted supplied-semantics tree to scratch. Candidate
`runtime-kompiled`, `verification-kompiled`,
`verification-base-kompiled`, caches, logs, and traces were not copied or used.

### Concrete definition

I freshly translated [auditor-smoke.py](/audit-output/evidence/auditor-smoke.py),
compiled the trusted semantics with LLVM as `MPY-KRUN`, and ran eight assertions
covering the examples, empty/zero/negative boundaries, a later deficit, and
large integers. All three commands exited 0. The final K configuration has
`.K`, `NoExc`, an empty stack, and exit code 0. Evidence:
[03-kompile-llvm.log](/audit-output/evidence/03-kompile-llvm.log) and
[03-krun-smoke.log](/audit-output/evidence/03-krun-smoke.log).

The LLVM compiler reported non-exhaustiveness warnings for several unrelated
supplied helpers (for example float/string functions on internal `cellsMark`
values). None is on this program's dependency slice. They are fixed-model
limitations, not candidate additions, and no warned symbol occurs in any
target or connection claim.

### Bridge-free proof definition

I freshly compiled `verification-base.k` with the Haskell backend. Then I ran
each claim in [connection-spec.k](/candidate/connection-spec.k) separately:

| Claim | Exit | Result |
|---|---:|---|
| `CONNECTION-SPEC.call-prefix-connection` | 0 | `#Top` |
| `CONNECTION-SPEC.for-to-loop-connection` | 0 | `#Top` |
| `CONNECTION-SPEC.loop-connection` | 0 | `#Top` |

The corresponding logs are
[call prefix](/audit-output/evidence/03-kprove-call-prefix.log),
[for-to-loop](/audit-output/evidence/03-kprove-for-to-loop.log), and
[loop](/audit-output/evidence/03-kprove-loop.log). This definition imports
`verification-base.k` and the supplied `MPY` modules; it does not import the
operational call bridge in `verification.k`.

### Target proof definition

I separately compiled [verification.k](/candidate/verification.k) with the
Haskell backend and ran only `SPEC.below-zero` from
[spec.k](/candidate/spec.k). It exited 0 and printed `#Top`
([03-kprove-target.log](/audit-output/evidence/03-kprove-target.log)). I also
reran the positive continuation-containment claim; it exited 0 and printed
`#Top` ([04-kprove-context.log](/audit-output/evidence/04-kprove-context.log)).

All fresh compilation/proof warnings were unused-variable warnings. There was
no timeout, backend failure, reuse of compiled evidence, or unclosed positive
claim.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.below-zero` starts from the supplied semantics' complete initial state,
loads the translated module, and calls its installed `below_zero` closure with
`list(INPUT)`. Its precondition `allInts(INPUT)` says that `INPUT` is any finite
`ValSeq` whose every element is a K `Int`; there is no length or integer-bound
restriction. Its postcondition requires the actual returned K value to be
`belowFrom(0, INPUT)`. It also requires the final environment, heap, allocation
counters, stack, return state, exception state, and exit code to have their
specified restored/preserved values; the module scope contains the exact
installed closure.

`belowFrom(B, VS)` is false on an empty suffix. For an integer head `V`, it is
true if `B+V < 0`; otherwise it recurses on the tail from balance `B+V`. By
structural induction on `VS`, `belowFrom(0, INPUT)` is true exactly when some
nonempty prefix sum is negative. It is a result constraint, not a free
variable, implication, or tautology.

The connection claims have these meanings:

1. `call-prefix-connection` executes fixed lookup, argument evaluation, frame
   creation, parameter binding, both local initializations, and evaluation of
   the iterable, reaching the exact `For` term in environment 1.
2. `for-to-loop-connection` performs the fixed `For` to `#loop` lowering while
   universally framing all omitted cells.
3. `loop-connection` is the unbounded finite-sequence circularity. It executes
   iteration, target binding, addition, comparison, early return or tail
   recursion, frame deletion, and caller restoration, reaching
   `belowFrom(BALANCE, VS)`.

The poststate of each segment exactly instantiates the prestate of the next;
reachability transitivity therefore supplies the bridge-free universal
connection for every configuration matched by the operational bridge.

### Satisfiability, concrete substitution, and pinning

The precondition is plainly satisfiable: `.ValSeq`, `vCons(1,.ValSeq)`, both
documented lists, and every other finite integer sequence satisfy it. The
reviewer ground-summary spec
[auditor-ground-summary-spec.k](/audit-output/evidence/auditor-ground-summary-spec.k)
instantiated empty, all-positive, documented-deficit, and exact-zero-then-deficit
inputs; the corrected configuration-shaped claims printed `#Top` with exit 0.
The results (`false`, `false`, `true`, `true`) match both Python
implementations and the independent oracle.

The mechanical
[pinning_check.py](/audit-output/evidence/pinning_check.py) reports:

- regenerated/submitted `solution.mpy`'s `Module` equals the module inside the
  target `#loadAll` after only normalizing the parser-equivalent empty statement
  list spellings `, )` and `.Stmts`;
- the function name, parameter binding, constructor-level body, and defining
  environment equal the exact `closureVal` matched by the call bridge;
- the target destination closure has that same body;
- the target invokes `below_zero` and requires the explicit
  `belowFrom(0,INPUT)` result under `allInts(INPUT)`.

That check exited 0; see
[04-pinning-check.log](/audit-output/evidence/04-pinning-check.log). No omitted
runtime operation or typing-only rewrite separates the executed body from the
trusted regeneration.

The operational bridge has no `...` continuation in its `<k>` cell and pins
every other state cell. The rerun context claim shows a following `#notB`
continuation executes under fixed semantics rather than being discarded. A
fresh, stronger body-sensitivity mutation changed the program's actual
`AugAssign` constructor from `+` to `-`; the exact bridge no longer matched,
fixed execution on `[1]` reached `true`, and the deliberately retained `false`
postcondition failed with `WarnStuckClaimState` and exit 1. See
[auditor-body-sensitivity.k](/audit-output/evidence/auditor-body-sensitivity.k)
and [its log](/audit-output/evidence/04-kprove-body-sensitivity.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv) enumerates every
top-level require/import/module item, configuration, syntax declaration,
function/total/opaque declaration, context, ordinary rule, priority rule,
simplification rule, and claim in all 24 supplied K files plus
`verification-base.k`, `verification.k`, `spec.k`, and `connection-spec.k`.
There are 1,125 rows from 28 files, including 123 function declarations, 26
opaque/symbol declarations, 45 priority rules, 7 simplification rules, 657
other operational/equational rules, 5 contexts, 1 configuration, and 4 claims.
The inventory command and category counts are in
[05-rule-inventory-final2.log](/audit-output/evidence/05-rule-inventory-final2.log).

Every supplied rule is marked either `FIXED_MODEL_USED_SLICE_REVIEWED` or
`FIXED_MODEL_UNREACHED_BY_SOLUTION`. This is important: the supplied semantics
is the immutable selected model, but only its used slice can affect this
theorem. Unreached opaque float, sort, MD5, string, dictionary, comprehension,
slice, set, tuple, and unrelated builtin rules introduce no equality or control
fact into the proof path. Their known model restrictions are not silently used
to establish the result.

### Construct-to-rule mapping

Every constructor in `solution.mpy` has an active fixed-semantics path:

| Program construct | Declaration/evaluation path |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `ImportFrom("typing","List")` | `syntax.k:43`; generic no-op `controls.k:36` |
| `FuncDef`, closure install | `syntax.k:53`; `functions.k:14-16` |
| integer/Boolean literal | `syntax.k:9-11`; `core.k:194-195` |
| `Assign` | strict RHS in `syntax.k:41`; scope update `controls.k:9-11` |
| `For`, list iteration, loop target binding | `syntax.k:45`; `controls.k:65-74`; `list.k:9-10`; `tuple.k:31-34` |
| `Name` lookup | `syntax.k:12`; `core.k:130-154` |
| `AugAssign("+")` | strict RHS `syntax.k:44`; update `controls.k:20-23`; guarded integer addition lemma and fixed `int.k:9` |
| `Compare("<")` | contexts/dispatch `operators.k:14-17`; integer comparison `int.k:22` |
| `If` | strict guard and branches `syntax.k:49`; `controls.k:51-54` |
| `Return`, call and frame pop | `syntax.k:50`; `call.k:18-21,69-75`; `functions.k:63-90` |

The configuration in `core.k:49-60` supplies every cell mentioned in the
claims. Evaluation is left-to-right through K strictness/contexts and the
explicit argument evaluator. The loop mutates only callee-local `balance` and
`operation`; the fixed `#pop` removes that frame and restores the caller.

### Candidate extension decisions

| Extension | Class and audit decision |
|---|---|
| `allInts` | Exhaustive, disjoint, structurally descending definitional predicate on `ValSeq`; sound. |
| `definedProjectInt` | Exact alias for generated `isInt`; sound. |
| `projectIntTotal` and cast/definedness simplifications | Opaque only off the integer guard. Under every use, `isInt(V)` makes the `Val :> Int` projection exact. Concrete identity, reverse orientation, definedness, and idempotence agree on overlaps. No non-integer projected value can affect a target branch/result. Sound guarded sort projection. |
| `belowFrom` | Empty/integer/noninteger cases are exhaustive and disjoint; the target and bridge use only the integer case. Recursion strictly consumes the `ValSeq` tail. It defines, rather than assumes, the prefix result. Sound. |
| guarded `applyBin("+",I,V)` simplification | When `isInt(V)`, it is exactly the fixed `Int + Int` equation after guarded projection. Its overlap with `int.k:9` has the same RHS value. Sound derived lemma. |
| fresh-map deletion simplification | The guard says `L` is absent from `STORE`; deleting the separately adjoined `L |-> Scope` entry therefore yields exactly `STORE`. It normalizes the real `#pop` update and changes no program value. Sound map identity. |
| exact `below_zero` call rule | Operational bridge. It pins binding, body, input type, empty continuation, environment, both scopes, counters, heap, stack, return, exception, and exit code. The three separately rebuilt bridge-free claims cover the entire match domain and complete state footprint. Sound. |

There are no local priority rules in the candidate extension. The supplied
generic call rule is `[owise]`, so the exact bridge is selected only when its
full pattern and guard match. There is no fresh result symbol shared circularly
between execution and postcondition: `belowFrom` is fully defined, and its value
is connected to fixed execution by `loop-connection`.

No inventoried candidate rule is unsound. Accordingly there is no false
conclusion witness to report. The fixed-model compiler warnings and unreachable
opaque symbols are narrower modeling/evidence boundaries, not rules enabling a
false target conclusion.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. I authored
[auditor-false-postcondition.k](/audit-output/evidence/auditor-false-postcondition.k),
which keeps the exact submitted module and state but specializes the satisfying
input `[1,2,3]` and falsely requires `true`.

The `kprove --dry-run` command exited 0, so the mutation parsed and built against
the fresh proof definition. The actual proof exited 1 with
`WarnStuckClaimState`; its reachable residual contains final `<k> false </k>`
and the otherwise correct final cells, while the destination demanded `true`.
This is the expected unmet result obligation, not a parse error, missing import,
timeout, or unrelated crash. Evidence:
[dry run](/audit-output/evidence/06-false-postcondition-dry-run.log) and
[proof failure](/audit-output/evidence/06-false-postcondition-proof.log).

The target is therefore non-vacuous and discriminates a deliberately false
result.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied MPY semantics and the audited proof-local
mathematical rules, for every finite `ValSeq` consisting solely of K integers,
loading the exact trusted-regenerated module and calling its exact
`below_zero` binding reaches the Boolean `belowFrom(0,INPUT)` whenever the call
terminates. The connection proof establishes lookup, binding, local state,
iteration, early return, ordinary return, and restoration of every modeled
state cell. Structural induction on the definition of `belowFrom` identifies
that Boolean with “some nonempty prefix balance is below zero.” This is the
docstring property over arbitrary list length and arbitrary-magnitude Python
integers, not a bounded unrolling or examples-only theorem.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Supplied read-only MPY semantics | Defines all modeled execution, state, calls, and control for every claim. | Required benchmark trust boundary; candidate copy is byte/type identical. Used slice was statically reviewed and concretely smoke-tested. |
| K parser, reachability logic/circularity/transitivity, generated sort/map hooks, Haskell backend and solver | Establish closure, induction/circularity, guarded casts, and map reasoning. | Standard machine-checking trust boundary; fresh K 7.1.293 builds and individual proofs succeeded. |
| `projectIntTotal` guarded projection and fresh-map identity | Affect symbolic addition and frame cleanup in connection/target proofs. | Audited ordinary K sort/map facts; guards cover every use and overlaps agree. No unconstrained on-domain interpretation remains. |
| Trusted `py2mpy.py` translation | Connects Python AST to submitted K constructor term. | Trusted input; fresh translation is byte-identical, and constructor-level claim/bridge comparison passes. |
| Empty `Stmts` spelling normalization | Translator prints an empty concrete-list field while the K files spell `.Stmts`. | Parser-level representation identity only; pinning script isolates this sole normalization. |
| Bare `list(ValSeq)` claim argument versus heap-backed list literals | Represents external read-only list inputs without allocating a heap reference. | Explicitly supported by fixed `core.k`; this program only iterates and never mutates/tests identity. Fixed execution, concrete heap-backed smoke calls, and Python differential agree. |
| `belowFrom` to natural-language prefix property | Connects the formal returned summary to the docstring. | Direct exhaustive recurrence; justified by structural induction, with ground K and broad differential checks as supporting evidence. |
| Canonical implementation and finite differential | Supports source fidelity and concrete edge behavior. | Helper witness/evidence only; never used as a proof rule or as contract ground truth. |
| Supplied opaque float/sort/MD5 and other unused helpers | Present in imported fixed theory but absent from all reachable target terms. | No control/value/state influence on this theorem; listed in the exhaustive inventory, not silently trusted for the result. |

The formal precondition excludes non-integer elements, infinite inputs, and
non-list/exotic containers. That is the ordinary material domain expressed by
the source signature `List[int]`. Boolean values, floats, custom numeric
objects, concurrent mutation, and other exotic runtime inputs are not behavior
determined by this docstring and do not create a material source-contract
narrowing under campaign v3. The program itself remains faithful on ordinary
CPython integer lists. The reachability theorem is partial correctness; it does
not itself assert termination, although fixed execution consumes one element
per iteration for finite lists.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
evidence auditability) all pass. The clean target closes, the connection is
sound and body-sensitive, the theorem covers the unrestricted material domain,
and the fresh false result is rejected.

VERDICT: PASS
LEGITIMACY: LEGIT
