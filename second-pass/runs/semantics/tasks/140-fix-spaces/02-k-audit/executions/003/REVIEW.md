# Independent adversarial audit: 140-fix-spaces

The candidate is not a legitimate proof. Fresh reconstruction does reproduce
all four reported `#Top` results, and the end-to-end claim is non-vacuous and
mechanically pinned to the submitted constructor program. However, both
character-step summary rules are materially unsound over their declared match
domains. They ignore possible module-level shadowing of `ord`, even though the
fixed call semantics performs ordinary scope lookup. Machine-checked witnesses
show that fixed semantics rejects the bridge conclusions while the
bridge-enabled definition proves them. There is also a result divergence from
the trusted canonical implementation on every input ending in exactly two
spaces.

All candidate and generation artifacts were treated as untrusted evidence.
All execution, generated tests, definitions, and mutations were created under
`/tmp/audit-work/140-fix-spaces`; reviewer artifacts and bounded logs are under
`/audit-output/evidence`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `140-fix-spaces`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- candidate mount `/candidate`;
- trusted prompt, canonical, translator, and supplied-semantics mounts under
  `/reference`.

The supplied-semantics mode and mounts are consistent:
`/reference/reference-semantics` is present. Recursive
`diff -r --no-dereference` between that tree and
`/candidate/reference-semantics` exited 0. Both trees contain the same 24
regular K files with the same modes and sizes; neither tree contains a symlink.
There are no missing, additional, mistyped, changed, or symlinked candidate
semantics entries.

The candidate and trusted copies of `prompt.py` compare byte-for-byte, as do
the candidate and trusted copies of `py2mpy.py`. Independently computed direct
hashes match every applicable hash recorded by the launcher for the canonical,
prompt, translator, run/task/result manifests, invocation, metrics, usage,
generation prompt, `codex-last.txt`, and `codex-output.log`.

`/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block in
`/audit-input.json`; its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher record. The audit prompt hash also matches the
campaign block.

All records required for `legacy-selected-stage1` were present and readable:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
`runtime-metrics.json` is absent, but the prompt explicitly says it is not a
required historical record for this layout.

The structured trace has 967 JSONL records, all valid JSON, from the recorded
session. Its SHA-256 is
`1a779b6dc122d56bf557fb11fd96e388167fe88e2635c2d12abdfa4ce6fcd96f`,
matching `generation-result.json` and `invocation.json`. The full 148,615-line
generation output was scanned and independently hashed; it contains historical
failed attempts as well as the eventual positive runs, so its final report was
not treated as proof.

One untrusted-record inconsistency is documented: `usage.json` says its source
trace hash is
`c0f79487678615e309c7a63d0fe732f1c1be292721308cd56407843f03cf06f2`,
which is not the mounted trace hash above. The launcher itself records and
hashes both mounted artifacts as they exist, and the result/invocation trace
entry matches the mounted trace. I therefore treat this as a legacy usage
record inconsistency, not a missing/malformed launcher mount or an
infrastructure breach.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log`
- `evidence/trace_summary.py`
- `evidence/generation_log_summary.py`
- `evidence/generation_log_summary.log`

Stage 1 result: integrity gate passed; no condition/mount contradiction and no
audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt gives an unrestricted string argument. Its direct prose reading is:
copy non-space characters; replace a run of one or two literal spaces by the
same number of underscores; replace a run longer than two spaces by one
hyphen.

The trusted canonical at `/reference/canonical.py:17` scans the string while
tracking a pending run. For non-final runs, it emits underscores equal to a
one- or two-space run and one hyphen for a longer run. At lines 32-35 its final
flush is different: it emits only one underscore for *either* one or two final
spaces.

The submitted `/candidate/solution.py` implements the direct prose reading.
In particular, lines 22-25 emit `"__"` for exactly two trailing spaces. It uses
`ord(char) - 32` as the truth test, which is equivalent to `char != " "` for
every one-character Python string.

### Translation fidelity

The source artifacts were copied to clean scratch. Running the trusted command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp solution.mpy regenerated-solution.mpy` exited 0. Both files have
SHA-256
`5c42c1a38d15ba4bcbec6313f653bb1dd871da78ec0cfcb5f79257dcab5887dc`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
and generated entry point. It covers the four documented examples, empty
input, runs of lengths 1-4 at leading/internal/trailing positions, mixed runs,
non-ASCII characters, newline/tab/NUL non-spaces, every string over
`{" ", "a", "b"}` through length 8, and 2,000 deterministic generated strings
using seed 140. After deduplication, it tested 11,780 inputs.

Results:

- candidate versus trusted canonical: 750 mismatches;
- candidate versus direct prose oracle: 0 mismatches;
- trusted canonical versus direct prose oracle: 750 mismatches.

Every observed mismatch is the same material boundary case: an input ending
in exactly two spaces. For example:

```text
input       = 'a  '
canonical   = 'a_'
candidate   = 'a__'
prose model = 'a__'
```

Thus the trusted natural-language and canonical sources disagree on this
boundary. Under the benchmark's trusted canonical behavior, the generated
implementation is not faithful on the unrestricted string domain. Even if the
prose reading were selected over the canonical at this boundary, the
independent proof-rule unsoundness in Stage 5 still determines the final
verdict.

Evidence:

- `evidence/stage2_program_fidelity.sh`
- `evidence/stage2_program_fidelity.log`
- `evidence/differential_test.py`

Stage 2 result: translation fidelity passed; canonical behavioral fidelity
failed on exactly-two-trailing-space inputs.

## 3. Clean proof reconstruction

The live tools independently report K version 7.1.293. No candidate-compiled
definition or cache was copied or reused.

From source in clean scratch I built:

1. LLVM `MPY-KRUN` from the trusted supplied semantics;
2. Haskell `FIX-SPACES-BASE`;
3. Haskell `FIX-SPACES-FLUSH-VERIFICATION`;
4. Haskell `FIX-SPACES-STEP-VERIFICATION`;
5. Haskell `FIX-SPACES-VERIFICATION`.

The copied concrete test module ran to a normal `.K` configuration with
`NoExc` and exit code 0. Each positive target module was then run directly:

| Spec module | Claims covered | Exit | Result |
|---|---:|---:|---|
| `FIX-SPACES-FLUSH-SPEC` | 4 | 0 | `#Top` |
| `FIX-SPACES-STEP-SPEC` | 2 | 0 | `#Top` |
| `FIX-SPACES-LOOP-SPEC` | 1 | 0 | `#Top` |
| `FIX-SPACES-MAIN-SPEC` | 1 | 0 | `#Top` |

The rebuild emitted known unused-variable warnings in `str.k`. The LLVM build
also identified several non-exhaustive total functions elsewhere in the
supplied subset. None caused a build or proof failure, and none is used by this
program. All five builds and all four positive proof commands exited 0.

Evidence:

- `evidence/stage3_clean_rebuild.sh`
- `evidence/stage3_clean_rebuild.log`

Stage 3 result: the candidate's positive verification result is reproducible.
This establishes closure only under the candidate's extended theory, not that
the extensions are sound.

## 4. Adequacy and real-program pinning

### Claims in plain language

The eight claims state:

- `flush-zero`: a tail flush with `spaces = 0` leaves `result` unchanged.
- `flush-one`: a tail flush with `spaces = 1` appends one underscore.
- `flush-two`: a tail flush with `spaces = 2` appends two underscores.
- `flush-many`: a tail flush with `spaces > 2` appends one hyphen.
- `step-space`: one loop-body step on code 32 increments the pending count and
  leaves the accumulated result unchanged.
- `step-non-space`: one loop-body step on any code other than 32 flushes the
  pending count, appends that code, and resets the count.
- The loop claim structurally summarizes every remaining `IntSeq`, preserving
  the exact final `result`, `spaces`, and `char` locals.
- The main claim loads `solutionModule`, invokes `fix_spaces` on arbitrary
  `IS:IntSeq`, and returns
  `appendPending(fixSpacesLoop(.IntSeq, IS, 0),
  trailingSpaces(IS, 0))` in a normal final configuration.

All auxiliary preconditions are satisfiable. For example, empty sequences
satisfy the main claim and the zero cases; `N = 1`, `N = 2`, and `N = 3`
satisfy the other flush cases; code 32 and code 97 satisfy the two step cases.

### Mechanical program identity

Using the freshly built proof parser, I fully expanded `solutionModule` and
parsed the regenerated submitted `solution.mpy`, both as sort `Module` and JSON
KAST. `cmp` exited 0. Both 19,364-byte artifacts have SHA-256
`08d795c515069e63de23365edfb6ba0ce52e126858c8d33a25921591214b4ba0`.
Therefore the main claim executes the submitted function binding and body;
the proof macros are constructor-identical normalization, not a substituted
algorithm.

For the satisfying ground input `IS = [97, 32, 32]` (`"a  "`), the formal
summary simplifies to codes `[97, 95, 95]`, or `"a__"`. The ground K claim
closed with `#Top`; candidate Python also returns `"a__"`, while trusted
canonical Python returns `"a_"`.

### Body sensitivity

In a scratch-only copy I changed the actual executed function tail from
`Str("__")` to `Str("_")`, leaving the formal result summary unchanged. The
mutated definition built successfully. The end-to-end proof then exited 1 with
`WarnStuckClaimState`; its residual explicitly contrasts one underscore with
two under `trailingSpaces(IS, 0) = 2`. This mutation changes the term loaded by
`solutionModule`, so it is a valid body-sensitivity test.

The main result is not a free variable, tautology, or one-way implication. It
is a concrete recursive summary of the entire input. Pinning and result
constraint therefore pass, although the theorem is derived using unsound
rules and disagrees with the canonical boundary behavior.

Evidence:

- `evidence/program_from_claim_macro.json`
- `evidence/program_from_submitted_mpy.json`
- `evidence/ground-result-spec.k`
- `evidence/verification-body-mutated.k`
- `evidence/spec-body-mutated.k`
- `evidence/stage4_pinning_and_sensitivity.sh`
- `evidence/stage4_pinning_and_sensitivity.log`

Stage 4 result: real-program pinning and body sensitivity passed; canonical
intent adequacy did not.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5_static_and_context.log` indexes every module, import,
configuration, context, syntax declaration, rule, claim, guard, and relevant
attribute by source file and line. It covers 26 source files, including all
supplied helper K files, `verification.k`, and `spec.k`. Totals are:

- 1 configuration;
- 5 explicit contexts;
- 238 syntax declarations;
- 715 rules (695 supplied-semantics rules plus 20 candidate rules);
- 8 reachability claims.

The per-file rule inventory and disposition is:

| File/module | Rules | Static disposition |
|---|---:|---|
| `semantics.k` assembly | 0 | Import graph only; proof module imports `MPY`, not `MPY-CONCRETE`. |
| `syntax.k` | 0 | Constructor grammar; declarations cover every submitted constructor. |
| `core.k` | 46 | Configuration, sequencing, lookup, literals, truth, allocation, and total folds. Relevant rules preserve cells and evaluation order. |
| `iter.k` | 0 | Iterator protocol declarations only. |
| `range.k` | 6 | Guarded range length/iteration; unused here. |
| `operators.k` | 10 | Strict dispatch and heap dereference; relevant integer subtraction/comparison path is sound. |
| `int.k` | 16 | Ordinary integer arithmetic/comparisons; relevant subtraction is exact. Division-by-zero behavior is outside this program. |
| `bool.k` | 13 | Truth/short-circuit rules; unused except `truthy(Int)` from core. |
| `float.k` | 121 | Opaque/concrete float boundary; wholly unreachable here. Duplicate mixed-operation equations agree where overlapping. |
| `str.k` | 28 | String iteration, literal encoding, concatenation, membership/order. Iteration, ASCII literals, and concatenation used here are constructor-faithful. |
| `set.k` | 12 | Defined set-code folds; unused. |
| `list.k` | 27 | Lists, iteration, equality, mutation; unused. |
| `tuple.k` | 21 | Tuple construction/iteration and target binding. `#bindTgt(Name, Val)` is used by the loop and correctly updates the current scope. |
| `subscript.k` | 40 | Index/slice subset, including intentionally total opaque OOB behavior; unused. |
| `comprehension.k` | 7 | Macro expansion only; unused. |
| `methods.k` | 75 | String/list method subset; unused. |
| `controls.k` | 34 | Assign/AugAssign, If, For, loop control, and dereference. The submitted path uses assignment, branching, and `For`; state footprints agree with Python for this program. |
| `functions.k` | 15 | Closure creation, binding, return, and frame pop. The main call/return path restores the caller and leaves a normal return value. |
| `builtins.k` | 137 | Builtins and folds. Only `ord` is used; its one-character code rule is exact. Opaque `md5hexCodes` and other unused functions do not influence this theorem. |
| `call.k` | 21 | Callee lookup, left-to-right argument evaluation, and dispatch. Ordinary lookup/shadowing is material to the counterexamples below. |
| `sort.k` | 19 | Opaque symbolic sort trust boundary and concrete twin; unused. |
| `assert.k` | 3 | Assert success/failure; used only by concrete smoke tests, not the proof. |
| `dict.k` | 28 | Ordered dictionary subset; unused. |
| `concrete.k` | 16 | LLVM-only deep equality/keyed sort; absent from all Haskell proof definitions and unused. |
| `verification.k` | 20 | Six mathematical/macro families and four operational summary rules; audited individually below. |

The submitted constructors map to fixed rules as follows:

| Submitted construct | Declaration/rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and sequencing |
| `FuncDef`, `Return` | `functions.k` closure/call/pop rules |
| `Name`, `Int`, `Str` | `core.k` lookup/literals; `str.k` literal codes |
| `Assign`, `AugAssign`, `If`, `For` | `controls.k` |
| string iteration/character binding | `str.k` `#iterNext`; `tuple.k` `#bindTgt` |
| `Call(Name("ord"), ...)` | `call.k` lookup/evaluation; `builtins.k` `ord` |
| `BinOp("-")`, `Compare` | `operators.k`; `int.k`; `core.k` truthiness |
| string `+` | `str.k` `applyBin("+")` and `seqConcat` |

The fixed configuration cells are all accounted for. The program changes
`<scopes>`, temporarily `<env>`, `<scopeLoc>`, `<stack>`, and `<ret>` during
the call, and leaves `<heap>`, `<heapLoc>`, `<exc>`, and `<exit-code>`
unchanged.

### Candidate functions, macros, and simplifications

- `pendingSpaces` and `appendPending` use exhaustive nested integer guards.
  Their cases are disjoint and agree with the candidate program for all
  reachable `N >= 0`.
- `fixSpacesLoop` has disjoint empty/space/non-space constructors, structurally
  descends on the suffix, and exactly records emitted output while deferring
  the final pending run.
- `trailingSpaces` has the same exhaustive constructor split and records the
  final pending count.
- `finalChar` structurally returns the prior `char` on empty input and the last
  iterated character otherwise.
- The six macros at `verification.k:70-135` fully expand to the submitted
  constructor body, as mechanically checked in Stage 4.
- The `[simplification]` equations are the same truthful structural equations;
  no overlap has conflicting right-hand sides.

These definitional summaries are not unconstrained oracles.

### Tail bridge

The rule at `verification.k:143-179` replaces the tail statement with
`appendPending(A, N)` for `N >= 0`. Its four bridge-free claims import only
`FIX-SPACES-BASE` and cover `N = 0`, `1`, `2`, and `> 2`. The statement uses no
heap, call, abrupt control, or external binding. Its arbitrary continuation is
preserved rather than discarded.

A ground observable-continuation probe (a following assignment to `"Z"`)
closed under both fixed semantics and the bridge-enabled definition. The
candidate does not provide a universal connection claim explicitly quantified
over arbitrary continuations, so this remains a proof-documentation limitation,
but no false conclusion witness was found for this bridge.

### Character-step bridges: concrete unsoundness

The rules at `verification.k:186-244` are operational bridges. Their fixed
step claims use the exact module scope:

```text
scope("fix_spaces" |-> FUNCTION, parent(-1))
```

but both promoted rules instead accept:

```text
(0 |-> MODULE:Scope)
```

Their only binding guard is `BUILTINS ==K builtinsScope`. This does not show
that `Name("ord")` resolves to the builtin: ordinary lookup checks the arbitrary
module scope before the builtins scope. The promoted rule domain is therefore
strictly broader than the bridge-free theorem domain.

Two machine-checked false-conclusion witnesses establish actual unsoundness,
not just a missing proof:

1. Non-space bridge (`verification.k:214-244`):

   - local `char = "a"` (code 97), `result = ""`, `spaces = 0`;
   - module scope binds `ord` to a closure returning 32;
   - builtins scope remains exactly `builtinsScope`.

   Fixed execution resolves the shadowing closure, computes `32 - 32 = 0`,
   takes the space branch, and ends with `result = ""`, `spaces = 1`.
   `FIXED-SHADOW-OUTCOME-SPEC` proves that outcome with `#Top`. Fixed semantics
   rejects the bridge conclusion (`result = "a"`, `spaces = 0`) with
   `WarnStuckClaimState`. The bridge-enabled definition proves that false
   conclusion with `#Top`.

2. Space bridge (`verification.k:186-212`):

   - local `char = " "` (code 32), `result = ""`, `spaces = 0`;
   - module scope binds `ord` to a closure returning 97;
   - builtins scope remains exactly `builtinsScope`.

   Fixed execution computes `97 - 32`, takes the non-space branch, appends the
   literal space, and leaves `spaces = 0`.
   `FIXED-SHADOW-SPACE-OUTCOME-SPEC` proves that outcome with `#Top`. Fixed
   semantics rejects the bridge result (`result = ""`, `spaces = 1`), while
   the bridge-enabled definition proves it with `#Top`.

Both witnesses use ordinary one-character string inputs and satisfy every
guard and cell pattern of the corresponding candidate rule. The false result
is enabled solely by the omitted binding condition. Rule priority makes each
bad bridge preempt fixed execution; it does not justify the rewrite.

The actual generated module does not add an `ord` binding, but the proof
extension is globally false over its declared domain. The Kit soundness
contract expressly disallows defending a globally false rule by saying its bad
states are off the main path. The rule must have constrained the module scope
or been supported by a connection theorem over the broader domain.

Evidence:

- `evidence/bridge-shadow-witness.k`
- `evidence/step_bridge_shadow_witness.sh`
- `evidence/step_bridge_shadow_witness.log`

### Loop bridge

The rule at `verification.k:252-289` gives exact result, pending-count, and
final-character summaries and preserves its continuation. Unlike the step
rules, it pins the module scope to only `fix_spaces` and pins the builtins
scope. The bridge-free structural loop claim has the same state footprint.
Ground fixed/extended observable-continuation probes agree.

Nevertheless, the loop connection proof imports
`FIX-SPACES-STEP-VERIFICATION`, so its `#Top` is derived in the theory
containing the two unsound step rules. It cannot serve as a sound connection
theorem. The end-to-end main proof in turn imports and uses this loop bridge.

Stage 5 result: Gate A failed. Two proof-local operational rules admit and
machine-prove false state transitions; the main proof depends on a loop summary
whose connection proof uses those rules.

## 6. Fresh non-vacuity test

I did not rely on any candidate mutation artifact. The fresh
`evidence/spec-vacuity.k` changes the end-to-end result obligation to require
one extra code 33 (`"!"`) after the complete returned value.

The empty string is a concrete satisfying input:

```text
actual candidate result = ""
mutated required result = "!"
```

`kprove --dry-run` exited 0, proving that the mutation parsed and compiled to a
KORE proof command. The actual mutation run exited 1 with
`WarnStuckClaimState` and an implication residual comparing each genuine result
branch against that branch followed by `iCons(33, .IntSeq)`. It was not a
parser error, missing import, timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log`

Stage 6 result: non-vacuity passed. The end-to-end claim discriminates a false
result, but non-vacuity cannot make the proof-local theory sound.

## 7. Proven versus assumed accounting

### What the reconstructed `#Top` establishes

Inside the supplied semantics plus all candidate rules, the main reachability
claim establishes:

> For every constructor `IS:IntSeq`, loading the submitted `fix_spaces`
> function into the specified empty module/builtin configuration and calling
> it terminates symbolically at the candidate recursive summary, with the
> function closure installed and all explicitly listed control/state cells in
> their stated normal final values.

That is a partial-correctness reachability result under the extended theory.
It does not by itself establish that every extension is a theorem of fixed
semantics or that the result equals the trusted canonical.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K integer/Boolean/string/map/list hooks | Evaluation, guards, code sequences, scopes | Ordinary low-level trusted base; acceptable. |
| Supplied MPY semantics | All source execution | Integrity-verified and adequate for every construct used here. It is a documented Python subset, not full CPython. |
| `IntSeq` as input-string code sequence | Input/result representation | Main claim is at least as broad as Python Unicode code sequences; no material narrowing. Invalid code integers are an over-broad formal domain, not a source-domain exclusion. |
| ASCII-only `Str` literal translation | Program constants | All submitted literals are ASCII; acceptable here. |
| `ord` rule for a one-code string | Branch control | Fixed primitive is defined exactly; the candidate bridges fail to preserve its dynamic binding. |
| Candidate recursive functions | Final result and locals | Fully defined by disjoint, descending equations; acceptable as mathematical summaries. |
| Tail operational bridge | Result and local scope | Four fixed-semantics claims plus ground continuation evidence; no false witness found, though universal arbitrary-context theorem is not explicit. |
| Two character-step bridges | Branch, result, pending count | Illegitimate. Concrete shadowing witnesses show false conclusions provable. |
| Loop operational bridge | Entire loop result and locals | Its stated summary is plausible and ground-sensitive, but its connection claim depends on the unsound step bridges; unusable as a sound theorem. |
| Opaque float/sort/keyed-sort/MD5 symbols in supplied semantics | None on this program | Unreachable and do not influence any target claim. |
| Differential testing | Canonical/prose bridge only | Finite evidence over 11,780 inputs; not a universal K proof. It exposes rather than repairs the canonical discrepancy. |
| Macro/KAST comparison | Program identity | Mechanical identity evidence only; not correctness evidence. |

### Gate and decision accounting

- Gate A, real-program soundness: **FAIL**. Both step operational bridges are
  globally false over their declared module-scope domain, with fixed-versus-
  extended machine witnesses. The main proof depends transitively on them.
- Gate B, intent adequacy: **FAIL** under the trusted canonical behavior because
  exactly two trailing spaces produce different results on an unrestricted
  input domain. The prose and canonical disagree on this boundary; that
  ambiguity does not mitigate Gate A.
- Gate C, evidence auditability: the reviewer evidence is reproducible and
  hashed in `evidence/evidence_manifest.log`. The historical `usage.json`
  source-trace mismatch is recorded and not used to support the proof.

Fresh `#Top`, constructor identity, body sensitivity, and non-vacuity show that
this is a substantive theorem about the submitted candidate program under its
theory. They do not rescue a theorem whose proof theory contains result- and
control-affecting false operational rewrites. Per the benchmark decision
boundary, materially unsound proof rules require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
