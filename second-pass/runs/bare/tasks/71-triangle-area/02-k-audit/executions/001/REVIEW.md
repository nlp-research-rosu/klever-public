# Independent adversarial audit: 71-triangle-area

## Audit conclusion

The candidate is **not a legitimate proof of the real generated Python
program**. Fresh reconstruction does produce `#Top` for all seven claims, the
claims are non-vacuous, and `verification.k` pins the submitted translated AST.
However, the generated semantics replaces CPython floating-point division,
exponentiation, and rounding with exact rational/mathematical operations. That
replacement enables a false result on a concrete valid integer input satisfying
the candidate's own universal precondition:

- Input: `(10^16, 10^16, 1)`.
- All three strict triangle inequalities hold.
- Trusted canonical and submitted Python result: `0.0`.
- Fresh K execution result:
  `VRounded(500000000000000000)`, interpreted as
  `5000000000000000.00`.
- A ground K claim requiring that false-real-program result closes with `#Top`.

This is a Gate-A real-program soundness failure with a concrete false-conclusion
witness. The successful positive proof establishes a theorem only about the
candidate's exact-rational model, not about execution of `solution.py` under
Python.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` does not exist, as required. I did not search
for, infer, or use any hidden semantics. There is no trusted-mount
contradiction, so this is a candidate audit rather than `AUDIT_ERROR`.

The candidate contains the required source artifacts:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. It also contains the expected audit metadata and untrusted
generation materials: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, and one structured JSONL trace.
There are no candidate helper K files, compiled definitions, caches, or
symlinks. No required source artifact is missing or mistyped. There is no
candidate `PROOF.md` or `spec-vacuity.k`; neither was a generation deliverable,
and the latter was created freshly during this audit.

The candidate prompt is byte-identical to `/reference/prompt.py`, and the
candidate translator is byte-identical to `/reference/py2mpy.py`. Their hashes
match `run-input.json`:

- prompt:
  `08897376ea63666a837e51f16608bd0abb6d1633e025ccacde662a7844e19626`
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

I read the untrusted generation materials only as claims. The 268-record
structured trace and final logs claim that a single all-claims `kprove` run
printed `#Top`; the output log also records many failed intermediate builds.
None of these reports or their prior `#Top` results were reused as proof
evidence.

Evidence: [provenance script](/audit-output/evidence/01_provenance_check.sh),
[bounded provenance log](/audit-output/evidence/01_provenance_check.log), and
[full-trace summarizer](/audit-output/evidence/trace_summary.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt asks for the area of a triangle from three side lengths,
rounded to two decimal places. A triangle is valid exactly when every pair of
sides sums to more than the third side; invalid inputs return `-1`. The prompt
does not state an integer-only type or numeric bound.

The trusted canonical implementation checks the disjunction of the three
invalidity conditions, computes Heron's formula using Python `/`, `** 0.5`, and
`round(..., 2)`, then returns the result. The candidate implementation expands
the invalidity disjunction into three sequential early returns and otherwise
uses the same formula. That is control-flow equivalent for the actual Python
function.

### Translator identity

I regenerated `solution.mpy` in scratch with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/71-triangle-area/solution.py \
  > /tmp/audit-work/71-triangle-area/regenerated.mpy
```

The command exited `0`. `cmp` exited `0`, and both regenerated and submitted
files have SHA-256
`35de37a7e93043616019084e065f12e0e38b89d278c59c344bdce3ef793f737d`.

### Independent differential test

The reviewer-authored test imports `/reference/canonical.py` and the scratch
copy of the submitted `solution.py` as separate modules. It exercises:

- both documented examples;
- empty arity, all-zero, negative, and equality/near-equality boundaries;
- each of the three ordered invalid branches and the valid side adjacent to
  each boundary;
- valid and boundary floating-point cases;
- large finite, `inf`, and integer-to-float-overflow behavior;
- all 1,331 integer triples with each component in `[-2, 8]`;
- 250 fixed-seed integer triples in `[-10000, 10000]`; and
- 250 fixed-seed finite-float triples in `[-100, 100]`.

All 1,849 calls matched, including return types or exception class/message:
zero mismatches. Thus the submitted Python program itself is faithful to the
trusted canonical over this finite corpus. This finite evidence is not used as
a universal proof.

Evidence: [differential test](/audit-output/evidence/differential_test.py) and
[command/results log](/audit-output/evidence/02_fidelity_and_differential.log).

## 3. Clean proof reconstruction

I copied only the candidate source artifacts to
`/tmp/audit-work/71-triangle-area`. No candidate definition or cache existed or
was reused. The installed independently invoked toolchain is K
`v7.1.293`.

### Fresh builds

The following fresh source builds all exited `0`:

1. LLVM concrete definition from `semantic.k`, main module `SEMANTIC`, syntax
   module `MPY-SYNTAX`.
2. Haskell proof definition from `verification.k`, main and syntax module
   `VERIFICATION`.
3. Haskell concrete definition directly from `semantic.k`, main module
   `SEMANTIC`, syntax module `MPY-SYNTAX`.

The Haskell concrete semantics executes `(3,4,5)` to `VRounded(600)` and the
first equality boundary `(1,2,3)` to `VInt(-1)`, each with exit `0`.

The LLVM definition does not execute any tested valid area path: it exits `113`
with residual `sqrtHundredths(...)`, because the only entry equation is marked
as a concrete simplification. Invalid paths still execute. This backend
limitation is a candidate portability/executability concern, but it is not the
decisive verdict because the freshly built Haskell semantics executes the same
sources.

### Fresh positive proofs

The original all-claims command exited `0` and printed `#Top`. To preserve
per-claim evidence, I made a source-equivalent labeled copy of `spec.k` and ran
each claim independently against the same fresh proof definition. All seven
commands exited `0` and printed `#Top`:

1. `(3,4,5) -> VRounded(600)`
2. `(5,12,13) -> VRounded(3000)`
3. `(2,2,2) -> VRounded(173)`
4. universal valid-integer claim
5. first invalid branch
6. second invalid branch
7. third invalid branch

Evidence: [labeled spec](/audit-output/evidence/spec-labeled.k) and
[complete bounded reconstruction log](/audit-output/evidence/03_clean_reconstruction.log).

### Generated-semantics comparison with real Python

Normal small cases agree. The semantics is nevertheless false over the formal
unbounded-integer domain. For `A=B=10^16, C=1`, CPython rounds
`(A+B+C)/2` to binary64 `10^16`; `s-A` becomes `0.0`, and both Python
implementations return `0.0`. The generated semantics' division rule at
[semantic.k](/candidate/semantic.k:135) creates exact rational
`10^16 + 1/2`; its exact square-root/rounding path returns
`VRounded(500000000000000000)`.

Fresh Haskell `krun` confirms the K result with exit `0`. A specialized ground
claim for that result also exits `0` with `#Top`. This is not a timeout,
container failure, or interpretation of a stuck state.

There are two further model limitations:

- On `(10^100,10^100,10^100)`, both real Python implementations return `inf`,
  while the exact K model has a finite mathematical result.
- A valid float input `(0.5,0.5,0.75)` returns `0.12` in both Python
  implementations, while K stops at
  `BinOp("+",VFloat(...),VFloat(...))` with `NoResult`.

Evidence:
[witness spec](/audit-output/evidence/precision-witness-spec.k),
[witness/build/execution log](/audit-output/evidence/03b_generated_semantics_witness.log),
and [Python oracle](/audit-output/evidence/python_semantics_oracle.py).

## 4. Adequacy and real-program pinning

### Entry claims in plain language

| Claim | Precondition | Postcondition | Satisfying witness |
|---|---|---|---|
| concrete 3-4-5 | Exact initial empty maps/result and those integer arguments | computation consumed; result is 600 hundredths | `(3,4,5)` |
| concrete 5-12-13 | Same shape with those arguments | result is 3000 hundredths | `(5,12,13)` |
| concrete 2-2-2 | Same shape with those arguments | result is 173 hundredths | `(2,2,2)` |
| universal valid | Integer `A,B,C` and all three strict pair-sum inequalities | result is `VRounded(sqrtHundredths(heronRadicand(A,B,C)))` | `(3,4,5)`; also the refuting bridge witness `(10^16,10^16,1)` |
| invalid first | `A+B <= C` | result is `-1` | `(1,2,3)` |
| invalid second | `A+B > C` and `A+C <= B` | result is `-1` | `(1,3,2)` |
| invalid third | first two guards false and `B+C <= A` | result is `-1` | `(3,2,1)` |

The three invalid claims are ordered exactly like the real early-return control
flow and partition invalid integer triples. The valid inequalities imply
positive integer sides.

### Program and result pinning

The `<k>` cell launches `solutionProgram`; the rule defining that constant is a
literal copy of the submitted `solution.mpy`. Whitespace-normalized tokens are
identical, and Stage 2 independently established that `solution.mpy` is the
trusted translator's exact output. There is no substituted program.

Every claim starts from a realizable initial configuration with empty
environment/function maps and `NoResult`. Each destination consumes the
computation and constrains `<result>` to a concrete value or a specific
function term. No right-hand result is a fresh variable.

For the ordinary satisfying witnesses, substitution agrees with both Python
implementations: `6.0`, `30.0`, `1.73`, and `-1` on each invalid branch.
However, the universal valid result repeats the same
`sqrtHundredths(heronRadicand(...))` abstraction inserted by the semantic
rounding rule. It constrains the result inside the candidate theory but does
not establish that this abstraction equals real Python execution. The
precision-loss witness makes that missing bridge false over the claim's own
domain.

Evidence: [adequacy script](/audit-output/evidence/claim_adequacy.py) and
[results](/audit-output/evidence/04_claim_adequacy.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all local declarations and all 47 explicit
rules: 45 in `semantic.k` and two in `verification.k`. It also records
strictness-generated evaluation, configuration/cell footprints, all
`[function]`, `[total]`, `[simplification]`, `[concrete]`, and `[owise]`
attributes, and the absence of `[functional]` or explicit priority rules.

The full rule-by-rule assessment and used-construct mapping is preserved in
[05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md), supported
by [machine inventory commands](/audit-output/evidence/05_static_inventory_commands.log).
The central findings are:

### Syntax, control, and state

- Every AST constructor actually present in `solution.mpy` has syntax and a
  rule path: module/function loading, parameter binding, no-else `if`,
  assignment, early/terminal return, literals/names, unary negation, binary
  arithmetic, `<=`, exponent `0.5`, and `round(...,2)`.
- `seqstrict` evaluates binary operands left-to-right. Comparison saves the
  evaluated left operand and then evaluates the right. The statement sequencer
  and branch continuations match source order.
- `<env>`, `<functions>`, and `<result>` cover the state needed by this
  single-function program. There is no heap or allocation.
- The return rule discards the remaining computation and clears maps. This is
  correct for an early return from the sole active entry call. It is broader
  than justified for nested calls/arbitrary continuations, but no such context
  is reachable from the submitted program; without an intended-domain false
  witness, I record this as a reuse limitation rather than a separate
  unsoundness.
- `asRat` is the sole `[total]` declaration. Its `VInt` and `VRat` equations are
  disjoint and exhaustive. Integer-specific arithmetic/comparison rules and
  their `[owise]` rational fallbacks have controlled overlap.

### Exact-square-root helper

Within its reached invariant (`R >= 0`, positive upper bound, and a valid
bisection interval), the upper-bound, bisection, and ties-to-even rules are
mathematically coherent: guards are disjoint/exhaustive and recursion descends.
For negative `R` or arbitrary nonpositive helper arguments, the names no longer
denote a truthful/terminating square-root search. No valid source path reaches
those cases, so they are narrower coverage/reuse gaps, not additional claimed
unsound rules.

The top-level `sqrtHundredths` equation applies only for concrete `R`. Therefore
the universal proof leaves the function symbolic and places that same symbol
in the postcondition. There is no universal K connection theorem showing that
fixed real-Python execution produces this abstraction's value.

### Materially unsound numeric bridge

The rule at [semantic.k](/candidate/semantic.k:135) says that Python `/` on
modeled integers/rationals yields an exact K rational. That is false wherever
CPython binary64 conversion rounds or overflows. A direct operation-level
witness is:

```text
Python: 20000000000000001 / 2 == 1e16
K rule: 20000000000000001 /Rat 2 == 10000000000000000.5
```

The exponent/round rules at [semantic.k](/candidate/semantic.k:137) and
[semantic.k](/candidate/semantic.k:153), plus the helper rules, continue this
exact-mathematics bridge to the observable result. The end-to-end witness
`(10^16,10^16,1)` shows the false conclusion enabled by this rule cluster on a
satisfying intended/formal input: K produces `5×10^15`, while the real program
produces `0.0`. This changes `<result>` and omits real exceptional/`inf`
behavior. It is a smuggled replacement of property-bearing program computation,
not an acceptable low-level primitive.

The verification rule `solutionProgram` is sound program pinning.
`heronRadicand` is a truthful exact mathematical formula, but because its
dependents use the false exact-rational language model, it does not characterize
the real Python intermediates universally.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was present or trusted. I created a fresh module
whose realizable input is `(3,4,5)` and changed only the observable result from
the correct `VRounded(600)` to the false `VRounded(601)`.

The mutation dry-run/build exited `0`. The actual proof exited `1` with
`WarnStuckClaimState`; the residual configuration had `.K` and
`VRounded(600)`, which did not unify with the required `VRounded(601)`. This is
the expected unmet result obligation, not a parser/import error, timeout, or
unreachable mutation.

Thus non-vacuity passes: the claims discriminate results under the candidate
theory. This does not repair the theory's real-program mismatch.

Evidence: [mutation](/audit-output/evidence/spec-vacuity.k),
[runner](/audit-output/evidence/06_non_vacuity.sh), and
[build/proof residual log](/audit-output/evidence/06_non_vacuity.log).

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate's K theory:

1. The three concrete inputs terminate in K with `600`, `3000`, and `173`
   hundredths.
2. Every K-integer triple satisfying the three strict inequalities executes
   the pinned AST to
   `VRounded(sqrtHundredths(exact-Heron-radicand(A,B,C)))`.
3. Every K-integer triple in one of the three ordered invalid partitions
   executes to `VInt(-1)`.

It does **not** establish that `sqrtHundredths(exact-Heron-radicand(...))`
equals the value produced by Python `/`, `** 0.5`, and `round`; that proposition
is false on the preserved witness.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K integer/rational/Boolean/list/map primitives and Haskell prover | Control, arithmetic, maps, proof execution | Acceptable low-level tool/mathematics trust boundary. |
| Trusted `/reference/py2mpy.py` | Program identity | Acceptable trusted input; exact regeneration and literal pinning checked. |
| `solutionProgram` rule | Entire executed program | Acceptable: pins the real submitted translated AST. |
| `heronRadicand` exact formula | Universal valid postcondition | Truthful ordinary mathematics, but only for the exact model; it does not bridge CPython intermediates. |
| Exact-rational `/` and downstream exact `sqrt`/round model | Final value, `inf`, exceptions | **Illegitimate.** This is program-defined observable computation inside the theorem, and the concrete satisfying witness disproves equivalence. |
| Symbolic `sqrtHundredths` abstraction | Universal final result | Concerning independently and illegitimate as used: the operational rule and postcondition share the symbol, with no universal connection theorem to real Python. |
| Omitted float-side arithmetic | Input-domain coverage | Material adequacy gap: prompt has no integer-only restriction, and a valid float input gets stuck in K. |
| Omitted Python overflow/exception state | Result/control behavior on unbounded integers | Material soundness gap; the formal K integer domain includes inputs where Python returns `inf` or raises. |
| Canonical/submitted differential test | Implementation-fidelity bridge only | Useful finite evidence (1,849 calls, zero mismatches), not a proof of semantic equivalence. |
| Informal Heron/rounding interpretation | Human-facing meaning | Ordinary mathematics for exact values, but insufficient to justify the false CPython bridge. |

Gate A (real-program soundness) fails because a materially unsound generated
semantic rule enables a false observable conclusion on the candidate's own
universal domain. Gate B also has an integer-only/formal-domain mismatch with
the untyped prompt. Gate C evidence is reproducible, but its trust ledger
contains the illegitimate numeric bridge. Passing reconstruction and
non-vacuity cannot substitute for Gate A.

Accordingly, the candidate proves a non-vacuous property of a substituted
exact-arithmetic language model, not partial correctness of the real generated
Python program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
