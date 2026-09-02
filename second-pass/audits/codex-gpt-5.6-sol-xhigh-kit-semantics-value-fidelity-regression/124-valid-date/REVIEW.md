# Independent adversarial review: 124-valid-date

Decision: **CONCERNS / LEGIT**.

The candidate contains a genuine, non-vacuous partial-correctness proof of the
submitted translated program under the supplied MPY semantics. Both target
claims close independently after a clean rebuild; the proof-local theory has no
execution shortcut or result oracle; and a separately generated module-loading
claim connects the submitted `solution.mpy` to the closure assumed by the entry
claims. The concern is external to proof soundness but material to task
fidelity: the trusted `canonical.py` contradicts the natural-language contract.
On exact-format dates with permitted days 30 or 31, the generated program
follows the prompt while the canonical implementation returns `False`.

All candidate prose, logs, traces, compiled definitions, and prior results were
treated only as untrusted claims. Builds and experiments used
`/tmp/audit-work/124-valid-date`; reviewer artifacts and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so the trusted mounts do
not contradict the rendered mode.

I read the candidate's `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured JSONL trace only as generation claims.
They claim a successful run, `#Top`, a validated proof, and 30,015 differential
cases. The bounded summary in
`/audit-output/evidence/00-untrusted-generation-summary.log` records hashes,
sizes, trace structure, and the candidate's final claims; none of those claims
was used as proof evidence.

The independent provenance check
(`/audit-output/evidence/provenance_check.py`, output
`/audit-output/evidence/01-provenance-check.log`) established:

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k` are present as regular files, not symlinks or mistyped
  entries.
- One regular structured trace is present and parses as 356 JSONL records.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`,
  SHA-256
  `71bb688daf8e872a52f7dfb4d4a09c07db640afd5fc1f8845baa1470a2930b78`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`,
  SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The candidate and trusted `reference-semantics/` trees each contain the same
  25 recursively inventoried entries. Every corresponding entry has the same
  type and bytes. There are no missing, additional, changed, mistyped, or
  symlinked entries.

Candidate-provided `runtime-kompiled/`, `verification-kompiled/`, Python caches,
proof logs, and reports were not copied into or used by the scratch build.
There is no provenance-integrity failure and no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt requires a Boolean validator for a date string in exact
`mm-dd-yyyy` format:

- the string is nonempty (implied by the exact ten-character format);
- the month is 1 through 12;
- the day is at least 1 and at most 31 in months 1, 3, 5, 7, 8, 10, 12;
- the day is at most 30 in months 4, 6, 9, 11;
- the day is at most 29 in February;
- the prompt imposes no leap-year condition on February 29.

The generated `solution.py` implements a strict reading of that contract. It
requires length ten, hyphens at positions 2 and 5, ASCII digits at the other
eight positions, converts the fixed two-character month/day fields, and applies
the stated month-dependent cap. It uses a different algorithm from
`canonical.py`, which is allowed if behavior agrees.

The trusted canonical implementation does not, however, implement the same
contract. It strips surrounding whitespace and accepts variable-width numeric
fields. More importantly, the unparenthesized conditions at
`/reference/canonical.py:32`, `:34`, and `:36` make `day > 29` an unconditional
rejection by the final test. Thus, for example, canonical returns `False` for
`01-31-2000`, although the prompt explicitly permits that date.

### Translation identity

I regenerated the MPY program in scratch using the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The command exited 0
(`/audit-output/evidence/02-regenerate-solution-mpy.log`), and `cmp -s` exited
0 against the submitted `solution.mpy`
(`/audit-output/evidence/03-solution-mpy-byte-identity.log`). Both files have
SHA-256
`9d8629c5452c16deca583947a8bb2b63e1f0789b8e060229f0228bed3046a72d`.

### Independent differential test

The reviewer-authored test is
`/audit-output/evidence/differential_test.py`; explicit inputs are in
`/audit-output/evidence/differential_cases.json`, and all generated inputs and
outputs are preserved in
`/audit-output/evidence/04-differential-inputs.jsonl`. It imports the entry
points directly from `/reference/canonical.py` and the scratch copy of
`solution.py`. A separate regex/month-table oracle encodes the strict prompt
contract without importing candidate test or proof code.

The deterministic scope was 34,396 unique strings:

- all five documented examples;
- empty and length boundaries;
- each separator and digit position perturbed below, within, and above the
  ASCII digit range, including Unicode numerals;
- every month `00..99` and day `00..99` for years `0000`, `2000`, and `9999`;
- explicit month/day branch boundaries;
- 5,000 seeded representative strings of length 0 through 15.

The run exited 0 and reported:

```text
total_unique_inputs=34396
generated_vs_canonical_mismatches=86
generated_vs_prompt_oracle_mismatches=0
```

See `/audit-output/evidence/04-differential-test.log` and
`/audit-output/evidence/04-differential-results.json`.

Of the 86 canonical disagreements:

- 54 are exact-format dates on which generated and prompt oracle return
  `True`, while canonical returns `False`: for each of the three exhaustive
  years, day 30 in the eleven non-February months and day 31 in the seven
  31-day months.
- 32 are whitespace, variable-width, signed, or Unicode-numeral forms accepted
  by canonical but rejected by both generated and strict prompt oracle.

This is a material candidate-versus-canonical divergence, including inputs
squarely within the prompt's intended exact-format domain. I do not treat it as
a false implementation, because the generated program agrees with the explicit
natural-language rule and the independent prompt oracle. It prevents an
unqualified `PASS`, because the two trusted sources of task intent are
inconsistent.

## 3. Clean proof reconstruction

Only source files were copied into `/tmp/audit-work/124-valid-date`. The
semantics copy came from the trusted tree after the recursive integrity check.
No candidate-built definition or cache was reused.

Fresh concrete definition:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0
(`/audit-output/evidence/05-kompile-llvm.log`). Warnings concerned incomplete
matches in unused supplied helpers and documented total/opaque operations; none
is on this program's execution path.

Fresh proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0
(`/audit-output/evidence/06-kompile-haskell.log`).

Each positive target claim was then run independently:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-wrong-length
```

Exit 0, `#Top`:
`/audit-output/evidence/07-kprove-wrong-length.log`.

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-ten-chars
```

Exit 0, `#Top`:
`/audit-output/evidence/08-kprove-ten-chars.log`.

Reviewer-authored concrete assertions cover the prompt examples and normal,
empty, format, month, day, February, 30-day, 31-day, year-digit, and length
boundaries. The Python run and MPY/LLVM run both exit 0:

- source and generated input:
  `/audit-output/evidence/09-concrete-audit.py` and
  `/audit-output/evidence/09-concrete-audit.mpy`;
- generation, Python, and K logs:
  `/audit-output/evidence/09-generate-concrete-audit-mpy.log`,
  `/audit-output/evidence/10-python-concrete-audit.log`, and
  `/audit-output/evidence/11-krun-concrete-audit.log`.

The K run finishes with `.K`, exit code 0, empty heap/stack, environment 0, and
the loaded `valid_date` closure in module scope. Concrete execution is
supporting evidence only; it does not substitute for either `#Top`.

## 4. Adequacy and real-program pinning

### Plain-language claims

`valid-date-wrong-length` starts from the explicit standalone module state with
`valid_date` bound to `validDateClosure`. Its precondition is:
`CS` is any MPY string code sequence and `isLen(CS) != 10`. Its postcondition
requires the call to return exactly `false` and all modeled cells—environment,
scopes, scope allocator, heap, heap allocator, stack, return state, exception,
and exit code—to be restored to their stated values. The empty sequence is a
concrete satisfying state.

`valid-date-ten-chars` has no side condition because its constructor pattern
itself fixes exactly ten integer codes. Its postcondition requires the returned
Boolean to equal `validDate10(C0,...,C9)`, not an unconstrained variable.
`validDate10` is true exactly when:

- codes 2 and 5 are ASCII hyphens;
- all other codes are ASCII digits;
- the two-digit month is 1 through 12;
- the two-digit day is at least 1 and no greater than the month cap 29/30/31.

The year affects validity only through its required four ASCII digits, matching
the prompt. The postcondition is an equality, not a tautology or one-way
implication. The two entry claims exhaust all constructor-form `IntSeq` values.
There are no loop/helper circularities; the program is straight-line control
flow with early returns.

### Pinning the submitted program

The target claims begin at a call with a prebound closure; they do not literally
start with the `#loadAll` configuration for `solution.mpy`. I therefore created
an independent connection claim. The generator
`/audit-output/evidence/make_pinning_spec.py` asks `kast` to parse the submitted
scratch `solution.mpy` as an MPY `Module`, places that exact parsed term under
`#loadAll`, and requires module loading to produce the exact
`validDateClosure` binding used by the target claims.

That generated claim is
`/audit-output/evidence/13-audit-pinning-spec.k`. It exits 0 with `#Top` under
the same fresh proof definition
(`/audit-output/evidence/13-kprove-pinning-claim.log`). Combined with byte
identity of submitted and trusted-translator output, this connects the source
artifact, submitted MPY bytes, parsed module AST, module binding, and entry
claims.

Body sensitivity was checked separately. In
`/audit-output/evidence/17-audit-body-mutated-solution.mpy`, only the final
`return day <= 31` was changed to `return False`. The corresponding parsed
module-loading claim
(`/audit-output/evidence/18-audit-body-mutation-pinning-spec.k`) exits 1 with
`WarnStuckClaimState`; its residual scope visibly contains the mutated
`Return(false)` closure and cannot unify with `validDateClosure`
(`/audit-output/evidence/18-kprove-body-mutation-pinning-expected-failure.log`).

Concrete satisfying results are recorded in
`/audit-output/evidence/14-python-witness-results.log`:

```text
input=''             canonical=False generated=False
input='03-11-2000'   canonical=True  generated=True
input='15-01-2012'   canonical=False generated=False
input='02-29-0000'   canonical=True  generated=True
input='01-31-2000'   canonical=False generated=True
```

Ground evaluations of the formal predicate for true, false, and canonical-
disagreement witnesses close with `#Top` in
`/audit-output/evidence/15b-kprove-witness-postconditions.log`. The initial
pure-functional formulation in
`15-kprove-witness-postconditions.log` was rejected because this backend does
not support functional claims; it is not counted as evidence. The successful
version uses ordinary configuration reachability claims.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory generator is
`/audit-output/evidence/k_rule_inventory.py`. Its complete output,
`/audit-output/evidence/16-k-rule-inventory.md`, lists the source location,
kind, attributes, disposition, audit basis, and bounded source text for every
declaration/rule in the trusted semantics copy, `verification.k`, and `spec.k`.
It records:

- 700 source rules;
- 231 syntax declarations;
- 111 syntax declarations bearing `total`;
- no declarations bearing `functional`;
- 34 priority rules;
- one simplification rule;
- 22 explicit `no-evaluators`/opaque declarations;
- one configuration, five evaluation contexts, and two target claims.

Every row has a disposition. Of the rules, 94 supplied rules are marked as
proof/program-path rules and were reviewed directly, 16 belong only to
`MPY-CONCRETE` and are absent from the proof definition, and the remaining
supplied rules are sort/construct-disjoint from all reachable terms here. This
is an acceptance of the problem-supplied fixed semantics as the declared
language model, not a claim that every unused rule is a full CPython semantics.

### Construct-to-rule map and execution review

The submitted MPY uses `Module`, `FuncDef`, `Call`, `Name`, `Int`, `Bool`,
`Str`, `Compare`/`CmpOp`, `BoolOp("or")`, `Subscript` with integer and slice
indices, `Assign`, `If`, and `Return`. Their declarations are in
`semantics/syntax.k`; the relevant behavior is:

| Program operation | Supplied rules reviewed |
|---|---|
| Module load and sequencing | `core.k:124-127` |
| Function definition/closure | `functions.k:14-16` |
| Name and builtin lookup | `core.k:130-181` |
| Callee/argument evaluation | `call.k:19-32`, `core.k:183-191` |
| Frame allocation/binding | `call.k:69-74`, `functions.k:62-75` |
| Literals/string codes | `core.k:193-196`, `str.k:12-17` |
| Integer/string comparison | `operators.k:14-17`, `int.k:22-27`, `str.k:24-59` |
| Short-circuit `or` | `bool.k:13-25` |
| String index and slices | `subscript.k:16-121` |
| `len` and two-digit `int` | `builtins.k:20-26`, `builtins.k:151-160` |
| Assignment and branches | `controls.k:8-18`, `controls.k:50-54` |
| Return and frame restoration | `functions.k:77-90` |

Strictness/context declarations produce left-to-right evaluation of callees,
arguments, comparisons, assignment right-hand sides, and conditions. The call
rule allocates one fresh scope, binds `date`, runs the actual closure body, and
pushes a frame containing the exact continuation and caller environment.
Return sets the return value and `#pop` restores environment, stack, scope map,
and scope allocator. The program allocates no heap object. The target
postconditions explicitly constrain every modeled cell, so no state mutation,
exception, frame, or control effect is silently framed away.

The length check precedes every index, so all executed indices are in bounds.
Every two-character call to `int` is control-dominated by eight ASCII digit
checks. This matters because the supplied multi-digit `intDigAcc` rule does not
itself reject non-digits; the real program establishes its needed domain before
the call. Slices are fixed positive-step slices of an exact ten-code sequence.

### Five proof-local rules

1. `strLt(iCons(A,.IntSeq), iCons(B,.IntSeq)) => A <Int B`
   `[simplification]` is a derived lemma, not an operational bridge. The fixed
   semantics has three exhaustive nonempty-head cases: `A<B` gives true,
   `A>B` gives false, and `A=B` recurses to
   `strLt(.IntSeq,.IntSeq)=false`. Thus the right side agrees by integer
   trichotomy. To avoid relying on the lemma to justify itself, I compiled
   `/audit-output/evidence/21-audit-verification-no-lemma.k`. The three guarded
   fixed-semantics branches all close with `#Top` in
   `/audit-output/evidence/23-kprove-strlt-fixed-semantics-branches.log`.
   An attempted single unguarded connection claim
   (`22-kprove-strlt-derived-without-local-lemma.log`) remained stuck because
   the supplied function is intentionally opaque on symbolic inputs; that is a
   prover-evaluation limitation, not a false witness, and it is not counted as
   successful evidence.

2. `validDateClosure` has one unconditional, nonrecursive equation expanding
   to a closure. It reads/writes no cells and replaces no execution. The
   independent parsed-module connection and body-sensitivity failure above
   establish its exact relation to the submitted program.

3. `twoDigit(A,B)` has one unconditional arithmetic equation
   `(A-48)*10+(B-48)`. It is total over mathematical integers. Its uses in the
   result predicate are guarded by ASCII-digit tests.

4. `daysInMonth(M)` is a total, terminating, overlap-free conditional:
   February maps to 29; months 4, 6, 9, 11 map to 30; all others map to 31.
   Values outside 1 through 12 cannot make `validDate10` true because the
   predicate separately rejects those months.

5. `validDate10(C0,...,C9)` has one unconditional total Boolean equation. It
   contains no fresh symbol or oracle and directly states the prompt's format
   and month/day constraints. The positive entry claim universally connects
   fixed execution to this exact value.

There are no proof-local priority rules, call interceptions, abrupt-control
bridges, auxiliary circularities, opaque result symbols, or rules that encode a
return without executing the body.

### Opaque and priority boundaries

The supplied semantics deliberately contains opaque proof-domain operations
for floats, sorting, and MD5, including the 22 `no-evaluators` declarations
listed individually in the inventory. `floorFI`, `toF`, and `ceilF` also have
only concrete evaluation equations for their relevant argument forms. No such
symbol is syntactically or dynamically reachable from this program, its
postcondition, or either proof. `MPY-CONCRETE` is imported only by the LLVM
definition, not `VERIFICATION`.

All 34 inventoried priority rules belong to the supplied baseline. The
reference/heap and specialized-call priorities that could affect control have
guards or constructors absent from this program's proof state. No candidate
priority preempts lookup, call, body execution, return, or any result-bearing
operation.

I found no materially unsound proof-local rule, so there is no false-conclusion
witness to report. The narrower limitations—symbolic `strLt` opacity and
incomplete unused semantics—are documented rather than mislabeled as
unsoundness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation is
`/audit-output/evidence/19-audit-false-result-spec.k`. It calls the actual
prebound closure on `02-29-0000`, a satisfying ten-character input that the
prompt, generated Python, canonical Python, and `validDate10` all classify as
true, but deliberately changes the required result to `false`.

The mutation builds successfully:

```text
kprove audit-false-result-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run
```

Exit 0:
`/audit-output/evidence/19-false-result-mutation-dry-run.log`.

The real mutation proof exits 1:

```text
kprove audit-false-result-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC
```

`/audit-output/evidence/20-kprove-false-result-expected-failure.log` contains
`WarnStuckClaimState` and the expected residual:

```text
<k> true ~> .K </k>
```

The failure is the reached true result failing to unify with the mutated false
destination. It is not a parser failure, missing import, timeout, or unrelated
crash. This establishes result constraint and non-vacuity.

One preliminary reviewer body-mutation file had a surplus closing parenthesis
and was rejected before the corrected body-sensitivity experiment; its log is
preserved as `17-generate-body-mutation-pinning-spec.log` and is not used as
non-vacuity evidence.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied definition and K toolchain, the successful
reachability proofs establish partial correctness for the exact standalone
entry configuration in `spec.k`:

- every MPY `str(IntSeq)` whose code-sequence length is not ten returns
  `false`;
- every exact ten-code MPY string returns exactly
  `validDate10(C0,...,C9)`;
- normal return restores every modeled state cell in the claim;
- the parsed submitted `solution.mpy` module loads the exact closure used by
  those entry claims.

The theorem is partial correctness. It does not separately assert termination,
although the submitted function contains no loop or recursion and all concrete
tests terminate.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted `reference-semantics/` | Defines all execution, values, control, and state in both claims | Acceptable and mandated by `SUPPLIED_SEMANTICS`; byte-identical candidate copy. It is a subset model, not a universal CPython theorem. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable mandated translator boundary; byte identity proves faithful use of that translator, not the translator's semantic correctness. |
| K frontend, Haskell backend, solver, LLVM backend | Parsing, compilation, symbolic proof, and concrete execution | Standard unavoidable toolchain trust. Definitions were rebuilt from source. |
| Integer/code-sequence string model | Represents inputs and ASCII format | Adequate for this program. Claims actually range over all constructor `IntSeq` values, including integers outside Unicode, and reject non-ASCII date positions. |
| One-code `strLt` lemma | Resolves symbolic ASCII range comparisons | Acceptable derived mathematics, supported by all three fixed-semantics branch claims and integer trichotomy; no fresh value or control effect. |
| `validDate10` to English contract | Human-facing meaning of the formal postcondition | Directly inspectable equation plus finite independent testing. It is not an empirical oracle used to close execution. |
| Trusted canonical implementation | Alternate executable task reference | Concerning: it materially contradicts the prompt on valid day-30/day-31 dates and accepts non-format strings. The proof does not establish equivalence to canonical. |

No empirical bridge, candidate report, differential suite, or concrete trace is
used in place of the two universal K reachability proofs. Differential testing
supports only the finite Python-to-prompt and canonical-discrepancy observations
described in Stage 2.

### Final judgment

Gate A (real-program soundness) passes: the exact parsed program is pinned, the
body executes under fixed semantics, every proof-local equation is sound, the
result is constrained, and the fresh false mutation is rejected.

Gate B is adequate relative to the explicit prompt but has a material
authoritative-source conflict: the trusted canonical implementation specifies
different results on intended exact-format dates. Because the candidate follows
the prompt and proves that behavior honestly, this is a concern rather than an
illegitimate proof.

Gate C passes: assumptions and opaque baseline operations are inventoried,
commands and bounded outputs are preserved, and empirical evidence is not
presented as universal proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
