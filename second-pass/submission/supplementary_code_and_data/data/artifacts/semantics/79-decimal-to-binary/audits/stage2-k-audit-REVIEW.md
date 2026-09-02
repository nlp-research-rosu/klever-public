# Independent adversarial review: 79-decimal-to-binary

## Executive conclusion

The candidate contains a legitimate partial-correctness proof for the intended
nonnegative-integer domain. I rebuilt the supplied concrete semantics and the
proof definition from source, and the only positive target claim printed
`#Top` and exited 0. The claim executes a constructor-level copy of the
submitted function body, constrains the exact returned string, has a
satisfiable precondition, rejects both a false result mutation and a material
body mutation, and does not use a result oracle.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the proof
depends on one proof-local slice acceleration for which the candidate supplies
no bridge-free, machine-checked universal connection theorem. The equation is
nevertheless sound: an independent structural argument shows that it is
exactly the fixed semantics of `[2:]`, and fixed-versus-extended ground and
continuation probes agree. I found no false conclusion witness for it and
therefore do not characterize it as unsound. The missing universal K
connection is a non-fatal auditability limitation.

## 1. Input and provenance integrity

The launcher declares `record_layout: legacy-selected-stage1`,
`semantics_mode: SUPPLIED_SEMANTICS`, and `mount_reference_semantics: true`.
All required launcher records are real readable files, the candidate and trace
mounts are real directories, and none of the recursively checked semantics or
trace entries is a symlink or unsupported node.

The independently checked records were:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/usage.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`, and
  `/generation-evidence/prompt.txt`;
- all 207 JSON records in the structured trace
  `/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T02-11-34-019f8dd0-b9b0-7f80-951f-e1dd2fd9eb01.jsonl`.

Historical runtime metrics were not present, but they are not required for
this legacy-selected layout. The campaign-lock JSON is exactly equal to the
`audit_campaign` block and its file hash is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded leaf-file hash checked by the reviewer matches. The structured
trace file hash is
`3a8087a7fb3dff69c2172694b06132890b8c486fdf2e3bc583a12ed5bc57e4f3`;
the independently recomputed pipeline tree hash is
`97fb9d05a0f0c565d0b121c2aeac8d0813b28a4f59a626464ff0e656b8461aed`,
matching `usage.json`. The independently recomputed candidate workspace tree
hash is
`01353420051a24e0acdc8b063ab5581b41a8fcccd8b1235703cc2ec0d7d8179a`,
matching both the invocation and generation-result records. The launcher also
records alternate aggregate tree digests; I treated them as recorded values,
not as leaf-file hashes, and relied on the reproducible pipeline hashes plus
leaf-by-leaf comparison.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Most importantly for
supplied-semantics mode, recursive entry-type, path, and file-hash comparison
shows that all 24 entries in `/candidate/reference-semantics` exactly match
the trusted `/reference/reference-semantics`: there are no missing, additional,
changed, mistyped, or linked entries. Both trees have pipeline hash
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

The generation trace claims a successful prior proof, but that claim was not
used as proof evidence. Its complete parsed summary is preserved only for
provenance review.

Evidence:

- `evidence/provenance_check.py`
- `evidence/01-provenance.log` — command exit 0
- `evidence/provenance-hashes.json`
- `evidence/generation_trace_summary.py`
- `evidence/01-generation-trace.log` — command exit 0

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and domain

The trusted prompt asks for conversion of a decimal number to binary digits,
with `db` prefixed and suffixed. In plain language, for a nonnegative integer
`n`, the intended result is:

```text
"db" + the ordinary base-two digits of n + "db"
```

The nonnegative restriction is not an artificial proof restriction. The
prompt requires every payload character to be `0` or `1`; negative Python
integers would make the canonical expression `bin(n)[2:]` begin with `b`
(for example, `n = -1` gives `"b1"`), contradicting that stated format.
Thus the consistent source-contract domain is nonnegative integers. `0` is the
zero/empty-magnitude boundary and must produce `db0db`.

The trusted canonical body is:

```python
return "db" + bin(decimal)[2:] + "db"
```

The candidate uses exactly this body. Translating the scratch copy with the
trusted translator produced a byte-identical `solution.mpy`; both submitted
and regenerated files have SHA-256
`b6ff40e8ee7da4fb4cc501f09c4cc85a38fa63951d9f53479c1922bd949c6666`.

### Independent differential test

The independent oracle imports `/reference/canonical.py`; it does not reuse K
equations. It compared the candidate on:

- both documented examples;
- zero, one, powers of two, and values immediately around powers of two;
- every integer from 0 through 512;
- 200 deterministic generated integers up to `10^18`;
- six 256- and 1024-bit boundaries;
- six negative probes, explicitly outside the formal contract.

All 752 results match, with no nonnegative-format failures. The negative probes
also confirm implementation identity but are not claimed by the proof.

Evidence:

- `evidence/02-regeneration.log` — exact command, byte comparison, exit 0
- `evidence/differential_test.py`
- `evidence/differential-inputs.json`
- `evidence/02-differential.log` — 752 cases, zero mismatches, exit 0

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/task`. No
`*-kompiled` directory, K cache, or candidate-built definition was copied or
reused. The observed toolchain is K v7.1.293 and Python 3.10.12.

The fresh concrete build command was:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0. A reviewer-authored concrete program exercised `0`, `1`, `2`,
`15`, `32`, `103`, `256`, `-1`, and `-15`; translating it with the trusted
translator and running it with `krun ... --output none` exited 0. A broader
concrete K-versus-Python program then checked 100 deterministic cases,
including every value 0 through 64, more branch boundaries, 20 generated
values, and five negative probes; it also exited 0.

The fresh proof build command was:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. `spec.k` contains exactly one positive target claim. The
independently run command was:

```bash
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC \
  --output pretty
```

It printed `#Top` and exited 0.

The compiler emitted warnings about unused `strLt` variables and
non-exhaustive functions in unrelated float/map/join/index parts of the
minimal supplied semantics. None is reachable from this target. No build or
proof warning changes the successful exit/result above.

Evidence:

- `evidence/03-kompile-runtime.log` — exit 0
- `evidence/k-probes/audit_concrete.py`
- `evidence/03-krun-concrete.log` — exit 0
- `evidence/generate_k_differential.py`
- `evidence/k-differential-inputs.json`
- `evidence/k-probes/k_differential.py`
- `evidence/03-k-vs-python-differential.log` — 100 cases, exit 0
- `evidence/03-kompile-verification.log` — exit 0
- `evidence/03-kprove-positive.log` — `#Top`, exit 0

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry precondition is `N >=Int 0`. The initial state is fully concrete:
module environment 0, only module and builtin scopes, next scope location 1,
empty heap and stack, `noRet`, `NoExc`, and exit code 0.

The postcondition says that the final `<k>` cell is exactly the K string whose
character codes are:

```text
100, 98, binCodes(N), 100, 98
```

That is `db`, followed by the supplied semantics' base-two digits for `N`,
followed by `db`. This is an equality-bearing destination, not a free result,
tautology, existential oracle, or one-way implication. The final environment,
scopes, allocation counters, heap, stack, return state, exception state, and
exit code are also fixed to their initial/restored values.

`N = 0` with the displayed cells is an explicit satisfying state. Substitution
gives character codes `[100, 98, 48, 100, 98]`, or `db0db`, agreeing with both
Python implementations. Independent substitutions for `1`, `15`, `32`, `103`,
and `256` likewise agree exactly; all values and code lists are recorded in
`evidence/04-program-pinning.log`.

### Mechanical program identity

The translated module is:

```text
Module(FuncDef("decimal_to_binary", Params("decimal"), Return(...)))
```

The entry wrapper calls a closure with parameter `"decimal"` and the identical
`Return(...)` constructor body. After only whitespace removal and the
singleton-statement normalization `BODY` versus `BODY .Stmts`, the body match
is exact; its normalized SHA-256 is
`a16747d7a04e31342da306ad630dc02576feca91a31c995122337444b8c5963c`.

The wrapper omits loading the one-definition module and looking up the exported
name, but this is semantically inert here: module load would bind precisely
that closure in environment 0, and the claim directly invokes the same closure
with the same defining environment and argument. It does not omit or summarize
the function body. The actual calls, parameter binding, `bin` lookup, argument
evaluation, slice, both string concatenations, return, and frame pop execute
under the semantics. The one slice operation is accelerated by the reviewed
derived equation discussed in stage 5.

### Body sensitivity

I changed the final literal in the constructor term actually executed by the
claim from `Str("db")` to `Str("dx")`, rebuilt the mutated definition
successfully, and reran the unchanged intended result obligation. `kprove`
exited 1 with a meaningful residual comparing final code `120` (`x`) against
required code `98` (`b`). This is a body mutation of the proof term, not merely
an edit to an ignored external Python file.

Evidence:

- `evidence/program_pinning.py`
- `evidence/04-program-pinning.log` — constructor match and witnesses, exit 0
- `evidence/k-probes/verification-body-mutation.k`
- `evidence/k-probes/spec-body-mutation.k`
- `evidence/04-body-mutation-build.log` — exit 0
- `evidence/04-body-mutation-proof.log` — expected exit 1 and relevant residual

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried all supplied K sources plus `verification.k` and `spec.k`: 26
files and 1,099 declarations/items. The inventory contains 697 ordinary rules,
228 syntax declarations, five contexts, one configuration, one claim, and all
module/import/require entries. For every row it records the complete normalized
text, source span, attributes, target reachability, disposition, and note.
Attributes include 148 function declarations, 110 `total` declarations, 50
priority rules, 30 `owise` rules, 56 concrete rules, 25 symbolic declarations,
and all strict/macro declarations. There are no local `simplification` or
`functional` attributes.

The complete per-entry record is `evidence/rule-inventory.csv`; counts and
dispositions are summarized in `evidence/rule-inventory-summary.md`. Entries
outside the execution slice were also inspected for overlaps or priorities
that could preempt a used construct. None does. Their disposition is relative
to this theorem and the supplied minimal-language level, not a claim that the
supplied semantics models every behavior of full CPython.

### Mapping the submitted program to semantics

| Program construct | Declaration/rule route | Finding |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` load/sequence; `functions.k` closure binding | Concrete execution loads the exact function. The proof uses the mechanically equivalent direct closure. |
| `Call` and argument | `call.k` callee route; `core.k` left-to-right `#evalArgs`; closure dispatch | Callee then argument order is preserved. |
| Parameter `decimal` | `functions.k` `#bindP`; a fresh callee scope | The integer argument is bound under the exact source parameter name. |
| `Name("bin")` | `core.k` `#look`; parent chain to `builtinsScope` | No local binding shadows `bin`; lookup selects `builtinV("bin")`. |
| `bin(decimal)` | `call.k` builtin dispatch; `builtins.k` `applyBuiltin("bin", N, .Vals)` | For `N >= 0`, returns code prefix `0b` plus the defined `binCodes(N)`. |
| `"db"` | `str.k` `Str`/`strToCodes` | Both characters are ASCII and reduce to codes 100, 98. |
| `[2:]` | `subscript.k` bound evaluation and `doSlice`; proof-local specialized equation | Bounds evaluate in source order. The specialized equation is reviewed below. |
| string `+` | `operators.k` dispatch; `str.k` `applyBin` and `seqConcat` | Both concatenations preserve order and exact codes. |
| `Return` | `functions.k` return, `#pop`, frame/state restoration | Returned value and all observable cells in the claim are preserved/restored. |

The relevant `binCodes` and `binAcc` rules have disjoint guards and complete
coverage on the formal domain. `binCodes(0)` is `"0"`; positive inputs recurse
by division by two while prepending the remainder digit. `pyMod(N,2)` is 0 or
1 on the positive path. This is the ordinary base-two recurrence. String
concatenation is structurally recursive and guard-free. No heap allocation,
mutable state, I/O, exception, loop control, or opaque value occurs on the
target path.

### Proof-local extension 1: entry wrapper

```text
#runDecimalToBinary(N)
  => Call(closureVal("decimal", exact Return body, 0), N)
```

This is an operational entry wrapper, but it does not replace the program
body. Its binding, body, argument, defining environment, continuation, and
state footprint agree with invoking the sole submitted module binding.
Constructor comparison and body sensitivity validate this. It reads/writes no
cell itself; ordinary call/return rules account for all state effects.

### Proof-local extension 2: specialized slice equation

The only substantive extension is:

```text
doSlice(
  str(iCons(FIRST, iCons(SECOND, REST))),
  someB(2), noB, noB)
  => str(REST)
  [priority(40)]
```

Classification: derived equational lemma / operational acceleration of the
fixed `doSlice` function.

Complete match domain: any K `IntSeq` with at least two constructors, exact
start 2, absent stop, and absent step. It has no cell pattern, binding,
control-stack action, exception, or state effect. As a pure function equation,
an arbitrary surrounding continuation receives only its returned string.

The fixed semantics computes step 1, sequence length
`2 + isLen(REST)`, start `min(2, length) = 2`, stop `length`, and then
`buildIS` at indices 2 through `length - 1`. Structural induction on `REST`
shows that this is exactly `REST`. Therefore the priority-40 right-hand side
agrees with the overlapping generic `doSlice` equation everywhere the
specialized rule applies. `FIRST` and `SECOND` may be any integer codes; their
values are irrelevant to dropping two positions, so the rule is not
over-broad.

Independent fixed-versus-extended K probes checked empty, one-code, and
two-code tails with an observable `#bang` continuation. Both definitions
printed `#Top`. A `[1:]` probe lies outside the specialized match; both
definitions retained the second prefix code and printed `#Top`. Removing the
bridge from the actual unbounded program proof produces the expected fixed
semantics residual at `buildIS`, confirming both that the extension is
exercised and exactly where it contributes.

The limitation is auditability: the candidate did not provide a bridge-free
universal K theorem. My fresh universal fixed-semantics claim also exits 1,
stuck on symbolic `isLen/buildIS`; this is the prover limitation the extension
was intended to address. The structural derivation above establishes that the
equation is true, and no false witness exists, but the required universal
connection is not machine-checked. This is the reason for `CONCERNS`, not a
reason to call the rule unsound.

Evidence:

- `evidence/rule_inventory.py`
- `evidence/05-rule-inventory.log` — exit 0
- `evidence/rule-inventory.csv`
- `evidence/rule-inventory-summary.md`
- `evidence/k-probes/slice-fixed.k`
- `evidence/k-probes/slice-extended.k`
- `evidence/k-probes/spec-slice-fixed-ground.k`
- `evidence/k-probes/spec-slice-extended-ground.k`
- `evidence/05-slice-probe-build.log` — both builds exit 0
- `evidence/05-slice-ground-context.log` — fixed and extended both `#Top`
- `evidence/k-probes/spec-slice-fixed-universal.k`
- `evidence/05-slice-universal-fixed.log` — expected symbolic stuck state, exit 1
- `evidence/k-probes/verification-without-bridge.k`
- `evidence/k-probes/spec-without-bridge.k`
- `evidence/05-without-bridge-build.log` — exit 0
- `evidence/05-without-bridge-proof.log` — expected slice residual, exit 1

### Opaque and total symbols

The supplied semantics declares these 25 symbolic/trusted primitives:

`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`.

None is reachable from this integer/string program or appears in its
postcondition. They have no dependent target claim and cannot influence its
branch, value, state, exception, or termination reasoning. Target-relevant
`total` declarations are constructor-recursive or have guards covering the
actual nonnegative/in-bounds path. No task answer is smuggled through an opaque
proof-local symbol.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a distinct fresh
module that leaves the precondition and executed program unchanged but demands
`binCodes(N + 1)` instead of `binCodes(N)`. It is demonstrably false at the
satisfying input `N = 0`: the real result is `db0db`, while the mutation
demands `db1db`.

The mutated spec parsed and reached the prover using the freshly built
definition. `kprove` exited 1 with `WarnStuckClaimState`; its residual compares
the actual `binCodes(N)` result with the demanded `N + 1` recurrence. This is
the expected unmet result obligation, not a parser error, timeout, missing
import, unreachable mutation, or unrelated crash.

Evidence:

- `evidence/k-probes/spec-vacuity-audit.k`
- `evidence/06-kprove-false-mutation.log` — meaningful residual, exit 1

The separate body mutation in stage 4 supplies complementary execution
sensitivity. Together the tests show that the theorem constrains both the
program body and its result.

## 7. Proven versus assumed accounting

### What the successful K claim establishes

Under the supplied K definition plus the reviewed slice equation, for every K
mathematical integer `N >= 0`, starting in the exact displayed initial state,
executing the constructor-identical body of `decimal_to_binary` reaches:

```text
str(iCons(100, iCons(98,
    seqConcat(binCodes(N), iCons(100, iCons(98, .IntSeq))))))
```

with environment 0, the original module/builtin scopes, scope location 1,
empty heap and stack, `noRet`, `NoExc`, and exit code 0. This is a
partial-correctness statement. It is unrestricted over nonnegative integers;
it is not a finite-size proof, example proof, or bounded unrolling.

### Trust ledger

1. **K kernel/backend and SMT arithmetic.** The interpretation of K
   reachability, builtin integers/booleans/maps/lists/strings, rewriting,
   unification, and solver answers is trusted. Every K proof depends on this
   low-level boundary.

2. **Trusted translator.** The CPython-AST-to-constructor translator is outside
   the K theorem. Its mounted hash matches the launcher record, and fresh
   translation is byte-identical to the submitted `.mpy`. The wrapper-body
   comparison independently connects that constructor output to the executed
   term.

3. **Supplied semantics.** The candidate's supplied-semantics tree is
   byte-for-byte the trusted tree. The relevant call, binding, builtin,
   slicing, string, and return rules were statically audited. The 25 opaque
   primitives listed in stage 5 are all unreachable and have no target
   dependents.

4. **Meaning of `binCodes`.** This is not opaque: the fixed semantics defines
   it by the usual repeated-division-by-two equations. Identifying that
   recurrence with the human phrase “binary format” uses ordinary mathematical
   induction and trust that the supplied `bin` semantics models Python's
   builtin. The 100-case concrete K program and 752-case independent Python
   differential test are finite support, not substitutes for the recurrence
   argument.

5. **Proof-local slice equation.** Its value affects the final result and the
   target claim depends on it. It is justified by the complete structural
   argument and fixed-versus-extended probes in stage 5. The missing
   bridge-free universal K theorem is the documented concern.

6. **Source-domain bridge.** K `Int` is an arbitrary-precision mathematical
   integer, aligning with Python integers for this arithmetic. `N >= 0`
   matches the only domain consistent with the prompt's binary-digit
   guarantee. Boolean, float, negative, non-integer, exceptional, Unicode,
   mutable-state, and external-state behavior is outside the theorem.

The generation report, its historical `#Top`, and differential tests were not
used as substitutes for the reconstructed reachability proof.

## Final decision

The proof closes cleanly, is non-vacuous and result-constraining, executes the
real submitted function body, and covers the full material source-contract
domain. No materially unsound rule or false conclusion witness was found. The
proof-local slice equation is universally true but lacks the candidate-side
machine-checked connection artifact required for a fully clean validation
record. That limitation is non-fatal and warrants `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
