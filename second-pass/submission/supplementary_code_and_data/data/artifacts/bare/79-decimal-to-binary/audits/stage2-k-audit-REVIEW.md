# Independent adversarial audit: 79-decimal-to-binary

## Executive conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program under its generated semantics. The trusted translator regenerates the
submitted `solution.mpy` byte-for-byte; every entry claim executes that exact
constructor term; the candidate semantics soundly covers every construct used
by the term; and the two symbolic claims cover all mathematical integers.

I rebuilt separate LLVM and Haskell definitions from source in
`/tmp/audit-work/audit79`, without using `/candidate/.kbuild`. The original
five-claim `spec.k` returned `#Top`, and an inertly labeled copy allowed each
claim to be replayed separately, with `#Top` and exit 0 each. Both a body
mutation and a distinct false-postcondition mutation built successfully and
were rejected for the expected unmet result equality.

The proof is conditional on the correctness of K 7.1.293 and its domain
primitives, as all K proofs are. The generated Python-subset semantics is also
outside the reachability theorem, but its complete local rule set is small,
non-oracular, and directly justified below. It introduces no material adequacy
gap for this program.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as this mode requires; no hidden or
inferred reference semantics was used.

I inspected `/audit-input.json` before candidate artifacts and then checked:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object equals the `audit_campaign` block exactly.
- Every record required for `legacy-selected-stage1` is a regular readable
  file: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. Historical
  `runtime-metrics.json` is absent, but is not required for this declared
  legacy layout.
- Direct SHA-256 checks match every corresponding recorded regular-file hash.
  The trace's sole JSONL file has the result-recorded hash
  `6aa61a88652123ba80984d409d6dd0bf28a940f7b4f28414dc804bad2612ab9a`.
  All 175 trace lines parse as JSON and include one user message and one
  completed-task event.
- An independent length-delimited tree digest of `/candidate` is
  `2b4eb312652d8bac39f9c391fffcbb4f281f84eea6d6c92d3ea98bf044058830`,
  matching the retained-workspace hash in both the stage result and invocation.
  The corresponding trace-tree digest is
  `3f538cb02d7b66fe04d61c34c1c2439f53201e89afaa050897100eea3201e9b4`,
  matching `usage.json`.
- No entry below `/candidate` or `/generation-evidence` is a symlink.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  `/reference` files and match the recorded hashes.
- All required candidate proof artifacts are present as regular files.

The prior `KPROVE_PASSED` text in the log/trace was treated only as an
untrusted historical claim. Full checks, hashes, trace type counts, and exact
statuses are in
[`stage1_integrity.log`](evidence/stage1_integrity.log); the independent checker
is [`stage1_integrity.py`](evidence/stage1_integrity.py).

Stage 1 result: **PASS; no infrastructure breach.**

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an integer `decimal`, return a string consisting of `"db"`, followed by
the payload produced by Python `bin(decimal)[2:]`, followed by `"db"`.
The documented examples are `15 -> "db1111db"` and
`32 -> "db100000db"`. The prose describes a binary payload; for the usual
nonnegative HumanEval domain it contains only `0` and `1`. The trusted
canonical implementation is exactly:

```python
return "db" + bin(decimal)[2:] + "db"
```

The candidate implements the same expression. On negative Python integers the
canonical expression has the perhaps surprising payload beginning with `b`
(for example `-5 -> "dbb101db"`); the candidate and theorem preserve that
canonical behavior in addition to covering the ordinary nonnegative domain.

### Translator and differential results

Running the trusted `/reference/py2mpy.py` on the scratch `solution.py`
produced SHA-256
`b6ff40e8ee7da4fb4cc501f09c4cc85a38fa63951d9f53479c1922bd949c6666`,
byte-identical to submitted `solution.mpy`. After removing the canonical
docstring, the canonical and candidate function arguments and bodies are also
AST-identical.

The independent differential used the trusted canonical module as oracle. It
tested 1,149 deterministic integers: both examples, `-2,-1,0,1,2,3`, the dense
range `[-128,128]`, neighborhoods around powers of two through exponent 129,
and seeded signed values up to 512 bits. There were zero mismatches. Empty and
other non-integer values are outside the K `Int` theorem; an additional parity
probe confirmed that `""`, `None`, `0.0`, `[]`, and `{}` raise the same Python
exceptions in both implementations.

Artifacts:

- [`differential_test.py`](evidence/differential_test.py)
- [`differential_inputs.json`](evidence/differential_inputs.json)
- [`stage2_fidelity.log`](evidence/stage2_fidelity.log)

Stage 2 result: **PASS.**

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/audit79`; candidate-provided
compiled definitions, `__pycache__`, and caches were not copied or used.
`kup` is absent, but independently installed `kompile`, `krun`, and `kprove`
are all available at K version 7.1.293.

The final clean replay used:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition concrete-kompiled-final

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition verification-kompiled-final

kprove spec.k --definition verification-kompiled-final --spec-module SPEC
```

Both compilations exited 0. The original `spec.k` proof printed `#Top` and
exited 0.

For per-claim checking, [`label_positive_spec.py`](evidence/label_positive_spec.py)
added only labels and changed the module name. The resulting
[`spec-labeled.k`](evidence/spec-labeled.k) was run five times with `--claims`.
The nonnegative symbolic claim, negative symbolic claim, example 15, example
32, and example -5 each printed `#Top` and exited 0.

The clean LLVM semantics was independently executed on 12 normal and boundary
inputs: huge negative, `-17,-2,-1,0,1,2,3,15,32,1024`, and a huge positive.
Every `krun` exited 0 and every K result matched both trusted canonical Python
and candidate Python. This exercises the sign split, the `binDigits` base and
recursive cases, both documented examples, and arbitrary-precision values.

The complete successful clean replay is
[`stage3_rebuild_final.log`](evidence/stage3_rebuild_final.log), driven by
[`stage3_rebuild_final.sh`](evidence/stage3_rebuild_final.sh) and
[`concrete_semantics_compare.py`](evidence/concrete_semantics_compare.py).
An earlier preserved log, `stage3_rebuild.log`, has an audit-local exit 1
because the first version of the result parser did not allow K's printed
`~> .K` wrapper; its visible K values and all proof commands were successful.
The parser was corrected, then the entire clean replay above completed with
driver exit 0. This was a reviewer diagnostic defect, not a candidate or
infrastructure failure.

Stage 3 result: **PASS.**

## 4. Adequacy and real-program pinning

### Plain-language claims

| Claim | Satisfiable precondition | Required final result |
|---|---|---|
| 1 | any `I >= 0`, e.g. `I=0` | `strVal(decimalToBinarySpec(I))` |
| 2 | any `I < 0`, e.g. `I=-1` | `strVal(decimalToBinarySpec(I))` |
| 3 | argument `15` | `strVal("db1111db")` |
| 4 | argument `32` | `strVal("db100000db")` |
| 5 | argument `-5` | `strVal("dbb101db")` |

Claims 1 and 2 partition all mathematical `Int`, so there is no finite bound
or material source-domain narrowing. Substitution gives, among others,
`I=0 -> "db0db"` and `I=-1 -> "dbb1db"`; these agree with both Python
implementations and the clean K executions.

[`program_pinning.py`](evidence/program_pinning.py) removed whitespace and
mechanically compared the constructor term between `<k>` and `=> .K` in every
entry claim against submitted `solution.mpy`. All five terms have normalized
SHA-256
`fbb7ca290d81c351043a0db996ba32e407e861e9e68b38dadba0cba1bbca954b`
and compare equal. Trusted regeneration connects `solution.py` to
`solution.mpy`; this constructor comparison connects `solution.mpy` to the
claimed program.

The entry rule also pins the function name `decimal_to_binary`, parameter
`decimal`, `Return(E)`, supplied argument, and initial empty result. It binds
the actual argument to `decimal` and evaluates the actual body `E`; it does
not inject the expected result. There are no helper or loop claims and no free
right-hand-side result variable.

A separate body-sensitivity test changed the final constructor inside the
executed claim term from `Str("db")` to `Str("xx")`, leaving the original
postcondition intact. The mutated spec parsed (`--dry-run` exit 0), then
`kprove` exited 1 with `WarnStuckClaimState` and the residual equality
`"...db" = "...xx"`. See
[`spec-body-mutation.k`](evidence/spec-body-mutation.k) and
[`stage4_pinning_and_body.log`](evidence/stage4_pinning_and_body.log).

The immutable spec duplicates the translated constructor term rather than
regenerating it automatically. That is a maintenance observation, not a
pinning defect here, because both regeneration and mechanical identity hold.

Stage 4 result: **PASS.**

## 5. Rule-by-rule static soundness review

The exhaustive declarations/rules/claims inventory is
[`rule-inventory.md`](evidence/rule-inventory.md), corroborated by the corrected
[`stage5_static_scan_rerun.log`](evidence/stage5_static_scan_rerun.log).
The first preserved scan log contains a malformed reviewer regex; the corrected
scan confirms the intended absence check.

### Construct coverage

Every constructor in `solution.mpy` is declared and governed:

| Used constructor | Declaration / behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | exact entry rule consumes module and evaluates return expression |
| `BinOp`, `Str` | structural `eval` plus string `addValues` |
| `Subscript`, `Slice`, `Int`, `NoBound` | exact `[2:]` evaluation plus `suffixFrom` |
| `Call`, `Name("bin")` | exact builtin-call equation plus `callBin` |
| `Name("decimal")` | exact one-binding environment lookup |

The configuration has only the necessary `<k>`, `<arg>`, and `<result>` cells.
The program is pure: no heap, mutation, output, exceptions, allocation, or
control stack is used. Evaluation of the two concatenation operands is
represented by pure K functions, so the lack of an effectful sequencing cell
does not change observable behavior.

### Every semantic and verification rule

| Rules | Judgment |
|---|---|
| S1 entry (`semantic.k:56-63`) | Sound entry adapter. Exact name, parameter, and return-body shape; reads `<arg>`, consumes `<k>`, and writes only `<result>`. It continues with structural evaluation rather than a result oracle. |
| S2-S4 literals/name (`65-67`) | Sound constructor interpretation and exact matching one-variable lookup. |
| S5-S7 expression forms (`68-72`) | Sound for pure `+`, the fixed builtin binding `bin`, and `[START:]`. The submitted term uses only string `+` and `START=2`, for which downstream rules are present. Unsupported forms visibly remain stuck. |
| S8-S9 value addition (`74-75`) | Ordinary mathematical integer addition and K string concatenation. Constructors make the cases disjoint. Only the string case is material here. |
| S10-S11 `callBin` (`78-82`) | Guards `I>=0` and `I<0` are disjoint and exhaustive for `Int`. They correctly model Python strings `"0b"+digits` and `"-0b"+digits` via distinct internal wrappers. |
| S12-S13 slicing (`84-85`) | Correctly implement index 2: `"0b"+S` becomes `S`, while `"-0b"+S` becomes `"b"+S`. Wrapper constructors are disjoint. |
| S14-S15 `binDigits` (`87-90`) | Guards `0<=I<2` and `I>=2` are disjoint and cover every reachable argument. The base returns `"0"` or `"1"`; the recurrence uses quotient and remainder by 2 and strictly decreases for `I>=2`. This is the standard binary expansion recurrence. |
| V1-V2 specification (`verification.k:11-16`) | Disjoint exhaustive equations over all `Int`; they state the wrapper around the same fully defined binary-digit function and match canonical negative slicing. They summarize the desired mathematical result but do not replace execution. |

There are 15 local semantic rules and two verification equations. There are no
local `[total]`, `[functional]`, `[simplification]`, `[concrete]`, priority,
`owise`, macro, alias, opaque, or fresh-result declarations. All function
equations are deterministic on their used domains; all recursion descends.
There are no proof-local operational bridges, program-body shortcuts, derived
lemmas, or circularities.

Partiality outside the submitted subset is deliberate and visible: for example,
noninteger `bin` arguments, other slice starts, and other AST forms can become
stuck. No such construct is reachable from the submitted program with a K
`Int` argument. Generated-semantics mode expressly permits this minimal
coverage.

I found no unsound local rule and therefore make no unsoundness allegation
requiring a false-conclusion witness. The concrete semantics checks corroborate
the static reasoning but are not used as a substitute for it.

Stage 5 result: **PASS.**

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact; none was submitted. The fresh
[`spec-vacuity.k`](evidence/spec-vacuity.k) retains the exact original program
term and changes only the result obligation to demand an extra `"x"`:

```text
strVal(decimalToBinarySpec(I) +String "x")
```

`I=0` is a satisfying witness: the real result is `"db0db"`, while the mutation
demands `"db0dbx"`. `kprove --dry-run` exited 0, demonstrating successful
parsing/building. The actual proof exited 1 with `WarnStuckClaimState`; its
residual displays the failed equality between the original result and the
extra-suffix result. This is an expected unmet obligation, not a parser error,
timeout, missing import, or unrelated crash.

Exact command, status, and residual:
[`stage6_nonvacuity.log`](evidence/stage6_nonvacuity.log).

Stage 6 result: **PASS (meaningful false claim rejected).**

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the submitted generated semantics and K's imported domain theory, if the
exact submitted module is run with a mathematical integer argument and reaches
the modeled final state, then:

- for every nonnegative integer, the result is
  `"db" + standardBase2Digits(I) + "db"`;
- for every negative integer, the result matches canonical Python slicing,
  `"dbb" + standardBase2Digits(-I) + "db"`;
- in particular, the three fixed example claims have their stated strings.

The two symbolic guards cover all `Int`. The proof constrains `<result>` to a
specific function of the input and consumes `<k>`; it is neither vacuous nor an
existential/free-result theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, LLVM/Haskell backends, and `kprove` | all machine-checked results | Necessary low-level proof-tool trust; version recorded and cleanly replayed. |
| Imported `INT`, `STRING`, and `BOOL` domain primitives (`+Int`, `-Int`, `/Int`, `%Int`, comparisons, `Int2String`, `+String`) | evaluator, `binDigits`, spec equations | Acceptable fixed primitives. Used on domains where their ordinary meanings match Python arbitrary-precision integers and ASCII strings. |
| Trusted `py2mpy.py` | source-to-constructor bridge | Launcher-trusted input; independently rerun with byte identity, then constructor-level claim comparison. |
| Generated-semantics/CPython correspondence | interpretation of the reachability theorem as a Python result | Not a theorem inside K. Accepted here after exhaustive local rule review: every used construct is directly modeled, no result oracle exists, and 12 clean K/Python boundary executions provide finite corroboration. |
| `binDigits` as the mathematical meaning of binary output | human-facing contract | Fixed by exhaustive, disjoint, descending equations for every nonnegative integer. Its recurrence is ordinary positional-base-2 mathematics, not an opaque assumption. |
| Termination | partial-correctness interpretation | The requested theorem is partial correctness. Independently, all local recursion reached by concrete inputs descends; termination is not used to weaken the postcondition. |

Excluded behavior is limited to inputs outside the HumanEval integer domain and
unused Python constructs. Booleans, user objects with `__index__`, noninteger
exceptions, alternate builtins, arbitrary slicing, mutation, and other Python
features are not modeled. The candidate does not narrow the material integer
domain: its symbolic claims include every K integer.

Gate A (real-program soundness): **PASS**.  
Gate B (intent adequacy): **PASS**.  
Gate C (trust/evidence auditability): **PASS**.

The clean proof is sound, result-constraining, pins the real generated program,
and covers the unrestricted material integer domain. The appropriate benchmark
mapping is `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
