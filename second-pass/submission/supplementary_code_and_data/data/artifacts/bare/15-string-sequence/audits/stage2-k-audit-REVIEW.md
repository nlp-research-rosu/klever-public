# Independent adversarial review: 15-string-sequence

This audit followed the required `using-kit`, `validating-proof`, and
`writing-semantics` paths. All candidate and generation material was treated as
untrusted. Candidate-built caches were not used; only source files copied to
`/tmp/audit-work` were compiled. The reconstructed theorem passes the
real-program soundness, intent-adequacy, and evidence-auditability gates.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout` =
`legacy-selected-stage1`, condition `bare`, and `semantics_mode` =
`GENERATED_SEMANTICS`. I used its `container_paths` and did not follow the
host-only provenance paths.

All layout-required records are present, readable, real regular files or real
directories, and on read-only mounts:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  `codex-trace/`; and
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

No symlink or unsupported filesystem node occurs below `/candidate`,
`/reference`, or `/generation-evidence`. The required proof artifacts
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh` are all present as regular files. Historical
`runtime-metrics.json` is absent, which is permitted for this
`legacy-selected-stage1` record; `usage.json`, which is present, was inspected.

Independent SHA-256 values for all recorded regular files agree with the values
in `/audit-input.json`. In particular:

- campaign lock:
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- run/task/result:
  `16ab5496...`, `754b3a55...`, `442b9606...`;
- invocation/metrics/usage:
  `b7443a80...`, `d7fc1b9c...`, `9643c4e8...`;
- generation last/output/prompt:
  `d18f6001...`, `3eda335c...`, `4fbd8d83...`; and
- trusted canonical/prompt/translator:
  `24ccdbb0...`, `1eb46648...`, `406485ea...`.

The mounted candidate's independent pipeline content-tree digest is
`4dcd159bc8476ee9fbe842d41c046f39bd87b97adf3fc9fe1332fa9df8d62159`,
exactly the retained workspace digest recorded in both
`/generation-result.json` and `/generation-evidence/invocation.json`. The
structured trace parses completely as one regular JSONL file with 172 events;
its independent pipeline tree digest
`d5652e019c11fbf619ac489ef47c691fb6fa8157aeb1aba3f0da3cc4b3bcddb2`
equals `usage.json`'s recorded source-trace digest. The additional aggregate
tree fields in `/audit-input.json` use a launcher-owned digest scheme not
declared in the record; file-by-file inspection and the independently
reproducible pipeline digests establish the mounted content.

The JSON object in `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` object embedded in `/audit-input.json`, and its file hash is
the recorded campaign-lock hash. The campaign ID, audit image ID, K version,
Kit commit/tree, Codex version, and prompt/toolchain lock fields all agree.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted counterparts. Because this is `GENERATED_SEMANTICS`,
`/reference/reference-semantics` is correctly absent. No infrastructure breach
or semantics-mode contradiction exists.

The retained generation report and prior `#Top` were used only as historical
claims. The complete small records, bounded large-log inspection, and parsed
structured trace are preserved in
`evidence/stage1-generation-records.log` and
`evidence/generation-trace-summary.log`. Reproducible integrity checks are in
`evidence/stage1_integrity.sh` and `evidence/stage1-integrity.log`.

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `string_sequence(n: int) -> str` to return decimal
numbers from 0 through `n`, inclusive, separated by single spaces. The trusted
canonical implementation is:

```python
' '.join(str(x) for x in range(n + 1))
```

Thus the canonical result is empty for negative `n`, `"0"` for zero, and
`"0 1 ... n"` for positive `n`.

The candidate uses an explicit negative branch, initializes `"0"`, and appends
each integer from 1 through `n`. It has the same behavior over the complete
source `int` domain; it is not a fixed-size or example-only implementation.

Using the trusted translator copied from `/reference/py2mpy.py`, I regenerated
`solution.mpy` from `solution.py`. Both submitted and regenerated files have
SHA-256
`11366253bbb1d88f6881db189674885fb00045eb3fa69b16ad69c45d07077774`
and compare byte-for-byte equal.

The independent differential script
`evidence/differential_test.py` imports the trusted canonical and the scratch
copy of the candidate without importing any proof equations. It tests the two
documented examples, the `n < 0` boundary (`-1/0`), the loop boundary (`0/1`),
nearby values, larger values through 500, and a seeded broader sample. All 206
distinct inputs and the complete input list are recorded; mismatch count is
zero. Relevant witnesses are:

- `n=-1`: both return `""`;
- `n=0`: both return `"0"`;
- `n=1`: both return `"0 1"`;
- `n=5`: both return `"0 1 2 3 4 5"`; and
- `n=12`: both return `"0 1 2 3 4 5 6 7 8 9 10 11 12"`.

Commands, inputs, exit statuses, and results are in
`evidence/stage2-fidelity.log`; the runner is
`evidence/stage2_fidelity.sh`.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/reconstruction`; the
candidate's `__pycache__` was not copied and no candidate-provided compiled
definition existed or was reused. K 7.1.293 was independently observed.

Fresh builds:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
# exit 0

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled
# exit 0
```

The LLVM definition was concretely run on `-3`, `-1`, `0`, `1`, `5`, `12`,
and `50`. Every `krun` exited 0. A reviewer-authored parser extracted the final
`SVal`; every value equaled both the candidate Python result and the trusted
canonical result. This exercises the negative return, zero-iteration loop,
first iteration, normal multi-iteration behavior, and a larger run.

The original four-claim spec was first proved as submitted:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC
#Top
# exit 0
```

I then made a label-only copy of the exact claims and selected each target
independently. The unrestricted entry and concrete entry selections include
the independently selected loop invariant because it is their circularity
dependency. Each command exited 0 and printed an exact `#Top` line:

- loop invariant;
- loop invariant plus unrestricted entry;
- loop invariant plus the `n=0` entry; and
- loop invariant plus the `n=5` entry.

Build evidence is in `evidence/stage3-build.log`; concrete comparisons are in
`evidence/stage3-concrete.log`; all proof commands and outputs are in
`evidence/stage3-proofs.log`. The source runners and label-only spec are
preserved beside those logs.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim has precondition `I >= 1` and `N >= 0`. Starting with local
bindings `i=I`, `n=N`, and `result=S`, it executes the actual submitted loop.
It preserves `n`, all other environment bindings, the function map, stack, and
arbitrary caller continuation. It returns to that continuation with:

- `i = indexAfter(I,N)`, namely the first index greater than `N`; and
- `result = sequenceFrom(I,N,S)`, namely `S` with `" I ... N"` appended.

The unrestricted entry claim has no precondition beyond K's inferred
`N:Int` sort. From a clean environment, function map, and stack it executes
`init(targetProgram(),N)` and requires final result `SVal(sequence(N))`, with
the clean caller environment/stack restored and the submitted function binding
installed. `sequence(N)` is exhaustively defined as empty for negative `N` and
as `"0"` followed by 1 through `N` otherwise. No right-only/free result
variable occurs.

The remaining entry claims instantiate that theorem at `N=0` and `N=5` and
require the literal results `"0"` and `"0 1 2 3 4 5"`.

Every precondition is satisfiable. For example, the loop state
`I=1, N=0, S="0", REST=.Map, KREST=.K` satisfies its precondition and takes
the zero-iteration path. The entry claims admit every K integer; `N=-1`,
`N=0`, and `N=5` are concrete satisfying witnesses. Substitution reduces the
claimed result respectively to `""`, `"0"`, and `"0 1 2 3 4 5"`, matching
both Python implementations and fresh K execution.

### Mechanical program identity

The identity chain is:

```text
solution.py
  --trusted py2mpy.py, byte equality-->
submitted solution.mpy
  --K parser/KORE equality-->
the explicit Module constructor in pinning.k
  --targetProgram/targetBody equations-->
the term executed by every entry claim
```

`kast` parses the submitted and explicit target module to identical KORE
(`c22cda12...` for each). A reachability equality under the fresh Haskell
definition establishes that `targetProgram()` normalizes to that constructor
term and prints `#Top`. The claim is reported as trivial after frontend
function normalization, which is expected for an exact `[function]`
abbreviation; it is not the correctness theorem. The byte/KORE links and the
execution-sensitive check below prevent it from serving as an unconnected
alias. Evidence is in `evidence/stage4-pinning.log`; the two initial
reviewer-probe parser diagnostics are also retained separately.

Typing annotations are the only source syntax omitted by the trusted
translator, and are semantically inert for this function. Every material
statement, expression, binding, call, and control effect is present.

### Body sensitivity

In a separate scratch definition I changed the target body actually expanded
by `targetProgram()` so that `result` starts as `"X"` instead of `"0"`. The
mutant definition compiled successfully. The original unrestricted result
claim then exited 1 with `WarnStuckClaimState`; its residual explicitly
required the false equality
`sequenceFrom(1,N,"X") = sequenceFrom(1,N,"0")` on the nonnegative branch.
The concrete satisfying witness `N=0` gives mutant `"X"` versus required
`"0"`. This mutation changes the theorem's executed program term, not merely
an external Python file. See `evidence/stage4-body-sensitivity.log`.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive inventory. It enumerates every
local syntax declaration, configuration cell, `[function]` declaration,
ordinary rule, helper equation, and used-constructor mapping.

In summary, `semantic.k` contains 31 local operational rules:

- module initialization and left-to-right statement sequencing;
- function installation;
- assignment with disjoint existing/new-key cases;
- `while` and `if` guard evaluation and Boolean dispatch;
- return evaluation, caller-environment restoration, continuation restoration,
  and one-frame pop;
- literal/name evaluation;
- left-to-right integer/string addition;
- left-to-right `<` and `<=`;
- builtin integer-to-string conversion; and
- one-argument named function call/return.

The four state cells are all necessary and their updates are consistent. The
caller continuation saved by the call rule is exactly the continuation
restored by return; return correctly discards the remaining current-function
statements. Functions are framed across calls. There is no heap, allocation,
I/O, exception, or external state used by this program.

All submitted constructors (`Module`, `FuncDef`, `Params`, `If`, `Assign`,
`While`, `Return`, `Int`, `Str`, `Name`, `BinOp`, `Compare`, `CmpOp`, and both
forms of `Call`) have applicable declarations and rule paths. Evaluation and
statement order match the submitted Python subset. Numeric values use
unbounded K `Int`, matching the mathematical source `int` domain.

`functionEnd()` is declared but has no rule for implicit fall-through. This is
a visible, unused language limitation rather than an unsound fabrication:
both target branches execute a `Return`. Generated semantics is permitted to
omit unused constructs and behaviors.

`verification.k` adds eight fully equated `[function]` symbols through 11
rules. `sequenceFrom`, `sequence`, and `indexAfter` are mathematical
post-state definitions, not execution replacements. Their guards are
pairwise disjoint and exhaustive over K integers, their ground recursion
descends toward a base case, and their equations agree with ordinary integer
and string mathematics. The loop claim is the bridge-free universal
connection from actual loop execution to those summaries.

`loopCondition`, `loopBody`, `targetBody`, `targetFunction`, and
`targetProgram` are exact AST abbreviations. They introduce no result-bearing
oracle. The mechanical pinning and body-sensitive mutation validate their
connection to the immutable submitted program.

There are no local `[total]`, `[functional]`, `[simplification]`, priority,
`[concrete]`, `[trusted]`, or opaque declarations; no local priority or
simplification rules; no fresh unconstrained result; and no operational proof
rule that bypasses execution. Operational case overlaps are disjoint by
value/operator constructors or guards. Mathematical helper guards are
disjoint/exhaustive.

No rule was classified as unsound, so no false-conclusion witness is being
asserted or omitted. The one narrower evidence boundary—implicit
`functionEnd()` behavior—is explicitly outside the used program and is not
called unsound.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

No candidate mutation evidence was trusted or needed. I created
`evidence/spec-vacuity-audit.k`, which keeps the reachable `N=0` entry
configuration but changes its required result from `SVal("0")` to the false
`SVal("1")`.

The mutated spec first passed `kprove --dry-run` with exit 0, establishing that
it parses and builds under the fresh proof definition. The actual proof then
exited 1 with `WarnStuckClaimState`. Its residual final configuration contains
`SVal("0") ~> .K` and explicitly reports that it cannot unify with the
destination. This is the intended unmet result obligation, not a parse error,
timeout, missing import, or unrelated crash.

The exact commands and residual are in
`evidence/stage6-nonvacuity.log`; the runner and mutation are preserved in
`evidence/stage6_nonvacuity.sh` and
`evidence/spec-vacuity-audit.k`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What is formally established

Under the freshly compiled `semantic.k`, the K reachability proof establishes
partial correctness for the actual trusted-regenerated candidate body:

- for every K integer `N`, any terminating execution from the clean entry
  configuration returns `SVal(sequence(N))`;
- the loop summary holds for every `I >= 1`, `N >= 0`, and arbitrary starting
  result string/irrelevant framed state;
- negative inputs return empty, nonnegative inputs return the single-space
  decimal sequence from 0 through `N`; and
- the concrete `0` and `5` claims are valid instances.

The theorem is unrestricted over the source-contract integer domain. The loop
claim's nonnegative precondition does not narrow entry coverage: negative
inputs return before the loop, and every nonnegative entry reaches the loop
with `I=1`.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K 7.1.293 frontend, LLVM/Haskell backends, and reachability logic | All K build/run/proof results | Standard low-level toolchain trust; version independently recorded and all definitions rebuilt. |
| K builtin `Int`, `Bool`, `String`, `Map`, `List`, K sequencing, arithmetic/comparison, and concatenation | Operational semantics and helper equations | Acceptable fixed primitives. No task answer is encoded in them. |
| `Int2String` corresponds to Python's decimal `str(int)` on reachable positive loop indices | K/Python meaning bridge and final strings | Acceptable primitive bridge. It is the same builtin used by fixed loop execution and the summary; fresh K/Python runs through index 50 and static semantics support it. |
| Trusted CPython execution of `/reference/canonical.py` and `/reference/py2mpy.py` | Program-fidelity and source-intent bridge | Launcher-designated trusted inputs. Translator output is byte-identical; differential evidence has zero mismatches over 206 recorded inputs. |
| Generated `semantic.k` faithfully models the used Python subset | Interpretation of the K theorem as a Python-program theorem | Audited rule-by-rule, exercised on every branch boundary, and body-sensitive. This remains the normal explicit trust boundary of generated semantics, not a hidden assumption or oracle. |
| `sequenceFrom`, `sequence`, and `indexAfter` equations are ordinary mathematical definitions | Postcondition meaning | Exhaustive, disjoint, terminating on ground inputs, and universally connected to loop execution by the proved invariant. |
| Exact target AST abbreviation | Real-program identity | Machine-linked by trusted regeneration, KORE constructor equality, reachability normalization, and an executed-body mutation. |

Differential and concrete tests support only the stated Python/K bridges; they
are not used as a substitute for the universal K reachability proof.

### Excluded claims

This is a partial-correctness proof. It does not separately prove termination,
time or memory bounds, behavior for non-`int` arguments, or Python language
features absent from the submitted body (implicit `None` return, closures,
multiple/default arguments, exceptions, heap mutation, or I/O). None of those
exclusions narrows the material HumanEval source contract or a construct used
by the real submitted program.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. The candidate contains a sound,
result-constraining reachability proof of the trusted-regenerated program over
the full material source domain. There is no material adequacy gap and no
unsound proof extension.

VERDICT: PASS
LEGITIMACY: LEGIT
