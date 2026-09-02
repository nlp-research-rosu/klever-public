# Independent adversarial review: 145-order-by-points

The candidate does not contain a legitimate partial-correctness proof of the
requested function over its intended input domain. Fresh reconstruction confirms
that all 13 submitted claims close, but the claim set never proves the universal
result property: its only arbitrary-list entry claim stops at the semantics'
internal `sortWith` term, and the claimed connection from `sortWith` to the
declarative `specSort` covers only empty and singleton lists plus insertion into
an exactly one-element tail. Three ground executions and one ground ordering
check do not close that gap.

There is a second, independent trust gap in the generated semantics. The exact
program-defined lambda is rewritten directly to `PointKey`, whose application is
then defined as `pointScore`, without generic lambda-call execution or a
bridge-free universal connection theorem. The arithmetic appears faithful, so I
do not call that rule mathematically false; it remains an unproved,
result-bearing operational bridge.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` is absent. There is
therefore no infrastructure breach and a candidate verdict is appropriate.

All expected generation and source artifacts are regular files, and there are
no symlinks anywhere under `/candidate`. The candidate includes:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  one regular structured JSONL trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and executable `prove.sh`.

No source/helper K file referenced by these sources is missing. There is no
candidate `PROOF.md` or `spec-vacuity.k`, but neither was a required deliverable
of the recorded generation prompt. The extra `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/` trees are untrusted generated
artifacts; they were not copied or reused.

The candidate prompt is byte-identical to `/reference/prompt.py` (SHA-256
`7a5c9e6cb4cbac4500da147421870d0aaac0c5e8f98d646aca7a6349fa239c3e`).
The candidate translator is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

I read the metadata and generation reports only as claims. They report a
successful run and `#Top`. The structured trace has 239 parseable records and no
parse errors. Of note, it reports that an attempted arbitrary-list
`sortWith(VS) => specSort(VS)` claim failed and was then replaced with the
current fragmentary claims. That history is not needed for the verdict; the
delivered `spec.k` independently exhibits the gap.

Evidence:

- `/audit-output/evidence/stage1-integrity.log`
- `/audit-output/evidence/stage1-required-artifact-types.log`
- `/audit-output/evidence/stage1-untrusted-generation-claims.log`
- `/audit-output/evidence/inspect_trace.py`
- `/audit-output/evidence/stage1-trace-summary.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and intended domain

For every finite Python list of integers, return a new list ordered by the
canonical digit score in ascending order, preserving original relative order
when scores tie. The trusted canonical implementation clarifies negative
numbers: if `abs(n)` has leading digit `d` and ordinary decimal digit sum `s`,
then a negative number's score is `s - 2*d`; nonnegative numbers have score
`s`. Thus `-12` scores `-1 + 2 = 1`, and `-1` scores `-1`.

The submitted Python implementation uses stable Python `sorted` and the key

`digitSum(abs(n)) - (2 * leadingDigit(abs(n)) if n < 0 else 0)`.

For `n >= 0`, this is the canonical digit sum. For `n < 0`, it is exactly the
canonical signed-leading-digit formula above. For `n = 0`, `str(abs(n))[0]` is
well-defined and the correction branch is not taken. Python's stable sort
supplies the original-index tie break. The implementation does not mutate
`nums`.

### Translator identity

I regenerated the term using the trusted translator:

`python3 /reference/py2mpy.py /tmp/audit-work/proof145/solution.py`

The regenerated term is byte-identical to `/candidate/solution.mpy`; both have
SHA-256
`74c6b868e58611b8799447498c1ad9182b0ab1569f6a477546e42ab920771141`.

### Independent differential test

`/audit-output/evidence/differential.py` independently imports
`/reference/canonical.py` and the fresh scratch copy of `solution.py`. It tests:

- both documented examples;
- explicit empty, singleton, sign, zero, power-of-ten, duplicate, stability,
  and arbitrary-precision boundaries;
- every list of length 0 through 3 over a boundary-heavy 17-value alphabet;
- 1,000 deterministic generated lists of length 0 through 12.

All 6,231 cases matched, with no input mutation and zero result mismatches.
This is strong finite evidence that the Python implementation meets the
contract. It is not a replacement for a K reachability theorem.

Evidence:

- `/audit-output/evidence/stage2-scratch-and-translation.log`
- `/audit-output/evidence/differential.py`
- `/audit-output/evidence/differential-inputs.json`
- `/audit-output/evidence/differential-results.json`
- `/audit-output/evidence/stage2-differential.log`

## 3. Clean proof reconstruction

I copied only source inputs to the previously absent
`/tmp/audit-work/proof145` directory. Candidate-compiled definitions and caches
were neither copied nor referenced.

Toolchain:

- K `v7.1.293`, build date 2025-10-03;
- Python `3.10.12`.

Fresh builds:

1. Concrete definition:
   `kompile semantic.k --backend llvm --main-module MPY-SEMANTICS
   --syntax-module MPY-SYNTAX --output-definition
   semantic-audit-kompiled` — exit 0.
2. Proof definition:
   `kompile verification.k --backend haskell --main-module VERIFICATION
   --syntax-module MPY-SYNTAX --output-definition
   verification-audit-kompiled` — exit 0.

Fresh concrete execution compared the LLVM semantics with both Python
implementations on five classes of input: the documented example, empty input,
zero/sign/decimal boundaries, tie stability, and arbitrary-precision integers.
Every `krun` exited 0 and every normalized K output matched both Python results.

The unmodified combined command

`kprove spec.k --definition verification-audit-kompiled --spec-module SPEC`

exited 0 and printed `#Top`. To run each target independently, I made a
mechanical copy changing only the module name and adding labels. All 13
individually selected claims exited 0 and printed `#Top`. The backend explicitly
reported 10 of the 13 as `WarnTrivialClaim: Claim proven without rewriting`;
the three nontrivial ones are the ground `init` executions.

Thus the narrow reconstruction gate—closure of every submitted positive
claim—passes. This says nothing yet about whether those claims express the
requested universal theorem.

Evidence:

- `/audit-output/evidence/tool-versions.log`
- `/audit-output/evidence/stage3-build-concrete.log`
- `/audit-output/evidence/concrete_semantics_compare.py`
- `/audit-output/evidence/concrete-semantics-results.json`
- `/audit-output/evidence/stage3-concrete-execution.log`
- `/audit-output/evidence/stage3-build-proof.log`
- `/audit-output/evidence/stage3-proof-all.log`
- `/audit-output/evidence/spec-audit-labeled.k`
- `/audit-output/evidence/stage3-labeled-spec-diff.log`
- `/audit-output/evidence/stage3-claim-01.log` through
  `/audit-output/evidence/stage3-claim-13.log`
- `/audit-output/evidence/stage3-proof-individual-summary.log`

## 4. Adequacy and real-program pinning

### Plain-language meaning and satisfiability of the claims

The 13 claims in `/candidate/spec.k` establish only the following:

1. Claims 1–4: four ground evaluations of `pointScore`:
   `-12 -> 1`, `-11 -> 0`, `-1 -> -1`, and `11 -> 2`.
2. Claim 5: for an arbitrary K `Vals` sequence, invoking the closed
   `order_by_points` representation rewrites to
   `ListVal(sortWith(VS, PointKey, solutionDefs))`.
3. Claims 6–7: `sortWith` equals `specSort` for the empty sequence and a
   singleton integer sequence.
4. Claims 8–9: `insertWith` equals `specInsert` when inserting `N` into the
   exactly one-element sequence `[M]`, separately under score `<=` and `>`.
5. Claims 10–12: end-to-end results for exactly the documented nonempty list,
   the empty list, and `[12, 21, -12, 3]`.
6. Claim 13: one ground result sequence rewrites under `isOrdered` to `true`.

Every precondition is satisfiable. Claims 1–7 and 10–13 have no explicit
`requires`; their displayed left configurations are witnesses. For claim 8,
`N=1, M=11` witnesses `pointScore(N) <= pointScore(M)`. For claim 9,
`N=11, M=1` witnesses `pointScore(N) > pointScore(M)`. The three actual `init`
entry witnesses are their exact displayed input lists. Those three inputs were
substituted into the fresh concrete semantics and both Python functions in
stage 3, with identical results.

### Program pinning

The proof does not parse `solution.mpy` as its program. It places
`solutionProgram` in `<program>`, and rules in
`/candidate/verification.k:10-42` expand that symbol to a manually duplicated
AST. Static comparison shows that term matches the submitted `solution.mpy`,
which in turn is byte-pinned to `solution.py` by the trusted translator.
Consequently the closed term matches the submitted program at audit time, but
this is an external source-to-term identity bridge rather than a fact proved by
the reachability claims.

Under the submitted semantics, the ground `init` claims execute that closed
term through `invokeOrder`, `exec`, and `eval`. Claim 5 also unfolds the closed
function body, but terminates its theorem at the internal `sortWith` result.

### Decisive adequacy failure

There is no claim of either of these necessary forms:

- arbitrary submitted entry execution produces the intended declarative
  stable ordering; or
- `sortWith(VS, PointKey, solutionDefs) => specSort(VS)` for every integer
  sequence `VS`.

The empty/singleton cases and two one-element insertion branches do not form a
K induction or circularity over arbitrary lists. They do not claim the
recursive step for a general tail, and no loop/recursive invariant claim
connects them. Likewise, the single ground `isOrdered` claim proves neither
universal orderedness, permutation preservation, nor stable tie behavior.

Claim 5 is result-constraining only to a candidate-defined internal computation.
It is not the intended postcondition. Claims 10–12 are meaningful but finite
examples. Therefore the candidate proves a substituted fragmentary theorem,
not partial correctness of `order_by_points` on the intended domain.

## 5. Rule-by-rule static soundness review

`/audit-output/evidence/stage5-rule-inventory.log` is the exhaustive inventory.
It records 18 syntax-declaration groups, one four-cell configuration, and 48
rules in `semantic.k`; and 4 syntax-declaration groups plus 11 rules in
`verification.k`. I use `S01`–`S48` and `V01`–`V11` in exactly that inventory
order.

There are 16 semantic and 5 verification `[function]` productions. There are
no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`, or
priority declarations/rules. Thus no such attribute is being mistaken for a
proof of truth or coverage.

### Syntax, configuration, and used-construct coverage

The syntax covers every constructor in `solution.mpy`: `Module`, `FuncDef`,
`Return`, statement/parameter/name lists, `Name`, `Int`, `Call`, `KwArg`,
`Lambda`, `BinOp`, `IfExp`, `Compare`/`CmpOp`, `Subscript`, and expression
lists. `ListExpr` covers external inputs. The configuration has exactly the
used components: computation, closed program, input expression, and returned
output. No source construct used by the submitted term is undeclared.

The constructor-to-rule map is:

- `Module`/entry: S01;
- `FuncDef`, `Return`, parameters, and definition scan: S29–S32;
- integer/list/name expressions: S02–S10;
- keyword, call, and argument lists: S11, S13, S20–S27;
- exact lambda/key application: S12 and S36;
- subtraction/multiplication: S14–S15;
- conditional expression: S16–S17;
- `<` comparison: S18;
- subscript: S19 and S28;
- helper value projections: S33–S35;
- stable sorting: S37–S41;
- decimal scoring: S42–S48.

Missing behavior for unused Python constructs is not a defect in this mode.
The declared generic `Closure` value is unused, and there is no generic lambda
invocation rule; that is material because the used lambda is instead
special-cased, as discussed below.

### Decision for every semantic rule

- **S01:** Faithful for this exact one-entry-function harness: it consumes
  `init`, evaluates the external list, and writes only `<output>`. It is not a
  general Python module-execution rule, but that broader behavior is unused.
- **S02–S04:** Truthful literal, list, and environment lookup equations on
  their guarded domains.
- **S05–S10:** Correct for the reachable environments of this exact program,
  which bind only `nums` (and would bind `n` under a generic lambda call).
  They are over-broad as written because they ignore Python name shadowing.
  Concrete symbolic witness: with
  `ENV = "sorted" |-> IntVal(7)`, S04 permits `IntVal(7)` while S05 permits
  `Builtin("sorted")`. Python lookup chooses the local value. No submitted
  `list[int]` entry can create that binding, so this is recorded as a
  non-material scope defect rather than a false conclusion on a reachable
  submitted entry.
- **S11 and S13–S21:** Faithful for the pure expression subset actually used.
  Argument/operand evaluation has no modeled order, but every used operand is
  side-effect-free, so no observable result or state difference follows.
  Conditional guards are disjoint once the used comparison returns a Boolean.
- **S12 and S36:** Result-bearing program abstraction. S12 recognizes the
  exact submitted lambda body and replaces it with `PointKey`; S36 says its
  integer key is `pointScore(N)`. The equations S42–S48 make that value
  determinate, and the signed-digit formula appears mathematically correct.
  I found no concrete false arithmetic conclusion and therefore do not label
  these equations false. The narrower, decisive evidence gap is that the
  program-defined body never executes and there is no bridge-free universal
  connection theorem proving that its fixed execution equals `pointScore`.
  Removing only S12 from a fresh variant still compiles, but `krun` exits 113
  stuck exactly at evaluation of the submitted `Lambda(...)`; this confirms
  that no independent used-lambda semantics exists.
- **S22–S28:** Faithful abstractions of `abs`, nonnegative decimal conversion,
  digit mapping/sum, digit-to-int, stable-key sorting dispatch, and index zero
  for the exact types produced by this program. `DecimalVal` omits general
  strings but preserves every observable operation used here.
- **S29–S32:** Faithful function selection, parameter binding, and single
  return for the exact module with one matching definition. They would not
  model Python's last-definition-wins behavior for duplicate definitions, but
  that syntax is absent from the submitted program.
- **S33–S35:** Truthful partial projections. No totality is claimed.
- **S37–S41:** Truthful stable insertion sort on `IntVal` sequences. Sorting
  the tail and inserting the earlier head before an equal-score element
  preserves original order. The `<=` and `>` guards are disjoint and
  exhaustive for integer scores. Other `Val` types can get stuck, but the
  intended input domain is integers and no totality is declared.
- **S42–S48:** Truthful, terminating equations on their guarded uses:
  nonnegative decimal digit sum, leading digit, and the canonical signed score.
  Guards are pairwise disjoint and cover every integer passed to
  `pointScore`; recursive arguments strictly decrease for positive values.

The S12 sensitivity artifacts are:

- `/audit-output/evidence/make_bridge_free_variant.py`
- `/audit-output/evidence/semantic-no-point-bridge.k`
- `/audit-output/evidence/stage5-make-bridge-free.log`
- `/audit-output/evidence/stage5-build-bridge-free.log`
- `/audit-output/evidence/stage5-run-bridge-free.log`

### Decision for every verification rule

- **V01–V02:** Definitional expansion of `solutionProgram`/`solutionDefs`.
  The expanded AST matches the submitted term, but the equality to the actual
  file is externally checked, not proved in K.
- **V03–V07:** Truthful declarative stable insertion-sort equations on integer
  values. Their branch guards are disjoint and exhaustive. They closely mirror
  S37–S41; merely defining both functions does not prove their equivalence for
  arbitrary recursive lists.
- **V08–V11:** Truthful orderedness equations on integer lists. Empty and
  singleton lists are ordered; an ordered first pair recurses, and a descending
  first pair makes the entire list unordered. The guards are disjoint. No
  totality is claimed for malformed/non-integer `Vals`.

There are no proof-local simplification rules, lemmas, priorities, or ordinary
operational rules beyond these inventoried function equations. `PointKey` is
the only task-specific result-bearing summary symbol. `DecimalVal`,
`MappedDigits`, and `DigitVal` are low-level representation tags with exhaustive
behavior for their reachable uses.

## 6. Fresh non-vacuity test

I created a new spec, independent of any candidate mutation, changing the last
element of the documented expected result from `11` to `12`. The exact
satisfying input is `[1, 11, -1, -11, -12]`; both trusted canonical execution
and the fresh semantics produce `[-1, -11, 1, -12, 11]`, so the mutation is
demonstrably false.

`kprove ... --dry-run` exited 0, establishing that the mutation parses and
builds against the fresh proof definition. The real proof run exited 1 with
`WarnStuckClaimState`. Its residual final configuration explicitly contains
`IntVal(11)` where the mutated destination requires `IntVal(12)`. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

The test shows that the concrete end-to-end claim is non-vacuous and
result-sensitive. It does not create or validate the missing universal claim.

Evidence:

- `/audit-output/evidence/spec-vacuity-audit.k`
- `/audit-output/evidence/stage6-mutation-build.log`
- `/audit-output/evidence/stage6-mutation-proof.log`

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Conditional on the submitted K theory, it establishes:

- four ground `pointScore` reductions;
- exact closed-program reduction from arbitrary `ListVal(VS)` to the internal
  `sortWith(VS, PointKey, solutionDefs)` term;
- equality of executable and declarative sorting only at empty/singleton bases
  and the two branches of inserting into an exactly one-element list;
- three concrete end-to-end outputs;
- one ground `isOrdered` result.

It does **not** establish that every intended input returns `specSort(VS)`, or
that every returned list is universally ordered, a stable permutation of the
input, or equivalent to the trusted canonical result.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser, LLVM/Haskell backends, built-in Int/Bool/String/Map/List mathematics | Every build, run, and proof | Ordinary accepted toolchain trust; versions and commands are recorded. |
| Trusted `/reference/py2mpy.py` | Source-to-`solution.mpy` identity | Authorized trusted input; byte identity was freshly checked. |
| Manual `solutionProgram`/`solutionDefs` AST | All K claims | Exact static match to the submitted term, but kprove executes the duplicate closed term, not the file itself. Acceptable only as an externally audited pinning bridge. |
| S12 exact lambda `=> PointKey` and S36 `keyInt => pointScore` | Every nonempty sort result and all score comparisons | Program-derived, result-bearing operational abstraction. It has truthful-looking equations and finite evidence, but no generic execution or bridge-free universal connection theorem. Materially concerning and not established by the proof. |
| Candidate models of `sorted`, `sum`, `map`, `int`, `str`, `abs` | Every computed key/result | Sound on the exact reachable integer/pure subset by rule review and concrete evidence; behavior outside that subset is excluded. |
| Mathematical argument equating `pointScore` with canonical negative-digit behavior | Intent bridge for all integers | Convincing informal derivation, not a K theorem. Ground K checks and finite differential tests support it only on tested values. |
| Python's stable `sorted` and trusted canonical implementation | Natural-language interpretation and differential oracle | Appropriate external intent oracle, but neither finite differential testing nor Python behavior substitutes for a universal K claim. |
| 6,231 Python differentials and five concrete K comparisons | Program/canonical and semantics/Python bridges | Reproducible finite evidence with zero mismatches; not universal proof. |
| Partial-correctness termination boundary | All claims | Nontermination is outside reachability partial correctness. For finite integer lists the Python function terminates, but the submitted claim set still lacks the universal postcondition. |

### Decision

The clean `#Top` is genuine for the claims that were submitted, and the Python
program itself is strongly supported as correct. The candidate nevertheless
does not prove the requested theorem. The missing arbitrary-list
`sortWith`/`specSort` (or equivalent end-to-end) reachability claim is a
material adequacy failure, not a thin evidence limitation. The result-bearing
lambda abstraction adds a separate unproved semantics bridge. These defects
place the candidate squarely in `FAIL / NOT_LEGIT`, even though its concrete
claims are non-vacuous and all positive commands close.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
