# Independent adversarial audit: 124-valid-date

The reconstructed K proof is legitimate and pins the real translated program.
It is not a proof of equivalence to the trusted `canonical.py`: the canonical
implementation conflicts materially with the literal prompt contract and with
the proved program on both properly formatted boundary dates and malformed
strings. That conflict prevents an unqualified `PASS`, but it does not make the
reachability proof unsound or vacuous.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no infrastructure-mode
contradiction.

I treated `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, the JSONL trace, all candidate logs, `PROOF.md`, and both
candidate kompiled directories only as untrusted claims. A bounded parse and
hash summary is in
[`evidence/01a_untrusted_generation_summary.log`](evidence/01a_untrusted_generation_summary.log);
the reviewer script is
[`evidence/summarize_untrusted_generation.py`](evidence/summarize_untrusted_generation.py).
The trace has 311 valid JSON records and no parse error. Its final report claims
`#Top`, validation, and zero mismatches against the candidate's own oracle;
none of those claims was reused as proof evidence.

The independent integrity checker
[`evidence/integrity_check.py`](evidence/integrity_check.py) found:

- every required top-level artifact is a regular file;
- the structured trace is a real directory containing one regular JSONL file;
- candidate `prompt.py` is byte-identical to `/reference/prompt.py`, SHA-256
  `71bb688daf8e872a52f7dfb4d4a09c07db640afd5fc1f8845baa1470a2930b78`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- the candidate and trusted semantics trees each have exactly 25 entries
  below their roots (one helper directory and 24 K files);
- every corresponding semantics entry has the same type and every file has
  the same SHA-256; there are no missing, additional, changed, mistyped, or
  symlinked entries.

The exact output and exit 0 are in
[`evidence/01_integrity.log`](evidence/01_integrity.log). Candidate kompiled
definitions and Python caches were not copied. The scratch-copy manifest is
[`evidence/00_scratch_copy.log`](evidence/00_scratch_copy.log). K 7.1.293 and
Python 3.10.12 were independently available; see
[`evidence/00_environment.log`](evidence/00_environment.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`prompt.py` asks for `valid_date(date)` on a date string. A date is valid when
it has `mm-dd-yyyy` format, month 1 through 12, day at least 1, and an upper
bound of 29 for February, 30 for months 4/6/9/11, and 31 for the other months.
There is no leap-year rule and no year-range rule. The most literal reading of
`mm-dd-yyyy` is two ASCII decimal digits, a hyphen, two ASCII decimal digits, a
hyphen, and four ASCII decimal digits.

`solution.py` implements exactly that literal reading:

1. reject every length other than 10;
2. require hyphens at indices 2 and 5;
3. use `ord` to require ASCII codes 48 through 57 in the other positions;
4. compute the two-digit month and day;
5. implement the stated month/day partition.

It is loop-free and every index is protected by the length guard.

The trusted translator was run on the scratch copy:

```text
python3 ../trusted/py2mpy.py solution.py > solution.regenerated.mpy
```

It exited 0, and `cmp -s solution.mpy solution.regenerated.mpy` exited 0. Both
MPY files have SHA-256
`cfc7f7962c579c74b5ebe187a7312c754a0e5cf44756675e58c7244a52606901`.
See
[`evidence/02_translation_identity.log`](evidence/02_translation_identity.log).

### Independent differential result

The reviewer-authored test
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point and the generated entry point independently. It
also uses a separately structured regular-expression/table oracle for the
literal prompt contract. Its 4,082 unique strings include:

- all five documented examples;
- empty and malformed values;
- every material result branch and adjacent digit/separator boundaries;
- every month 00 through 13 and day 00 through 33 for three years;
- ASCII, non-ASCII decimal, and near-digit characters at every checked
  position;
- 3,000 deterministic generated strings of lengths 0 through 14.

All inputs and three results are preserved in
[`evidence/differential_cases.jsonl`](evidence/differential_cases.jsonl).
The exact command exited 1 because divergence is intentionally an audit signal:

```text
tested=4082
canonical_generated_mismatches=79
prompt_generated_mismatches=0
```

There are 54 cases where the canonical returns `False` while both the generated
program and literal prompt oracle return `True`, and 25 where the canonical
returns `True` while both return `False`. The complete summary and witnesses
are in [`evidence/03_differential.log`](evidence/03_differential.log).

This is not an algorithmic difference with equal results. It comes from
`canonical.py` lines 32-36. Python's `and` binds tighter than `or`, so:

- line 34's `... and day < 1 or day > 30` rejects day 31 for every month;
- line 36's `... and day < 1 or day > 29` rejects days 30 and 31 for every
  month.

For example, `04-30-2000` is valid under the prompt and generated program but
the canonical returns `False`. Conversely, the canonical calls `strip`,
`split`, and `int` without checking component widths, so it accepts such
non-format strings as `3-11-2000`, whitespace-padded dates, and some Unicode
decimal digits.

Thus the generated implementation agrees with the literal prompt but is not
extensionally equivalent to the trusted canonical over the intended string
input type. This is a material reference/contract conflict and is the reason
for the final `CONCERNS` verdict.

Stage 2 result: **CONCERN** for canonical divergence; program-to-literal-prompt
fidelity and translator identity otherwise pass.

## 3. Clean proof reconstruction

All source needed for execution was copied into `/tmp/audit-work`; no candidate
definition, cache, or generated backend artifact was used.

The supplied semantics was freshly compiled for concrete execution:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/runtime-kompiled
```

It exited 0. The compiler reported fixed-semantics non-exhaustiveness warnings
for several declared-total helpers. None is reached by this program; the used
string access is `intSeqAt` on exact in-bounds positions. The full bounded log
is [`evidence/04_kompile_llvm.log`](evidence/04_kompile_llvm.log).

The independent concrete program
[`evidence/concrete_audit.py`](evidence/concrete_audit.py) contains 20
assertions covering all prompt examples and all material branch boundaries. It
was translated with the trusted translator and run against that clean LLVM
definition. `krun` exited 0 with `.K`, environment 0, empty heap and stack,
`noRet`, `NoExc`, and exit code 0. See
[`evidence/05_concrete_krun.log`](evidence/05_concrete_krun.log).

The proof definition was freshly compiled:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

It exited 0; see
[`evidence/06_kompile_haskell.log`](evidence/06_kompile_haskell.log).
I then ran the whole positive spec and each target claim independently:

```text
kprove spec.k --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
kprove spec.k --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-non-ten
kprove spec.k --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-ten
```

All three commands exited 0 and printed `#Top`. Logs:
[`evidence/07_kprove_all.log`](evidence/07_kprove_all.log),
[`evidence/08_kprove_non_ten.log`](evidence/08_kprove_non_ten.log), and
[`evidence/09_kprove_ten.log`](evidence/09_kprove_ten.log).

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.valid-date-non-ten` starts from the complete normal MPY initial state,
loads `solutionProgram`, and calls `valid_date(str(CS))`. Its precondition is
`isLen(CS) =/=Int 10`. It requires the returned K value to be exactly `false`,
with environment, scope allocator, heap, heap allocator, stack, return state,
exception state, and exit code restored.

`SPEC.valid-date-ten` starts from the same state and calls the function on
exactly ten arbitrary integer codes `C0` through `C9`. The ten-code constructor
is the claim's shape precondition. It requires the returned K value to be
exactly `validDate10(C0,...,C9)`, not a fresh variable or implication. That
predicate is true exactly for ASCII digits in the eight non-separator
positions, code 45 at positions 2 and 5, and the stated month/day predicate.

The final scope map is deliberately unconstrained by both claims. Module
loading installs `valid_date` in scope 0, while the task observes the return
value. All other state cells are constrained. There is no global assignment,
heap allocation, output, exception, or loop in the program.

### Pinning

The `solutionProgram` equation contains the complete function AST; it does not
replace a call or body execution. The trusted translator output, submitted
`solution.mpy`, and embedded RHS were checked independently.

An initial diagnostic attempt to feed the embedded K-only `.Stmts` spelling to
the MPY *program* parser was rejected, as recorded in
[`evidence/10_program_pinning.log`](evidence/10_program_pinning.log); that
parser error is not pinning evidence. The clean `kompile` had already parsed
the embedded term as K. The successful comparison then tokenized both complete
terms, erased only the six explicit `.Stmts` empty-list tokens used inside the
K rule, and found all remaining 983 tokens identical. No identifier, literal,
operator, argument, statement, or ordering difference was normalized. See
[`evidence/compare_program_surface.py`](evidence/compare_program_surface.py)
and
[`evidence/10b_program_pinning_surface.log`](evidence/10b_program_pinning_surface.log).

There are no helper claims and no loops. The used-construct/control/state map is
[`evidence/used_construct_map.md`](evidence/used_construct_map.md).

### Satisfiable states and ground substitution

The non-ten precondition is satisfied by the empty code sequence. The ten-code
precondition is satisfied by the codes of `03-11-2000`, `15-01-2012`, and
`04-30-2000`. Ground substitution agrees with generated Python in every
witness. It also exposes the canonical conflict on `04-30-2000`; see
[`evidence/11_ground_witnesses.log`](evidence/11_ground_witnesses.log).

As an independent body-sensitivity check, I changed only the embedded final
`return day <= 31` to `return False`, left the positive spec unchanged, and
rebuilt a separate proof definition. The corrected mutant compiled
successfully, but `SPEC.valid-date-ten` exited 1 with
`WarnStuckClaimState` and a residual returned `false`. The mutation and log are
[`evidence/verification_body_mutant.k`](evidence/verification_body_mutant.k)
and
[`evidence/13b_body_sensitivity_valid.log`](evidence/13b_body_sensitivity_valid.log).
An earlier malformed-parenthesis attempt in
[`evidence/13_body_sensitivity.log`](evidence/13_body_sensitivity.log) is
explicitly not counted.

Stage 4 result: **PASS** for theorem adequacy to the generated program and
literal prompt predicate; canonical equivalence is excluded.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[`evidence/rule_inventory.csv`](evidence/rule_inventory.csv), generated by
[`evidence/inventory_k.py`](evidence/inventory_k.py). It includes source text,
file and line, classification, attributes, reachability from this AST, and an
assessment for every record. Its SHA-256 and summary are in
[`evidence/12_rule_inventory.log`](evidence/12_rule_inventory.log):

- 26 K source files;
- 938 records total;
- 231 syntax-declaration statements, one configuration, five evaluation
  contexts, 238 ordinary operational rules, 461 equational/data rules, and two
  entry claims;
- 149 syntax statements with one or more `[function]` productions, 111 with
  one or more `[total]` productions, zero `[functional]` declarations;
- 22 explicit opaque/no-evaluator declaration statements, 45 priority-rule
  records, four macro statements, and zero simplification/simplifier rules.

Each of the 938 rows has a decision. The 140 used fixed-semantics records were
reviewed against the AST, binding, order, control, cells, and equations. The
remaining 788 fixed records are individually inventoried as accepted at the
selected supplied-semantics level but unreachable from this program and
postcondition. The eight proof-local records and two entry claims are assessed
separately.

### Proof-local extensions

There are exactly four declarations and four equations in `verification.k`:

1. `solutionProgram : Module [function,total]` has one exact AST equation. It
   materializes syntax and reads or writes no cell. Calls, binding, body
   execution, return control, and cleanup remain in fixed semantics.
2. `dateCodes : IntSeq [function,total]` has one exhaustive equation that
   constructs exactly ten `iCons` cells.
3. `validDate10 : Bool [function,total]` has one exhaustive, nonrecursive
   equation for digit/separator checks and the month/day formula.
4. `monthDayOK : Bool [function,total]` has one exhaustive, nonrecursive
   equation. Its outer conjunction enforces month 1-12 and day at least 1;
   its three disjoint month categories impose 29, 30, or 31.

There is no proof-local operational rule, call interception, return shortcut,
priority rule, simplification, opaque term, fresh oracle, or auxiliary
reachability claim. The static searches are recorded in
[`evidence/15_static_checks.log`](evidence/15_static_checks.log). The trusted
semantics contains none of the task-specific symbols.

### Used fixed-semantics path

The execution path has the following relevant properties:

- `#loadAll` sequences the real module and `FuncDef` installs its closure.
- name lookup selects the local `valid_date` binding and walks to the fixed
  builtin frame for `len` and `ord`; the local/fallback guards are disjoint;
- call semantics evaluates the callee, then arguments left-to-right, allocates
  a callee scope, binds `date`, executes the actual body, and restores the
  caller;
- `If`, `Return`, assignment, `BoolOp`, comparison contexts, `BinOp`
  `seqstrict`, and subscript contexts preserve Python evaluation and
  short-circuit order for this body;
- the non-ten path returns before any index; the ten-code path uses only
  in-bounds `intSeqAt`;
- fixed `len`, `ord`, ASCII `"-"` conversion, integer arithmetic, and integer
  and string comparisons have direct exhaustive equations on all reached
  values;
- return discards the remaining function-body suffix, as Python return must,
  then restores all constrained cells.

Potential priority overlaps involving heap references or closure cells have
false guards here: the input is an unboxed `str`, the frame has no `$cells`,
and the program allocates no collection. The generic call `[owise]` route
therefore handles `valid_date`, `len`, and `ord` without a competing
task-specific interception.

All reached declared-total functions (`isLen`, list append helpers,
`dateCodes`, `validDate10`, and `monthDayOK`) have exhaustive terminating
equations. `intSeqAt` is not declared total and is reached only at proven
in-bounds indices. None of the fixed opaque/no-evaluator symbols influences a
branch, result, state, exception, or postcondition.

I found no materially unsound rule and therefore make no unsoundness
allegation requiring a false-conclusion witness. The body mutation is
sensitivity evidence, not an allegation about a rule.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation
[`evidence/spec-audit-vacuity.k`](evidence/spec-audit-vacuity.k) uses the
satisfying prompt example `06-04-2020` and changes its required result from
`true` to `false`. Both trusted canonical Python and generated Python return
`True` for this witness.

The mutation first built successfully:

```text
kprove spec-audit-vacuity.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module AUDIT-VACUITY --dry-run
```

Dry-run exit: 0. The real proof command then exited 1 with
`WarnStuckClaimState`. Its final configuration contains
`<k> true ~> .K </k>`, while the destination demands `false`; this is the
expected reachable unmet result obligation, not a parser error, timeout, or
unrelated crash. Exact commands and bounded output are in
[`evidence/14_nonvacuity.log`](evidence/14_nonvacuity.log).

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics and the fresh Haskell proof definition:

- for every algebraic `IntSeq CS` whose length is not 10, loading the submitted
  module and calling `valid_date(str(CS))` reaches returned value `false`;
- for every ten integers `C0,...,C9`, the same real execution reaches returned
  value exactly `validDate10(C0,...,C9)`;
- the result predicate is the explicit ASCII `mm-dd-yyyy` and 29/30/31-day
  formula in `verification.k`;
- environment, allocator, heap, stack, return state, exception state, and exit
  code finish in the constrained normal state. Final module-scope contents are
  not a theorem output.

This is a partial-correctness reachability result under the selected semantics.
The program is loop-free and all symbolic paths close, but the report does not
claim a separate CPython liveness theorem.

### Trust boundary and assumptions

- **Supplied semantics:** all candidate semantics sources are byte-identical to
  the trusted mount. MPY's function, string, integer, call, and control rules
  define the execution model. This is the required low-level trust boundary,
  not a candidate-added conclusion.
- **Translator bridge:** `/reference/py2mpy.py` is trusted to translate the
  Python source. The submitted translation is byte-identical to a fresh run,
  and the proof AST is exact-pinned modulo only explicit empty-list spellings.
- **K implementation:** K 7.1.293, the LLVM/Haskell backends, builtin
  integer/Boolean/string/map/list hooks, and backend reasoning are trusted.
- **Natural-language bridge:** the theorem interprets `mm-dd-yyyy` as fixed
  width and ASCII decimal. That is strongly supported by the prompt text and
  has zero mismatches against the independent literal oracle, but the trusted
  canonical implements a different, internally buggy predicate. The K proof
  does not resolve which source should dominate.
- **Python-string representation:** actual Python strings map to sequences of
  code points. The formal MPY domain is over-broad because it also admits
  arbitrary K integers as codes. The rules remain sound on this larger domain,
  and the extra values do not permit a false conclusion about real strings.

The 22 explicit fixed opaque/no-evaluator symbols are:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`.
They are all listed with locations in the inventory and none is reachable.
The LLVM compiler also warned about non-exhaustive declared-total helpers
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none is on
the proof path. There is no proof-local opaque or trusted primitive.

### Empirical evidence and exclusions

The 4,082-case differential supports generated-program equivalence to the
literal prompt oracle only on those recorded inputs; it is not the K proof.
The 20-case `krun` execution supports the concrete MPY/Python bridge on recorded
ASCII branches; it is not a universal connection theorem. The ground witnesses
and mutations demonstrate satisfiability and result/body sensitivity.

Not established:

- equivalence to `canonical.py` (affirmatively false on recorded witnesses);
- acceptance of variable-width, whitespace-padded, signed, or Unicode-decimal
  components;
- leap-year or year-range validation not requested by the prompt;
- non-string Python arguments or behavior outside the supplied MPY subset;
- preservation of an exact final module-scope map.

### Final decision

Gate A passes: clean reconstruction closes, the real body executes, proof-local
equations are sound, the result is exact, and both body and postcondition
mutations are rejected. The proof is therefore **LEGIT**.

An unqualified pass is withheld because the trusted canonical differs
materially on the string domain, including valid fixed-format day-30/day-31
inputs. The generated program and theorem instead match the literal prompt.
This is an intent/reference adequacy concern, not a proof-theory unsoundness.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
