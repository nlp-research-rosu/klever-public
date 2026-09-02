# Independent adversarial review: 144-simplify

The candidate reconstructs to `#Top`, constrains the returned Boolean, and
mechanically executes the submitted constructor term.  It is nevertheless not
a legitimate proof of the real generated Python program over its own
unrestricted formal precondition.  The generated semantics models every
`int(string)` conversion of a canonical positive decimal string as a successful
unbounded K integer conversion.  Actual CPython 3.10.12 raises `ValueError` when
the decimal has more than its default 4,300 digits.  A concrete 5,000-digit
input satisfies both the HumanEval contract and the general K claim's
precondition; rebuilt K execution returns `true`, while the submitted Python
program raises.  This is a material, used-operation/exception mismatch, not an
unused-language omission.

## 1. Input and provenance integrity

The launcher record declares:

- problem `144-simplify`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`; and
- no mounted reference semantics.

`/audit-campaign-lock.json` is a regular file with SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Its parsed object is exactly equal to the `audit_campaign` block in
`/audit-input.json`.  The campaign identifiers, image digest, prompt digest,
Kit commit/tree, K version, and toolchain lock therefore agree.

All launcher-declared container paths exist and are non-symlinked.  The required
legacy-selected-stage1 records were read:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the one structured trace file under
  `/generation-evidence/codex-trace/2026/07/22/`.

The historical `legacy-metrics.json` and `legacy-run-input.json` were also
inspected.  A historical `runtime-metrics.json` is absent, which is permitted
for this declared layout.  All 216 JSONL trace records parse; the trace contains
41 tool calls, 41 tool outputs, and one task-complete record.  The generation
records are treated only as untrusted historical claims.

Every checkable SHA-256 recorded in `/audit-input.json` matches its mounted
file, including the run/task/result manifests, generation prompt, invocation,
metrics, usage, output, final message, trusted prompt, trusted translator, and
canonical implementation.  The trace file also matches the per-file digest in
`/generation-result.json`.  An independent content manifest records every
mounted candidate file with path, mode, size, and SHA-256; its canonical JSON
digest is
`56344d727e41e9b9a3e37ab9d75604c00222ebaa38351b5cd75af18a6470333a`.
This is an independently chosen manifest encoding, separate from the launcher's
opaque tree-digest encoding.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
trusted `/reference` copies.  Candidate, reference, and generation-evidence
trees contain no symlinks or special files.  The required proof sources are
regular readable files.  `/reference/reference-semantics` is absent, and both
reference-semantics hashes in `/audit-input.json` are null, as
`GENERATED_SEMANTICS` requires.

There is no infrastructure breach.  Full checks, exact hashes, file inventory,
trace counts, and command exit 0 are in
`/audit-output/evidence/stage1_integrity.py` and
`/audit-output/evidence/stage1_integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For `x = a/b` and `n = c/d`, where `a,b,c,d` are positive whole numbers,
`simplify(x,n)` must return whether the exact rational product is a whole
number.  Equivalently, it returns:

```text
(a * c) mod (b * d) == 0
```

The three required examples are true for `1/5 * 5/1`, false for
`1/6 * 2/1`, and false for `7/10 * 10/2`.

The submitted `/candidate/solution.py` splits both strings, converts all four
components with Python `int`, multiplies numerators and denominators, and tests
the exact remainder.  This is the intended mathematical algorithm.

The trusted translator was rerun on the scratch copy:

```text
python3 /tmp/audit-work/reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`7ecb2f7431d89174b428beaf24f9780e442ad6baecbeeda3d22924443d88ef3d`;
`cmp` exited 0.  Thus the submitted `solution.mpy` is byte-identical to trusted
regeneration.  See `/audit-output/evidence/stage2.log`.

### Independent differential test

`/audit-output/evidence/differential.py` independently imports the trusted
canonical entry point and the generated entry point.  It also uses an exact
integer oracle derived directly from the contract.  Its valid input scope is:

- all three documented examples;
- explicit minimum, divisibility-boundary, remainder-one, leading-zero, and
  large-integer cases;
- every positive quadruple `a,b,c,d` in `1..20`; and
- 10,000 deterministic pseudo-random quadruples in `1..10^9` with seed 144.

This is 170,015 valid cases, whose serialized input list has SHA-256
`22b410227f521498853ae74272c1658d1a329613c05185299ecb5f4efc0165e7`.
There were zero generated-program/exact-oracle mismatches.

The trusted canonical had three discrepancies:

1. `18014398509481985/2 * 1/1` is not integral, but its float division rounds
   to an integer-valued float and canonical returns `True`.
2. The two 400-digit probes raise `OverflowError` in canonical's float
   division.

These are defects/limits of the trusted reference implementation relative to
the exact natural-language contract, not defects in the candidate's modulo
algorithm.  Empty strings and a zero denominator were retained as explicitly
out-of-contract diagnostics; both implementations reject them, with differing
exception messages.  Exact results and exit 0 are in
`/audit-output/evidence/stage2.log`.

## 3. Clean proof reconstruction

Only source files copied explicitly from `/candidate` were used.  No
candidate-built K definitions or K caches were copied.  K reports version
7.1.293.

The independently executed builds were:

```text
kompile --backend haskell semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Both exited 0.  See `/audit-output/evidence/stage3_build.log`.

The source-generated semantics was concretely run on the actual
`solution.mpy`, not on `simplifyProgram`.  The cases were:

| `x` | `n` | K result | Python result |
|---|---|---:|---:|
| `1/5` | `5/1` | true | true |
| `1/6` | `2/1` | false | false |
| `1/1` | `1/1` | true | true |
| `0001/0006` | `0002/0001` | false | false |
| `18014398509481985/2` | `1/1` | false | false |
| one 401-digit power of ten over `1` | `1/1` | true | true |

Every `krun` exited 0 with `.K` and the expected result cell.  The exact
commands and complete configurations are in
`/audit-output/evidence/stage3_concrete.log`.

Every positive target claim was then selected and run independently:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.<label>
```

| Claim | Exit | Proof output |
|---|---:|---|
| `simplify-general` | 0 | `#Top` |
| `example-true` | 0 | `#Top` |
| `example-false-one` | 0 | `#Top` |
| `example-false-two` | 0 | `#Top` |

The individual logs are
`/audit-output/evidence/stage3_claim_simplify-general.log`,
`stage3_claim_example-true.log`, `stage3_claim_example-false-one.log`, and
`stage3_claim_example-false-two.log`.  The only diagnostics are unused
right-hand-side map-variable warnings.

Dynamic reconstruction therefore passes.  This proves closure under the
candidate's theory; it does not cure the semantic mismatch identified in
Stage 5.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

| Claim | Precondition | Postcondition |
|---|---|---|
| `simplify-general` | `A,B,C,D` are unbounded K integers and each is strictly positive.  Inputs are the canonical decimal strings `A/B` and `C/D` produced by `Int2String`.  Function and environment maps start empty and result starts `noResult`. | Computation is empty and result is exactly `boolVal(((A*C) % (B*D)) == 0)`.  Final function/environment maps are existentially unconstrained, but the result is not. |
| `example-true` | The concrete inputs are `1/5`, `5/1`; maps/result have the same initial state. | Computation is empty and result is exactly true. |
| `example-false-one` | Inputs `1/6`, `2/1`. | Computation is empty and result is exactly false. |
| `example-false-two` | Inputs `7/10`, `10/2`. | Computation is empty and result is exactly false. |

All four claims place `simplifyProgram ~> invoke("simplify",...)` in `<k>`.
There are no helper, loop, or invariant claims.

`/audit-output/evidence/program_pinning.py` mechanically extracts the balanced
right-hand side of the `simplifyProgram` rule, parses it and the trustedly
regenerated `solution.mpy` through `kast`, canonicalizes the KAST JSON, and
compares it.  Both constructor trees have KAST SHA-256
`bfef01035e778450b9537f6d51c0c18b33646996b45ddd271856876ba2827072`.
The constructor terms are equal.  Differences in extracted source-text hashes
are whitespace only.  This establishes the permitted constructor-level
pinning: the rule expands to the exact submitted function binding and body.

Satisfiable states include:

- `A=B=C=D=1`, with claimed/canonical/generated result true;
- `A=1,B=2,C=D=1`, with all three results false; and
- `A=1,B=5,C=5,D=1`, with all three results true.

The precondition is therefore not contradictory, and substitution agrees with
both Python implementations on these witnesses.  See
`/audit-output/evidence/stage4_program_pinning.log`.

A separate body-sensitivity mutation changed the executed constructor
`CmpOp("==", Int(0))` to `CmpOp("==", Int(1))` in the scratch
`verification.k`.  It did not merely change external `solution.py`.  The
mutated definition compiled, but the original `example-true` claim exited 1
with `WarnStuckClaimState`; the residual had result false.  The mutated source
is `/audit-output/evidence/verification-body-mutated.k`, and the exact run is
in `/audit-output/evidence/stage4_body_mutation.log`.  The theorem is sensitive
to the executed body.

The formal general claim does cover all positive numeric values, but only their
canonical `Int2String` encodings.  Other accepted spellings such as arbitrarily
many leading zeroes are not universally claimed; the finite leading-zero
concrete/differential tests do not prove that additional string domain.  This
scope observation is secondary to the decisive canonical 5,000-digit witness,
which is inside the claim itself.

## 5. Rule-by-rule static soundness review

There are no generated helper K files.  The local inventory contains 32 rules
in `semantic.k`, four rules in `verification.k`, and four reachability claims
in `spec.k`.  The independently enumerated source is preserved in
`/audit-output/evidence/stage5_inventory.log`.

### Syntax, declarations, attributes, and cells

Every local syntax declaration is:

| Source | Declaration |
|---|---|
| `semantic.k:5` | `ParamList ::= List{String,","}` |
| `semantic.k:6` | `Params ::= Params(ParamList)` |
| `semantic.k:8-15` | `Expr ::= Name(String) | Int(Int) | Str(String) | Attribute(Expr,String) | Call(Expr,Expr) | Subscript(Expr,Expr) | BinOp(String,Expr,Expr) | Compare(Expr,CmpOp)` |
| `semantic.k:16` | `CmpOp ::= CmpOp(String,Expr)` |
| `semantic.k:18-20` | `Stmt ::= FuncDef(String,Params,Stmts) | Assign(Expr,Expr) | Return(Expr)` |
| `semantic.k:21` | `Stmts ::= List{Stmt,""}` |
| `semantic.k:22` | `Module ::= Module(Stmts)` |
| `semantic.k:24-30` | `PyVal ::= intVal(Int) | boolVal(Bool) | strVal(String) | pairList(PyVal,PyVal) | builtinInt | splitMethod(PyVal) | slashSplit(String)` |
| `semantic.k:31` | `Int ::= decimalValue(String)` |
| `semantic.k:32` | injection `Expr ::= PyVal` |
| `semantic.k:33` | `PyVals ::= List{PyVal,","}` |
| `semantic.k:35` | `Function ::= function(Params,Stmts)` |
| `semantic.k:36` | `Result ::= noResult | result(PyVal)` |
| `semantic.k:52-64` | `KItem ::= exec | invoke | bind | finishReturn | getAttribute | callWith | apply | indexWith | indexApply | binRight | binApply | compareRight | compareApply`, with the argument sorts shown in source |
| `verification.k:6` | `Module ::= simplifyProgram` |

Only `slashSplit` and `decimalValue` are locally declared `[function]`.  Neither
is declared `total`; both have an `[owise]` equation.  There are no local
`[total]`, `[functional]`, `[opaque]`, or explicit `priority(n)` declarations.
The three verification equations are `[simplification]`.  No syntax or rule
encodes the desired Boolean as an oracle.

The configuration has exactly the state used by the subset: `<k>`,
`<functions>`, `<env>`, and `<result>` inside `<simplify>`.  There is no heap,
I/O, exception, or call-stack cell.

The constructor inventory of `solution.mpy` is `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, `Call`, `Attribute`, `Str`, `Subscript`, `Int`, `BinOp`,
`Return`, `Compare`, and `CmpOp`.  Each is declared above and has a material
execution path below.

### All semantic and verification rules

| ID / source | Rule role | Static judgment |
|---|---|---|
| S1 `semantic.k:66` | `Module(SS) => exec(SS)` | Correctly enters module statement execution. |
| S2 `:67` | empty `exec` disappears | Correct list base case. |
| S3 `:68` | execute head statement before tail | Correct source statement order. |
| S4 `:70-71` | store a `FuncDef` in `<functions>` | Correct for the sole top-level definition; preserves other map entries. |
| S5 `:73-75` | invoke a stored two-parameter function and bind two already-evaluated `PyVal`s | Correct on the entry path.  It resets the environment and has no Python call stack, which is adequate only for this non-recursive, top-level call. |
| S6 `:77` | assignment evaluates RHS then schedules `bind` | Correct evaluation order. |
| S7 `:78-79` | bind computed value into environment | Correct local update. |
| S8 `:81` | return evaluates its expression then schedules `finishReturn` | Correct evaluation order. |
| S9 `:82-83` | finish return, discard remaining function continuation, set result | Correct for this sole top-level function call.  The match is globally broad and no frame restoration is modeled, but the exact submitted path has only the remaining function-statement continuation and no caller frame. |
| S10 `:85` | integer literal to `intVal` | Correct. |
| S11 `:86` | string literal to `strVal` | Correct. |
| S12 `:87` | name `int` to builtin marker | Correct because the actual environment never shadows `int`. |
| S13 `:88-89` | environment lookup | Correct on the actual bound names.  It could overlap S12 in an off-program environment that binds `int`; no such reachable intended state was found. |
| S14 `:91` | evaluate attribute receiver before attribute lookup | Correct ordering. |
| S15 `:92` | bind `split` method marker | Correct for string values.  It is syntactically broad over `PyVal`, but non-string application has no succeeding used rule. |
| S16 `:94` | evaluate call target before argument | Correct Python order for the one-argument calls used. |
| S17 `:95` | evaluate argument before application | Correct. |
| S18 `:96-97` | dispatch `str.split("/")` to `slashSplit` | Correct binding and delimiter on the actual call sites. |
| S19 `:98-103` | split at the first slash into a two-element `pairList` | Correct for valid fraction strings containing exactly one slash.  For an off-contract string with multiple slashes it does not model the full Python list, but no false intended-domain conclusion witness follows. |
| S20 `:104` | dispatch Python `int(str)` to unbounded `decimalValue` | **Materially unsound as a model of the real program over the formal domain.**  It omits CPython's used conversion exception; witness below. |
| S21 `:105` | `decimalValue(S) => String2Int(S)` fallback | Mathematically parses K integer strings, but together with S20 fabricates a normal result where CPython raises; same witness below. |
| S22 `:107` | evaluate subscript base first | Correct. |
| S23 `:108` | evaluate index second | Correct. |
| S24 `:109` | pair index 0 | Correct on split results. |
| S25 `:110` | pair index 1 | Correct on split results; disjoint from S24. |
| S26 `:112` | evaluate binary left operand first | Correct. |
| S27 `:113` | evaluate binary right operand second | Correct. |
| S28 `:114` | integer multiplication | Correct for Python's mathematical integers. |
| S29 `:115-116` | integer remainder with nonzero divisor | Correct for the positive denominator product; the guard is guaranteed by the entry precondition. |
| S30 `:118` | evaluate comparison left operand | Correct for the single comparison used. |
| S31 `:119` | evaluate comparison right operand | Correct. |
| S32 `:120-121` | integer equality to Boolean | Correct. |
| V1 `verification.k:7-31` | `simplifyProgram` expands to the submitted module | Exact KAST equality was mechanically established; all four claims depend on it. |
| V2 `:36-38` | symbolic slash split of two `Int2String` components | The equation is ordinary mathematics for all integers because integer renderings contain no slash.  It is a proof-local operational acceleration and has no bridge-free machine-checked universal connection; finite concrete evidence is supportive only. |
| V3 `:39` | `decimalValue(Int2String(I)) => I` | Mathematically true for K's hooks.  No bridge-free universal proof closes.  It also participates in the inadequate unbounded model of Python conversion. |
| V4 `:40` | `String2Int(Int2String(I)) => I` | Mathematically true inside K and required for symbolic closure.  As a bridge to actual Python `int`, it is false over the unrestricted formal domain because Python can raise; witness below. |

The specialized V2/V3 rules overlap the S19/S21 fallbacks only where the
specialized rules apply; `[owise]` gives the specialized equations precedence.
For canonical positive decimal strings their mathematical right-hand sides
agree.  Index rules, binary-operation rules, and comparison rules have
disjoint constructor/operator patterns.  No unsoundness is inferred merely
from broader off-program contexts.

Bridge-free connection claims were attempted in complete configuration
contexts against `audit-semantic-kompiled`, which excludes `verification.k`.
All three universal equations remained stuck: the Haskell backend did not
symbolically establish the needed string-hook identities.  This is not a
counterexample to the equations, so it is recorded as a narrower universal
evidence gap rather than labeled mathematical unsoundness.  Exact artifacts
and residuals are in `/audit-output/evidence/bridge-check.k` and
`/audit-output/evidence/stage5_bridge_checks.log`.  The earlier functional-claim
form was rejected as unsupported and is separately retained as
`stage5_bridge_checks_attempt1.log`; it is not treated as proof evidence.

### Concrete false-conclusion witness for the unsound Python-conversion model

Let:

```text
A = 10^4999
B = C = D = 1
x = the canonical 5000-digit Int2String(A) followed by "/1"
n = "1/1"
```

All four K integers are positive, so this satisfies `simplify-general`.
The strings have exactly the required canonical positive-fraction format.  On
the actual audit/runtime Python 3.10.12,
`sys.int_info.default_max_str_digits == 4300`.  The submitted program's first
`int(...)` raises:

```text
ValueError: Exceeds the limit (4300) for integer string conversion:
value has 5000 digits
```

The freshly rebuilt candidate `semantic.k`, on the exact same
`solution.mpy` and strings, exits 0 with `.K` and:

```text
<result> result ( boolVal ( true ) ) </result>
```

The exact input has SHA-256
`24064dc320c75fc39fa370010c5b88e3b31789971f8dc0b913e5073755864c57`.
The independent script and bounded output are
`/audit-output/evidence/long_input_semantics.py` and
`/audit-output/evidence/stage5_long_input_semantics.log`.

Thus S20/S21 and the V4 proof bridge enable a concrete false execution
conclusion on an intended input satisfying the entry precondition: K concludes
that the real function returns true, but the real function returns no Boolean
and raises.  Because integer conversion is a material operation used four
times by the submitted program, this is not acceptable minimal semantics or an
unused-construct gap.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`.  A fresh reviewer-authored mutation
is preserved at `/audit-output/evidence/spec-vacuity.k`.  It executes the exact
submitted term on `x="1/5", n="5/1"` but changes the result obligation from true
to false.

The witness satisfies the entry state and direct Python execution returns true.
The scratch verification definition and mutated spec both compiled.  The
independent proof command was:

```text
kprove spec-vacuity.k --definition nonvacuity-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-result-mutation
```

It exited 1 with `WarnStuckClaimState`.  The residual is a completed `.K`
configuration whose result cell is `result(boolVal(true))`, which does not
unify with mutated false.  This is the expected unmet result obligation, not a
parse error, timeout, missing import, or unrelated crash.

The mutation therefore passes the non-vacuity test.  Exact build/proof commands,
inner exit status, and residual are in
`/audit-output/evidence/stage6_nonvacuity.log`.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Inside the candidate's K theory, the successful general reachability claim
establishes:

> For all unbounded K integers `A,B,C,D > 0`, executing the exact submitted
> constructor module and invoking `simplify` on canonical K-rendered strings
> `A/B` and `C/D` reaches an empty computation with result exactly
> `boolVal(((A*C) % (B*D)) == 0)`.

It also establishes the three concrete prompt examples.  The result is
constrained; the fresh false result is rejected.  No `PROOF.md`, historical
trace, or differential test is used as a substitute for these reachability
proofs.

### Trust ledger

| Boundary / assumption | Effect and dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` | Establishes source-to-constructor correspondence for all claims. | Acceptable here: trusted mount equals candidate copy and fresh output is byte-identical. |
| Candidate-authored operational semantics S1-S32 | Defines all execution used by every claim. | Most rules are adequate for the submitted subset.  S20/S21's missing used exception is illegitimate over the claim's unbounded domain. |
| K integer hooks `*Int`, `%Int`, comparisons | Determine arithmetic and result. | Acceptable mathematical primitives for positive integers. |
| K string hooks `+String`, `Int2String`, `String2Int`, `findString`, `substrString`, `lengthString` | Determine input construction, splitting, and conversion; general claim depends on them. | Hook implementations are trusted.  Their use as a complete model of CPython `int` is illegitimate because the concrete 5,000-digit witness diverges. |
| V2 slash-split simplification | Lets the general proof bypass symbolic string search/substrings. | Equation appears mathematically sound, but lacks the required bridge-free universal connection proof.  This is an evidence/trust limitation, not the witnessed false rule. |
| V3/V4 inverse-conversion simplifications | Fix the symbolic integer values and close the general claim. | True inside ideal K string arithmetic; no bridge-free universal proof closes.  V4 is also part of the false bridge to actual CPython conversion behavior. |
| `simplifyProgram` expansion | Pins the actual module term for all claims. | Acceptable: constructor-level parser comparison is exact and a body mutation invalidates the theorem. |
| Differential and concrete tests | Support Python algorithm fidelity and selected semantic bridges. | Finite evidence only.  They do not prove universal semantics correspondence; the broader 5,000-digit probe in fact refutes it. |
| Trusted canonical implementation | Comparison oracle requested by the audit. | Not a universal exact oracle because its float arithmetic has demonstrated rounding/overflow discrepancies.  Those do not excuse the candidate semantic mismatch. |

### Gate and decision accounting

- Fresh positive verification: **pass**.  Every claim independently prints
  `#Top` and exits 0.
- Result constraint and body sensitivity: **pass**.
- Fresh non-vacuity: **pass**.
- Real-program semantic soundness: **fail**.  A used Python conversion and its
  exceptional control effect are replaced with unconditional unbounded K
  conversion, with the concrete false-conclusion witness above.
- Intent/domain adequacy: **fail for the claimed unrestricted domain**.  The
  formal precondition includes the 5,000-digit canonical input, but the real
  generated program does not have the proved return behavior.
- Trust/evidence: independently reproducible, but the proof-local string
  equations additionally lack bridge-free universal connection theorems.

The benchmark decision boundary requires `FAIL / NOT_LEGIT` for a proof that
relies on materially unsound generated semantics.  A genuine `#Top` under that
semantics cannot establish partial correctness of the real generated program.
The consolidated exact-command/exit-status index is
`/audit-output/evidence/COMMANDS.md`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
