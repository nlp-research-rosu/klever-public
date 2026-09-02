# Independent adversarial review: 113-odd-count

The candidate's commands are reproducible and all four submitted claims close,
but the resulting theory does not prove the HumanEval result. The decisive
defects are a result-bearing opaque `decimalCodes` symbol shared circularly by
execution and the postcondition, and an outer-loop operational bridge that
directly installs the desired fold without an independent connection proof.

## 1. Input and provenance integrity

The audit infrastructure is intact.

- `/audit-input.json` is a real regular file with SHA-256
  `bc5498dfb28fa995d970874c50bbd46accbea69e3a2c954aa17bd72735f174b8`.
  It declares `record_layout = legacy-selected-stage1` and
  `semantics_mode = SUPPLIED_SEMANTICS`.
- `/audit-campaign-lock.json` has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
  its parsed JSON is exactly equal to the `audit_campaign` block in
  `/audit-input.json`.
- I read and independently hashed `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, the legacy records that
  were present, and the complete structured trace. Every direct hash recorded
  in the launcher manifest and both generation evidence maps matches the
  mounted file. The one JSONL trace has 641 valid records. The raw generation
  transcript has 75,802 lines and the recorded SHA-256
  `1df549eaae2478f2af5d9f63d09297955762f36ff46565d2c3bf181714bfb210`.
  Historical `runtime-metrics.json` is not required for this legacy layout.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is present, as SUPPLIED_SEMANTICS requires.
  The candidate and trusted semantics contain the same 25 entries. Entry type,
  relative path, and every regular-file digest agree; neither tree contains a
  symlink or extra entry. Their independent per-entry manifest digest is
  `51c71872287731bc1458ed960ef68fb8126adae2af5e488b22b5549c1a8e69ec`.
  This exact recursive comparison is independent of the launcher's tree-hash
  serialization.
- The complete candidate tree was also scanned without following links. It has
  36 entries and no linked or unsupported node. Every candidate file digest is
  recorded in the integrity log.

The generation record's `KPROVE_PASSED` marker and prior `#Top` outputs were
treated only as untrusted claims. Reproducible evidence is in
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py),
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log),
[trace_inventory.log](/audit-output/evidence/trace_inventory.log), and
[generation_log_scan.log](/audit-output/evidence/generation_log_scan.log).

## 2. Program fidelity and candidate-versus-canonical checks

The source contract is: for every string in a list of digit-only strings,
count its odd digits and return a sentence in which that count replaces each
of the four `i` positions. Empty lists and empty strings are valid; the prompt
states no size bound.

`solution.py` implements that contract with nested loops. For each character it
adds `int(digit) % 2`, then constructs the exact required sentence and appends
it. This is a different implementation from the generator expression in the
canonical program, but no semantic discrepancy was found.

Trusted regeneration was checked with:

```text
python3 reference/py2mpy.py solution.py | cmp - solution.mpy
```

It exited 0, establishing byte identity with submitted `solution.mpy`; see
[solution_mpy_identity.log](/audit-output/evidence/solution_mpy_identity.log).

The independent differential script imports the trusted canonical and
candidate entry points separately. It covers both documented examples, empty
outer and inner collections, each decimal digit and parity branch, all 100
two-digit strings, count transitions at 9/10/11, a 1,000-character string, and
1,000 deterministic generated list cases (seed 113). All 1,127 cases matched
and neither implementation mutated its input. See
[differential_test.py](/audit-output/evidence/differential_test.py) and
[differential_test.log](/audit-output/evidence/differential_test.log). This is
finite implementation evidence, not a universal K proof.

## 3. Clean proof reconstruction

Only candidate source files and the trusted supplied-semantics source tree were
copied to `/tmp/audit-work/rebuild`. Candidate archives, compiled definitions,
and caches were not copied or reused. The observed tools are K 7.1.293 and
Python 3.10.12; see [toolchain.log](/audit-output/evidence/toolchain.log).

The independent concrete reconstruction used:

```text
python3 reference/py2mpy.py concrete_audit.py > concrete_audit.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_audit.mpy --definition runtime-kompiled --output none
```

All commands exited 0. The K program includes empty input/string, even and odd
digits, both prompt examples, and the two-digit result count 10. Sources and
logs are [concrete_audit.py](/audit-output/evidence/concrete_audit.py),
[kompile-runtime.log](/audit-output/evidence/kompile-runtime.log), and
[krun-concrete-audit.log](/audit-output/evidence/krun-concrete-audit.log).

The fresh proof definition was built with:

```text
kompile verification.k --backend haskell \
  --main-module ODD-COUNT-VERIFICATION \
  --syntax-module ODD-COUNT-VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0; see
[kompile-verification.log](/audit-output/evidence/kompile-verification.log).
Each positive claim was then run separately:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC --claims digit-loop
kprove spec.k --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC --claims outer-empty
kprove spec.k --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC --claims outer-loop
kprove spec.k --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC --claims target
```

Each exited 0 and printed `#Top`; the corresponding logs are
[digit-loop](/audit-output/evidence/kprove-digit-loop.log),
[outer-empty](/audit-output/evidence/kprove-outer-empty.log),
[outer-loop](/audit-output/evidence/kprove-outer-loop.log), and
[target](/audit-output/evidence/kprove-target.log). A combined unfiltered run
also exited 0 with `#Top`; see
[kprove-all.log](/audit-output/evidence/kprove-all.log).

Thus the reconstruction gate succeeds: these claims verify under the submitted
extended theory. The later stages show why that theory is not a legitimate
proof theory for the requested result.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

- `digit-loop`: for any ASCII digit-code sequence `CS`, executing the real
  inner loop from count `N` consumes the loop, changes count to
  `oddDigitsFrom(N, CS)`, and leaves the loop variable equal to its last
  character (or its old value for the empty sequence).
- `outer-empty`: an outer loop over an empty list consumes no body iterations,
  preserves the neutral locals, and leaves the result accumulator unchanged.
- `outer-loop`: from the candidate's neutral-local loop head and a nonempty
  digit-string list, consume the complete remaining outer loop and replace the
  result accumulator by `oddCountFrom(ACC, INPUT)`.
- `target`: load the `odd_count` binding, call it on an arbitrary `ValSeq`
  satisfying `validDigitStrings`, return heap reference 0, and place
  `list(oddCountSpec(INPUT))` at heap location 0 with the specified final
  control cells.

The precondition is not bounded: it recursively covers arbitrary finite lists
of arbitrary finite ASCII digit strings, including both empty cases. A
satisfying witness is `INPUT = ["3"]`, encoded as
`list(vCons(str(iCons(51, .IntSeq)), .ValSeq))`. Both Python implementations
return:

```text
["the number of odd elements 1n the str1ng 1 of the 1nput."]
```

See [concrete_claim_witness.log](/audit-output/evidence/concrete_claim_witness.log).

### Program identity

The target does not execute a substituted body. I parsed trusted-regenerated
`solution.mpy` and `ODD-COUNT-PROGRAM` with the fresh definition, expanded all
macros, emitted KORE, and compared the results. Both files have SHA-256
`4a34a58a8e7d19c4b544030f424325af31c054c17538c65418ecc9c365bc8e25`
and are byte-identical. See
[constructor_hashes.log](/audit-output/evidence/constructor_hashes.log) and
[constructor-program-identity.log](/audit-output/evidence/constructor-program-identity.log).

### Result inadequacy

For the concrete witness `["3"]`, the formal postcondition reduces only to a
one-element list containing an `oddText(1)` whose four numeric fields are
`decimalCodes(1)`. There is no equation or theorem reducing
`decimalCodes(1)` to code 49 (`"1"`); the only connection is the
reverse-oriented asserted simplification that replaces the fixed computation
by this symbol. A fresh ground claim asking for the actual intended string
builds but fails with `WarnStuckClaimState`; its residual explicitly requires
the missing equality between the concrete `"1"` codes and four occurrences of
`decimalCodes(1)`. See
[spec-ground-intended.k](/audit-output/evidence/spec-ground-intended.k) and
[kprove-ground-intended.log](/audit-output/evidence/kprove-ground-intended.log)
(exit 1).

The proof is also insensitive to a material change in the executed body. I
changed `int(digit) % 2` to `% 1` in both the trusted-translated program and the
macro term used by the claim. The mutated submitted-program term and mutated
claim term remain byte-identical, but their KORE hash changes to
`a08de516611f0c3fda8afdc9c41fdeba9d08afcf93539c4f7b6b5e0257881c71`.
On `["3"]`, real mutated Python returns the sentence containing `0`, while the
unchanged target summary still uses `% 2` through `oddDigits`. Nevertheless
the mutated target again exits 0 with `#Top`. See
[body_sensitivity_witness.log](/audit-output/evidence/body_sensitivity_witness.log),
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
and [kprove-body-mutated-target.log](/audit-output/evidence/kprove-body-mutated-target.log).
This sensitivity failure is caused by the outer-loop operational bridge
matching the shared body macro and installing its old result summary.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory contains one source-ranged row and a
disposition for every supplied/candidate K declaration, rule, context,
configuration, and claim. It enumerates 1,147 records: 727 rules, 243 syntax
declarations, 156 function-bearing declaration blocks, 116 total-bearing
blocks, zero `functional` declarations, 26 opaque-symbol declarations, 47
priority rules, one simplification rule, eight macro-bearing blocks, one
configuration, and four claims. The candidate verification module contributes
48 syntax/rule records. See
[k_source_inventory.tsv](/audit-output/evidence/k_source_inventory.tsv) and its
reproducible generator
[k_source_inventory.py](/audit-output/evidence/k_source_inventory.py).

All supplied-semantics rows are classified as the fixed selected baseline.
Exact tree identity was established in stage 1. The 25 supplied opaque symbols
belong to unused float, sorting, or MD5 facilities; none can influence this
program's branch, state, or result.

The constructs actually used by `solution.mpy` map to the following fixed
rules:

| Program construct | Fixed-semantics path |
|---|---|
| module/function/load | `core.k` `#loadAll` and statement sequencing; `functions.k` `FuncDef`; `call.k` closure dispatch/frame creation |
| list literal/result allocation | `list.k` `ListExpr`; `core.k` `#evalArgs` and `#alloc` |
| list/string iteration | `controls.k` `For`, `#loop`, and `#loopStep`; `list.k` and `str.k` `#iterNext`; `tuple.k` `#bindTgt` |
| assignment and `+=` | strict syntax plus `controls.k` `Assign` and `AugAssign` |
| `int(digit) % 2` | `call.k` builtin/type dispatch; `builtins.k` single-digit `int(str)`; `int.k` `applyBin("%",...)` and `pyMod` |
| string literals/concatenation/`str(count)` | `str.k` `Str`, `strToCodes`, `seqConcat`, string `applyBin`; `builtins.k` `str(int)` |
| `result.append(text)` | `call.k` attribute/bound-method routing; `list.k` in-place append heap update |
| return | `functions.k` return, frame pop, environment restoration |
| input-domain predicate | candidate recursion plus trusted `methods.k` `isDigitC`/`allDigit` |

This path has left-to-right strict argument evaluation, explicit scope/heap
allocation, loop control, call/return state, and the required append mutation.
The proof-local bridges preempt material portions of that path:

1. `oddDigits`, `oddDigitsFrom`, and `lastDigit`
   (`verification.k:7-18`) have disjoint constructor cases, total coverage on
   their declared algebraic domains, strict structural descent, and ordinary
   mathematical right-hand sides. They are acceptable definitional summaries.
2. `decimalCodes` (`verification.k:26-27`) is declared total, symbolic, and
   evaluator-free, with no equations whose left-hand side defines its values.
   The simplification
   `strToCodes(Int2String(N)) => decimalCodes(N)` at line 28 replaces a fixed,
   result-bearing computation by that unconstrained symbol. The final
   `oddText` and `oddCountSpec` use the same symbol, so their agreement with
   execution is circular rather than a value connection.
3. `oddText` and the `oddCountSpec`/`oddCountFrom` fold
   (`verification.k:30-69`) are structurally terminating and cover their
   algebraic arguments, but every output string depends on the illegitimate
   `decimalCodes` boundary.
4. The `outerDigits`, `outerCount`, `outerDigit`, `outerText`,
   `DigitStrings`, `asValues`, and `validDigitInput` equations are structurally
   sound but unused by the target. They cannot justify target closure.
5. `validDigitStrings` recursively covers both `ValSeq` constructors.
   `validDigitString` is sound for string constructors and uses trusted
   `allDigit`. `codesProj` is declared total over all `Val` but has an equation
   only for `str`; that is a totality/coverage gap outside the satisfying
   string branch, not a demonstrated false equation on the intended domain.
6. The four program macros at lines 119-125, 169-206, 245-255, and 256-262
   were mechanically checked against `solution.mpy` and are semantically inert
   naming expansions.
7. The inner `For` rule at lines 132-168 is an operational bridge. It consumes
   the entire loop under arbitrary continuation, reads `<env>`/`<scopes>`, and
   writes count and the loop variable while framing the remaining state. The
   independently closing `digit-loop` claim gives strong evidence for the same
   transformer after fixed `For => #loop` initialization. However, that claim
   still imports the module containing the proposed bridge; the candidate
   supplies no separate bridge-free definition and connection theorem. I found
   no concrete false transition for this exact guarded bridge, so I classify
   it as the narrower connection-evidence gap rather than asserting a separate
   false rule.
8. The `[priority(40)]` outer `#loop` rule at lines 210-244 is an operational
   bridge over arbitrary valid remaining lists and arbitrary continuation. It
   deletes all fixed body execution and directly writes
   `oddCountFrom(ACC, INPUT)` to the heap. The `outer-loop` claim imports this
   rule and states substantially the same transition, so it is circular and
   cannot be its connection theorem. Removing this bridge did not produce a
   bridge-free proof within a bounded 60-second diagnostic; that timeout is
   not used as a candidate defect. The decisive evidence is instead the
   constructor-level body-sensitivity failure described in stage 4.

### Required false-conclusion witness

The result-bearing abstraction has a concrete opposite-interpretation witness
on the intended domain. Because the candidate gives `decimalCodes` no
independently established or reducing definition, I tested the proof under the
ground proof-side interpretation
`decimalCodes(1) = iCons(57, .IntSeq)` (the code for `"9"`). I operationalized
only that interpretation in
[verification-opposite.k](/audit-output/evidence/verification-opposite.k).
For satisfying input `["3"]`,
[spec-opposite.k](/audit-output/evidence/spec-opposite.k) requires the false
sentence:

```text
the number of odd elements 9n the str9ng 9 of the 9nput.
```

The rebuilt opposite-interpretation definition and proof both exit 0, and the
proof prints `#Top`; see
[kompile-opposite.log](/audit-output/evidence/kompile-opposite.log) and
[kprove-opposite-result.log](/audit-output/evidence/kprove-opposite-result.log).
Both independent Python implementations return the sentence containing `1`.
The added interpretation is a value-sensitivity probe, not part of the
immutable candidate, and the unmodified target does not literally state the
`"9"` sentence. The significance is that the candidate's oriented
abstraction/postcondition pair does not reject the opposite interpretation:
no bridge-free universal theorem fixes the program-derived decimal rendering.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh ground
mutation for satisfying input `["3"]` that requires the returned list to be
empty:

[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k)

The exact command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module ODD-COUNT-SPEC-VACUITY
```

It parsed and ran successfully as a proof task, then exited 1 with
`WarnStuckClaimState`. The residual is the actual one-element heap list, so the
failure is the expected unmet result obligation, not a parser error, timeout,
or unrelated crash. See
[kprove-vacuity.log](/audit-output/evidence/kprove-vacuity.log).

This establishes non-vacuity at the result-list length level. It does not cure
the unconstrained string content or prove that the body produced the summary.

## 7. Proven versus assumed accounting

What `#Top` actually establishes is conditional partial correctness in the
candidate's extended theory: for every modeled finite ASCII digit-string list
satisfying `validDigitStrings`, the macro-pinned program reaches reference 0
and heap value `list(oddCountSpec(INPUT))`, where `oddCountSpec` is interpreted
through the proof-local loop bridge and the oriented rewrite to the opaque
`decimalCodes` function.

Trust and assumption ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 prover/backend | all reachability results | Ordinary toolchain trust; version recorded and all work rebuilt |
| trusted translator and canonical Python | program identity and differential oracle | Acceptable; hashes match trusted mounts, constructor identity is mechanical, differential evidence is finite |
| supplied MPY semantics | values, control, heap, calls, ASCII strings | Required fixed model; exact candidate/trusted tree identity; concrete boundary tests pass |
| mathematical parity/sequence folds | count and list summary | Acceptable definitions in isolation |
| `decimalCodes` plus line-28 simplification | every numeric field of every output string and the final postcondition | Illegitimate result-bearing oracle; no independently proved/reducing definition or bridge-free theorem; opposite interpretation is not rejected |
| inner `For` bridge | inner count and loop-variable transition | Exact guarded transformer has evidence but lacks the required separately bridge-free connection artifact |
| outer `#loop` bridge | all outer body execution, heap result, and continuation | Illegitimate circular execution bypass; exact same summary is assumed by the rule, and body sensitivity fails |
| differential tests | candidate-vs-canonical behavior for 1,127 inputs | Useful empirical bridge only; cannot prove universal K correspondence |

Gate A (real-program soundness and result connection) fails. The source-domain
precondition is not finitely bounded, and the claim is constructor-pinned to
the real submitted body, but those positive facts cannot rescue an
unconstrained result-bearing abstraction or an unproved operational summary.
The fresh mutation shows some discrimination, not legitimacy. No audit
infrastructure uncertainty contributes to this decision.

Under the benchmark decision boundary, a proof that does not constrain the
exact intended result and bypasses the material computation without an
independent connection theorem is not a legitimate partial-correctness proof
of the HumanEval program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
