# Independent adversarial audit: 124-valid-date

The candidate does not contain a proof of the unrestricted HumanEval source
contract. A clean rebuild does prove its submitted `spec.k`, but that file has
only 33 fixed-string program executions and 14 claims about a separate
declarative helper. There is no symbolic entry claim connecting execution of
`solutionProgram` on an arbitrary input string to `validDateSpec`, and
`validDateSpec` is not referenced by any claim. Under the benchmark's explicit
mapping, this materially finite narrowing is `FAIL / NOT_LEGIT`.

There is a second real-program limitation: the generated semantics models
`str.isdigit()` as ASCII-only. The submitted Python program accepts Unicode
decimal digits, while fresh K execution rejects Arabic-Indic and full-width
decimal dates. This is a concrete operational-fidelity counterexample, not a
mere absence of tests.

## 1. Input and provenance integrity

Result: PASS. The audit infrastructure is intact.

I first read `/audit-input.json` and used only its `container_paths` for mounted
inputs. It declares:

- problem `124-valid-date`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference semantics.

`/audit-campaign-lock.json` is structurally identical to the
`audit_campaign` block and has the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The campaign ID, image ID, prompt hash, K version, Kit commit/tree, and
toolchain hashes all agree.

I inspected the required legacy-selected-stage1 records:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
I also inspected the present legacy records `legacy-metrics.json` and
`legacy-run-input.json`. Historical runtime metrics are absent, which is
permitted for this record layout. The trace consists of one regular JSONL file
with 308 parseable objects. There are no symlinked or special entries in the
candidate or trace trees.

Every recorded leaf hash matches, including the prompt, translator, canonical
implementation, generation logs, JSON records, and trace JSONL file. The
candidate prompt and translator are byte-identical to the trusted mounts. The
fresh pipeline-contract tree hash of `/candidate` is
`8ac89997862c6f85b89e77bd74ac9c7bafcc9dbb3e2b51a897e9f8a46e0ba907`,
which matches both the stage result and invocation workspace hashes. The fresh
pipeline trace-tree hash is
`4c82fcd0da02aa6d9417b5c0cfddd4c68160b2cafa7adc198b9df495262275d3`,
matching `usage.json`. The additional launcher digests in `audit-input.json`
were recorded separately and are retained in the log; the independently
reproducible file and pipeline-tree hashes all match.

The generated-semantics boundary is also consistent: `/reference` contains
only `canonical.py`, `prompt.py`, and `py2mpy.py`; there is no
`/reference/reference-semantics`, and all reference-semantics fields in
`audit-input.json` are null.

Evidence:

- `evidence/provenance_check.py`
- `evidence/01-provenance-check-final.log` — command exit 0, `FAILURES=NONE`
- `evidence/01-generation-record-summary.log` — bounded inspection of the
  untrusted generation log and complete structured trace

The earlier `01-provenance-check.log` is superseded: its reviewer script
initially compared two differently defined trace-tree digests. The final script
checks the trace leaf hash plus the pipeline hash named by `usage.json`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` asks for a function on a date string that returns true
exactly when the date is in `mm-dd-yyyy` format, the month is 1 through 12, and
the day is:

- 1 through 31 for months 1, 3, 5, 7, 8, 10, and 12;
- 1 through 30 for months 4, 6, 9, and 11;
- 1 through 29 for February.

No leap-year condition or numeric year range is stated. The format wording
supports two month digits, two day digits, four year digits, and hyphens at
positions 2 and 5.

The trusted `/reference/canonical.py` does not exactly implement that prose. It
strips surrounding whitespace, accepts variable-width and signed integer
components, and its unparenthesized conditions at lines 32, 34, and 36 apply
`day > 29` to every month. Thus, for example, it returns false on
`"04-30-2020"` and `"01-31-0000"`, contrary to the prompt. I report this
oracle/prose discrepancy instead of treating the canonical's precedence bug as
the natural-language contract.

### Translation and implementation

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
fb4a7d0caadab15af3f85da978c9739d8db1e71ec10e5efe2ab9d84d3b8d1b8a  solution.mpy
fb4a7d0caadab15af3f85da978c9739d8db1e71ec10e5efe2ab9d84d3b8d1b8a  solution.regenerated.mpy
EXIT_STATUS=0
```

The candidate keeps the required `valid_date(date)` signature. For ordinary
ASCII strings in exact `mm-dd-yyyy` form, its branch structure implements the
prompt's month/day limits. It deliberately rejects other widths and surrounding
whitespace.

### Independent differential test

`evidence/differential_test.py` imports the scratch copies of the trusted
canonical and candidate entry points independently. It covers the five prompt
examples, empty and format boundaries, every month/day branch boundary, the
full grid `month=0..13`, `day=0..32`, four year values, canonical parser
tolerances, Unicode decimal digits, and 1,000 seeded malformed strings.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 with no exceptions and reported:

```text
TOTAL_CASES=2931
EXCEPTIONS=0
MISMATCHES=95
```

The 95 differences consist of the canonical's permissive width/whitespace
parsing and its prompt-contradicting day-30/day-31 precedence behavior. The
candidate and canonical both accept Unicode decimal dates such as
`"٠٣-١١-٢٠٠٠"`.

Evidence:

- `evidence/02-translation-identity.log`
- `evidence/differential_test.py`
- `evidence/02-differential.log`

## 3. Clean proof reconstruction

Result: the submitted claims reconstruct successfully, but fresh semantics
execution exposes a real Python/K mismatch.

I copied source artifacts to `/tmp/audit-work/124-valid-date` and did not copy or
reuse any compiled definition or cache. K reports version 7.1.293.

Fresh concrete definition:

```text
kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY \
  --output-definition /tmp/audit-work/124-valid-date/build/semantic-kompiled
```

Exit status: 0. See `evidence/03-build-semantic.log`.

Fresh proof definition:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition /tmp/audit-work/124-valid-date/build/verification-kompiled
```

Exit status: 0. See `evidence/03-build-verification.log`.

All 47 submitted positive claims were then run together, which is the
candidate's only target-proof command:

```text
kprove spec.k \
  --definition /tmp/audit-work/124-valid-date/build/verification-kompiled \
  --spec-module VALID-DATE-SPEC --smt-timeout 5000
```

It exited 0 and printed `#Top`. K also printed `WarnTrivialClaim` for each of
the 14 symbolic `validMonthDay` claims. See
`evidence/03-positive-kprove.log`.

For generated-semantics validation, `evidence/semantic_differential.py` ran the
fresh LLVM definition on 17 normal and boundary strings and compared it with
both Python implementations. All 15 ASCII cases agreed with the submitted
Python program. Two Unicode decimal cases did not:

```text
input='٠٣-١١-٢٠٠٠' k=False candidate_python=True canonical_python=True
input='０３-１１-２０００' k=False candidate_python=True canonical_python=True
TOTAL_CASES=17
K_CANDIDATE_MISMATCHES=2
EXIT_STATUS=1
```

Each individual `krun` exited 0; the script's exit 1 denotes detected
differential mismatches. Exact per-case commands and outputs are in
`evidence/03-semantic-differential-final.log`. The earlier
`03-semantic-differential.log` is superseded because its first parser expected
a bare term rather than the printed `<k>` configuration.

## 4. Adequacy and real-program pinning

### Claim preconditions and postconditions

There are 47 claims:

1. The 33 entry claims at `spec.k:7-83` have no `requires` condition. Each
   precondition is one fixed initial `<k>` computation
   `runProgram(solutionProgram, "valid_date", vals(strVal(CONSTANT)))`.
   Each postcondition fixes the result to one concrete `boolVal(true)` or
   `boolVal(false)`. Every precondition is satisfiable by that displayed initial
   configuration.
2. The 12 claims at `spec.k:87-112` quantify an arbitrary integer `D`, but
   their `<k>` term is only `boolVal(validMonthDay(FIXED_MONTH, D))`; it does
   not execute `solutionProgram`. The postcondition restates the corresponding
   arithmetic day bound.
3. The claim at `spec.k:115-116` assumes `M < 1 or M > 12` and reduces the
   declarative helper to false. A witness is `M=0, D=1`.
4. The claim at `spec.k:117-118` assumes an in-range month and `D < 1` and
   reduces the declarative helper to false. A witness is `M=1, D=0`.

All displayed postconditions are result-constraining; the defect is their
scope and connection, not a free result variable.

`evidence/claim_witnesses.py` mechanically extracted all 33 entry constants and
substituted them into both Python functions. It found:

```text
GROUND_ENTRY_CLAIMS=33
CANDIDATE_PYTHON_MISMATCHES=0
CANONICAL_PYTHON_MISMATCHES=13
EXIT_STATUS=0
```

The 13 canonical differences are the format tolerance and calendar precedence
issues described in stage 2.

### Program pinning

The ground entry claims do execute the submitted constructor body. After
trusted regeneration, I extracted the `solutionProgram` right-hand side from
`verification.k`, removed only the K spelling `.Stmts` for an empty list, and
parsed both terms through the fresh K parser as `Program`. The normalized KAST
JSON files are byte-identical:

```text
9fd4a067903fd0ea2c16efc12d3db65cf8cb1b7cbeb8eb63ce973ad47e4a71ef  solution-mpy.kast.json
9fd4a067903fd0ea2c16efc12d3db65cf8cb1b7cbeb8eb63ce973ad47e4a71ef  solutionProgram-rhs.kast.json
EXIT_STATUS=0
```

See `evidence/04-constructor-pinning-final.log`. The earlier
`04-constructor-pinning.log` records the expected parser rejection before this
empty-list spelling normalization.

A body-sensitivity mutation changed the actually executed final day cap in
`solutionProgram` from 31 to 30, rebuilt a separate definition, and reran the
formerly true `"01-31-0000"` claim. The definition compiled at exit 0 and the
claim failed at exit 1 with the residual `boolVal(false)`. See
`evidence/body-sensitivity.patch`,
`evidence/04-body-sensitivity-build.log`, and
`evidence/04-body-sensitivity-proof.log`.

### Fatal adequacy gap

There is no claim of the required form

```text
runProgram(solutionProgram, "valid_date", vals(strVal(S)))
  => boolVal(validDateSpec(S))
```

for arbitrary `S`, nor any equivalent partition that covers all strings.
`validDateSpec` is defined in `verification.k:74-113` but is referenced by zero
claims. The symbolic month/day claims are about a separate function and are
not helper/loop claims matching program control flow. Consequently:

- the 33 ground program proofs do not generalize beyond their constants;
- the 14 symbolic helper reductions do not connect to the source body;
- no theorem relates parsing, separators, digit checks, or source branches to
  the declarative contract for an arbitrary input.

This is a material finite narrowing of an unrestricted HumanEval string domain.
The Kit classification is at best `SOUND-BUT-LIMITED`; the benchmark prompt
explicitly maps that condition to `FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

`evidence/05-rule-inventory.log` is the source-derived inventory. Local files
contain 35 syntax declarations, one configuration, 60 rules, and 47 claims.
There are no local declarations marked `total` or `functional`, no opaque
symbols, no priority rules, and no `simplification`, `owise`, `anywhere`, or
macro rules. The only special attribute is `[function]`.

### `semantic.k` exhaustive inventory

Syntax:

- `Program`: `Module(Stmts)`.
- `Stmts`: an unseparated list of `Stmt`.
- `Stmt`: `FuncDef`, `Return`, `Assign`, and `If`.
- `Expr`: `Int`, `Bool`, `Str`, `Name`, `UnaryOp`; `BoolOp` of arity 2, 3, or
  4; `Compare`; indexed and sliced `Subscript`; `Attribute`; zero-argument and
  one-argument `Call`.
- `CmpOp`: operator string plus right expression.
- `SliceExpr`: bounded `Slice` with `NoBound` step.
- Semantic data: `Val` (`intVal`, `boolVal`, `strVal`), `Vals`, `Env`
  (`.Env`/`bind`), `ExecResult` (`normal`/`returned`), and `Command`
  (`runProgram`).
- Configuration: a single `<k>` cell initialized with a `Command`.

All constructs used by regenerated `solution.mpy` map to those productions:
module/function/parameter structure; `If`, `Return`, and `Assign`; all literal
and name forms; `not`; 2/3/4-way `and`/`or`; all used comparisons; fixed indices
and slices; `len`, `int`, and zero-argument `.isdigit()` calls. No used
constructor is unmodeled.

Rules and assessment:

- `runProgram` (one ordinary cell rule, lines 53-57) selects an exact
  one-function module, requires the invoked name to equal the bound function
  name, and binds the one argument. For the submitted module, this preserves
  binding and control.
- `finish` (two function rules, lines 60-61) returns a `returned` value and maps
  fall-through to false. Mapping Python's implicit `None` to false is not a
  general Python rule, but the submitted function returns on every string path,
  so the fall-through rule cannot affect its claimed executions.
- `exec` (four rules, lines 64-69) handles empty statements, abrupt return,
  assignment with shadowing, and conditional dispatch. `branch` (two rules,
  lines 72-73) chooses the true/false body; `resume` (two rules, lines 76-77)
  propagates return or resumes the suffix. These rules preserve the source
  statement order and return control for this straight-line function.
- `lookup` (two guarded/disjoint rules, lines 80-82) implements latest-binding
  lookup. Same-name and different-name cases are disjoint.
- `eval` has 17 rules: four literal/name rules (85-88); one `not` rule (90);
  six Boolean rules for `and`/`or` at arities 2/3/4 (92-107); one comparison
  dispatcher (109-110); two subscript rules (112-114); and three call rules for
  `len`, `int`, and `.isdigit()` (116-118). The Boolean rules evaluate eagerly
  and always return booleans rather than modeling Python short-circuit operand
  values. In this submitted body, every operand is a pure, defined boolean
  computation on the path where it occurs, so this limitation has no target
  witness; it is a reuse limitation rather than a demonstrated false target
  conclusion.
- `asBool` and `pyNot` each have one boolean-only rule (121, 124). Every target
  use has a boolean operand.
- `compare` has eight disjoint rules (127-134): six integer operators and
  string equality/inequality. They match all and only target comparison
  type/operator pairs.
- `pyLen`, `pyIndex`, `pySlice`, and `pyInt` each have one rule (137, 140, 143,
  146). Indexing does not model Python out-of-range exceptions, slicing omits
  general clamping/negative bounds, and `String2Int` does not model conversion
  exceptions. The submitted length and digit guards make every used
  index/slice/conversion safe, so none of those gaps enables a false conclusion
  on a submitted ASCII execution.
- `pyIsDigit` has one rule (150); `isDigits` has two disjoint length cases
  (153-154); `isDigitsAt` has two disjoint index cases (157-161); and
  `isDigitChar` has one rule (164). Recursion advances from 0 to the finite
  string length, so it descends and covers reachable calls.

The digit rules are nevertheless an unsound model of the operation actually
called by `solution.py`. They recognize only characters found in
`"0123456789"`, while CPython `str.isdigit()` and `int()` accept Unicode decimal
digits. Concrete false-conclusion witnesses are:

```text
solution.valid_date("٠٣-١١-٢٠٠٠") == True
K runProgram(..., "٠٣-١١-٢٠٠٠") == boolVal(false)

solution.valid_date("０３-１１-２０００") == True
K runProgram(..., "０３-１１-２０００") == boolVal(false)
```

Fresh commands, exit statuses, and configurations are in
`evidence/03-semantic-differential-final.log`. This mismatch is reachable from
the real submitted function on string inputs.

### `verification.k` exhaustive inventory

- `solutionProgram` is a `[function]` constant with one rule containing the
  exact constructor body. It does not bypass execution; `runProgram` consumes
  that body. Constructor-level identity and body sensitivity were established
  in stage 4.
- `validDateSpec` has one equation delegating to `specLength`.
- `specLength` has two disjoint boolean equations.
- `specSeparators` has two disjoint boolean equations.
- `specDigits` has two disjoint boolean equations.
- `validMonthDay` has one total mathematical expression over its two integer
  arguments.
- `isThirtyDayMonth` has one equation characterizing months 4, 6, 9, and 11.

These ten rules are truthful definitions of an exact-width, ASCII-digit
reading of the prose. Their cases are disjoint where they overlap in symbol,
and recursive descent is not involved. They do not introduce an oracle into
program execution. Their critical defect is relevance: `validDateSpec` is never
claimed equal to program execution. The 14 `validMonthDay` claims reduce a
definition to its own arithmetic cases and K reports them as trivial; they
cannot establish source parsing or branch correctness.

### Configuration, state, and trust boundary

The target needs no heap, allocation, I/O, exceptions on successful guarded
paths, loops, or mutable objects, so the single `<k>` cell plus immutable
binding chain is adequate for the submitted ASCII executions. Evaluation and
state rules have no local priority overlaps. Imported `INT`, `BOOL`, and
`STRING` domain operations are low-level trusted primitives, discussed in
stage 7.

## 6. Fresh non-vacuity test

Result: PASS for discrimination of a ground entry claim.

The candidate supplied no `spec-vacuity.k`; I created a fresh reviewer artifact
`evidence/spec-vacuity-audit.k`. It leaves the program unchanged and mutates
the true `"03-11-2000"` result obligation to `boolVal(false)`. The initial
state is plainly satisfiable, and both Python implementations return true.

The dry run:

```text
kprove spec-vacuity-audit.k \
  --definition /tmp/audit-work/124-valid-date/build/verification-kompiled \
  --spec-module AUDIT-VACUITY-SPEC --dry-run
```

parsed and built successfully at exit 0. See
`evidence/06-vacuity-build.log`.

The actual proof used the same command without `--dry-run`. It exited 1 with
`WarnStuckClaimState`; the residual was:

```text
<k>
  boolVal ( true ) ~> .K
</k>
```

This is the expected unmet result obligation, not a parser error, timeout, or
unreachable mutation. See `evidence/06-vacuity-proof.log`.

This test shows the fixed ground claims are not vacuous. It does not repair the
absence of an arbitrary-input theorem.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's K definition:

- the exact submitted constructor program returns the listed booleans on the
  33 constant ASCII strings in `spec.k`;
- the declarative `validMonthDay` function reduces to the listed day-bound
  formulas for each fixed in-range month and to false under the two displayed
  guarded out-of-range cases.

That is all. It does not establish, for an arbitrary string, that the submitted
program returns true exactly for valid dates. It does not establish any
connection between `runProgram` and `validDateSpec`.

### Assumptions and boundaries

- **K toolchain/backend:** correctness of K 7.1.293 parsing, compilation,
  rewriting, and reachability proving is trusted. Every formal claim depends on
  it. This is an ordinary acceptable proof-system boundary.
- **Imported domain primitives:** `lengthString`, `substrString`,
  `findString`, `String2Int`, integer comparisons/arithmetic, and Boolean
  operations from `domains.md` are trusted. They affect values and branches.
  This is acceptable low-level trust where their guards match use; it does not
  justify the Unicode `isdigit` abstraction.
- **Translator/source bridge:** the trusted `py2mpy.py` is assumed to preserve
  the relevant Python AST constructors. Byte regeneration and KAST identity
  show that the claims execute the submitted translated body, but no formal
  CPython-to-K translation theorem is provided.
- **Generated semantics/CPython bridge:** all operational rules are
  candidate-generated and are not formally connected to CPython. Exhaustive
  target-rule review and finite execution support the 33 claimed ASCII cases.
  The bridge is not valid on the full actual string behavior because of the two
  Unicode witnesses.
- **Contract interpretation:** exact-width `mm-dd-yyyy` and the month-specific
  day caps come from the prompt. The canonical implementation has documented
  contradictory behavior. This is an informal intent bridge, supported but not
  universally proved.
- **No opaque symbols or external oracles:** every local function is equationally
  defined. `validDateSpec`/`validMonthDay` encode the declarative answer but do
  not replace program execution; instead, they remain unconnected and therefore
  cannot carry the desired theorem.
- **Finite tests:** differential, concrete, constructor-pinning, body-sensitivity,
  and non-vacuity artifacts are reproducible evidence only. None substitutes
  for the missing arbitrary-input K claim.

### Gate accounting and decision

- Gate A for the literal finite submitted theorem: PASS. The 33 entry results
  are constrained, their preconditions are satisfiable, their constructor body
  is pinned, all agree with the submitted Python program, and both result and
  body mutations are rejected. The symbolic helper claims are truthful but
  independent.
- Gate B: FAIL. The theorem covers finitely many entry inputs and never links
  arbitrary program execution to the contract. The generated semantics also
  excludes reachable Unicode behavior of the real program.
- Gate C: PASS for auditability of the limited theorem. Commands, inputs,
  outputs, assumptions, and counterexamples are preserved. Finite evidence is
  not presented as universal proof.

The resulting Kit status is `SOUND-BUT-LIMITED`. The benchmark prompt
specifically requires a materially narrowed HumanEval source-contract theorem
to be classified as `FAIL / NOT_LEGIT`, not as a concern-level legitimate
proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
