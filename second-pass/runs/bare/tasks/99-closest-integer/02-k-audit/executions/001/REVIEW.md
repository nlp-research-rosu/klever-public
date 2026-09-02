# Independent adversarial review: 99-closest-integer

The candidate is **not a legitimate proof of the real generated Python
program**. Fresh reconstruction succeeds and the claims are non-vacuous, but
the generated semantics models `Decimal` addition and subtraction as exact
rational arithmetic. The submitted Python program instead performs those
operations under the ambient decimal context (default precision 28). This is a
material real-program soundness failure: two valid numeric-string witnesses
make K prove normal return values different from the values returned by the
submitted function.

All candidate artifacts, logs, traces, compiled definitions, and prose were
treated only as untrusted evidence. Execution used source copies under
`/tmp/audit-work/99-closest-integer`; no candidate-provided compiled definition
or cache was reused. Reviewer scripts and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. There is therefore no
trusted hidden semantics to compare against, and no infrastructure
contradiction. The candidate’s own `semantic.k` was audited on its merits.

Evidence: `evidence/stage1_integrity.log`.

### Required artifacts and types

The following candidate artifacts are present as regular files:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the JSONL structured trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

No symlink exists anywhere under `/candidate`. No required source artifact is
missing or mistyped. There are no additional generated helper K source files.
The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`; these are extra derived
artifacts, not source inputs, and were deliberately ignored. A candidate
`PROOF.md` and `spec-vacuity.k` are absent, but neither is a required generated
source artifact for this condition.

The scratch-source hashes match the corresponding candidate source hashes.
Evidence: `evidence/stage1_untrusted_claims.log`.

### Trusted prompt and translator

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`53ad185333496f1faa011070d323b24af3e23506e32f52ced0b3c0f9867d2719`).
`/candidate/py2mpy.py` is byte-identical to
`/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

### Untrusted generation claims

`run-input.json` identifies the bare/no-supplied-semantics condition and
records the same trusted prompt and translator hashes. `metrics.json` claims
an exit code of zero without a timeout. `codex-last.txt`,
`codex-output.log`, and the trace claim that 11 specifications closed with
`#Top`. The structured trace contains 154 valid JSON records and one final
agent message making that claim. These records were read but were not accepted
as proof evidence.

Evidence:

- `evidence/stage1_untrusted_claims.log`
- `evidence/trace_summary.py`
- `evidence/stage1_integrity.log`

**Stage 1 result: PASS.** There is no infrastructure breach or provenance
integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt requires `closest_integer(value)` to take a string
representing a number and return its closest integer. Exact half ties must be
rounded away from zero. The examples require:

- `"10" -> 10`
- `"15.3" -> 15`
- `"14.5" -> 15`
- `"-14.5" -> -15`

The trusted canonical implementation strips trailing zeros in one-dot
spellings, converts with binary `float`, recognizes textual `.5` ties, and
otherwise uses Python `round`.

### Submitted implementation and translation

`solution.py` constructs `Decimal(value)`, constructs `Decimal("0.5")`, and
then:

- for nonnegative numbers, returns `int(number + half)`;
- for negative numbers, returns `int(number - half)`.

This is the standard exact-arithmetic formula for nearest rounding with ties
away from zero. It is correct only when the intermediate `Decimal`
addition/subtraction does not change the relevant value through context
rounding. The implementation does not establish a local precision or otherwise
remove that dependency.

The trusted translator was rerun against the scratch copy:

```text
python3 /tmp/audit-work/99-closest-integer/trusted/py2mpy.py \
  /tmp/audit-work/99-closest-integer/source/solution.py \
  > /tmp/audit-work/99-closest-integer/build/regenerated.mpy
```

It exited zero, and `cmp` established byte identity with submitted
`solution.mpy`; both have SHA-256
`2b5c8519404cc2114c057ce044ba6085fb57df75861e95e9c12005d775d5500e`.

Evidence: `evidence/stage2_program_fidelity.log`.

### Independent differential test

`evidence/differential.py` independently imports the trusted canonical entry
point and the submitted entry point. It covers all documented examples, empty
input, the sign branch at zero, both sides and the exact point of positive and
negative half boundaries, alternate decimal spellings, exponent notation,
high fractional precision, decimal-context precision boundaries, and 80
deterministically generated ordinary decimal strings.

The final run covered 114 inputs:

- 108 matching normal returns;
- 6 differences.

The differences were:

1. empty input: both implementations reject it, but with different exception
   types (`ValueError` versus `decimal.InvalidOperation`);
2. `"1.45e1"`: candidate `15`, canonical `14`;
3. the two values immediately below positive/negative `1.5` at precision
   beyond binary float: candidate `1`/`-1`, canonical `2`/`-2`;
4. the two 28-digit `.4` decimal-context witnesses: candidate returns
   `±10000000000000000000000000000`, while the binary-float canonical returns
   `±9999999999999999583119736832`.

The scientific and near-half differences show limitations in the canonical
binary-float implementation; the candidate results there agree with the
literal-number contract. The final two differences are material for the
candidate too: the mathematically nearest results are
`±9999999999999999999999999999`, so neither implementation returns the
natural-language result. More importantly for this audit, K returns that exact
mathematical result while the submitted Python candidate does not.

Evidence:

- `evidence/differential.py`
- `evidence/stage2_differential_addendum.log`

**Stage 2 result: FAIL on the broad documented domain.** Translation fidelity
passes, and ordinary cases pass, but a valid numeric string exposes a real
implementation/intent difference. Stage 5 separately establishes that the K
proof also disagrees with the real generated program on that input.

## 3. Clean proof reconstruction

### Toolchain and isolation

The live toolchain is K `v7.1.293`. Source-only copies were made under
`/tmp/audit-work/99-closest-integer/source`; trusted inputs were copied under
`trusted/`. Before compilation, no `*-kompiled` directory existed in the
source directory. Fresh definitions were written to:

- `/tmp/audit-work/99-closest-integer/build/semantic-fresh-kompiled`
- `/tmp/audit-work/99-closest-integer/build/verification-fresh-kompiled`

Candidate `semantic-kompiled/` and `verification-kompiled/` were never read by
the build or proof commands.

### Fresh generated-semantics build and concrete execution

The command

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend haskell --output-definition .../semantic-fresh-kompiled
```

exited zero.

The corrected concrete comparison ran the submitted `solution.mpy` through
that fresh definition and compared it to independent Python execution. It
found 16/16 equal returned integers across examples, sign/half boundaries,
long fractional inputs, and scientific notation. Empty input raises
`InvalidOperation` in Python and produces `#Bottom` in K because exceptions are
not modeled.

The combined build log contains an earlier reviewer-harness formatting bug:
the first version failed to recognize spaces in K’s `pyInt ( N )`
pretty-print and therefore mislabeled displayed equal results as mismatches.
The regex was corrected and the entire concrete suite rerun; the authoritative
corrected result is in `evidence/stage3_concrete_rerun.log`.

### Fresh proof build and all positive targets

The command

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition .../verification-fresh-kompiled
```

exited zero.

The original target command

```text
kprove spec.k --definition .../verification-fresh-kompiled \
  --spec-module SPEC
```

exited zero and printed `#Top`.

To run every positive claim independently, the reviewer made
`evidence/spec-audit.k`, which adds labels but leaves all eleven claim bodies
unchanged. Each selection
`SPEC-AUDIT.audit-01` through `SPEC-AUDIT.audit-11` exited zero and printed
`#Top`.

Evidence:

- `evidence/stage3_rebuild.sh`
- `evidence/stage3_rebuild.log`
- `evidence/concrete_compare.py`
- `evidence/stage3_concrete_rerun.log`
- `evidence/spec-audit.k`

**Stage 3 result: mechanical reconstruction PASS.** Fresh `#Top` is genuine
closure under the candidate theory. It is not evidence that the generated
theory is faithful to Python.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Every claim starts with `solutionProgram`, consumes the `<k>` computation to
`.K`, initializes the environment from `.Map`, and constrains `<result>` from
`noResult` to a specific `pyInt`.

| Claim | Preconditions and input | Required result | Satisfying witness |
|---|---|---|---|
| 1 / `audit-01` | Abstract exact numeric string `N/D`, `D>0` | Exact-rational nearest integer, ties away, via `roundNearestAway(N,D)` | `N=3,D=2`, input `"1.5"`, result `2` |
| 2 / `audit-02` | `I>=0`, value `I+1/2` | `I+1` | `I=0`, `"0.5" -> 1` |
| 3 / `audit-03` | `I>=0`, value `-(I+1/2)` | `-(I+1)` | `I=0`, `"-0.5" -> -1` |
| 4 / `audit-04` | `I>=0`, value `I+1/4` | `I` | `I=0`, `"0.25" -> 0` |
| 5 / `audit-05` | `I>=0`, value `I+3/4` | `I+1` | `I=0`, `"0.75" -> 1` |
| 6 / `audit-06` | `I>=0`, value `-(I+1/4)` | `-I` | `I=0`, `"-0.25" -> 0` |
| 7 / `audit-07` | `I>=0`, value `-(I+3/4)` | `-(I+1)` | `I=0`, `"-0.75" -> -1` |
| 8 | Concrete `"10"` | `10` | `"10" -> 10` |
| 9 | Concrete `"15.3"` | `15` | `"15.3" -> 15` |
| 10 | Concrete `"14.5"` | `15` | `"14.5" -> 15` |
| 11 | Concrete `"-14.5"` | `-15` | `"-14.5" -> -15` |

`evidence/claim_witnesses.py` substituted these states into every claim and
compared the claimed result with both Python implementations. All 11 selected
witnesses agreed. Claim 1 was also checked with an independent
`fractions.Fraction` oracle.

### Program identity and control-flow pinning

`solutionProgram` is a `[function]` that expands to an inline constructor term.
The term contains the exact import, function name, parameter, two assignments,
comparison, positive return, and negative return in submitted
`solution.mpy`. Trusted-translator byte identity pins `solution.py` to
`solution.mpy`.

The reviewer’s configuration reachability check in
`evidence/pinning-spec.k` places the submitted constructor term on the
right-hand side of `solutionProgram`. `kprove` returns `#Top`; it reports the
claim as trivial because frontend function simplification has already made the
terms identical. Evidence: `evidence/stage4_pinning_rerun.log`.

The target proof does not read `solution.mpy` at proof time; it relies on this
inline copy. The current copy is exact, so this is an audited source-to-term
identity bridge rather than a substituted body. A later change to
`solution.mpy` alone would not affect the proof, which is why the independent
translation and pinning checks are necessary.

There are no loops or helper reachability claims. The claims symbolically
execute the real constructor sequence under `semantic.k`. The
`roundNearestAway` function occurs only in a postcondition and does not bypass
the submitted statements.

### Result constraint and domain adequacy

The postconditions are not tautologies or free-variable results. Every claim
requires a concrete mathematical result and a completed `.K` computation. The
fresh mutation in Stage 6 confirms this constraint dynamically.

However, claims 1–7 use `rationalString(N,D)`, a candidate-added `Value`
constructor, rather than the actual `pyStr(S)` input form. The bridge

```text
rationalString(N,D) ~> toDecimal => exactNum(N,D)
```

defines an abstract exact numeric-string contract. No theorem connects every
real string accepted by `Decimal` to this constructor. Four concrete claims
exercise the actual parser, but they do not establish the universal
string-to-rational bridge. That is an adequacy limitation even before the
decimal-context counterexample.

**Stage 4 result: mixed.** Program-term identity and result constraint pass,
and satisfying ground witnesses exist. Universal real-input pinning is only
conditional on the `rationalString` abstraction and candidate semantics; it is
not independently established for Python strings.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in `evidence/rule_inventory.md`. It enumerates:

- all 41 local syntax/configuration/function declarations;
- all 36 rules in `semantic.k`;
- all 3 function equations in `verification.k`;
- the only `[total]` declaration;
- the absence of local functional, simplification, priority, concrete, macro,
  anywhere, and opaque-function declarations;
- the constructor-to-rule coverage for every term in `solution.mpy`.

### Coverage, control, and state

The submitted term’s module/function/parameter shell is consumed by the exact
entry rule. Statement sequencing, both assignments, literal/name lookup,
left-to-right calls and binary operations, comparison, branching, and abrupt
return all have applicable rules. The environment and result updates agree
with the single-frame program. No heap, allocation, I/O, nested user call, or
loop is used.

Function guards for `exponentPosition` are disjoint and complete, supporting
its `[total]` attribute. The `parseDecimal`, `parseMantissa`, and
`scaleDecimal` branch guards are pairwise disjoint over their intended calls.
`roundNearestAway` has mathematically true positive/negative equations over
`D>0`.

Several narrower limitations do not by themselves enable a witnessed false
target-domain return:

- `rationalString` conversion lacks a `D>0` guard, although every symbolic
  target claim supplies `D>0`;
- `parseExponent(S,P)` and `parseMantissaAt(S,P)` require only `P>=0`, while
  their intended callers establish that `P` is the actual delimiter
  position;
- `Decimal` spellings and exceptions outside the parser subset can get stuck;
- the return rule admits arbitrary remaining K, but the modeled target
  language has no outer user-call/cleanup frame for it to mishandle.

These are recorded as containment/coverage gaps rather than labeled
unsoundness, because no false conclusion on an intended target input was
established from them.

### Materially unsound Decimal arithmetic rules

`semantic.k` lines 96–101 implement addition and subtraction of
`exactNum` values by unbounded integer cross multiplication. This is exact
rational arithmetic. It is not the semantics of the program’s Python
`Decimal` operations.

Python `Decimal` construction from a string is exact, but arithmetic uses the
active decimal context. Under the ordinary default context used by the
submitted program, precision is 28 and rounding is `ROUND_HALF_EVEN`.
`solution.py` does not install an unlimited or sufficiently large local
context. The K configuration has no decimal-context cell.

Concrete false-conclusion witnesses:

| Rule | Valid input string | Real `solution.py` return | K return / exact-rational postcondition |
|---|---|---:|---:|
| S17 addition | `"9999999999999999999999999999.4"` | `10000000000000000000000000000` | `9999999999999999999999999999` |
| S18 subtraction | `"-9999999999999999999999999999.4"` | `-10000000000000000000000000000` | `-9999999999999999999999999999` |

For the positive witness, real `number + half` becomes
`1.000000000000000000000000000E+28` before `int`; the negative witness is
symmetric. K retains the exact fraction and truncates it to the 28-digit
integer ending in `9`.

The witnesses are inside both relevant domains:

- each is a valid string representing a finite number under the prompt;
- the universal exact-rational claim admits the corresponding `N/D` with
  `D=10>0`.

This is not merely an empirical discrepancy. The reviewer added two ground
reachability claims using the actual `pyStr` inputs and candidate theory.
`kprove` printed `#Top` and exited zero for both false real-program results.
Thus S17 and S18 demonstrably enable false conclusions about the submitted
program.

Evidence:

- `evidence/decimal_context_witness.py`
- `evidence/unsound-witness-spec.k`
- `evidence/stage5_unsound_witness.log`

**Stage 5 result: FAIL.** S17 and S18 are materially unsound operational
semantics for the real program. They replace a property-bearing computation
with an idealized computation and omit observable decimal-context state. This
is a Gate A real-program soundness failure.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust or reuse. The reviewer created
`evidence/spec-vacuity-audit.k` by taking the reachable concrete `"10"` claim
and changing only its result obligation from `pyInt(10)` to the demonstrably
false `pyInt(11)`.

The mutation:

- has satisfying input `"10"`;
- successfully parses/builds under `kprove --dry-run` (exit 0);
- reaches the relevant final configuration;
- fails proof with exit 1 and `WarnStuckClaimState`;
- shows the residual final result `pyInt(10)`, which cannot match
  `pyInt(11)`.

This is the expected unmet result obligation, not a parser error, import
failure, timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6_nonvacuity.log`

**Stage 6 result: PASS.** The target theory is discriminating and
result-constraining. Non-vacuity does not repair the false operational
semantics.

## 7. Proven versus assumed accounting

### What successful `#Top` actually establishes

Under the candidate-defined `MPY` transition system, the successful
reachability proof establishes:

1. for every K integer `N` and positive K integer `D`, when the configured
   argument is the abstract constructor `rationalString(N,D)`, the inline
   constructor program terminates with
   `pyInt(roundNearestAway(N,D))`;
2. the stated positive/negative half and quarter families are consequences of
   that exact-rational execution model;
3. the four concrete parser examples terminate with their stated results.

It also establishes the specified final environment maps and consumed `.K`
computations. It does **not** establish that CPython `Decimal` arithmetic
behaves as `exactNum` arithmetic for all those inputs.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K toolchain and imported `INT`, `BOOL`, `STRING`, and `MAP` hooks, including integer division, string slicing/search/conversion, maps, and exponentiation | All semantics and claims | Ordinary low-level trusted runtime/math boundary; acceptable for this audit. |
| Trusted `py2mpy.py` translation | Program identity | Acceptable: regenerated output is byte-identical. |
| Inline `solutionProgram` equation | All target claims | Acceptable for the current source after independent parse/text pinning, but proof-time file sensitivity is external to the claim. |
| Exact module/import/function-entry pattern S01 | All claims | Acceptable for this one-function subset, conditional on the `decimal.Decimal` binding and omitted import/exception behavior. |
| `Decimal(str)` parsing helpers S10 and S27–S36 | Concrete claims and concrete executions | Empirically supported over tested ordinary/scientific forms; incomplete for the full `Decimal` input language. Finite tests do not prove universal parsing equivalence. |
| Abstract `rationalString(N,D)` bridge S11 | Symbolic claims 1–7 | Concerning but explicit: it gives an exact value contract, not a proved relationship to every real `pyStr`. Its value-level dependents are all symbolic theorem claims. |
| `exactNum` addition/subtraction S17/S18 as models of Python `Decimal` | Every positive or negative result claim | **Illegitimate.** The rules affect branches/results and are false for valid intended inputs under the real default decimal context. Two direct witnesses and two false ground `#Top` claims establish the failure. |
| Exact comparison and `int` truncation S14/S21 | All branch/result claims | Correct for finite exact values with positive denominator; empirically confirmed on both signs. |
| `roundNearestAway` equations V02/V03 | Universal postcondition and symbolic arithmetic corollaries | Ordinary mathematics, true over the guarded `D>0` domain. It specifies the ideal property but does not connect false Decimal operational rules to CPython. |
| Differential and concrete tests | Intent/bridge evidence only | Finite evidence. They support tested cases and expose counterexamples; they are not substitutes for the K proof or a universal connection theorem. |
| Partial-correctness treatment of exceptions/stuck inputs | Inputs outside the modeled normal-return subset | Excluded behavior. Empty input demonstrates Python exception versus K `#Bottom`. |

### Gate accounting and decision

- **Gate A, real-program soundness: FAIL.** Exact-rational S17/S18 are false
  models of the submitted program and enable false result claims.
- **Gate B, intent adequacy: FAIL on the unbounded string-number contract.**
  The prompt gives no 28-significant-digit bound; the actual program and the K
  theorem diverge on a valid numeric string. The abstract `rationalString`
  theorem also lacks a universal concrete-string connection.
- **Gate C, trust/evidence auditability: FAIL for the candidate validation.**
  The candidate did not state the ambient Decimal context as an assumption or
  test its precision boundary. The audit evidence is reproducible, but it
  disproves rather than validates the crucial bridge.

The successful proof is therefore a proof of an idealized exact-rational
machine, not a legitimate partial-correctness proof of the real generated
Python program. The required decision is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
