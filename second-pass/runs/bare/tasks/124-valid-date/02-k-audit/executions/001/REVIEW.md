# Independent adversarial audit: 124-valid-date

## Executive finding

The candidate does not contain a proof of `valid_date` over its intended string
input domain. A clean reconstruction does establish all 47 submitted claims,
but those claims are only 33 fixed test vectors and 14 direct facts about the
task-specific helper `validMonthDay`. There is no quantified entry claim
connecting execution of `solutionProgram` to `validDateSpec`, or to any other
result specification, for an arbitrary input string. A fresh audit claim stating
that missing theorem gets stuck rather than producing `#Top`.

There is also a material generated-semantics error. Python `str.isdigit()` is
not ASCII-only, while `semantic.k` defines it by membership in
`"0123456789"`. On the satisfying input `"٠٣-١١-٢٠٠٠"`, the real submitted
Python function returns `True`, while the freshly rebuilt K semantics returns
`false`. On `"⁰3-11-2000"`, the Python function raises `ValueError` after
`isdigit()` succeeds, while K returns `false`; the K configuration has no
exception behavior. These are concrete false-conclusion witnesses on the
formal `String`/Python-string domain, not merely missing support for an unused
language construct.

The fresh false-result mutation behaves discriminatingly for one submitted
ground claim, but that cannot turn finite examples into a universal
partial-correctness theorem.

## Evidence and audit isolation

All source builds used regular-file copies in `/tmp/audit-work/candidate-src`.
Candidate-provided `semantic-kompiled/` and `verification-kompiled/` were never
used. Reviewer-authored scripts, derived specs, complete test inputs/results,
and bounded command logs are under `/audit-output/evidence`.

The toolchain was K v7.1.293:
[00_toolchain.log](/audit-output/evidence/00_toolchain.log).

## Stage 1 — Input and provenance integrity

### Trusted-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required condition holds:
`/reference/reference-semantics` is absent. No hidden or inferred reference
semantics was used. This is not an infrastructure breach.

### Artifact and type checks

The required source artifacts are present as regular, non-symlink files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
`prove.sh`, `prompt.py`, and `py2mpy.py`. The requested untrusted provenance
files are also present: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and one JSONL structured trace. No required artifact is
missing, mistyped, changed into a symlink, or accompanied by an unexpected
candidate helper K source file.

The candidate also contains untrusted compiled definitions and caches. Those
are additional generated outputs, not trusted source or integrity baselines;
they were inventoried and ignored. The complete file/type inventory and the
mode-boundary check are in
[01_provenance_integrity.log](/audit-output/evidence/01_provenance_integrity.log).

The candidate prompt is byte-identical to `/reference/prompt.py`, SHA-256
`71bb688daf8e872a52f7dfb4d4a09c07db640afd5fc1f8845baa1470a2930b78`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Untrusted generation claims

`run-input.json` claims problem `124-valid-date`, condition `bare`, and hashes
that agree with the independently computed prompt/translator hashes.
`metrics.json` claims an untimed-out exit 0. `codex-last.txt` and the final log
claim a successful `#Top`.

The structured trace is especially revealing but was not trusted as proof: it
records a failed universal program-versus-`validDateSpec` attempt, after which
the submitted ground/helper claim set was proved. The audit independently
reproduced both the submitted `#Top` results and the missing universal claim's
failure. Extracted claims and trace-type inventory are in
[01_generation_claims.log](/audit-output/evidence/01_generation_claims.log).

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Contract restatement

From the trusted prompt, a valid input is a nonempty date in `mm-dd-yyyy`
format: two month positions, two day positions, four year positions, hyphens
at positions 2 and 5, month in 1 through 12, day in 1 through 29 for February,
1 through 30 for April/June/September/November, and 1 through 31 otherwise.
The prompt does not impose leap-year arithmetic or a numerical year range.

The trusted canonical function has materially different executable behavior:
it strips surrounding whitespace, splits on `-`, converts three variable-width
fields with `int`, and does not enforce field widths. Because each source
condition is written without parentheses, Python precedence makes the final
`or day > 29` reject day 30 or 31 for every month, not only February.

The candidate implements the prompt's fixed-width shape more directly:

1. require length 10;
2. require hyphens at offsets 2 and 5;
3. slice month/day/year fields;
4. call Python `isdigit()` on all three;
5. convert month/day with `int`;
6. apply the stated month-specific caps.

This matches a strict ASCII reading of the natural-language examples, but it
is not total over Python strings: `isdigit()` accepts some characters that
`int()` does not, so `"⁰3-11-2000"` raises rather than returning a Boolean.
It also accepts non-ASCII decimal digits such as the Arabic-Indic input above.

### Translator fidelity

Regeneration with the trusted translator produced SHA-256
`fb4a7d0caadab15af3f85da978c9739d8db1e71ec10e5efe2ab9d84d3b8d1b8a`,
identical byte-for-byte to submitted `solution.mpy`. See
[02_translator_identity.log](/audit-output/evidence/02_translator_identity.log)
and the preserved
[regenerated-solution.mpy](/audit-output/evidence/regenerated-solution.mpy).

### Independent differential

The reviewer differential imports `/reference/canonical.py` and the scratch
copy of generated `solution.py`; it does not reuse K equations. It ran:

- all five documented examples;
- empty, length 9/10/11, separator, and non-digit cases;
- every month 0 through 13 and day 0 through 32 for years 0000, 2000, and 9999;
- Unicode and exception-sensitive cases;
- 1,000 deterministic malformed strings (seed 124).

There were 2,276 distinct inputs and 64 candidate/canonical result
divergences. Material examples include:

| Input | Candidate | Canonical | Reason |
|---|---:|---:|---|
| `"04-30-2020"` | `True` | `False` | canonical precedence rejects all days above 29 |
| `"01-31-0000"` | `True` | `False` | same precedence behavior |
| `"03-11-200"` | `False` | `True` | candidate enforces four year positions |
| `" 03-11-2000 "` | `False` | `True` | canonical strips whitespace |
| `"⁰3-11-2000"` | `ValueError` | `False` | candidate's `isdigit`/`int` mismatch |

The candidate differed from the reviewer's strict-ASCII contract on two
inputs: it accepted Arabic-Indic digits and raised for the superscript case.
The test exits 1 because the required canonical differential is nonzero.
Artifacts:

- [differential_test.py](/audit-output/evidence/differential_test.py)
- [02_differential.log](/audit-output/evidence/02_differential.log)
- [differential_inputs.json](/audit-output/evidence/differential_inputs.json)
- [differential_results.json](/audit-output/evidence/differential_results.json)

The prompt/canonical conflict does not by itself decide proof soundness, but it
is a material intent bridge that any successful report would have to disclose.

## Stage 3 — Clean proof reconstruction

### Fresh builds

Fresh Haskell definitions were built only from the scratch source copy:

```text
kompile semantic.k --main-module MPY --syntax-module MPY --backend haskell \
  --output-definition /tmp/audit-work/semantic-audit-kompiled

kompile verification.k --main-module VERIFICATION --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition /tmp/audit-work/verification-audit-kompiled
```

Both exited 0. Logs:
[03_kompile_semantic.log](/audit-output/evidence/03_kompile_semantic.log) and
[03_kompile_verification.log](/audit-output/evidence/03_kompile_verification.log).

### Every submitted positive claim

The reviewer split all 47 submitted claims, without changing their bodies, into
one-claim spec modules and invoked `kprove` separately for each. All 47 exited
0 and printed an exact `#Top`.

The splitter records each original line span and body hash in
[positive_claims/manifest.json](/audit-output/evidence/positive_claims/manifest.json).
The aggregate result is in
[03_positive_claim_summary.log](/audit-output/evidence/03_positive_claim_summary.log);
the 47 exact commands and outputs are preserved as
`/audit-output/evidence/positive_claims/run-001.log` through
`run-047.log`. The reviewer scripts are
[split_positive_claims.py](/audit-output/evidence/split_positive_claims.py) and
[run_positive_claims.sh](/audit-output/evidence/run_positive_claims.sh).

Thus the candidate's narrow positive claims really close; the verdict does not
question that execution fact.

### Fresh concrete generated-semantics execution

Seventeen normal and boundary inputs were executed with `krun` against the
fresh definition and compared with independent Python execution. Fifteen
matched. Two did not:

| Input | Fresh K | Real candidate Python |
|---|---:|---|
| `"٠٣-١١-٢٠٠٠"` | `false` | `True` |
| `"⁰3-11-2000"` | `false` | raises `ValueError` |

Every K command, output, exit status, and Python result is in
[semantics_differential_results.json](/audit-output/evidence/semantics_differential_results.json);
the bounded summary is
[03_semantics_differential.log](/audit-output/evidence/03_semantics_differential.log)
and the driver is
[semantics_differential.py](/audit-output/evidence/semantics_differential.py).

## Stage 4 — Adequacy and real-program pinning

### What each submitted entry claim says

Claims 1–33 have no `requires` clause. Each precondition is simply the exact
displayed starting `<k>` configuration, and each postcondition is the listed
ground Boolean:

| Source lines | Plain-language precondition and postcondition |
|---|---|
| 7–16 | For exactly `"03-11-2000"`, `"15-01-2012"`, `"04-0-2040"`, `"06-04-2020"`, and `"06/04/2020"`, return respectively `true,false,false,true,false`. |
| 19–30 | For exactly `""`, `"03-11-200"`, `"003-11-2000"`, `"aa-bb-cccc"`, `"03-1a-2000"`, and `"03-11-20x0"`, return `false`. |
| 33–38 | For exactly `"00-01-2020"`, `"13-01-2020"`, and `"12-00-2020"`, return `false`. |
| 42–47 | For exactly `"02-01-2020"`, `"02-29-1900"`, and `"02-30-2020"`, return respectively `true,true,false`. |
| 50–65 | For each of months 04, 06, 09, and 11, day 30 returns `true` and day 31 returns `false` for the exact listed 2020 strings. |
| 68–83 | The exact day-31 strings for months 01, 03, 05, 07, 08, 10, and 12 return `true`; exact `"01-32-2020"` returns `false`. |

Every one of these preconditions is satisfiable: the exact ground
configuration displayed by the claim is a witness. The independently evaluated
results show zero mismatches against generated Python and 13 mismatches against
the trusted canonical implementation:
[04_entry_claims.log](/audit-output/evidence/04_entry_claims.log) and
[entry_claim_results.json](/audit-output/evidence/entry_claim_results.json).

Claims 34–47 do not invoke the program:

| Claims | Plain-language precondition and postcondition |
|---|---|
| 34 | For arbitrary integer `D`, `validMonthDay(2,D)` equals `1 <= D <= 29`. |
| 35–38 | For arbitrary `D` and fixed month 4, 6, 9, or 11, the helper equals `1 <= D <= 30`. |
| 39–45 | For arbitrary `D` and fixed month 1, 3, 5, 7, 8, 10, or 12, the helper equals `1 <= D <= 31`. |
| 46 | If `M < 1 or M > 12`, the helper is `false` for arbitrary day. |
| 47 | If `1 <= M <= 12 and D < 1`, the helper is `false`. |

Satisfying witnesses are `D=1` for every fixed-month claim, `M=0,D=1`
for claim 46, and `M=1,D=0` for claim 47. Concrete substitutions correspond,
for example, to `"02-29-2020"`, `"04-30-2020"`, `"01-31-2020"`,
`"00-01-2020"`, and `"01-00-2020"`. Generated Python agrees with those helper
formulas. Canonical Python disagrees on day 30/31 due to its precedence
behavior.

### Program identity

The `<k>` terms use a duplicated function constant, `solutionProgram`, rather
than loading `solution.mpy` at proof time. The audit therefore checked the
external pin explicitly:

1. trusted translator output is byte-identical to submitted `solution.mpy`;
2. the regenerated program and the extracted `solutionProgram` RHS were each
   parsed as sort `Program`;
3. their emitted KORE files are byte-identical, both SHA-256
   `d2787b4cebddfbdc3524361ba4f65fa62f895b8dec5278fca964ed4bc1f6482d`.

See
[04_program_kast_identity.log](/audit-output/evidence/04_program_kast_identity.log),
[extract_solution_program.py](/audit-output/evidence/extract_solution_program.py),
and [solutionProgram_rhs.mpy](/audit-output/evidence/solutionProgram_rhs.mpy).
An earlier direct rewrite-spec embedding was rejected by the concrete parser
because internal `.Stmts` units are not concrete-program tokens; that parser
error in `04_program_identity.log` is not used as evidence.

The snapshot is therefore the actual submitted program tree, although the K
claim itself relies on the duplicated constant plus this external identity
check.

### Missing target theorem

`validDateSpec` is never mentioned in any claim. No claim has a symbolic
`S:String` entry state, and no collection of fixed examples proves all strings.
The 14 helper claims match no actual control-flow head and establish no
connection between `validMonthDay` and the executed program.

The audit stated the missing natural entry theorem directly:

```k
claim <k> runProgram(solutionProgram, "valid_date", vals(strVal(S:String)))
        => boolVal(validDateSpec(S)) </k>
```

This well-formed claim reached real symbolic execution and failed with
`WarnStuckClaimState`, exit 1. It did not time out or fail to parse. See
[universal_target.k](/audit-output/evidence/universal_target.k) and
[04_missing_universal.log](/audit-output/evidence/04_missing_universal.log).

The ground entry claims constrain their individual returns and are not
tautologies or free-variable postconditions. The adequacy defect is that no
result-constraining theorem exists for an arbitrary admissible input.

## Stage 5 — Rule-by-rule static soundness review

### Complete declaration inventory

There are no generated helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`. The local syntax/configuration declarations
are:

| File:line | Declaration and role | Assessment |
|---|---|---|
| `semantic.k:9` | `Program ::= Module(Stmts)` | Exact submitted top-level constructor. |
| `semantic.k:10` | `Stmts ::= List{Stmt,""}` | Ordered statement sequence; covers the target. |
| `semantic.k:12–15` | `Stmt`: `FuncDef`, `Return`, `Assign`, `If` | Exactly the statement constructors used; nested `FuncDef` is syntactically broader but unused. |
| `semantic.k:17–30` | literals, names, unary/Boolean ops, compare, two subscript forms, attribute, zero/one-argument calls | Covers every submitted expression constructor and arity. |
| `semantic.k:32` | `CmpOp(String,Expr)` | Covers every submitted single comparison. |
| `semantic.k:33` | positive-bounds `Slice(...,NoBound)` | Covers all three submitted slices. |
| `semantic.k:42` | `Val`: integer, Boolean, string | Covers target values but has no `None` or exception value. |
| `semantic.k:43` | one-argument `vals(Val)` | Matches the target function. |
| `semantic.k:45` | persistent `Env`: empty/bind | Sufficient for local variables and shadowing. |
| `semantic.k:46` | `ExecResult`: normal/returned | Models normal and return control, but no exception. |
| `semantic.k:48` | `runProgram(Program,String,Vals)` | Audit entry command. |
| `semantic.k:49` | configuration containing only `<k>` | Locals are term-threaded; no heap/I/O is needed, but exceptions are absent. |
| `semantic.k:59` | function `finish` | Converts execution result to final value. |
| `semantic.k:63` | function `exec` | Statement evaluator. |
| `semantic.k:71` | function `branch` | Boolean branch selector. |
| `semantic.k:75` | function `resume` | Propagates returns or resumes a suffix. |
| `semantic.k:79` | function `lookup` | Environment lookup. |
| `semantic.k:84` | function `eval` | Expression evaluator. |
| `semantic.k:120` | function `asBool` | Boolean-only projection. |
| `semantic.k:123` | function `pyNot` | Boolean negation. |
| `semantic.k:126` | function `compare` | Typed comparison primitive. |
| `semantic.k:136` | function `pyLen` | String length bridge. |
| `semantic.k:139` | function `pyIndex` | String index bridge. |
| `semantic.k:142` | function `pySlice` | String slice bridge. |
| `semantic.k:145` | function `pyInt` | String-to-integer bridge. |
| `semantic.k:149` | function `pyIsDigit` | Intended Python-method bridge; materially incorrect. |
| `semantic.k:152` | function `isDigits` | ASCII digit-string helper. |
| `semantic.k:156` | function `isDigitsAt` | Recursive character scan. |
| `semantic.k:163` | function `isDigitChar` | ASCII substring-membership test. |
| `verification.k:9` | function constant `solutionProgram` | Exact parsed snapshot of submitted program. |
| `verification.k:74` | function `validDateSpec` | Task-specific strict-format predicate; unused by claims. |
| `verification.k:78` | function `specLength` | Predicate stage after length test. |
| `verification.k:86` | function `specSeparators` | Predicate stage after separator test. |
| `verification.k:95` | function `specDigits` | Predicate stage after ASCII digit test. |
| `verification.k:102` | function `validMonthDay` | Mathematical month/day predicate. |
| `verification.k:111` | function `isThirtyDayMonth` | Mathematical month-set predicate. |

All 24 marked attributes are `[function]`. There are no local `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, or
`anywhere` declarations; no opaque symbols; and no proof-local ordinary
operational rewrite. The exact declaration/rule scan is
[05_rule_inventory.log](/audit-output/evidence/05_rule_inventory.log).

### Construct-to-semantics map

The submitted term uses `Module`, `FuncDef`, `If`, `Assign`, `Return`,
`Int`, `Bool`, `Str`, `Name`, `UnaryOp`, Boolean operations of arity 2/3/4,
`Compare/CmpOp`, integer and slice `Subscript`, `Attribute`, and calls to
`len`, `int`, and `isdigit`. Counts and operators are preserved in
[05_construct_map.log](/audit-output/evidence/05_construct_map.log).

Every used constructor has a declaration. Operational coverage is:

- module/function call: rule 53;
- sequence, return, assignment, and if: rules 64–77;
- locals: rules 80–82;
- every used expression and call: rules 85–150;
- digit recursion: rules 153–164.

There are no loops, allocation, mutation outside local bindings, nested calls,
I/O, or heap effects in `solution.mpy`.

### Exhaustive semantic-rule inventory and decision

The following table accounts for all 50 candidate-authored rules in
`semantic.k`.

| Line | Rule | Decision |
|---:|---|---|
| 53 | `runProgram(Module(FuncDef(F,Params(P),BODY)),F,vals(V))` executes `BODY` with `P↦V` | Sound for the exact one-function/one-argument command. Repeated `F` pins the selected binding; no body is skipped. |
| 60 | `finish(returned(V)) => V` | Sound return extraction. |
| 61 | `finish(normal(_)) => false` | Not Python-general: fallthrough returns `None`. The submitted function has a return on every non-exception path, so no actual date-string path reaches this rule. This is an unused-language fidelity gap, not relied-on false target behavior. |
| 64 | empty statement list becomes `normal(ENV)` | Sound sequence base. |
| 65 | `Return(E)` evaluates `E`, discards suffix, returns | Sound control transfer for target pure expressions. |
| 66 | assignment evaluates RHS in old environment, then shadows binding | Sound for all five target name assignments. |
| 68 | `If` evaluates condition and passes branches/suffix to `branch` | Sound for target Boolean conditions. |
| 72 | true branch executes THEN then resumes suffix | Sound. |
| 73 | false branch executes ELSE then resumes suffix | Sound. |
| 76 | `resume(returned(V),_)` propagates return | Sound abrupt control. |
| 77 | `resume(normal(ENV),REST)` executes suffix | Sound normal control. |
| 80 | newest equal-name binding wins | Sound Python-local shadowing behavior. |
| 81 | unequal-name binding is skipped | Guard is complementary to line 80; sound. Empty lookup is intentionally undefined and unreachable in the target. |
| 85 | integer literal evaluation | Sound. |
| 86 | Boolean literal evaluation | Sound. |
| 87 | string literal evaluation | Sound. |
| 88 | name evaluation by environment lookup | Sound for all bound target names. |
| 90 | unary `"not"` via Boolean `pyNot` | Sound on the target, whose operand is Boolean. General Python truthiness is outside this subset. |
| 92 | two-operand `"and"` | Eager and Boolean-coercing, unlike general Python short-circuit/value semantics. Both target operands are pure Booleans, so no false target result witness exists. |
| 94 | three-operand `"and"` | Same target-sound restriction; used by the three pure `isdigit` results. |
| 97 | four-operand `"and"` | Declared but not used by the submitted term. Same restricted semantics. |
| 100 | two-operand `"or"` | Eager/Boolean-only, but target operands are pure comparisons; target result is preserved. |
| 102 | three-operand `"or"` | Declared but unused; restricted as above. |
| 105 | four-operand `"or"` | Target uses it for four pure month comparisons; result is preserved. |
| 109 | compare evaluates both pure operands then dispatches | Sound for target comparisons; no side-effect order issue. |
| 112 | integer string index via one-character substring | Sound for indices 2 and 5 after the exact-length guard. Negative/out-of-bounds exceptions are unmodeled but unreachable here. |
| 113 | positive string slice via `substrString` | Sound for target slices `[0:2]`, `[3:5]`, `[6:10]` after length 10. |
| 116 | `len` dispatch to `pyLen` | Sound for the string argument. |
| 117 | `int` dispatch to `pyInt` | Sound only for reachable K-side ASCII digit fields. Python exception behavior is absent and becomes material with the real `isdigit` domain. |
| 118 | `.isdigit()` dispatch to `pyIsDigit` | Materially unsound as a model of the used Python method; it routes to an ASCII-only predicate. Witness below. |
| 121 | Boolean projection | Sound on target Boolean operands. |
| 124 | Boolean negation | Sound. |
| 127 | integer `==` | Sound. |
| 128 | integer `!=` | Sound. |
| 129 | integer `<` | Sound. |
| 130 | integer `<=` | Sound. |
| 131 | integer `>` | Sound. |
| 132 | integer `>=` | Sound. |
| 133 | string `==` | Sound for target separator comparison capability, though target uses `!=`. |
| 134 | string `!=` | Sound for target separator comparisons. |
| 137 | string length through K `lengthString` | Acceptable primitive bridge; concrete Unicode length behavior agreed on tested inputs. |
| 140 | safe index through K `substrString` | Sound on the two guarded target indices. |
| 143 | safe positive slice through K `substrString` | Sound on the three guarded target slices. |
| 146 | `String2Int` | Sound for nonempty ASCII decimal fields reached in K. It is unguarded and has no Python exception result outside that path. |
| 150 | `pyIsDigit(strVal(S)) => boolVal(isDigits(S))` | Materially unsound for the used Python operation because `isDigits` is ASCII-only. |
| 153 | empty `isDigits` is false | Agrees with Python. Guard is disjoint from line 154. |
| 154 | nonempty `isDigits` starts recursive ASCII scan | As a Python bridge, materially unsound for non-ASCII digit characters. |
| 157 | scan at/past length is true | Sound for scans begun at 0 and incremented by 1. |
| 158 | scan checks current character and recursively increments | Terminating and sound for an ASCII-only predicate, but contributes to the false Python bridge. |
| 164 | character is found in `"0123456789"` | Exactly ASCII membership, not Python `isdigit`; materially unsound for the used method. |

#### Required false-conclusion witness

For `"٠٣-١١-٢٠٠٠"`, each Python field's `isdigit()` is `True`, both `int`
conversions succeed, and the real function returns `True`. Rules 118, 150, 154,
158, and 164 make the first Arabic-Indic character fail ASCII membership, so K
takes the false return and concludes `boolVal(false)`. This false conclusion
was reproduced by fresh `krun` with exit 0 in
[03_semantics_differential.log](/audit-output/evidence/03_semantics_differential.log).

For `"⁰3-11-2000"`, Python `month_text.isdigit()` is `True` but
`int("⁰3")` raises `ValueError`; K again rejects at the ASCII predicate and
concludes `false`. This witnesses both the incorrect operation domain and the
material absence of exception behavior.

The broader eager Boolean rules, general out-of-bounds behavior, unbound-name
behavior, and `finish(normal)` are narrower subset/reuse gaps. No false result
for the actual submitted program over an otherwise corresponding target path
was found for those rules, so they are not labeled as additional material
unsoundnesses.

### Exhaustive verification-rule inventory and decision

All 10 rules in `verification.k` are accounted for:

| Line | Rule | Decision |
|---:|---|---|
| 10 | `solutionProgram` expands to the constructor tree | Truthful definitional constant; parser-level identity to regenerated submission is established. |
| 75 | `validDateSpec(S)` starts with length 10 | Truthful for the chosen strict-format predicate, but not connected to execution. |
| 79 | failed length stage returns false | Truthful and disjoint from line 80. |
| 80 | successful length stage checks the two separators | Truthful. |
| 87 | failed separator stage returns false | Truthful and disjoint from line 88. |
| 88 | successful separator stage checks three digit fields | Truthful for its imported ASCII `isDigits`, not full Python `isdigit`. |
| 96 | failed digit stage returns false | Truthful and disjoint from line 97. |
| 97 | successful digit stage parses month/day and calls `validMonthDay` | Truthful on ASCII digit fields. |
| 103 | `validMonthDay` Boolean formula | Mathematically correct for all integer months/days under the prompt's caps. |
| 112 | exact 30-day-month disjunction | Mathematically correct. |

`validDateSpec` and its staged helpers are definitional summaries, not
operational bridges. They encode a plausible task predicate, but because no
entry claim mentions `validDateSpec`, they contribute no program-correctness
conclusion. The helper claims merely restate line 103 after function
simplification; many were reported by K as proven without rewriting.

### Overlap, coverage, state, and control summary

- The guarded `lookup`, `isDigits`, and `isDigitsAt` rule pairs are disjoint
  and cover their target call domains.
- Boolean-stage rules in `verification.k` are disjoint and exhaustive.
- Comparison operations/types used by the target are covered without overlap.
- Recursive digit scanning increments the index and terminates.
- Locals are threaded in `Env`; return correctly discards the remaining
  sequence. There is no allocation, external state, or I/O in the target.
- The missing exception state is material because the submitted Python
  function can raise on a string satisfying `isdigit()`.
- There are no priorities, simplification rules, opaque result oracles, or
  proof rewrites that bypass execution. The failure is instead a weak theorem
  plus an incorrect generated-semantics bridge.

## Stage 6 — Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. The audit created a fresh mutation
of submitted claim 1:

```k
claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-2000")))
        => boolVal(false) </k>
```

The exact start state is satisfiable. Both Python implementations return
`True` for this input:
[06_mutation_witness.log](/audit-output/evidence/06_mutation_witness.log).

The mutated spec dry-built successfully with exit 0:
[06_mutation_build.log](/audit-output/evidence/06_mutation_build.log).
The actual proof exited 1 with `WarnStuckClaimState` and the expected residual
`<k> boolVal(true) ~> .K </k>` unable to unify with `boolVal(false)`:
[06_mutation_proof.log](/audit-output/evidence/06_mutation_proof.log).
The mutation source is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k).

This demonstrates that the ground execution claim is result-constraining and
non-vacuous. It does not test or supply the absent universal theorem.

## Stage 7 — Proven versus assumed accounting

### Precisely proven

Conditional on the submitted K definition:

1. the exact hard-coded program returns the asserted Boolean on each of 33
   listed ground inputs; and
2. the pure `validMonthDay` helper simplifies to the listed cap formula for 12
   fixed valid months, all invalid months, and sub-one days.

That is the full machine-checked result. It does not establish
`runProgram(solutionProgram,...S) = validDateSpec(S)` for arbitrary `S`, does
not establish equivalence to the trusted canonical implementation, and does
not establish that the K semantics matches Python on all strings.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K parser/compiler/Haskell backend and imported `INT`, `BOOL`, `STRING` primitives | Every K execution/proof | Ordinary toolchain trust boundary; exact version and commands are recorded. |
| Trusted `py2mpy.py` | Program-tree bridge | Acceptable and checked by byte identity. |
| Duplicated `solutionProgram` constant | All 33 entry claims | Current snapshot is acceptably pinned by byte identity plus byte-identical parsed KORE; the proof itself does not load the file. |
| `lengthString`, `substrString`, `String2Int`, `findString` as Python-operation bridges | Every ground program claim | Informally justified/generated semantics, not universally proved against Python. Safe ASCII paths have finite concrete support only. |
| ASCII `isDigits` as Python `str.isdigit` | Digit branch and final result | Illegitimate on the stated string domain; two concrete opposite-behavior witnesses exist. |
| Absence of Python exceptions | Termination/result behavior | Illegitimate for `"⁰3-11-2000"`; real program raises while K returns false. |
| `validDateSpec` as natural-language interpretation | Would be the desired theorem | Plausible strict-ASCII predicate, but unused by every submitted claim and not connected to execution. |
| Trusted canonical implementation | Program-fidelity comparison | Independent executable oracle, but it conflicts materially with the prose because of precedence and width behavior. Candidate/canonical differential has 64 mismatches. |
| Differential testing | Only tested bridges/inputs | Finite evidence, never a substitute for a K reachability theorem; it also contains observed failures. |

There are no opaque symbols. The task-specific `validMonthDay` formula is fully
defined rather than unconstrained, but proving facts about that formula is not
proof that program control flow computes it.

### Decision

Clean reconstruction confirms a genuine `#Top` for every submitted claim and a
genuine failure of a false ground mutation. Nevertheless, the candidate omits
the target universal entry claim and therefore supplies tests plus helper
algebra rather than a partial-correctness proof of the function. The generated
semantics additionally makes false observable conclusions for real executions
on admissible Python strings. These are material adequacy and soundness
failures, not infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
