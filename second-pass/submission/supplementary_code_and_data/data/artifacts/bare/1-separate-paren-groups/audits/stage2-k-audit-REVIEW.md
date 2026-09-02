# Independent adversarial review: 1-separate-paren-groups

This review treats every candidate artifact and generation record as untrusted
evidence. I rebuilt only from copied source under `/tmp/audit-work/rebuild`;
candidate-built definitions, caches, `kprove.out`, `krun-*.out`, and
`kore-exec.tar.gz` were not used to establish the result.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. The trusted
mount correctly has no `/reference/reference-semantics`; therefore there is no
mode/mount contradiction and no infrastructure breach.

All records required for this layout were read and inspected:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the JSONL trace at
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T03-47-50-019f8902-81a0-7132-bf36-6f07efd73d96.jsonl`.

Historical runtime metrics are not required for this legacy layout and were
not reconstructed. `usage.json` was present and was inspected. The structured
trace contains 266 valid JSON events, including 50 tool calls and 50 tool
outputs. Its final assistant message merely claims `KPROVE_PASSED`; that claim
was not trusted. A bounded trace inventory is in
`evidence/generation-trace-inventory.log`.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json`, whose SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded file hash checked against a mounted file matched,
including the run/task/result manifests, invocation and metrics, usage,
prompt, final text, output log, and individual JSONL trace. The independently
recalculated pipeline tree hashes are:

- candidate:
  `2912ea3c0e4486e103d25d57ade56084b7f5534d35b8782cb3fc9a08c479138b`,
  equal to the retained workspace hash in the stage-1 records;
- trace:
  `f769a846b3cff15293680c9b9e1ea798cb9ee8d2d6141bd15dd8b51e9e68e190`,
  equal to `usage.json`'s source-trace hash.

The candidate and trace trees contain no symlinks. All 23 required mounted
files checked by the audit script are regular, non-symlink files. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts. Exact
checks, hashes, commands, and exit 0 are preserved in
`evidence/provenance_check.sh` and `evidence/provenance-check.log`.

Stage 1 result: PASS. The provenance mounts are intact.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py`, the input is a string made of separate balanced
groups of nested parentheses, with spaces ignored. The result is the ordered
list of those groups with spaces removed. For example,
`"( ) (( )) (( )( ))"` must return `["()", "(())", "(()())"]`.

The trusted `/reference/canonical.py` scans characters, tracks nesting depth,
accumulates parentheses for the current group, and emits the current group
whenever a closing parenthesis returns depth to zero.

### Submitted implementation

`/candidate/solution.py` implements the same scanner on the documented
parenthesis/space alphabet. It uses one string rather than a character list for
the current group. For any non-space character other than `"("`, its `else`
branch treats that character as a close parenthesis. That differs from the
canonical program outside the documented alphabet, but not on the source
contract domain.

The trusted translator was run as:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/rebuild/solution.py > /tmp/audit-work/rebuild/regenerated-solution.mpy
cmp -s /tmp/audit-work/rebuild/regenerated-solution.mpy /tmp/audit-work/rebuild/solution.mpy
```

Both commands exited 0. Both MPY files have SHA-256
`1a0f6c1f65d3abac6f021e0a791a9f33236254b0f377f9b2cb3a8168e85c51ef`.
See `evidence/translation-identity.log`.

The reviewer-authored differential test independently imports the trusted
canonical entry point and the submitted Python entry point. It checked:

- the documented example;
- eight explicit empty, spaces-only, single-group, nested, adjacent-group, and
  mixed-space boundaries;
- all 29,524 strings over `() ` through length 9, of which 1,374 are balanced;
- 1,000 larger, deterministically generated valid inputs containing up to
  seven groups and up to 12 pairs per group.

The command

```text
python3 /audit-output/evidence/differential_test.py
```

exited 0 with zero mismatches. The script, deterministic input construction,
seed, representative input, and output are in
`evidence/differential_test.py` and `evidence/differential-test.log`.
As a scope check, `"(a)"` gives canonical `["()"]` but submitted `["(a"]`;
this is outside the parenthesis/space contract and is not used as an
in-domain counterexample.

Stage 2 result: PASS on the intended domain.

## 3. Clean proof reconstruction

Only `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and
`spec.k` were copied to the scratch rebuild. K reports version 7.1.293.

The concrete definition was rebuilt from `semantic.k`:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

Exit: 0. Log: `evidence/kompile-concrete.log`.

The proof definition was rebuilt from `verification.k` and its required
`semantic.k`:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

Exit: 0. Log: `evidence/kompile-proof.log`.

The auxiliary target was selected and proved independently:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.loop-invariant --output pretty
```

Exit: 0; output: `#Top`. Log:
`evidence/kprove-loop-invariant.log`.

The end-to-end target depends on that circularity, so the required positive
configuration is the complete spec:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC --output pretty
```

Exit: 0; output: `#Top`. Log: `evidence/kprove-all-claims.log`. This run proves
both the invariant and `program-correct`; no other positive claims exist.

A diagnostic selection of only `SPEC.program-correct` intentionally excluded
its auxiliary invariant and kept unrolling. It was interrupted with exit 130
after about 2.5 minutes and is not treated as a target-proof failure. The exact
diagnostic and interpretation are recorded in
`evidence/kprove-program-correct-alone-diagnostic.log`.

The fresh LLVM definition executed the actual regenerated `solution.mpy` on
the prompt example, empty input, `"()"`, `"(((())))"`,
`"()(())(()())"`, and spaces-only input. Every `krun` exited 0 with `.K` and
the expected exact `OutList`; logs are `evidence/krun-prompt.log`,
`krun-empty.log`, `krun-single.log`, `krun-deep.log`,
`krun-adjacent.log`, and `krun-spaces.log`. The corresponding independently
executed Python results are in `evidence/python-concrete-cases.log`.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` says: from the exact loop head and exact translated loop
body, with arbitrary remaining character sequence `CS`, nonnegative Peano
depth `D`, current-group characters `CURRENT`, existing outputs `OUT`, and last
loop character `LAST`, execution of the remaining loop and actual return
finishes with result
`OutList(stateOutput(runSpec(CS,D,CURRENT,OUT,LAST)))`. The input,
function map, and final local environment are irrelevant to this return-value
property.

`SPEC.program-correct` says: load and execute the exact submitted module from
empty environment/function maps with structural input `Encoded(CS)`. The final
`<k>` is `.K`, and the returned value is exactly
`OutList(separateSpec(CS))`. `CS` is universally quantified over finite lists
of `LP`, `RP`, and `SP`; there is no fixed size or unrolling bound.

Both preconditions are satisfiable. For the entry claim, `CS = LP RP` is one
ground witness. Fresh concrete execution of `Encoded(LP RP)` exited 0 and
returned exactly `OutList(out(LP RP))`; see
`evidence/krun-satisfying-entry-witness.log`. Both Python programs return
`["()"]` for the corresponding string.

### Mechanical program identity

The module term on `spec.k` lines 46-64 was mechanically extracted. K's
internal `.Stmts` notation was normalized only to the concrete parser's empty
statement-list spelling. `kast --output kore --sort Program` was then run on
that extracted term and on regenerated `solution.mpy`. `cmp` exited 0 and both
constructor terms have SHA-256
`4e302d5eb6de0339be8f48861a5049f1b5f1afe2f5354d2bebe6e31beda847c7`.
Artifacts and exact commands are in `evidence/program-pinning.log`,
`extracted-claim-program.mpy`, `normalized-claim-program.mpy`,
`solution-program.kore`, and `claimed-program.kore`.

The only omitted source-level effect is the typing-only
`from typing import List`, represented in the MPY term as `ImportFrom` and
executed by the generated semantics as an inert import. The function binding,
all initializations, loop, branches, append, and return are present. The loop
claim's body and continuation are the same constructors as the real loop and
the actual trailing `Return`.

### Input representation and result constraint

`Encoded(CS)` does not bypass the body; it only supplies the same runtime
`SVal(CS)` that `Raw(S)` supplies after `#chars(S)`. A reviewer-authored
connection claim for
`#inputValue(Raw(S)) => #inputValue(Encoded(#chars(S)))` exited 0 with
`#Top` (`evidence/spec-input-bridge.k`,
`evidence/kprove-input-bridge.log`). More strongly, the unchanged invariant
proves a reviewer-authored raw-input corollary for the exact module:

```text
<input> Raw(S) </input>
<result> none => OutList(separateSpec(#chars(S))) </result>
```

That command exited 0 with `#Top`; see
`evidence/spec-raw-corollary.k` and
`evidence/kprove-raw-corollary.log`. On the documented ASCII alphabet,
`#chars` visibly terminates and is covered by the concrete executions.

The entry result is not a free variable or one-way implication. It is an exact
equality to `OutList(separateSpec(CS))`. Final environment and function maps
are existentially abstracted, but neither can weaken the constrained result.
The false-result mutation in Stage 6 was rejected. A separate body-sensitivity
mutation changed both actually executed loop terms to append `Str("")` while
leaving the result contract unchanged. It built successfully and failed with
`WarnStuckClaimState` on the closing-parenthesis branch; see
`evidence/spec-body-mutation.k`, `spec-body-mutation-dry-run.log`, and
`spec-body-mutation-proof.log`.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive local declaration list is preserved in
`evidence/local-declaration-rule-inventory.log`. There are 67 rules in
`semantic.k`, 11 definitional rules in `verification.k`, and two reachability
claims. There are no local `[total]`, `[functional]`, simplification, priority,
`owise`, macro, `anywhere`, or opaque declarations.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `Ids`, `Params`, `Program`, and juxtaposed `Stmts`;
- statement constructors `ImportFrom`, `FuncDef`, `Assign`, `AugAssign`,
  `For`, `If`, `Return`, and expression-statement `Expr`;
- expression constructors `Name`, `Str`, `Int`, empty `ListExpr`, `Compare`,
  `Attribute`, and two-argument `Call`, plus `CmpOp`;
- finite `Char = LP | RP | SP`, character/output lists, Peano nonnegative
  integers, runtime values, raw/encoded inputs, and one-argument functions;
- control items `#boot`, `#load`, `#invoke`, `#exec`, `#assign`,
  `#augAssign`, comparison continuations, branch/loop continuations, `#set`,
  `#append`, `#discard`, and `#return`.

The configuration contains exactly the used state: computation, input, local
environment, function map, and result. Every constructor in `solution.mpy` is
declared: `Module`, `ImportFrom`, `FuncDef`/`Params`, statement lists,
`Assign`, `Name`, empty `ListExpr`, `Str`, `Int`, `For`, `If`, `Compare`/
`CmpOp`, `AugAssign`, `Expr`, `Call`/`Attribute`, and `Return`.

The six verification functions are `runSpec`, the four state projections, and
`separateSpec`. The seven semantic functions are `#chars`, `#char`, `#concat`,
`#snocOut`, `#inputValue`, `#eqChars`, and `#eqChar`. `[function]` is the only
special attribute.

### All 67 semantic rules

| Lines | Count | Inventory and finding |
|---|---:|---|
| 95-98 | 2 | `#chars`: empty and positive-length string cases. Guards are disjoint and cover K strings. Recursion strictly shortens the string. |
| 100-102 | 3 | `#char`: exact decoding for `"("`, `")"`, and space. It is intentionally partial and visibly sticks on an unused alphabet character. |
| 104-105 | 2 | `#concat`: complete structural character-list concatenation with strict descent. |
| 107-108 | 2 | `#snocOut`: complete structural append to the output list with strict descent. |
| 110-111 | 2 | `#inputValue`: `Raw` decodes; `Encoded` supplies the already decoded list. Both produce the same `SVal` under the connection above. |
| 113-116 | 4 | `#eqChars`: both-empty, exactly-one-empty, and both-nonempty cases. Patterns are complete/disjoint and implement structural equality. |
| 118-126 | 9 | `#eqChar`: all 3×3 character pairs, equal pairs true and unequal pairs false. |
| 128 | 1 | `#boot`: exposes the submitted module statement list without changing other cells. |
| 130-133 | 3 | `#load`: empty list invokes the named entry point; typing import is ignored; the function definition stores its exact parameter/body. Constructor cases are disjoint. |
| 135-138 | 1 | `#invoke`: selects the stored exact binding/body, binds its single parameter to the decoded input, and starts `#exec`. This is lookup plus entry setup, not an opaque result summary. |
| 140-141 | 2 | `#exec`: empty termination and head-before-tail sequencing. |
| 143-145 | 2 | assignment: evaluate RHS, then update the named local. Correct for all submitted assignments. |
| 147-155 | 5 | augmented assignment: evaluate RHS; concatenate strings; increment Peano depth by one; decrement `succ(N)`; and saturate `zero - 1` at zero. The relevant patterns are disjoint. Saturation is discussed below. |
| 157-159 | 3 | conditional: evaluate guard, then execute exactly the selected branch. |
| 161-164 | 4 | for-loop: evaluate iterable, convert a string value to a structural loop, terminate on empty, or set the loop variable then execute the body before the tail. It returns to the exact loop head used by the invariant. |
| 166-167 | 1 | `#set`: exact loop-variable environment update. |
| 169-171 | 2 | return: evaluate the expression, set result, and discard the current function suffix. The submitted return is at the end of the sole top-level invocation, so no caller/frame behavior is omitted on a reachable target state. |
| 173-174 | 2 | expression statement: evaluate and discard its value. |
| 176-178 | 2 | list append: evaluate the argument, structurally append it to the exact named `OutList`, and return `none`. This models the only mutable operation used. |
| 180-192 | 10 | comparison: evaluate left then right; Peano `depth == 0`; `ch != " "` for all three chars; and `ch == "("` for all three chars. The orientation of `#cmpRight` stores the left value and the listed cases are complete for the two submitted comparisons. |
| 194-199 | 5 | name lookup, string literal decoding, integer literals 0/1, and allocation of the one empty output list. |

No operational rule returns `separateSpec`, `runSpec`, or an unconstrained
oracle. The submitted loop, updates, comparisons, append, and return execute
under these rules. There is no rule priority that preempts that execution.

The minimal evaluation orders differ from full Python only where the omitted
behavior is inert for this body: a simple augmented-assignment target is read
after a side-effect-free name/literal RHS, and the fixed `result.append`
receiver is accessed after a side-effect-free argument. There are no
properties, descriptors, user calls, alias-sensitive copies, exceptions, I/O,
or nested calls in the submitted program.

### All 11 verification rules and both claims

`runSpec` has six constructor-disjoint equations:

1. empty input returns the current scanner state;
2. space changes only `LAST`;
3. `LP` increments depth and extends `CURRENT`;
4. `RP` at `zero` saturates, emits `CURRENT+RP`, and clears current;
5. `RP` at `succ(zero)` decrements, emits, and clears;
6. `RP` at `succ(succ(D))` decrements and extends current without emitting.

These cases cover all `Chars × PInt` inputs and recursively consume one
character. Four projection equations select depth/current/output/last from
`scanState`. The final equation defines `separateSpec` as the output projection
from the empty scanner state. Guards do not overlap, recursion descends, and
every returned value is fixed.

These are definitional summaries, not operational bridges: none matches a
program term or changes a runtime cell. The loop claim connects the exact
runtime loop to `runSpec`; circularity can recur only after the nonempty loop
rule consumes one character. The entry claim then executes the exact module
and uses that established loop claim. Neither claim is an axiom that rewrites a
program-defined call to a desired answer.

### Scope witness for the generated semantics

The zero-decrement rule is not full Python integer semantics. On out-of-contract
unbalanced input `")"`, fresh K execution returns structural
`OutList(out(RP))`, whereas submitted Python returns `[]`; see
`evidence/krun-unbalanced-out-of-domain.log` and
`evidence/python-unbalanced-out-of-domain.log`. Thus the comment in `spec.k`
that arbitrary `Encoded(CS)` is a “strict superset” is true only as a theorem
of this generated language, not as a Python-behavior theorem on that entire
superset.

This witness is not on the intended domain: every prefix of a sequence of
balanced parenthesis groups has nonnegative depth, so a close parenthesis is
never executed at depth zero. On every intended input, decrement always uses
the exact `succ(N) -> N` rule. Accordingly, I do not classify the saturation
rule as an in-domain unsoundness or as a material domain narrowing. It is a
non-fatal semantics-scope limitation.

Stage 5 result: PASS for the target domain, with the documented out-of-domain
limitation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` existed. The reviewer-authored
`evidence/spec-vacuity.k` retains the actual program and necessary invariant
but changes the entry result to require one additional empty output group:

```text
OutList(#snocOut(separateSpec(CS), .Chars))
```

For the satisfiable ground input `CS = LP RP`, the actual and Python result is
one group `[LP RP]`; the mutation requires `[LP RP, empty]`.

First:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, proving that the mutation parses and builds
(`evidence/spec-vacuity-dry-run.log`).

Then:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

exited 1 with `WarnStuckClaimState`. The residual is the expected unmet
equality between
`#snocOut(stateOutput(runSpec(...)), .Chars)` and
`stateOutput(runSpec(...))`, followed by the prover's “cannot be rewritten
further” error. It is not a parser error, timeout, or unrelated crash. Full
bounded output is in `evidence/spec-vacuity-proof.log`.

Stage 6 result: PASS. The proof is result-discriminating.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the rebuilt generated K definition:

- the exact submitted loop computes the output component of the structurally
  recursive `runSpec` scanner for arbitrary finite remaining `Chars` and
  arbitrary represented scanner state;
- the exact regenerated function binding/body, started from empty maps, returns
  exactly `OutList(separateSpec(CS))` for every structural `CS`;
- the same invariant entails the reviewer-checked raw-input corollary
  `OutList(separateSpec(#chars(S)))`;
- a changed executed body and a false extra-output postcondition do not prove.

This is a partial-correctness result. The operational model is deterministic
and structurally consumes finite `Chars`, but the benchmark asks only for
partial correctness.

### Trust ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| K 7.1.293 parser, kompilers, LLVM/Haskell backends, and reachability/circularity implementation | All execution and proof checking | Standard proof-engine trust boundary; fresh builds and actual exit/output records were used. |
| K built-in strings (`lengthString`, `substrString`), booleans, maps, tokens, and list machinery | Raw decoding, guards, bindings, structural values | Low-level generated-language primitives. Their uses are small and concrete executions cover every used construct. |
| Trusted CPython-AST translator | Identity between `solution.py` and `solution.mpy` | Launcher-designated trusted input; byte regeneration and constructor-level claim comparison both passed. |
| Ignoring `typing.List` import | Module setup/control only | Semantically inert for this function in the available Python environment; the import remains present in the executed term. |
| Raw string to structural `Chars` representation | Entry argument and all character branches | Equationally connected by a machine-checked reviewer claim and raw-input corollary; concretely checked on normal/boundary inputs. Only the documented ASCII alphabet is supported. |
| `separateSpec` as the meaning of “separate balanced groups” | Final human-facing property | The equations transparently implement the usual depth scanner: spaces are ignored, parentheses are accumulated, and a group is emitted exactly when a close returns depth to zero. This final English-to-equations correspondence is an inspected mathematical intent bridge, supported but not universally proved by the differential tests. |
| Peano nonnegative depth and saturating zero decrement | Arithmetic branch and output on malformed inputs | Exact on balanced-group inputs; not Python-exact on unbalanced strings, as witnessed above. This limits the advertised superset, not the HumanEval domain. |
| Existential final environment/function maps | Unobserved local/module state | They do not affect or loosen the exact result cell. No opaque result-bearing symbol exists. |

Finite differential and concrete tests are used only as evidence for program
fidelity and the representation/intent bridges. They are not substituted for
the K proof.

### Gate assessment and decision

- Gate A (real-program soundness): PASS on the intended domain. The exact body
  executes, the loop summary is proved rather than assumed, the result is
  constrained, constructor pinning succeeds, and both mutations are rejected.
- Gate B (intent adequacy): PASS for all finite balanced parenthesis-group
  strings with arbitrary spaces. There is no fixed-size restriction. The
  generated semantics' stronger arbitrary-`Chars` claim must not be interpreted
  as Python correctness on unbalanced inputs.
- Gate C (trust/evidence auditability): PASS. Source, exact commands, exit
  statuses, positive outputs, residuals, scripts, and bounded logs are
  preserved under `/audit-output/evidence`.

The proof is legitimate and covers the material HumanEval source-contract
domain. I select `CONCERNS`, rather than `PASS`, because the semantic model is
provably non-Python outside the balanced domain while the candidate describes
its arbitrary-`Chars` theorem as a strict superset, and because the last
`separateSpec`-to-English intent correspondence remains an inspected
mathematical bridge rather than a separately stated K theorem. Neither
limitation enables a false conclusion on an intended input.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
