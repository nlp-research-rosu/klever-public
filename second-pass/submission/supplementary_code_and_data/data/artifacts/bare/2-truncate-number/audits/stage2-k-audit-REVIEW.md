# Adversarial audit: 2-truncate-number

The candidate's proof reconstructs successfully, is result-constraining, and
uses the exact translated program. It is nevertheless not a legitimate proof
of the real program because the generated operational semantics contains a
materially unsound, result-bearing rule. The rule for `int` accepts every
`num(I,F,S)` while being justified only for canonical positive decompositions.
The definition therefore proves a false result for an accepted configuration
that its own value declaration says denotes the positive source input `2.0`.

All candidate and generation artifacts were treated only as untrusted evidence.
All builds and experiments used scratch copies under `/tmp/audit-work`.

## 1. Input and provenance integrity

The launcher record is `/audit-input.json`. It declares:

- problem `2-truncate-number`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted inputs `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

The independent checker
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) was run as
recorded in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log). It checked
entry types without following links, read every launcher container path,
recursively rejected links and unsupported nodes, parsed the structured trace,
and independently hashed the mounted bytes.

Results:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files. The campaign-lock object is exactly equal to the `audit_campaign`
  object in `/audit-input.json`. Its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The generated-semantics boundary is coherent:
  `/reference/reference-semantics` is absent and
  `mount_reference_semantics` is false. No hidden or inferred reference
  semantics was used.
- The required legacy-selected-stage1 records are present as regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`, and
  `/generation-evidence/prompt.txt`. The trace root is a real directory.
  `usage.json` is present and was also inspected. Historical runtime metrics
  are not required for this layout.
- Every directly recorded byte SHA-256 for the campaign lock, canonical,
  trusted prompt, trusted translator, run/task/result records, invocation,
  metrics, usage, prompt, Codex output, and Codex last message matched.
- Every evidence file listed in `/generation-result.json`, including the
  single structured JSONL trace, matched its listed SHA-256. The trace file
  hash is
  `9acf8186f25198ffd72388c28b736fcd2e3e1df0d62a05cc1fb1f1d566b4c87b`.
  All 152 JSONL records parsed; the trace has 28 tool calls and 28 corresponding
  outputs.
- The candidate prompt and translator are byte-identical to their trusted
  mounts. No candidate entry is a symlink or unsupported node.
- A transparent reviewer tree hash and all nine candidate file hashes are in
  the integrity log. The launcher does not specify the serialization used for
  its aggregate tree fields, so those opaque aggregate strings were not
  compared to a differently serialized reviewer digest; the mounted files
  themselves were inventoried and hashed individually.

The required generation records were read, not credited as proof. A bounded
summary of every trace tool call and its recorded output is in
[generation-trace-summary.log](/audit-output/evidence/generation-trace-summary.log).
It confirms only what the generator claimed to do: author a small custom
semantics, obtain `#Top`, run a concrete example, and reject its mutation. None
of those historical results was reused.

There is no audit-infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` asks for `truncate_number(number: float)` on a positive
floating-point number that can be decomposed into an integer part and a
remainder smaller than one. It must return that remainder; the documented
example is `truncate_number(3.5) == 0.5`. The decomposability language excludes
NaN and positive infinity. The material source domain is therefore positive
finite Python floats.

The trusted canonical implementation is:

```python
return number % 1.0
```

The submitted implementation is:

```python
return number - int(number)
```

For positive finite values, `int(number)` is the floor, so this is an
appropriate different algorithm. The scalar contract has no meaningful
"empty" input; the closest lower boundary is the least positive float.

### Trusted regeneration

The scratch command was:

```text
python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/generated-tests/solution.trusted.mpy
cmp /tmp/audit-work/generated-tests/solution.trusted.mpy \
    /tmp/audit-work/source/solution.mpy
```

Both files have SHA-256
`e6e7d0d86c096c41a28fb0a9484ca5eba52d16a0e173de1bfa782f769552f26b`;
`cmp` exited zero. See
[stage2-translation.log](/audit-output/evidence/stage2-translation.log).

### Independent differential test

[stage2_differential.py](/audit-output/evidence/stage2_differential.py)
independently imports the trusted canonical and submitted modules. It checks
the documented example, the least subnormal, the normal/subnormal boundary,
values immediately below and above integer boundaries, exact integers,
the `2**52`/`2**53` precision boundaries, and the greatest finite float. It
then checks 50,000 deterministic, uniformly generated positive finite
bit-patterns using seed `0x2A11D17`.

The command exited zero with zero bit-level result mismatches; all explicit
inputs and outputs are in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
The same log records adjacent excluded behavior: the implementations diverge
on negative `-3.5`, and positive infinity produces `nan` in the canonical but
raises in the submitted implementation. Those values are outside the stated
decomposable-positive domain and do not narrow the material contract.

Program fidelity passes.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/source`. No candidate
`*-kompiled` directory, cache, log, or historical trace was copied or used.

### Fresh definitions

The concrete definition was built from `semantic.k`:

```text
kompile semantic.k --backend haskell \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build/concrete-kompiled
```

The proof definition was separately built from `verification.k`:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build/proof-kompiled
```

Both used K v7.1.293 and exited zero. Exact records:

- [stage3-build-concrete.log](/audit-output/evidence/stage3-build-concrete.log)
- [stage3-build-proof.log](/audit-output/evidence/stage3-build-proof.log)

### Fresh concrete generated-semantics execution

[stage3_concrete_runs.sh](/audit-output/evidence/stage3_concrete_runs.sh)
ran the exact regenerated `solution.mpy` on six canonical decompositions:

| Python value | K input | K result |
|---|---|---|
| `3.5` | `num(3,1,2)` | `num(0,1,2)` |
| `0.25` | `num(0,1,4)` | `num(0,1,4)` |
| `1.0` | `num(1,0,1)` | `num(0,0,1)` |
| immediately below `1.0` | `num(0,9007199254740991,9007199254740992)` | same fraction with integer component zero |
| immediately above `1.0` | `num(1,1,4503599627370496)` | `num(0,1,4503599627370496)` |
| `2**53` | `num(9007199254740992,0,1)` | `num(0,0,1)` |

Every `krun` exited zero with `.K`. The exact commands and complete bounded
configurations are in
[stage3-concrete-runs.log](/audit-output/evidence/stage3-concrete-runs.log).
[stage3_concrete_oracle.py](/audit-output/evidence/stage3_concrete_oracle.py)
computed the corresponding Python values and exact integer ratios independently;
it exited zero in
[stage3-concrete-oracle.log](/audit-output/evidence/stage3-concrete-oracle.log).
Together these runs exercise every operational rule used by the submitted
program, including both zero-integer and zero-fraction boundaries.

### Every positive claim

The original spec was run intact:

```text
kprove spec.k --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC
```

It exited zero and printed `#Top`:
[stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log).

Because the two candidate claims are unlabeled, exact one-claim copies were
made rather than relying on a possibly ambiguous label selector:

- [spec-symbolic-only.k](/audit-output/evidence/spec-symbolic-only.k) exited
  zero and printed `#Top` in
  [stage3-kprove-symbolic.log](/audit-output/evidence/stage3-kprove-symbolic.log).
- [spec-example-only.k](/audit-output/evidence/spec-example-only.k) exited zero
  and printed `#Top` in
  [stage3-kprove-example.log](/audit-output/evidence/stage3-kprove-example.log).

Thus every positive target claim closes independently. This establishes
closure under the candidate's theory, not the truth of that theory.

## 4. Adequacy and real-program pinning

### Claims in plain language

The symbolic entry claim starts with:

- the submitted module constructor;
- a request to invoke `truncate_number` on `num(I,F,S)`;
- an empty environment and `noResult`;
- `S > 0`, `I >= 0`, `0 <= F < S`, and `I > 0 or F > 0`.

It requires termination with empty `<k>`, the parameter bound to the original
value, and result `num(0,F,S)`. Its `ensures` says that this result has zero
integer component and a proper nonnegative fraction.

The second claim is the same statement at ground input `num(3,5,10)`, with
ground result `num(0,5,10)`.

Both preconditions are satisfiable. `I=3,F=5,S=10` witnesses the symbolic
claim, and the ground example has no additional precondition. Substitution
gives rational result `5/10`; both trusted canonical and submitted Python
implementations return `0.5`.

### Mechanical constructor identity

[stage4_pinning.py](/audit-output/evidence/stage4_pinning.py) tokenizes balanced
constructor terms rather than comparing prose. Both `Module(...)` terms in
`spec.k` are token-for-token identical to regenerated `solution.mpy`. It also
checks that the entry rule rewrites the matched `BODY`, rather than a summary
or external source placeholder. The checker exited zero; see
[stage4-pinning.log](/audit-output/evidence/stage4-pinning.log).

The trusted translator omits Python type annotations. Here that omission is
semantically inert for the requested return-value property: the built-in
`float` annotation is not rebound, and no result depends on function annotation
metadata.

There are no helper or loop claims. The real control path is:

```text
module/invoke -> function body -> Return -> left operand lookup
-> int-call argument lookup -> int application -> subtraction -> result
```

The result is fixed to `num(0,F,S)`, not fresh, unconstrained, tautological, or
only one-way related to the intended value.

### Body sensitivity

[body-mutation-spec.k](/audit-output/evidence/body-mutation-spec.k) changes the
constructor term actually executed by the claim from the submitted subtraction
body to `return int(number)`, while retaining the original expected fraction.
It builds, executes to `intValue(3)`, and `kprove` exits 1 with
`WarnStuckClaimState`. The validating wrapper exits zero after confirming the
expected residual:
[stage4-body-mutation.log](/audit-output/evidence/stage4-body-mutation.log).

The claim therefore pins and depends on the actual submitted body.

## 5. Rule-by-rule static soundness review

The line-numbered source and attribute search are preserved in
[stage5-rule-inventory.log](/audit-output/evidence/stage5-rule-inventory.log).

### Complete local declaration inventory

`semantic.k` declares:

- `Program ::= Module(Stmt)`;
- `Stmt ::= FuncDef(String,Params,Stmt) | Return(Expr)`;
- `Params ::= Params(String)`;
- `Expr ::= Name(String) | BinOp(String,Expr,Expr) | Call(Expr,Expr)`;
- `Value ::= num(Int,Int,Int) | intValue(Int)`;
- `Result ::= noResult | Value`;
- K items `invoke`, `eval`, `subtractLeft`, `subtractRight`, `applyInt`, and
  `finishReturn`.

The constructor productions have only `[symbol(...)]` attributes. `Result`
also has the `Value` subsort and `noResult` constructor. There are no local
strictness, priority, `owise`, concrete, simplification, functional, or opaque
function declarations.

The configuration has exactly `<python>` containing:

- `<k>` with the program followed by a one-argument invocation;
- `<env>` initially `.Map`;
- `<result>` initially `noResult`.

There is no heap, output, exception, or allocation cell. That is adequate for
this pure one-expression function, but it intentionally models no broader
Python state.

`verification.k` declares exactly two `[function,total]` symbols:
`validPositive(Value)` and `validFraction(Value)`. Each has one equation for
`num` and one for `intValue`, so the two constructor patterns are disjoint and
cover all `Value` constructors. The equations are nonrecursive and agree with
their stated predicates. There are no other proof-local functions, lemmas,
rewrites, priorities, simplifications, fresh variables, or opaque result
symbols.

`spec.k` contains exactly the two entry claims already reconstructed. Running
them separately rules out mutual claim circularity.

### Submitted constructor coverage

| Submitted constructor | Declaration and behavior |
|---|---|
| `Module` | `Program` production; function-entry rule |
| `FuncDef` | `Stmt` production; entry rule checks the definition and invocation names are the same |
| `Params("number")` | `Params` production; entry rule binds that parameter |
| `Return` | `Stmt` production; return evaluation and final-result rules |
| `BinOp("-")` | `Expr` production; three left-to-right subtraction rules |
| `Name("number")` | `Expr` production; map lookup rule |
| `Call(Name("int"), ...)` | `Expr` production; dedicated built-in-int evaluation and application rules |
| `Name("int")` | Syntactically present and selected by the exact call rule; it is not evaluated through the ordinary name rule |

No used construct is silently unmodeled.

### Every ordinary operational rule

| Source | Rule | Static assessment |
|---|---|---|
| `semantic.k:44-45` | `Module(FuncDef(F,Params(P),BODY)) ~> invoke(F,V)` becomes `BODY` and binds `P` | Executes the actual matched body. Name equality pins the selected binding. Reads/writes only `<k>` and the initially empty `<env>`. Sound for the exact one-function submitted module. |
| `semantic.k:47` | `Return(E)` becomes `eval(E) ~> finishReturn` | Preserves expression evaluation before result storage. Its framed arbitrary continuation is broader than the one-statement target context and does not implement general Python return unwinding. No such continuation is reachable from the submitted grammar/body; this is a scope gap, not the fatal witness below. |
| `semantic.k:49-50` | `eval(Name(X))` looks up `X |-> V` | Standard deterministic lookup; exact target environment contains `number`. |
| `semantic.k:52-53` | Start `BinOp("-")` by evaluating the left expression | Correct first step of Python's left-to-right evaluation. |
| `semantic.k:54-55` | Preserve the left value while evaluating the right | Correct ordering and binding for the target. |
| `semantic.k:56-57` | `intValue(J) ~> subtractRight(num(I,F,S))` becomes `num(I-J,F,S)` | Correct exact-rational subtraction under the stated `num` interpretation. For canonical positive binary-float encodings, the corresponding Python subtraction is exact; that correspondence is not proved in K and is accounted for in Stage 7. |
| `semantic.k:59` | Recognize `Call(Name("int"),ARG)` and evaluate `ARG` before `applyInt` | Correct for the exact module, which cannot rebind `int`. The rule would bypass arbitrary alternate bindings, but the submitted syntax/control path contains none. |
| `semantic.k:61` | Every `num(I,_F,_S) ~> applyInt` becomes `intValue(I)` | **Unsound over its complete match domain.** It omits the canonical-positive guard on which its comment and truth depend. This directly supplies the result-bearing integer used by subtraction. Concrete false witness below. |
| `semantic.k:63-64` | A returned `Value` is stored when result is `noResult` | Correct for the initial and only return of the submitted function. |

The operational rule shapes and continuations are otherwise disjoint; there is
no priority-dependent overlap. Evaluation strictly progresses through finite
continuation constructors. The two total Boolean functions have disjoint,
complete equations and no recursive descent issue.

### Fatal false-conclusion witness

The semantics itself states at `semantic.k:18-20` that
`num(I,F,S)` denotes `I + F/S`. Its initial configuration accepts arbitrary
integer `IPART`, `FRAC`, and `SCALE`, and the `applyInt` rule has no guard.
Consequently:

```text
num(0,2,1) denotes 0 + 2/1 = 2.0
```

This is a positive finite source-domain value. Fixed Python behavior is:

```text
int(2.0) = 2
truncate_number(2.0) = 2.0 - 2 = 0.0
```

The generated semantics instead performs:

```text
num(0,2,1) ~> applyInt  => intValue(0)
num(0,2,1) - intValue(0) => num(0,2,1)
```

and thus returns a value that its own declaration says denotes `2.0`.

[unsound-apply-int-witness.k](/audit-output/evidence/unsound-apply-int-witness.k)
contains the exact submitted constructor body and that input. The command:

```text
kprove unsound-apply-int-witness.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module UNSOUND-APPLY-INT-WITNESS
```

exited zero and printed `#Top`, while independent execution of the real
submitted Python program on `2.0` returned `0.0`. The complete machine-checked
false-conclusion witness is in
[stage5-unsound-apply-int-witness.log](/audit-output/evidence/stage5-unsound-apply-int-witness.log).

The target claim's `validPositive` precondition rejects this *representation*
because `F < S` is false. That does not validate the operational rule over its
complete match domain: the semantics configuration and rule both accept the
state, the state denotes an intended positive value according to the
candidate's own declaration, and the same unguarded result-bearing rule is used
to close the target proof. A sound small semantics could either make
canonicality part of the accepted configuration or guard `applyInt`; this
candidate does neither. Per the proof-extension soundness contract, an off-path
globally false rule is not repaired by a narrower target claim.

For additional boundary evidence,
[stage5-scope-boundaries.log](/audit-output/evidence/stage5-scope-boundaries.log)
records this execution and a negative-value execution. The negative witness is
outside the source contract and is not independently used to claim
unsoundness; the positive `2.0` witness above is sufficient.

This is a Gate A real-program soundness failure.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was not relied upon.

[fresh-vacuity-spec.k](/audit-output/evidence/fresh-vacuity-spec.k) is a fresh
symbolic mutation. It keeps the exact submitted body and full
`validPositive(num(I,F,S))` precondition, but changes the result from
`num(0,F,S)` to the false off-by-one obligation `num(0,F +Int 1,S)`.
`num(3,1,2)` is an explicit satisfying witness: the real and modeled result is
`num(0,1,2)`, not `num(0,2,2)`.

The mutated spec parsed and reached the final proof obligation. `kprove` exited
1 with `WarnStuckClaimState`; its residual explicitly contains the failed
implication `F #Equals F +Int 1`. The validating wrapper confirmed both the
stuck-claim diagnostic and implication failure:
[stage6-fresh-vacuity-validated.log](/audit-output/evidence/stage6-fresh-vacuity-validated.log).

An earlier preserved log,
`stage6-fresh-vacuity.log`, contains the same correct K failure, after which an
overly formatting-specific reviewer `rg` check made the wrapper exit 1. The
checker was narrowed to the semantic diagnostic and rerun in the validated log;
there was no parser error, timeout, or unrelated backend failure.

The proof is result-discriminating and non-vacuous. This does not cure the
unsound semantics rule.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate-authored K theory, for every integer triple satisfying

```text
S > 0
I >= 0
0 <= F < S
I > 0 or F > 0
```

execution of the exact submitted constructor body from the specified empty
environment terminates with `number` bound to `num(I,F,S)` and result
`num(0,F,S)`. The same theory establishes the `3.5` example. The fresh mutation
shows that the result equality is genuinely required.

That is a theorem of the supplied K theory. It is not, by itself, a theorem
that the theory faithfully implements Python.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 Haskell backend and built-in `Int`, `Bool`, `Map`, comparisons, Boolean operators, and `-Int` | Builds, symbolic simplification, all claims | Ordinary low-level tool/math trust; acceptable. |
| Trusted `/reference/py2mpy.py` | Program-term identity | Byte regeneration and constructor comparison establish the specific translation. Annotation omission is informally inert for this result property; acceptable. |
| Candidate `num(I,F,S)` interpretation as exact rational `I+F/S` | Input bridge, subtraction, postcondition meaning | Result-bearing language-model boundary. It is useful on canonical states but contradicted by the unguarded `applyInt` behavior on an accepted positive-value state; illegitimate as supplied. |
| Candidate direct function-entry and built-in-int selection rules | Binding and control | Exact submitted module has one function, one parameter, no rebinding, and no effects. Body sensitivity supports this narrow bridge. General Python module/call behavior is excluded. |
| Informal IEEE-754 bridge: every positive finite float has a canonical dyadic decomposition; positive `int` equals floor; subtracting that integer is exact for this operation | Claim that the rational theorem covers all positive finite floats | Mathematically plausible and supported by boundary/concrete tests, but not machine-checked in K. This would warrant a non-fatal concern if the operational theory were otherwise sound. |
| 19 explicit plus 50,000 generated differential cases | Implementation/canonical and float/rational adequacy evidence | Finite empirical evidence only; zero mismatches do not prove universal equivalence. |
| Candidate historical `#Top`, prose, logs, and mutation | None | Untrusted and not used for the verdict. |

### Gate and benchmark decision

- Dynamic reconstruction: pass. Every positive claim independently prints
  `#Top` and exits zero.
- Program identity/result constraint: pass.
- Non-vacuity: pass.
- Intent/domain adequacy: the formal canonical-triple domain can represent
  every positive finite float, so there is no material finite-size or
  bounded-unrolling restriction.
- Real-program soundness: fail. The central result-bearing `applyInt` rule is
  false over its actual match domain and enables the preserved positive-input
  false conclusion.
- Evidence/trust: the float bridge is informal and finite-tested, but that
  limitation cannot rescue Gate A.

The candidate therefore relies on materially unsound generated semantics.
Clean `#Top`, faithful source translation, and a good mutation test do not make
that a legitimate proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
