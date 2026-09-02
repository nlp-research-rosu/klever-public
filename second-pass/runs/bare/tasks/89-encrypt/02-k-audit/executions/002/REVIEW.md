# Independent adversarial audit: 89-encrypt

The candidate is not a legitimate proof of the HumanEval contract. Fresh
reconstruction does show a non-vacuous, body-sensitive `#Top` theorem under the
candidate's own K theory, and the theorem mechanically pins the submitted
constructor term. Two material bridges fail:

1. the submitted Python program changes every character, while the trusted
   canonical program changes only lowercase `a`–`z` and preserves every other
   character; and
2. the generated semantics is not a sound model of the submitted Python
   program over its stated string domain. It proves a value for invalid Python
   indexing and disagrees with Python on a concrete Unicode input.

The first is a source-contract failure and the second is a generated-semantics
soundness failure. Either is sufficient for `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

Status: PASS. There is no audit-infrastructure breach.

I read `/audit-input.json` first and used only its `container_paths` mounts.
The declared layout is `legacy-selected-stage1`, the condition is `bare`, and
the rendered mode is `GENERATED_SEMANTICS`.

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly matches the `audit_campaign` object in `/audit-input.json`, and
  matches its recorded hash.
- `/reference/reference-semantics` is absent, as generated-semantics mode
  requires. I did not look for or infer a hidden reference semantics.
- All required legacy-selected-stage1 records are present, regular, readable,
  and non-symlinked: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  The present `usage.json` was also checked. Historical runtime metrics are
  not required for this layout.
- The sole trace JSONL file has the declared SHA-256
  `3432913e924b1ba25979cb05a70418ca95107161be9bf474031104da259e1037`.
  All 258 records parse. The trace inventory contains one session record,
  50 custom tool calls with 50 outputs, two function calls with two outputs,
  and one task-complete event.
- Every generation output declared by both `invocation.json` and
  `generation-result.json` exists and matches its leaf hash. The run, task,
  stage-result, invocation, metrics, prompt, output, last-message, usage,
  canonical, prompt, translator, and lock hashes recorded by the launcher all
  match independently computed hashes.
- No symlink exists below `/candidate`, `/reference`, or
  `/generation-evidence`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.

The generation records claim `KPROVE_PASSED`, but I treated that only as
untrusted historical evidence. The independent checks and complete hashes are
in [01-provenance.log](evidence/01-provenance.log),
[check_provenance.py](evidence/check_provenance.py), and
[00-mounted-source-hashes.log](evidence/00-mounted-source-hashes.log).
The live tools were K 7.1.293 and Python 3.10.12; see
[00-toolchain.log](evidence/00-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

Status: FAIL.

### Trusted contract

The prompt at `/reference/prompt.py:2` says `encrypt` takes a string and
rotates alphabet letters by `2 * 2`, i.e. four places. It states no
lowercase-only precondition. The trusted implementation makes the intended
behavior precise at `/reference/canonical.py:17-24`: each lowercase character
in `"abcdefghijklmnopqrstuvwxyz"` is shifted four positions with wraparound,
and every character outside that alphabet is copied unchanged.

Thus the intended domain is unrestricted Python strings, not merely the finite
documented lowercase examples.

### Submitted implementation and regeneration

The submitted `/candidate/solution.py:1-4` recursively applies

```text
chr((ord(character) - 97 + 4) % 26 + 97)
```

to every character. It has no alphabet-membership branch and therefore does
not implement the canonical behavior outside lowercase `a`–`z`.

Regeneration with the trusted translator succeeded, and the result is
byte-identical to the submitted `solution.mpy`. Both files have SHA-256
`f0ce1818f2a6cbfcc0b656a5c4b604d24a526be95f6f285440ac91bae9ec7cab`.
The exact command, exit statuses, `cmp`, and hashes are in
[02-regeneration.log](evidence/02-regeneration.log). This proves translator
fidelity; it does not repair implementation fidelity.

### Independent differential test

[differential.py](evidence/differential.py) separately imports the trusted
canonical entry point and the submitted entry point. It covers:

- all four documented examples;
- empty/base and `a`, `v`, `w`, `x`, `y`, `z` wrap boundaries;
- uppercase, digits, whitespace, punctuation, and Unicode;
- every string of length 0–3 over a seven-character mixed alphabet;
- 300 deterministic generated strings of length 0–32; and
- a 1,200-character lowercase recursion boundary.

The exact run in [03-differential.log](evidence/03-differential.log) exits 0 as
a completed diagnostic and reports 610 mismatches among 724 inputs. Concrete
witnesses include:

| Input | Trusted canonical | Submitted Python |
|---|---:|---:|
| `"A"` | `"A"` | `"y"` |
| `"0"` | `"0"` | `"h"` |
| `"!"` | `"!"` | `"s"` |
| `"aA"` | `"eA"` | `"ey"` |

All documented examples and tested lowercase boundaries match. The mismatch is
the material, undocumented domain restriction: correctness holds only for
lowercase strings. The long lowercase case is a secondary discrepancy:
canonical Python returns a value while the recursive submission raises
`RecursionError`.

The benchmark decision rule explicitly maps such a material narrowing of the
HumanEval source-contract domain to `FAIL / NOT_LEGIT`.

## 3. Clean proof reconstruction

Status: the submitted all-claims K proof reconstructs, but its real-program
bridge fails in Stages 4–5.

I copied only candidate source artifacts to `/tmp/audit-work/candidate-src`.
No candidate-built definition or cache was copied or used.

### Fresh definitions and concrete execution

The LLVM definition was built from `semantic.k` and `verification.k` with:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled
```

It exited 0. See [04-kompile-concrete.log](evidence/04-kompile-concrete.log).
Fresh executions for `""`, `"hi"`, `"z"`, `"A"`, `"!"`, and `"aA"` all
terminated; the complete configurations and statuses are in
[05-krun-concrete.log](evidence/05-krun-concrete.log).

The Haskell proof definition was independently built with:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/proof-kompiled
```

It exited 0. See [06-kompile-proof.log](evidence/06-kompile-proof.log).

I also removed the `verification.k` requirement/import in an auditor scratch
copy and rebuilt the bare operational semantics. It compiled and executed
`"hi"` to `"lm"` without proof-local functions, showing that
`verification.k` does not contain a hidden operational shortcut. See
[semantic-base.k](evidence/semantic-base.k) and
[12-base-semantics-without-verification.log](evidence/12-base-semantics-without-verification.log).

### Fresh positive proof runs

The recursive call claim selected by label prints `#Top` and exits 0:

```text
kprove spec.k --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC --claims SPEC.encrypt-call-correct
```

See [07a-kprove-encrypt-call.log](evidence/07a-kprove-encrypt-call.log).

The candidate's submitted positive target—the complete two-claim proof
set—also prints `#Top` and exits 0:

```text
kprove spec.k --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC
```

See [07c-kprove-all.log](evidence/07c-kprove-all.log).

For completeness, I selected only `SPEC.program-correct`. That filter removes
the recursive helper circularity on which the entry theorem depends; it did not
terminate and was auditor-bounded after 144 seconds with status 130. See
[07b-kprove-program.log](evidence/07b-kprove-program.log). I do not mistake
this dependency diagnostic for a non-zero proof residual: the two-claim target
set itself closes. It does mean the entry claim has no isolated `#Top` after
its required companion claim is removed.

### Generated-semantics comparison

[compare_krun.py](evidence/compare_krun.py) invokes the fresh LLVM definition
and both Python implementations. For ASCII, K agrees with the submitted
Python, including its incorrect handling of non-lowercase characters. On
Unicode it exposes a generated-semantics defect:

| Input | Fresh K | Submitted Python | Canonical |
|---|---:|---:|---:|
| `"A"` | `"y"` | `"y"` | `"A"` |
| `"!"` | `"s"` | `"s"` | `"!"` |
| `"🙂"` | `"roil"` | `"t"` | `"🙂"` |

The exact completed diagnostic run is in
[08-krun-python-comparison.log](evidence/08-krun-python-comparison.log). Its
summary correctly reports that K does not match the submitted Python across
the tested string domain.

## 4. Adequacy and real-program pinning

Status: constructor pinning and result constraint pass; intent and execution
model adequacy fail.

### Claims in plain language

`encrypt-call-correct` at `/candidate/spec.k:7-17` says:

- for every K `String` `S`, arbitrary continuation `K`, map `ENV`, list
  `STACK`, and result cell value;
- provided the installed function is exactly named `"encrypt"`, has parameter
  `"s"`, and its body is exactly `solutionBody`;
- execution from an already evaluated string argument followed by
  `applyFun("encrypt")` reaches `rotate4(S)` followed by the same continuation;
  and
- the environment and call stack are restored and the result cell is
  unchanged.

This is the recursive circularity. It matches the actual call boundary reached
by the operational call rules and preserves the complete modeled state.

`program-correct` at `/candidate/spec.k:19-29` says:

- for every K `String` `S`;
- from the exact single-function module
  `Module(FuncDef("encrypt", Params("s"), solutionBody))`, the initial
  `start(S)`, empty function metadata, empty environment and stack, and
  `noResult`;
- execution consumes the entire `<k>` computation, installs the exact
  function and body, and leaves result exactly `rotate4(S)`.

There is no free result variable and no one-way implication in place of the
required equality.

Both preconditions are satisfiable. For example, the initial configuration
with `S = "a"` satisfies the entry precondition. The call claim is satisfied by
`S = "a"`, `K = .K`, the exact function cells, `ENV = .Map`,
`STACK = .List`, and `result = noResult`.

### Mechanical source and body pinning

The chain is:

1. trusted regeneration is byte-identical to `solution.mpy`;
2. the entry claim contains the same `Module`, `"encrypt"` binding, `"s"`
   parameter, and `solutionBody`;
3. `/candidate/verification.k:7-24` expands `solutionBody` to the exact
   constructor body in regenerated `solution.mpy`; and
4. a fresh K constructor equality claim over the full module prints `#Top`.

The last check is [pinning-spec.k](evidence/pinning-spec.k) with its exact run
in [09-pinning.log](evidence/09-pinning.log). K reports the claim as trivial
after function simplification, which is the expected result of constructor
identity.

Body sensitivity was tested independently. In
[body-mutation-spec.k](evidence/body-mutation-spec.k), the executed module term
changes the shift constant from 4 to 5 while retaining the shift-4 result
obligation on satisfying input `"a"`. K executes the mutated body to result
`"f"` and rejects the `"e"` obligation with `WarnStuckClaimState` and exit 1.
See [10-body-sensitivity.log](evidence/10-body-sensitivity.log). This is a real
program-term mutation, not an edit to an unused external source file.

### Concrete substitutions

| `S` | Claimed K result | Submitted Python | Canonical |
|---|---:|---:|---:|
| `""` | `""` | `""` | `""` |
| `"a"` | `"e"` | `"e"` | `"e"` |
| `"A"` | `"y"` | `"y"` | `"A"` |
| `"🙂"` | `"roil"` | `"t"` | `"🙂"` |

The theorem therefore pins the submitted constructor body, but it does not
prove the HumanEval result and does not describe the real submitted Python on
all strings.

## 5. Rule-by-rule static soundness review

Status: FAIL.

The machine-generated exhaustive declaration inventory is in
[11-rule-inventory.log](evidence/11-rule-inventory.log). It finds 11 syntax
declarations, one configuration, and 28 rules in `semantic.k`; two syntax
declarations and three rules in `verification.k`; and two claims in `spec.k`.
There are no other candidate K helper files.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: a list of `Stmt`;
- `Stmt`: `FuncDef`, `If`, and `Return`;
- `Params`: one string parameter;
- `Expr`: `Name`, `Str`, `Int`, `BinOp`, `Call`, `Subscript`, `Slice`, and
  `Compare`;
- `CmpOp`; and
- `Bound`: an expression or `NoBound`.

`MPY-SEMANTIC` additionally declares result values, value sorts, the 12
continuation/control constructors (`start`, `eval`, `exec`, `binLeft`,
`binRight`, `cmpLeft`, `cmpRight`, `subBase`, `applyFun`, `choose`, `endCall`,
and `finish`), and `appendStmts`.

The configuration has exactly the state used by the submitted program:
`<k>`, installed function name/parameter/body, current environment, saved
environment stack, and final result. There is no heap, I/O, exception, or
resource-limit cell.

Every constructor in `solution.mpy` maps to a declaration and an operational
path:

| Submitted constructor | Declaration/rule path |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax lines 7, 10, 14; load rule 67–71 |
| statement list, `If`, `Return` | lines 9–12; rules 110–116 |
| `Name`, `Str`, `Int` | lines 16–18; rules 73–76 |
| `BinOp("+", ...)` | line 19; rules 78–81 |
| `BinOp("-", ...)` | line 19; rules 78–80, 82 |
| `BinOp("%", ...)` | line 19; rules 78–80, 83 |
| `Compare`, `CmpOp("==", ...)` | lines 23–24; rules 85–90 |
| `Call` of `chr`, `ord`, `encrypt` | line 20; rules 98–108 |
| integer `Subscript` | line 21; rules 92–94 |
| `Slice(Int(1), NoBound, NoBound)` | lines 22, 25; rules 92, 95–96 |

Missing semantics for other Python constructs is not a defect in this
generated-semantics condition because the submitted program does not use them.

### Operational rules

Every local operational rule is decided below. “Sound on the submitted
reachable path” is deliberately narrower than global Python soundness.

| ID | Candidate lines | Decision |
|---|---:|---|
| S1 | `semantic.k:51` | Empty-list `appendStmts` equation is true. |
| S2 | `semantic.k:52` | Cons-list append is true, structurally decreases, and completes S1's totality coverage. |
| S3 | `semantic.k:67-71` | Exact one-function module load preserves the submitted binding/body and schedules the call before `finish`; sound for this module. |
| S4 | `semantic.k:73` | String literal evaluation is sound. |
| S5 | `semantic.k:74` | Integer literal evaluation is sound. |
| S6 | `semantic.k:75-76` | Map lookup is sound when the binding exists; missing bindings remain visibly stuck. |
| S7 | `semantic.k:78` | Binary evaluation schedules the left operand first, as Python does. |
| S8 | `semantic.k:79` | After a left value, schedules the right operand and preserves the left value; sound evaluation order. |
| S9 | `semantic.k:80` | Integer addition delegates to unbounded K integer addition; sound for used operands. |
| S10 | `semantic.k:81` | String concatenation preserves left-to-right order; sound for the tested ASCII path. Its Unicode value depends on K String representation. |
| S11 | `semantic.k:82` | Integer subtraction is ordinary mathematics and sound. |
| S12 | `semantic.k:83` | `modInt` with the program's positive divisor 26 agrees with Python's modulo; sound on the used path. |
| S13 | `semantic.k:85-86` | Comparison evaluates its left side first; sound. |
| S14 | `semantic.k:87-88` | Comparison then evaluates its right side and preserves the left; sound. |
| S15 | `semantic.k:89-90` | String equality wrapped in `PyBool` is sound for K strings and enables explicit truth branching. |
| S16 | `semantic.k:92` | Subscript base-before-index evaluation is sound for the submitted expressions. |
| S17 | `semantic.k:93-94` | Unsound as Python indexing: it has no bounds/exception guard and equates indexing with K substring. It proves `""[0] => ""`, while Python raises `IndexError`. It also participates in the Unicode mismatch. Concrete false-conclusion witness below. |
| S18 | `semantic.k:95-96` | Adequate for ASCII `s[1:]` when `s` is nonempty, but not a faithful Python Unicode slice model. With S17 it makes the real submitted program return `"roil"` for `"🙂"` instead of Python's `"t"`. Concrete false-conclusion witness below. |
| S19 | `semantic.k:98-99` | Evaluates the sole argument before dispatch, matching this program's calls. It models only one argument, which is sufficient here. |
| S20 | `semantic.k:100` | Delegates `chr` to `chrChar` without an explicit range guard. The actual arithmetic always yields 97–122, so the used path is safe; behavior outside that path is an unmodeled-error limitation, not used here. |
| S21 | `semantic.k:101` | Delegates `ord` to `ordChar` without a length guard. The ASCII reachable path supplies one-character substrings. K/Python Unicode-unit disagreement makes the overall bridge unsound for `"🙂"`. |
| S22 | `semantic.k:103-108` | Exact installed-name match, singleton local environment, and saved caller environment model the submitted recursive call. It discards unrelated locals, but this body needs only `s`. |
| S23 | `semantic.k:110-111` | Evaluates the condition before choosing; sound. |
| S24 | `semantic.k:112-113` | True branch appends then-statements before remaining statements; sound. |
| S25 | `semantic.k:114-115` | False branch appends else-statements before remaining statements; sound. |
| S26 | `semantic.k:116` | Return discards remaining statements in the current `exec` and evaluates the return expression; sound control behavior. |
| S27 | `semantic.k:118-120` | `endCall` restores exactly one saved environment and leaves caller continuation intact; sound for recursive calls. |
| S28 | `semantic.k:122-123` | `finish` consumes only a string and writes it to the result cell; sound for this function's normal return. |

S17 has an independent symbolic/ground false-conclusion witness. The auditor
claim in [invalid-index-witness.k](evidence/invalid-index-witness.k) starts from
`eval(Subscript(Str(""), Int(0)))` and requires value `""`. The candidate
theory proves it with `#Top` and exit 0. The paired Python command raises
`IndexError` and exits 1. Both outputs are in
[13-invalid-index-witness.log](evidence/13-invalid-index-witness.log).
This is not an allegation without a witness: the rule literally enables a
false Python conclusion.

S17–S18 also have a witness through the real submitted control flow on an
intended-domain string: input `"🙂"` reaches final K result `"roil"` while the
submitted Python reaches `"t"`, as recorded in
[08-krun-python-comparison.log](evidence/08-krun-python-comparison.log).

There is one latent overlap that I do not label as a material unsoundness of
this submitted program: the string-argument user-call rule S22 could overlap
the builtin `ord` rule S21 if the single installed function were itself named
`"ord"`. There is no priority. The submitted module installs only `"encrypt"`,
so that overlap has no real-program witness here and is recorded as a reuse
limitation rather than used to justify the verdict.

### Proof-local equations and attributes

| ID | Candidate lines | Class and decision |
|---|---:|---|
| V1 | `verification.k:6-24` | `solutionBody` is `[function, total]` with one unconditional constructor equation. It is a definitional name for the exact regenerated body, not an execution replacement. Its equation is true and complete. |
| V2 | `verification.k:26-27` | `rotate4("") => ""` is a truthful base equation for the candidate's shift-every-unit summary. |
| V3 | `verification.k:28-32` | The guarded recursive `rotate4` equation decreases by the K string tail, is disjoint from V2 via `S =/=K ""`, and matches the candidate K execution. It does not establish the HumanEval meaning and inherits K/Python Unicode disagreement. It is a definitional summary, not an opaque oracle or operational bridge. |

`appendStmts` is the only `[function, total]` helper in `semantic.k`; its two
disjoint equations cover all `Stmts`. `solutionBody` is also total and fully
defined. `rotate4` is a function without a `total` attribute; its base and
guarded recursive equations cover concrete K strings. There are no local
`[functional]`, `[concrete]`, priority, or `owise` declarations, and no opaque
symbols.

### Claims and proof dependency

| Claim | Class | Static decision |
|---|---|---|
| `encrypt-call-correct` | Recursive auxiliary reachability claim/circularity | It starts at the exact post-argument call boundary, requires the exact binding/body, executes the body, preserves arbitrary continuation and result, and restores environment/stack. No ordinary rule replaces the call with `rotate4`. Sound under the candidate K semantics. |
| `program-correct` | Entry reachability claim | It executes the exact module and body, consumes `<k>`, and constrains result to `rotate4(S)`. It uses the helper circularity. Sound under the candidate K semantics, but inadequate for Python and the HumanEval contract. |

No result-bearing opaque symbol exists. The same `rotate4` symbol appears in
the helper and entry postconditions, but it is fixed by exhaustive recursive
equations and the body is actually executed; this is not the circular-oracle
anti-pattern. The failure is instead that the fixed equations and operational
string model characterize the wrong external behavior.

### Static soundness conclusion

The local K theory is sufficient to execute the exact constructor program and
supports a genuine recursive proof. It is nevertheless not a sound semantics
for the real Python program on the declared string domain. S17 proves a
globally false indexing conclusion, and S17–S18 yield a false complete-program
result for `"🙂"`. These are witnessed false conclusions, not merely missing
semantics for unused constructs.

## 6. Fresh non-vacuity test

Status: PASS.

The candidate supplied no `spec-vacuity.k`. I created the independent
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k). Its initial state is
the exact submitted program with satisfying input `"a"`, but it changes the
result-constraining destination from the true `"e"` to the deliberately false
`"f"`.

The exact command was:

```text
kprove spec-vacuity-audit.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

The spec parses and reaches the backend. Execution reaches a complete
configuration with `.K`, restored empty environment/stack, and result `"e"`.
The destination requires `"f"`, so `kprove` emits `WarnStuckClaimState` and
exits 1. See [14-non-vacuity.log](evidence/14-non-vacuity.log).

An earlier auditor draft had a parser error and is preserved separately as
`10a-body-sensitivity-initial-parser-error.log`; it is not counted as
non-vacuity or body-sensitivity evidence. The valid artifacts cited above
build, execute, and fail on the expected unmet result.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the candidate K definition and K's builtins, the combined
reachability proof establishes this partial-correctness statement:

> For every K `String` `S`, if the exact submitted constructor module starts
> in the stated empty configuration and reaches normal completion under these
> rules, its result is the recursively defined K value `rotate4(S)`.

The auxiliary theorem states the corresponding call-level summary for the
exact installed binding/body while preserving the modeled continuation,
environment, stack, and result cell.

The proof does not establish:

- that the submitted Python satisfies HumanEval/89;
- that `rotate4` preserves non-lowercase characters;
- that candidate K strings/indexing/slicing are equivalent to Python strings;
- Python exception behavior;
- CPython recursion/resource behavior; or
- termination of the actual Python function over unrestricted lengths.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, Haskell/LLVM backends, and reachability kernel | All build, run, and proof results | Ordinary unavoidable proof-tool trust boundary; acceptable for interpreting `#Top`. |
| K `Int` primitives `+Int`, `-Int`, `modInt` | Arithmetic rules, `rotate4`, both claims | Acceptable ordinary mathematics for the actual positive divisor and unbounded Python integers. |
| K `String` primitives `+String`, `==String`, `lengthString`, `substrString`, `ordChar`, `chrChar` | Literal/equality rules, index/slice/ord/chr rules, `rotate4`, final theorem | Acceptable only as K primitives. The candidate informally treats them as Python-string semantics; that bridge is unproved and concretely false for `"🙂"`. Illegitimate for the claimed real-program theorem. |
| K Map/List primitives | Name lookup, call environment, stack restore | Adequate for this one-local recursive body; no observable omitted state is used. |
| Trusted `py2mpy.py` transliteration | Constructor pinning | Trusted launcher input; byte regeneration and a K constructor claim verify the submitted source-to-term instance. It supplies syntax identity, not semantic correctness. |
| `solutionBody` | Both claims | Fully defined exact constructor alias; acceptable. |
| `rotate4` | Both postconditions | Fully defined K summary, not opaque. Its human-intent bridge is false because it rotates all units rather than only lowercase alphabet characters, and its Unicode bridge to Python is false. |
| Generated operational semantics | Entire theorem's link to Python | Candidate-created and inside the audit target. Concrete invalid-index and Unicode witnesses show it is not an acceptable trust boundary. |
| Differential tests | Program/canonical and K/Python bridge evidence | Reproducible finite evidence only. They expose counterexamples; they are not substituted for the K proof. |

There are no opaque symbols, unconstrained result-bearing oracles, empirical
rules, or proof-local operational bridges. The proof's failure is therefore
not vacuity or a smuggled answer rule. It is a theorem about an incorrect
implementation under a materially inaccurate generated semantics.

### Gate and decision summary

- Fresh verification under the submitted K theory: PASS for the complete
  two-claim target (`#Top`, exit 0).
- Real-program soundness: FAIL. The generated semantics proves false Python
  conclusions, witnessed by `""[0]` and `"🙂"`.
- Intent adequacy: FAIL. The program and theorem materially narrow the
  unrestricted string contract to lowercase strings.
- Non-vacuity and constructor/body sensitivity: PASS.
- Reproducibility: PASS; all relied-upon artifacts, commands, exits, and
  bounded outputs are under `/audit-output/evidence/`.

Because a materially narrowed HumanEval contract is `FAIL / NOT_LEGIT` under
the benchmark-specific mapping, and because the generated semantics also has
witnessed material unsoundness, no lesser `CONCERNS / LEGIT` verdict is
available.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
