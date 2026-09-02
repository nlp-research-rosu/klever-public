# Independent adversarial review: 124-valid-date

## Outcome

The positive K proof is reproducible, result-constraining, and tied to the
actual regenerated `solution.mpy` term. It covers every MPY string, executes
the submitted function body through the supplied semantics, and uses no
proof-local operational bridge or opaque result oracle. Fresh result and body
mutations both fail at the expected obligations.

The remaining concern is not proof soundness: the trusted `canonical.py`
contradicts the natural-language prompt on material boundary cases. In
particular, Python operator precedence in the canonical code causes valid days
30 and 31 to be rejected. The submitted program and formal result formula agree
with the prompt instead. I therefore regard the proof as legitimate but do not
give an unqualified pass over the mutually inconsistent trusted intent
artifacts.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `124-valid-date`, and condition
`kit-semantics`. The supplied-semantics mount required by that mode is present.
There is no rendered-mode/mount contradiction and no infrastructure breach.

The independent check in
[`evidence/01-provenance.log`](evidence/01-provenance.log) established:

- `/audit-campaign-lock.json` is a regular file, its parsed JSON is exactly the
  `audit_campaign` block, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-declared container path exists with the required file or
  directory type and is readable.
- The regular-file hashes recorded for the canonical, prompt, translator,
  run/task/result manifests, invocation, metrics, runtime metrics, usage,
  generation prompt, last message, and output log all match independently
  computed hashes.
- The structured trace is valid JSONL with 407 parsed records. Its file hash is
  `0f991c44e4d03a80950afe9e4910a883b94357f3992c5b4fc12b1a97c99bae45`,
  exactly the trace-file hash recorded in both `generation-result.json` and
  `invocation.json`.
- The candidate prompt and translator are byte-identical to their trusted
  mounts.
- The candidate and trusted `reference-semantics/` trees have the same 25
  entries (one directory plus 24 files), the same entry types, and the same
  bytes for every file. Neither tree contains a symlink. An independent
  reviewer-defined recursive manifest gives the same digest
  `161f0813a4cd7f70e1e6d462e000bd62f6211b547814d06c786f1ce4c5205b8f`
  for both trees.
- The whole candidate tree contains no symlink, and all six required proof
  artifacts are regular files.

All pipeline-v3 records required by the prompt were read. A bounded rendering
of the manifests, all generation shell commands, all 407 trace records by type,
and all 59 structured function calls is in
[`evidence/25-generation-records.log`](evidence/25-generation-records.log).
Those generation records were treated only as untrusted historical claims.
The source artifact hashes used by this audit are preserved in
[`evidence/27-source-artifact-hashes.log`](evidence/27-source-artifact-hashes.log).

One telemetry-only inconsistency is visible: `usage.json` names
`ae312bb6...` as a `source_trace_sha256`, while the final mounted trace and both
launcher result records use `0f991c44...`. The usage file itself has the
launcher-recorded hash, and the authoritative per-output trace hash matches the
mounted trace. This does not affect any proof artifact or reconstruction and is
not an infrastructure breach.

Only source artifacts were copied to `/tmp/audit-work/fresh`; candidate
`runtime-kompiled`, `verification-kompiled`, `verification-mutant-kompiled`,
caches, binaries, and logs were not used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt requires `valid_date(date)` on a date string. It returns true
exactly when the string has literal `mm-dd-yyyy` form, the month is 1 through
12, and the day is:

- 1 through 31 for months 1, 3, 5, 7, 8, 10, and 12;
- 1 through 30 for months 4, 6, 9, and 11;
- 1 through 29 for month 2.

No leap-year condition is stated; the four year characters are format
characters only. Empty and malformed strings return false.

`solution.py` implements this literal contract. It first requires length 10,
requires hyphens at positions 2 and 5, requires ASCII digits in all eight other
positions, decodes the month and day, and checks the three month classes. It is
defined for every Python string and does not narrow that source domain.

The trusted translator was run afresh:

```text
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0, and the regenerated file is byte-identical to submitted
`solution.mpy`; both have SHA-256
`238a66385f2d2c34612a13d33a04de1a04d5d954ee4b8c2ec6443963cece8425`.
See [`evidence/02-translate.log`](evidence/02-translate.log) and
[`evidence/03-translation-byte-identity.log`](evidence/03-translation-byte-identity.log).
The translator's relevant handlers are pure constructor translations for
function definitions, returns, assignments, conditionals, calls, subscripts,
Boolean operators, comparisons, arithmetic, names, and literals; none silently
drops or interprets a used node.

### Independent differential result

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports the trusted canonical and generated entry points and uses a separately
written literal-format oracle. It exercises the five examples, empty and
length boundaries, every digit/separator position, every month/day pair
`00..99` for four years, explicit month-class boundaries, Unicode/malformed
cases, canonical-extension cases, and 5,000 deterministic generated strings.

The run in [`evidence/04-differential.log`](evidence/04-differential.log)
tested 44,308 unique inputs:

- documented-example failures: 0;
- generated-versus-prompt-oracle mismatches: 0;
- generated-versus-canonical mismatches: 85.

The canonical divergences are material and explainable from
`/reference/canonical.py:32-36`. Expressions such as
`month in [...] and day < 1 or day > 30` are parsed with `and` binding more
tightly than `or`. Consequently:

- `01-31-2000`, `04-30-2000`, `06-30-2000`, `09-30-2000`,
  `11-30-2000`, and `12-31-2000` are true under the prompt and submitted
  program but false under the canonical;
- the canonical's `strip`, split, and `int` path also accepts some strings that
  are not literal `mm-dd-yyyy`, such as `03-11-200` and Unicode decimal digits.

This is a disagreement in trusted intent evidence, not a substitution in the
proof. For the literal natural-language contract, the submitted program is the
aligned implementation and the canonical is the outlier. The concern in the
final verdict records that this material divergence cannot simply be ignored.

## 3. Clean proof reconstruction

The live toolchain is K `v7.1.293`, matching the campaign, as recorded in
[`evidence/05-toolchain.log`](evidence/05-toolchain.log). No candidate-provided
definition or cache was reused.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
```

This exited 0
([`evidence/06-kompile-llvm.log`](evidence/06-kompile-llvm.log)).
Reviewer-authored boundary assertions in
[`evidence/audit_concrete.py`](evidence/audit_concrete.py) were translated with
the trusted translator and executed with that definition. `krun` exited 0 at
`.K`, with `NoExc`, empty heap/stack, and exit code 0
([`evidence/07-audit-concrete-translate.log`](evidence/07-audit-concrete-translate.log),
[`evidence/08-krun-audit-concrete.log`](evidence/08-krun-audit-concrete.log)).

Fresh proof reconstruction:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

This exited 0
([`evidence/09-kompile-haskell.log`](evidence/09-kompile-haskell.log)).
Each positive target was then run independently:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-10
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-non10
```

Both commands exited 0 and printed `#Top`; see
[`evidence/10-kprove-valid-date-10.log`](evidence/10-kprove-valid-date-10.log)
and
[`evidence/11-kprove-valid-date-non10.log`](evidence/11-kprove-valid-date-non10.log).
Compiler warnings concern unused variables or non-exhaustive generic helpers;
none is a failed target or a reachable result abstraction for this program.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.valid-date-10` starts from the normal MPY initial configuration, loads
`validDateProgram`, calls its `valid_date` binding on a structurally
ten-element string whose ten codes are arbitrary integers, and requires
termination at a Boolean `R`. Its postcondition is the equivalence
`R ==Bool validDateResult(codes)`. Thus the result is not free and the property
is not one-way.

`SPEC.valid-date-non10` starts from the same realizable initial state, calls the
same binding on an arbitrary `IntSeq`, assumes its length is not 10, and
requires the final result to be literal `false`.

Together the structural ten-element case and `isLen(CS) =/=Int 10` cover every
ground MPY string, not finitely many sizes. The claims preserve environment,
scope allocation counter, heap, heap counter, stack, return state, exception
state, and exit code. Only the post-load scope map is existentially framed,
which hides the function binding retained after module loading but not any
HumanEval-observable result or call-control effect.

Satisfying ground witnesses are explicit in
[`evidence/16-claim-witnesses.log`](evidence/16-claim-witnesses.log):
`03-11-2000` satisfies the ten-character entry and produces true;
`02-30-2000` satisfies it and produces false; the empty string satisfies the
non-ten precondition and produces false. The formal summary and submitted
Python result agree in each case. The `01-31-2000` witness additionally shows
the prompt-aligned true result and the canonical discrepancy.

### Mechanical program identity

The `validDateProgram` right-hand side from `verification.k:13-166` was
independently extracted, with only explicit `.Stmts` units removed. Both that
term and the freshly regenerated `solution.mpy` were parsed to KORE using the
fresh LLVM syntax definition. Each parsed term is 37,017 bytes, each has
SHA-256
`95fe4d605646b064d9ebb0be32c666d5e7f71c5f8b9ca9c7639db436f5f91d28`,
and `cmp` exits 0. See
[`evidence/12-extract-claim-program.log`](evidence/12-extract-claim-program.log)
through
[`evidence/15-claim-program-identity.log`](evidence/15-claim-program-identity.log).
The claim therefore executes the submitted function binding and body, not a
substituted program.

For independent body sensitivity, the reviewer changed only the February body
bound from 29 to 28 using
[`evidence/make_body_mutant.sh`](evidence/make_body_mutant.sh). The mutant's
parsed program KORE hash changed to
`687bf5cca4c8a311648eb8155a4a1f6f9d0cffb20fee8659869383f65d44190d`,
so this is a mutation of the term actually executed by the claim
([`evidence/19-body-mutant-term-sensitivity.log`](evidence/19-body-mutant-term-sensitivity.log)).
The mutant definition built successfully, but the unchanged universal claim
exited 1 with `WarnStuckClaimState`; its residual explicitly contains
`day <= 28` versus the summary's `day <= 29`
([`evidence/20-kompile-body-mutant.log`](evidence/20-kompile-body-mutant.log),
[`evidence/21-kprove-body-mutant-expected-fail.log`](evidence/21-kprove-body-mutant-expected-fail.log)).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/17-k-inventory.log`](evidence/17-k-inventory.log) is the
line-numbered inventory of all K sources in scope: 24 supplied semantics files,
`verification.k`, and `spec.k`. It contains 1,224 declaration items, including
700 rules, 231 syntax declarations, one configuration, five contexts, and two
claims. It records every `function`, `total`, `symbol`, `concrete`, `owise`,
priority, strictness, macro, token, hook, associativity, and commutativity
attribute. There are no `functional` or `simplification` declarations.

The following module-level decisions apply to every individually listed rule:

| Source | Rules | Static decision |
|---|---:|---|
| `semantics.k`, `syntax.k`, `iter.k` | 0 | Import wiring and constructor/sort declarations only; accepted. |
| `core.k` | 46 | Configuration, loading/sequencing, scope lookup, literals, argument order, truthiness, and structural helpers are ordinary state-preserving encodings. The reachable cases are complete and accepted. |
| `functions.k`, `call.k` | 15 + 21 | The real closure is created, looked up, called, parameter-bound, framed, returned, and popped. No rule replaces the function body or fabricates its result. Accepted. |
| `controls.k` | 34 | Assignment, `If`, and branch rules used here preserve the current frame and Python-style truth selection. Return control is handled in `functions.k`. Accepted. |
| `operators.k`, `int.k` | 10 + 16 | Left-to-right heating/dispatch and integer arithmetic/comparison rules directly use K integer/Boolean operations. Used guards and sort cases are disjoint. Accepted. |
| `bool.k` | 13 | `and`/`or` evaluate the head and short-circuit while returning the selected value. Here every selected operand is Boolean. Accepted. |
| `str.k`, `subscript.k` | 28 + 40 | ASCII literal conversion, string equality, positive index normalization, and `intSeqAt` recursion are direct. Every program index is structurally in bounds in the ten-character claim and unreachable in the other claim. Accepted. |
| `builtins.k` | 137 | The used `len(str(IS)) -> isLen(IS)` and singleton `ord` rules are exact and name-selected through `builtinsScope`. Other builtin rules cannot match a reachable redex in this program. |
| `assert.k`, `comprehension.k`, `concrete.k`, `dict.k`, `float.k`, `list.k`, `methods.k`, `range.k`, `set.k`, `sort.k`, `tuple.k` | 3 + 7 + 16 + 28 + 121 + 27 + 75 + 6 + 12 + 19 + 21 | Reviewed as supplied subset encodings. None of their operation constructors is reachable from `solution.mpy`; their priorities, totalizations, and abstractions cannot affect either claim. No false conclusion witness on the intended program domain was found. |
| `verification.k` | 5 | Four exact, terminating definitions: the program AST constant and three mathematical summaries. Detailed below. |

### Used-construct map and execution fidelity

Every material constructor in `solution.mpy` has a fixed-semantics route:

- `Module`, `FuncDef`, statement sequencing, `Name`, and scope lookup:
  `syntax.k:53-61`, `core.k:123-181`, `functions.k:14-16`.
- `Call`, callee/argument evaluation, binding, frame creation, and cleanup:
  `core.k:183-191`, `call.k:18-32,69-75`,
  `functions.k:62-90`.
- `len` and `ord`: `builtins.k:17-26,140-145`, selected only after ordinary
  lookup through `core.k:129-181`.
- `Subscript` and positions 0 through 9:
  `subscript.k:16-41`; all accesses are in bounds on the only paths that reach
  them.
- `BinOp` and `Compare`: strict syntax in `syntax.k:14-15`, comparison contexts
  in `operators.k:14-17`, and exact integer/string cases in `int.k:7-27` and
  `str.k:12-26`.
- `BoolOp`: `bool.k:13-25`, preserving left-to-right short-circuiting.
- `Assign` and `If`: `controls.k:8-18,50-54`.
- `Return`: strict expression evaluation from `syntax.k:50`, then
  `functions.k:77-90`, which discards only the remaining callee continuation,
  records the return value, restores the caller frame, and exposes the result.

The claims start from the exact configuration expected by these rules. The
function has no loops, allocation, external state, output, or exceptional path
on the claimed string domain. Fixed semantics executes all property-bearing
operations.

### Proof-local extensions

The exact scan is in
[`evidence/26-proof-extension-scan.log`](evidence/26-proof-extension-scan.log).
There is no proof-local `<k>` rewrite, priority, `owise`, `concrete`,
`simplification`, opaque symbol, or auxiliary claim.

- `validDateProgram` is a total definitional AST constant. It changes no cell
  and does not replace execution. Its complete justification is the parsed-KORE
  identity check.
- `asciiDigit(C)` is the unconditional equation `48 <= C <= 57`.
- `validMonthDay(M,D)` is the unconditional disjoint union of the February,
  30-day, and 31-day month classes. It is a direct mathematical restatement of
  the prompt.
- `validDateResult(CS)` has two guards, length equal to 10 and length unequal to
  10. They are disjoint and exhaustive. Indexed accesses occur only under the
  length-10 guard, and the formula checks both separators, all eight digit
  positions, and the decoded month/day pair.

All definitions cover their declared use, descend structurally where
recursive, and have no inconsistent overlap. They appear as syntax selection
or postcondition mathematics, not as an oracle injected into execution. I make
no unsound-rule allegation, so no false-conclusion witness is asserted.

The supplied tree contains 25 explicitly symbolic/opaque declarations:
`md5hexCodes`; `sortVS`, `sortKeyVS`; and the float-family
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. None occurs in the program term, postcondition, residual, or used
execution chain. They have no dependent target claim here.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not relied on. The reviewer-authored
[`evidence/spec-audit-false.k`](evidence/spec-audit-false.k) changes the
result-constraining obligation for the satisfying input `03-11-2000` from its
real result `true` to `false`.

First, `kprove ... --dry-run` exited 0 and emitted the backend command, proving
that the mutation parses and builds rather than failing syntactically
([`evidence/23-false-spec-dry-run.log`](evidence/23-false-spec-dry-run.log)).
The actual proof then exited 1 with `WarnStuckClaimState`. The residual is the
fully executed configuration with `<k> true ~> .K </k>`, while the destination
requires `false`; this is exactly the intended unmet obligation, not a timeout,
parser error, missing import, or unrelated crash
([`evidence/24-kprove-false-spec-expected-fail.log`](evidence/24-kprove-false-spec-expected-fail.log)).
The proof is discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the exact supplied MPY Haskell definition and the stated initial
configuration:

1. for every structurally ten-code MPY string, loading the exact submitted
   module and calling its `valid_date` binding terminates at a Boolean equal to
   the explicit separator/digit/month/day formula; and
2. for every MPY string whose structural length is not 10, the same execution
   terminates at `false`.

The theorem constrains call-control, heap, allocation counters, exception
state, and exit status, and permits only the expected post-load scope map to be
existential. It is a partial-correctness claim in the Kit sense, although its
successful reachability result also exhibits termination within this modeled,
loop-free execution.

### Trust and evidence ledger

- **Supplied MPY semantics:** fixed by the benchmark and byte-verified against
  the trusted supplied tree. The used rules were reviewed above. This is still
  a model of the needed Python subset, not a machine-checked equivalence theorem
  to all CPython behavior.
- **K framework, Haskell backend, LLVM backend, SMT solver, and builtin
  theories:** trusted infrastructure. Used primitives are integer
  `+/-/*` and comparisons, Boolean connectives/equality, ASCII string
  `length/substr/ord`, finite map lookup/update/membership, list stack
  operations, K matching/sequencing, and backend reachability. They affect the
  proof as described by the fixed semantics; no proof-local replacement is
  made.
- **CPython parsing and trusted `py2mpy.py`:** trusted for the
  source-to-constructor bridge. Independent regeneration gives byte identity,
  and independent KORE parsing ties that output to the executed claim term.
  The translator itself is not formally verified.
- **Human interpretation of `mm-dd-yyyy`:** the proof formula uses ASCII
  digits and literal hyphens. This is the ordinary and most direct reading of
  the prompt, supported by all examples and the explicit format rule.
- **Differential evidence:** 44,308 finite Python cases and reviewer-authored
  LLVM assertions support the prompt/program and MPY/Python bridges. They do
  not replace either universal K proof.
- **Trusted canonical:** it is used as required differential evidence, not as a
  proof axiom. Its 85 observed disagreements include intended day-30/day-31
  boundaries and arise from source-visible precedence/format behavior. Because
  the prompt and canonical cannot both be the full intended oracle, this is the
  documented limitation that prevents an unqualified pass.
- **Opaque symbols:** all 25 are listed in Stage 5. None influences a branch,
  value, state, exception, or postcondition in either target claim.

There is no finite-size restriction, body substitution, free result, assumed
program helper, operational bridge, or task-answer rewrite. The candidate's
own `PROOF.md`, historical `#Top`, traces, tests, and compiled definitions were
not used as substitutes for this reconstruction.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
