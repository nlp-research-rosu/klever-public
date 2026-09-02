# Independent adversarial audit: 163-generate-integers

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program for the full source-contract domain of positive
integer endpoints. I rebuilt both K definitions from source, independently ran
the only positive target claim, obtained exit status 0 and `#Top`, checked that
the claim executes the same constructor term as trusted regeneration of
`solution.py`, reviewed every local syntax declaration and rule, and rejected
both a material body mutation and a fresh false result obligation.

The generated semantics is deliberately a small semantics for this one
translated function. That is the expected trust boundary in
`GENERATED_SEMANTICS` mode. It covers every constructor and reachable control
context in the submitted term and contains no result oracle or
execution-bypassing proof rule.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- problem `163-generate-integers`;
- generation condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- no mounted reference semantics.

I read and inspected `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and the JSONL trace under
`/generation-evidence/codex-trace/`. The legacy-selected-stage1 layout does not
require a historical runtime-metrics record; none was fabricated. The optional
`usage.json` was present and inspected.

Every required launcher record, provenance mount, generation-evidence leaf,
trusted input, and proof deliverable was a regular file or regular directory.
There were no symlinks in `/candidate`, `/reference`, or the structured trace.
Every one of the 171 structured-trace lines parsed as JSON.

The campaign lock JSON exactly equals the `audit_campaign` block in
`/audit-input.json`. Its independently calculated SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded value. All recorded file-level hashes, including the
single structured-trace leaf, matched independent hashes. A reviewer-local
type/path/content tree digest was also calculated for each mounted tree; it is
documented as a separate encoding rather than compared with an unspecified
launcher aggregate encoding.

The complete checks and hashes are in
[stage1-2.log](/audit-output/evidence/stage1-2.log), produced by
[provenance_check.py](/audit-output/evidence/provenance_check.py). A bounded
inspection of the untrusted generation narrative and trace is in
[generation-record-summary.log](/audit-output/evidence/generation-record-summary.log).
The prior `KPROVE_PASSED` marker was not used as proof evidence.

### Condition-aware semantics integrity

`/reference/reference-semantics` does not exist, as required for
`GENERATED_SEMANTICS`. I did not search for or use any hidden reference
semantics. The candidate's `semantic.k` was audited on its own merits.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, with
SHA-256
`746b974c17bfa8fea903c131acce2f7af0d087460803f42cb265a26d69e5089a`.
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`, with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The trusted canonical hash independently matched
`dbacb9ce5fd5158372e55a2fd55be03665faee8dec270eaccf8e6d9fbb24020b`.

There is no infrastructure contradiction or missing required record.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires `generate_integers(a, b)`, for two positive
integers, to return in ascending order the even decimal digits lying
inclusively between the endpoints, regardless of endpoint order. The examples
are:

- `(2, 8) -> [2, 4, 6, 8]`;
- `(8, 2) -> [2, 4, 6, 8]`; and
- `(10, 14) -> []`.

For positive endpoints, `0` can never be in the interval. Therefore the only
possible returned digits are exactly `2`, `4`, `6`, and `8`.

The trusted canonical implementation clips the unordered interval to `[2,8]`
and selects even integers. The candidate uses two endpoint-order branches and,
within each branch, appends each of `2,4,6,8` exactly when it lies between the
endpoints. This is a different but equivalent algorithm over the full positive
integer domain; it is not a bounded-input implementation.

### Trusted regeneration

In the scratch tree, I ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy
cmp -- /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
```

Both commands exited 0. Both files have SHA-256
`54429f6b9e491fb77c192588c91cb091f01486578cfabc7f76be228ac25eaeab`.
Thus the submitted `solution.mpy` is the exact trusted translation of
`solution.py`.

### Independent differential testing

[differential_test.py](/audit-output/evidence/differential_test.py) loads the
trusted canonical and generated entry points independently. It checks the
documented examples, equal endpoints, empty-output intervals, both orientations
at every threshold around `2,4,6,8`, all `17 x 17` small positive pairs,
30-digit endpoints, and 500 seeded positive pairs up to `10^9`.

Exact command and result:

```text
python3 /audit-output/evidence/differential_test.py
total_cases=821
mismatch_count=0
DIFFERENTIAL_TEST=PASS
EXIT_STATUS: 0
```

The complete fixed-case results are in
[stage1-2.log](/audit-output/evidence/stage1-2.log). This testing supports the
source-to-source adequacy bridge; it is not substituted for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/candidate`; no candidate
compiled definition or Python cache was copied. K was independently identified
as version 7.1.293.

The clean build and sole positive proof command were:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/semantic-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/candidate/verification-kompiled

kprove spec.k \
  --definition /tmp/audit-work/candidate/verification-kompiled \
  --spec-module SPEC
```

Both compilations exited 0. `kprove` exited 0 and printed exactly `#Top`. There
is one and only one `claim` in `spec.k`; therefore every positive target claim
was run. Exact output is preserved in
[stage3-build-proof.log](/audit-output/evidence/stage3-build-proof.log).

### Fresh generated-semantics executions

[concrete_semantics_compare.py](/audit-output/evidence/concrete_semantics_compare.py)
ran the freshly compiled LLVM semantics with JSON output, verified that `<k>`
was empty, extracted the list from `<result>`, and compared it with both Python
implementations. Seventeen normal and boundary inputs were checked, including
all four digit thresholds, equal and reversed endpoints, empty-output cases,
interior interval `(3,7)`, and 30-digit integers. Every `krun` exited 0 and all
three results agreed. The commands and results are in
[stage3-concrete.log](/audit-output/evidence/stage3-concrete.log).

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole entry claim starts with:

- arbitrary K integers `A` and `B`;
- the complete submitted module term in `<k>`;
- input `pair(A,B)`;
- an empty environment; and
- `noResult`.

Its precondition is `A >Int 0 andBool B >Int 0`, exactly the source contract's
positive-integer domain.

The destination requires:

- the complete computation to be consumed (`<k> .K </k>`);
- input `pair(A,B)` preserved;
- the environment to contain the original `a` and `b` plus local
  `result = listVal(expected(A,B))`; and
- `<result> = listVal(expected(A,B))`.

`expected(A,B)` concatenates, in ascending order, each of `2,4,6,8` iff that
digit lies inclusively between the endpoints in either orientation. The
returned value is therefore constrained twice. It is not a fresh variable,
tautology, one-way implication, or opaque term.

### Satisfiable entry state and concrete substitution

For example, `A=3`, `B=7`, the exact program term in `<k>`, input `pair(3,7)`,
empty environment, and `noResult` satisfy the entry pattern and precondition.
The claim's result specializes to `[4,6]`. Fresh K execution, candidate Python,
and trusted canonical Python all returned `[4,6]`. The boundary witness
`A=B=1` likewise satisfies the precondition and specializes to `[]`.

### Mechanical program identity

The claim spells empty `Exprs` and `Stmts` units explicitly, whereas concrete
`.mpy` syntax leaves those list positions empty. I mechanically extracted claim
lines 9-69, replaced only `.Exprs`/`.Stmts` unit tokens with their concrete
empty-list spelling, parsed both terms with `kast --sort Program --output
json`, and compared the resulting KAST JSON files. `cmp` exited 0; both have
SHA-256
`ee1b665736d0588b5bb0830f986c4b4938e4a8261868c7a7ea416513da00e970`.
The exact commands are in
[stage4-pinning-normalized.log](/audit-output/evidence/stage4-pinning-normalized.log).
The initial attempt, preserved in
[stage4-pinning.log](/audit-output/evidence/stage4-pinning.log), merely showed
that the concrete-program parser does not accept internal `.Exprs` syntax; it
was a parser-mode issue, not a comparison failure.

Together with byte-identical trusted regeneration, this pins the claim to the
actual submitted function binding and body. There are no helper or loop claims.

### Body sensitivity

I changed the `8` appended by the forward final branch to `7` inside the
program term executed by a separate claim, leaving the destination unchanged.
This is not a mutation of an unused external source file. The mutated proof
exited 1 with `WarnStuckClaimState`; its residual includes a reachable state
whose result is `[7]` under positive-input constraints (for example `A=7`,
`B=8`) rather than the required `[8]`.

The mutation is
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k), and the
diff, command, exit status, and residual are in
[stage4-body-sensitivity.log](/audit-output/evidence/stage4-body-sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). There are no
generated helper K files.

### Syntax, configuration, and construct coverage

`semantic.k` locally declares:

- `Program`: `Module`;
- statement lists and `FuncDef`, `Assign`, `If`, `Return`;
- parameter/string lists;
- `Name`, `Int`, `ListExpr`, `Compare`, `BinOp`, comparison lists and `CmpOp`;
- input pairs;
- integer, Boolean, list, and internal delayed-expression values;
- `noResult`;
- nine internal computation/continuation constructors; and
- the `<py>` configuration with `<k>`, `<input>`, `<env>`, and `<result>`.

Every local production and its line is individually listed in the inventory.
Every constructor in `solution.mpy` maps to a declaration and rules:

| Used constructor | Rules |
|---|---|
| `Module(FuncDef(...))`, `Params` | S1 entry binding/body execution |
| statement list | S2-S3 |
| `Assign(Name(...),...)` | S4-S5 plus S12 |
| `If` | S6-S8 |
| final `Return` | S9-S10 |
| `Int` | S11 |
| empty/singleton-integer `ListExpr` | S13-S14 |
| list `BinOp("+",...)` | S15-S17 |
| singleton integer `Compare` with `<=` | S18-S21 |

The configuration has no unused state cell. The semantics intentionally omits
unsubmitted Python constructs, which is permitted in generated-semantics mode.

### All operational rules

The 21 ordinary semantic rules are:

1. S1 binds the exact entry-point parameters to input integers and executes
   `BODY`; it does not replace the body with a summary.
2. S2 consumes an empty statement list.
3. S3 executes statement lists head-first.
4. S4 evaluates assignment RHSs first.
5. S5 updates the named local binding.
6. S6 evaluates an `If` guard first.
7. S7 selects the true branch.
8. S8 selects the false branch.
9. S9 evaluates the returned expression.
10. S10 stores the returned value in `<result>`.
11. S11 evaluates integer literals.
12. S12 performs environment lookup.
13. S13 evaluates the empty list.
14. S14 evaluates a singleton integer list.
15. S15 schedules a binary expression's left operand.
16. S16 then evaluates its retained right operand.
17. S17 performs order-preserving list concatenation for `"+"`.
18. S18 schedules a comparison's left operand.
19. S19 then evaluates its right operand.
20. S20 returns true under the K-integer `<=` condition.
21. S21 returns false under the complementary condition.

All these rules are valid on every state reached by the submitted program for
positive integer inputs. Their evaluation order, state footprint, branch
selection, and result behavior match the used Python operations. The apparent
operand-name reversal in S20/S21 is correct: the previously evaluated left
value is stored inside `cmpRight`, while the newly evaluated right value is at
the head of `<k>`.

S10 is deliberately only adequate for the submitted final-return context. It
is not a reusable early-return semantics: an off-scope body with `Return(1)`
followed by `Return(2)` would continue and overwrite the result with `2`. This
is a concrete boundary witness for the excluded context, not a false
conclusion reachable from the fixed submitted term, whose only `Return` is
last. The generated-semantics condition permits this minimal used-construct
scope, and the claim does not generalize the semantics to other programs.

`evalPlaceholder` is an explicit delayed-expression constructor used to enforce
left-to-right evaluation, not an opaque value oracle. It cannot reach the
submitted program's result.

There are no local priority rules, syntax macros, aliases, `total` or
`functional` declarations, simplification rules, concrete-only rules, opaque
symbols, allocation, I/O, exceptions, heap effects, loops, calls, or control
frames.

### Proof-local definitions and claim

`verification.k` has two `[function]` declarations and three rules:

- V1 maps `expectedDigit(A,B,D)` to `[D]` when `D` lies between the endpoints;
- V2 maps it to `[]` under the exact Boolean complement; and
- V3 expands `expected(A,B)` to the concatenation for `2,4,6,8`.

V1/V2 are disjoint and exhaustive over K integers, and V3 is unconditional.
All equations terminate and are ordinary mathematics. They are definitional
summaries of the destination, never operational bridges: no semantic execution
rule refers to either function. They do not encode a program result into
execution, use an unconstrained oracle, or create a circular equality.

`spec.k` contains only the one full-configuration reachability claim already
described. There is no framed-away observable cell or helper circularity.

I found no local rule capable of proving a false conclusion for the actual
submitted program on the intended positive-integer domain.

## 6. Fresh non-vacuity test

I created a fresh spec module that appends `ListItem(99)` to both
result-constraining destination obligations while leaving the executed program
and precondition unchanged:

```text
"result" |-> listVal(expected(A, B) ListItem(99))
<result> noResult => listVal(expected(A, B) ListItem(99)) </result>
```

This is demonstrably false for a satisfying input such as `A=B=1`: the real
result is `[]`, not `[99]`. The preserved mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k).

The dry run built successfully:

```text
kprove spec-vacuity.k \
  --definition /tmp/audit-work/candidate/verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The actual proof exited 1 with `WarnStuckClaimState` and an unmet result
obligation. The displayed residual branch has positive endpoints, `A > B > 8`,
and actual empty results; `A=10,B=9` is a concrete witness for that exact
residual. This is the expected proof failure, not a parser error, timeout, or
unreachable mutation. Exact diff, commands, dry-run hash, exit statuses, and
residual are in
[stage6-vacuity.log](/audit-output/evidence/stage6-vacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Relative to the freshly built `MPY`/`VERIFICATION` theory, for every K integer
pair `A,B` satisfying `A>0` and `B>0`, executing the exact submitted
`generate_integers` constructor body from the declared initial configuration
consumes the computation and produces in both the local `result` binding and
the observable `<result>` cell the ascending list of all members of
`{2,4,6,8}` lying inclusively between the endpoints in either orientation.

This is the requested partial-correctness theorem. The claim is universal over
unbounded K integers; it is not a finite-size proof or bounded unrolling.

### Trust ledger

| Boundary | Value/control influence | Dependents | Assessment and evidence |
|---|---|---|---|
| K 7.1.293 compiler, LLVM concrete backend, Haskell/KORE proof backend | All parsing, execution, and proof checking | Entire reconstruction | Standard unavoidable proof-tool trust boundary; versions and fresh commands are recorded. |
| Imported `INT`, `BOOL`, `STRING`, `LIST`, and `MAP` builtins, including `<=Int`, Boolean connectives, list concatenation, lookup, and update | Arithmetic guards, branch control, list result, environment | All semantics and postcondition rules | Acceptable low-level primitives, not task-answer oracles. Their used behavior is standard and concretely cross-checked at all thresholds. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Program pinning | Launcher-designated trusted input; candidate copy matches it byte-for-byte, regeneration matches `solution.mpy`, and parsed claim KAST matches. |
| Candidate-generated `semantic.k` | All modeled control and state | K theorem | Not assumed from a hidden baseline. Every local declaration/rule is inventoried and audited; 17 concrete executions match two Python implementations. |
| V1-V3 `expectedDigit`/`expected` equations | Destination value only | Sole claim | Truthful, terminating definitional summary with complementary guards; does not replace execution. |
| Interpretation of “even digits” as `2,4,6,8` for positive endpoints | Human-facing intent | Contract adequacy | Ordinary mathematical bridge: decimal even digits are `0,2,4,6,8`, and positivity excludes `0` from every allowed interval. |
| CPython adequacy of the modeled used subset | Source-behavior interpretation | Claim about the Python program | Structurally audited for exact entry binding, sequencing, names, unbounded integers, list literals/concatenation, comparisons, branches, and final return; supported by 821 Python differential cases and 17 three-way K/Python comparisons. No used exception or unmodeled control path exists. |
| Trusted canonical Python | Differential oracle only | Empirical adequacy evidence | Independently imported and never used in the K theory. Finite testing is not claimed as a universal proof. |

There are no opaque symbols, empirical result bridges inside the proof,
unproved operational summaries, helper claims, loop invariants, proof-local
priorities, or simplification axioms.

### Excluded behavior

The theorem does not cover nonpositive inputs, non-integer Python values,
different functions/program bodies, unused Python constructs, or general early
return contexts. These are outside the explicit HumanEval contract or the
immutable submitted term. The proof is partial correctness and does not claim a
general formalization of all CPython.

## Decision

All seven required stages completed. Provenance is intact; trusted translation
and constructor pinning succeed; clean proof reconstruction yields `#Top`; the
formal domain matches the full positive-integer contract; every local rule is
sound on the submitted program's reachable domain; and both body sensitivity
and false-postcondition non-vacuity tests fail for the expected semantic
reason. There is no material adequacy gap or illegitimate trust boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
