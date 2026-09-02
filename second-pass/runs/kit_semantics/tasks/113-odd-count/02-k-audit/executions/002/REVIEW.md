# Independent adversarial audit: 113-odd-count

## Executive conclusion

The candidate contains a legitimate partial-correctness proof of its submitted
program over every finite list of finite ASCII digit strings. I regenerated the
translated program byte-for-byte, compiled fresh LLVM and Haskell definitions
from the mounted source trees, replayed every positive target claim, checked the
actual constructor body used by the claims, and rejected fresh body and result
mutations.

The proof is result-constraining and unbounded: the empty/cons entry partition
and a circular outer-loop claim range over symbolic `ValSeq` and `IntSeq`
tails, not fixed list or string lengths.

I assign `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for one non-fatal
auditability limitation. The candidate's guarded `str.count` dispatch is
mathematically the fixed supplied rule lifted from `str(CODES)` to a `Val`
known by an exhaustive predicate to be a string. Its bridge-free constructor
theorem closes universally, distinct ground outcomes agree, and a wrong ground
interpretation is rejected. But an auditor-authored theorem stated in the
bridge's exact predicate-shaped symbolic form does not close without an
additional constructor-inversion lemma. There is no concrete or symbolic false
conclusion witness on the intended ground domain, so this is not an
unsoundness finding and does not make the proof illegitimate.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `113-odd-count`, and condition
`kit-semantics`. The supplied-semantics mount required by that mode is present.
There is no mode/mount contradiction.

I read and inspected:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the JSONL trace under `/generation-evidence/codex-trace/`.

The campaign lock is structurally equal to the campaign block embedded in
`/audit-input.json`, and its SHA-256 is the recorded
`053ed73c...dadd01`. Every launcher-recorded individual file hash checked by
the audit matches. The one trace leaf is a regular readable file with the
recorded SHA-256 `1ba4a398...6c40`; all 553 JSONL records parse. The trace
inventory found 127 tool calls and treats every message and command merely as
untrusted generation history.

The candidate prompt and translator are byte-identical to the trusted mounts.
The candidate and trusted `reference-semantics/` trees have exactly the same 25
entries (one directory and 24 regular files), entry type, relative path, and
file digest. Neither tree contains a symlink. This exact manifest comparison
also rules out missing, additional, changed, mistyped, or symlink-substituted
semantics entries, independently of the launcher's opaque aggregate-tree
digest encoding.

All required candidate deliverables are present as regular readable files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-provided compiled directories and logs were not used.

Reproducible evidence:

- [01_provenance_check.py](/audit-output/evidence/01_provenance_check.py) and
  [its exit-0 log](/audit-output/evidence/01_provenance_check.log);
- [01_trace_inventory.py](/audit-output/evidence/01_trace_inventory.py) and
  [its complete inventory log](/audit-output/evidence/01_trace_inventory.log).

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The docstring says that the input is a list of digit-only strings. The result
is a list in the same order. For each input string, count its odd digits and
replace every `i` in

`the number of odd elements in the string i of the input.`

with that count. The two documented examples require counts 4, 1, and 8.

The trusted canonical implementation computes
`sum(int(d) % 2 == 1 for d in arr)` and performs the same four textual
substitutions. It is a witness of the docstring, not the contract definition.

### Submitted implementation

`/candidate/solution.py` preserves the `odd_count(lst)` signature. For each
string it sums `s.count("1")`, `"3"`, `"5"`, `"7"`, and `"9"`, converts the
sum to decimal text, and constructs exactly the documented template. Over
ASCII digit strings this is equivalent to counting odd digits. It preserves
input order, emits one result per input element, does not mutate the input, and
handles an empty list and empty strings defensibly.

The exact trusted command

```text
python3 /reference/py2mpy.py /candidate/solution.py > /audit-output/evidence/solution.regenerated.mpy
```

exited 0. `cmp` against `/candidate/solution.mpy` exited 0; both translated
files have SHA-256 `c0b3fe37...f9639`. See
[02_translation_identity.log](/audit-output/evidence/02_translation_identity.log).

### Independent differential

[02_differential.py](/audit-output/evidence/02_differential.py) independently
imports `/candidate/solution.py` and `/reference/canonical.py`. Its oracle
counts membership in the independently written set `"13579"` and applies
`TEMPLATE.replace("i", str(count))`. The scope is:

- both documented examples;
- empty list, empty string, each parity boundary digit, all-even and all-odd
  strings;
- counts 9, 10, and 11, and mixed ordered lists;
- every ASCII digit string of lengths 0 through 4;
- 1,000 deterministic random lists of length 0 through 12 whose strings have
  lengths 0 through 250.

The exact command `python3 /audit-output/evidence/02_differential.py` exited 0
with `ASCII_CASES=12126` and `ASCII_MISMATCHES=0`; see
[02_differential.log](/audit-output/evidence/02_differential.log).

The differential also records a non-ASCII observation. For example, canonical
counts Arabic-Indic `"١"` as odd while the candidate counts zero. The
docstring does not state a Unicode-numeral policy, and campaign amendment v3
explicitly treats non-ASCII text as an underdetermined edge. The candidate's
ASCII `0`-through-`9` reading is defensible, is explicit in the formal
predicate, and does not violate any docstring-determined example or statement.
This observation is therefore not FAIL evidence.

Stage 2 result: PASS over the candidate's documented ASCII-digit reading, with
the Unicode edge recorded.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to the fresh directory
`/tmp/audit-work/odd-count-audit.XOEX9d`. No candidate `*-kompiled`,
`__pycache__`, cache, proof output, or trace was copied or consulted for proof
closure.

The installed tools independently report K version `v7.1.293`; see
[03_tool_versions.log](/audit-output/evidence/03_tool_versions.log).

### Concrete definition

The exact fresh build was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. The compiler's non-exhaustive warnings concern supplied-model
functions outside this program's used path and are accounted for in Stage 5.
See [03_kompile_llvm.log](/audit-output/evidence/03_kompile_llvm.log).

The reviewer-authored [smoke source](/audit-output/evidence/03_audit_smoke.py)
contains the exact candidate function plus assertions for empty input, empty
string, odd/even branch boundaries, both documented examples, and a two-digit
count. The trusted translator produced
[03_audit_smoke.mpy](/audit-output/evidence/03_audit_smoke.mpy). The command

```text
krun audit-smoke.mpy --definition audit-runtime-kompiled
```

exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`; see
[03_krun_smoke.log](/audit-output/evidence/03_krun_smoke.log).

### Proof definition and target claims

The exact fresh proof build was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0; see
[03_kompile_verification.log](/audit-output/evidence/03_kompile_verification.log).

The combined target command

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

printed `#Top` and exited 0. I also selected the claims independently:

| Selected claims | Output | Exit | Evidence |
|---|---:|---:|---|
| `SPEC.outer-loop-cons` | `#Top` | 0 | [log](/audit-output/evidence/03_kprove_outer.log) |
| `SPEC.odd-count-empty` | `#Top` | 0 | [log](/audit-output/evidence/03_kprove_empty.log) |
| `SPEC.outer-loop-cons,SPEC.odd-count-cons` | `#Top` | 0 | [log](/audit-output/evidence/03_kprove_cons_with_loop.log) |
| all three claims | `#Top` | 0 | [log](/audit-output/evidence/03_kprove_all.log) |

The cons entry is intentionally proved together with its loop circularity; the
combined run proves every claim in the target module.

For the count connection, I separately compiled the untouched supplied `MPY`
module with the Haskell backend. The bridge-free command

```text
kprove projection-spec.k --definition audit-reference-kompiled \
  --spec-module PROJECTION-SPEC
```

printed `#Top` and exited 0 for arbitrary `CODES:IntSeq` and
`PATTERN:IntSeq`; see
[03_kprove_projection.log](/audit-output/evidence/03_kprove_projection.log).

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.outer-loop-cons` starts at a nonempty `#loop` over
`list(vCons(HEAD, REST))`. Its environment is the live function frame, heap
location 0 contains an arbitrary accumulator `ACC`, and every remaining input
is an ASCII digit string. It consumes the complete remaining loop, preserves
the framed continuation and fixed control cells, permits the overwritten local
variables to change, and updates heap location 0 to
`oddLinesAcc(ACC, vCons(HEAD, REST))`.

`SPEC.odd-count-empty` starts by calling the actual `odd_count` closure on an
empty list in the module/builtins environment. It returns fresh `ref(0)`,
whose heap object is an empty list, increments `heapLoc` from 0 to 1, pops the
function frame, leaves no exception, and preserves exit code 0.

`SPEC.odd-count-cons` starts from the same call configuration on an arbitrary
nonempty finite list satisfying `allDigitStrings`. It returns fresh `ref(0)`,
whose heap object is exactly
`list(oddLinesAcc(.ValSeq, vCons(HEAD, REST)))`, with the same final control
state as the empty claim.

These claims constrain both the returned reference and its observable list
contents. They are not implications to a free result and do not omit the heap
that gives the reference its value.

### Satisfiable preconditions and ground substitutions

The empty entry state is an immediate witness for the empty claim. For both
nonempty preconditions, choose
`HEAD = str(iCons(49, .IntSeq))` (the string `"1"`),
`REST = .ValSeq`, and, for the loop claim, `ACC = .ValSeq`, integer `count`,
a string `count_string`, and any `s:Val`. The compiled predicate evaluates
this ground list to true.

[04_audit_witness_spec.k](/audit-output/evidence/04_audit_witness_spec.k)
contains that predicate witness and a complete ground entry claim for `["1"]`.
`kprove` printed `#Top` and exited 0; see
[04_kprove_witness.log](/audit-output/evidence/04_kprove_witness.log).

The corresponding Python substitution returns
`"the number of odd elements 1n the str1ng 1 of the 1nput."` in both
implementations. Empty input, the first documented example, and a count of 12
also agree; see
[04_ground_substitution.log](/audit-output/evidence/04_ground_substitution.log).

### Mechanical program identity

The claims need not reload the whole module because they bind the submitted
function as a closure, but that closure must contain the real translated body.
I parsed both `solution.mpy` and the two claim macros with fresh `kast`
invocations and macro expansion:

- the module contains one top-level `FuncDef` named `"odd_count"`;
- its only parameter is `"lst"`;
- its body has the same normalized constructor JSON as
  `ODD-COUNT-BODY`, SHA-256
  `16007b69...c1c6`;
- the `For` body has the same normalized constructor JSON as
  `ODD-COUNT-LOOP-BODY`, SHA-256
  `e1563e18...cdcc`.

Both comparisons are exact equality, not text similarity. See
[04_program_pinning.py](/audit-output/evidence/04_program_pinning.py),
[its log](/audit-output/evidence/04_program_pinning.log), and the preserved
[solution](/audit-output/evidence/04_solution.kast.json),
[body](/audit-output/evidence/04_body.kast.json), and
[loop](/audit-output/evidence/04_loop.kast.json) KAST.

Every material operation remains in the executed term: list allocation,
assignments, list iteration, target binding, five method calls, integer
addition, builtin lookup and `str(int)`, string concatenation, in-place append,
return, and frame pop.

### Body sensitivity

The reviewer-authored
[04_audit_body_sensitivity.k](/audit-output/evidence/04_audit_body_sensitivity.k)
changes the closure body actually present in the claim to allocate and return
an empty result list, while retaining the correct one-line postcondition for
`["1"]`. This is not a source-only mutation. `kprove` parsed and executed the
changed closure, then exited 1 with `WarnStuckClaimState`; its residual heap is
`0 |-> list(.ValSeq)`. See
[04_kprove_body_sensitivity.log](/audit-output/evidence/04_kprove_body_sensitivity.log).

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05_k_inventory.py](/audit-output/evidence/05_k_inventory.py) scanned every K
source file in the trusted supplied tree plus `verification.k` and `spec.k`.
The line-preserving
[inventory](/audit-output/evidence/05_k_inventory.log) contains each complete
declaration block, source span, and classification. In total it records:

- 638 ordinary, 59 concrete, 48 priority, 28 `owise`, and 2 simplification
  rules, plus one concrete-`owise` rule;
- 79 plain syntax declarations, 48 function declarations, 90 total-function
  declarations, 3 total symbolic declarations, and 25 opaque
  `symbol`/`no-evaluators` declarations;
- 5 contexts, one configuration, and the 3 target claims.

The following table gives the decision applied to every inventory row in each
file. “Fixed/unused” means the declarations are part of the supplied model but
cannot match any construct or term on this program's proof path; no correctness
conclusion here depends on them.

| File | Rules | Notable declarations | Static decision |
|---|---:|---|---|
| `semantics.k` | 0 | assembly modules/imports | exact trusted assembly |
| `syntax.k` | 0 | 16 AST syntax blocks | used syntax matches translator |
| `core.k` | 51 | configuration, values, lookup, allocation, helpers | used subset sound; other rows fixed/unused |
| `iter.k` | 0 | iterator protocol syntax | sound declaration |
| `range.k` | 6 | range helpers | fixed/unused |
| `operators.k` | 10 | 2 contexts, ref priorities | used integer/string dispatch sound |
| `int.k` | 19 | integer operations | used `+` rule is exact |
| `bool.k` | 16 | short circuit/context | fixed/unused on target path |
| `float.k` | 146 | 24 symbolic/opaque declarations | fixed/unused |
| `str.k` | 28 | codes, concatenation, comparison | used rules sound on ASCII model |
| `set.k` | 12 | set helpers | fixed/unused |
| `list.k` | 27 | list iteration/allocation/append | used rules sound |
| `tuple.k` | 21 | target binding and tuple operations | name binding used and sound |
| `subscript.k` | 40 | indexing/slicing | fixed/unused |
| `comprehension.k` | 7 | 3 macros | fixed/unused |
| `methods.k` | 75 | `count` and string/list helpers | used `count` equations sound for nonempty one-character patterns |
| `controls.k` | 34 | assignment and loops | used assignment/for rules sound |
| `functions.k` | 15 | closure/call-frame lifecycle | used call/return/pop rules sound |
| `builtins.k` | 154 | builtin folds, conversions, one opaque MD5 | used `str(int)` rule sound conditional on K hook |
| `call.k` | 21 | callee/argument/method routing, priorities | used path preserves binding/order |
| `sort.k` | 25 | 2 opaque sorts | fixed/unused |
| `assert.k` | 3 | concrete smoke assertion behavior | used only by smoke, sound |
| `dict.k` | 28 | dict helpers | fixed/unused |
| `concrete.k` | 26 | LLVM-only deep equality/keyed sort | unused by proof; no target-path overlap |
| `verification.k` | 12 | 6 local syntax/function declarations | detailed below |
| `spec.k` | 0 | 3 claims | sound circularity/entries |

The supplied compiler reports incomplete matches for `mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are documented subset or
opaque behaviors of the fixed supplied model. None occurs in `solution.mpy`,
any target postcondition, or a rule used to close these claims. I found no
overlap from these declarations that can rewrite a target term or enable a
false target conclusion.

### Construct-to-rule map for `solution.mpy`

- `ListExpr` and fresh result allocation use `list.k:14-15` and
  `core.k:117-121`.
- name lookup and left-to-right argument evaluation use `core.k:129-154` and
  `core.k:183-191`.
- assignments use `controls.k:9-18`.
- the `For` loop uses `controls.k:69-74`, list iteration uses `list.k:9-10`,
  and target binding uses `tuple.k:31-41`.
- `Attribute`/`Call` routing uses `call.k:16-32`; the fixed count equation is
  `methods.k:34-40`.
- integer additions use `int.k:9`; `str(count)` uses builtin lookup plus
  `builtins.k:192-193`.
- string additions use `str.k:20-26`.
- `result.append` keeps the receiver reference and performs the exact heap
  update in `list.k:53-55`.
- `Return` and frame restoration use `functions.k:78-90`.

Strict/`seqstrict` attributes enforce the source evaluation order. The call
rules evaluate the selected binding before arguments. The module, function,
and builtin scopes in the entry claims select the submitted closure and the
fixed `str` type object. The loop and entry claims state every configuration
cell used by these transitions. No exception-producing construct occurs on the
preconditioned domain.

### Candidate-local extensions

`ODD-COUNT-BODY` and `ODD-COUNT-LOOP-BODY` are syntax macros. The KAST equality
in Stage 4 proves that they expand to the submitted constructor bodies. They
have no independent state or control behavior.

`isStringVal` has a string-constructor equation and disjoint `owise` case.
`allDigitStrings` has exhaustive empty/cons equations and structurally recurses
on the strict tail. On every ground `Val`, it is true exactly for finite lists
whose elements are `str(CODES)` with each code in ASCII 48 through 57.

`stringCodes(str(CODES)) => CODES` is an exact constructor projection. It is
declared total and deliberately remains opaque for non-string `Val` terms.
Its only result-bearing target uses are under `isStringVal` /
`allDigitStrings`; the non-string projection value cannot affect a satisfying
ground target input. The lack of an off-domain equation is nevertheless part
of the concern stated below.

The guarded count rule

```text
applyMethod(V, "count", str(PATTERN), .Vals)
  => cntSub(stringCodes(V), PATTERN)
requires isStringVal(V)
```

is a pure, term-local acceleration after normal binding, receiver evaluation,
argument evaluation, and method routing. It reads or writes no cell, changes
no continuation, and introduces no abrupt control. On every satisfying ground
instance, `V = str(CODES)`; both this rule and the supplied rule reduce to
`cntSub(CODES, PATTERN)`. Its overlap with the supplied string-constructor rule
therefore agrees.

The bridge-free constructor theorem is universal over arbitrary code and
pattern sequences and closes with `#Top`. Independent fixed-semantics ground
claims establish outputs 0 and 2; see
[05_kprove_bridge_ground.log](/audit-output/evidence/05_kprove_bridge_ground.log).
The opposite interpretation `"11".count("1") = 1` exits 1 with a stuck claim;
see [05_audit_bridge_false.k](/audit-output/evidence/05_audit_bridge_false.k)
and [its log](/audit-output/evidence/05_kprove_bridge_false.log).

The auditability concern is precise: after removing the count acceleration,
an otherwise identical claim stated with symbolic `V` and
`requires auditIsStringVal(V)` does not prove the constructor inversion needed
to reduce the fixed rule. The definition compiled successfully, but the claim
exited 1 with a residual containing
`true #Equals auditIsStringVal(V)`. See
[05_audit_bridge_base.k](/audit-output/evidence/05_audit_bridge_base.k),
[05_audit_bridge_complete_spec.k](/audit-output/evidence/05_audit_bridge_complete_spec.k),
[the build log](/audit-output/evidence/05_kompile_bridge_base.log), and
[the proof log](/audit-output/evidence/05_kprove_bridge_complete.log).
An equivalent existential inversion attempt against the untouched reference
definition also becomes stuck; see
[05_kprove_bridge_universal.log](/audit-output/evidence/05_kprove_bridge_universal.log).

This failure does not exhibit a false rule instance: ground `Val` terms are
constructor-built, the predicate equations are exhaustive, every intended
string instance is fixed by the projection equation, and the wrong ground
result is rejected. It shows that the candidate's connection from predicate
to constructor is partly an inspected algebraic argument rather than one exact
guard-shaped machine theorem. Per the decision boundary, I report the narrower
evidence gap and do not label the rule unsound.

`oddDigitCount` is an unguarded exact sum of the five fixed one-character
`cntSub` calls. Under `allDigitStrings`, it is the odd-digit count.
`oddLine` builds the exact four-substitution string from that count.
`oddLinesAcc` has disjoint empty/cons equations and strictly recurses on the
remaining input tail while using the same `valSeqConcat` update as append.
They summarize values after, rather than replace, the executed loop.

Eleven focused ground claims cover positive/negative predicates, empty and
non-string domains, projection, count, line construction, list construction,
and guarded dispatch. They print `#Top` with exit 0; see
[05_audit_local_equations.k](/audit-output/evidence/05_audit_local_equations.k)
and [its log](/audit-output/evidence/05_kprove_local_equations.log).

`SPEC.outer-loop-cons` is a guarded circularity, not an operational rule in
the compiled definition. It executes one real nonempty iteration before
returning to its loop head, preserves the framed suffix, and is only applied
to a strictly shorter remaining `ValSeq`. Its broader arbitrary accumulator
and overwritten-local values are sound generalizations. The two entry claims
execute the real call, allocation, loop, return, and pop.

No candidate rule encodes an example-only answer, invents an unconstrained
result, intercepts the entry `Call`, skips the loop, or changes allocation,
state, exceptions, or control.

Stage 5 result: SOUND, with the documented connection-theorem auditability
concern and no false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`.
[06_audit_nonvacuity.k](/audit-output/evidence/06_audit_nonvacuity.k) uses the
satisfying ground input `["1"]`, executes the actual
`ODD-COUNT-BODY`, retains the correct returned `ref(0)`, but falsely requires
heap location 0 to contain an empty list.

The exact parse/build check

```text
kprove audit-nonvacuity.k --definition audit-verification-kompiled \
  --spec-module AUDIT-NONVACUITY --dry-run
```

exited 0; see
[06_nonvacuity_dry_run.log](/audit-output/evidence/06_nonvacuity_dry_run.log).
The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its terminal state contains the concrete one-line
result for count 1, while the destination requests `.ValSeq`; see
[06_nonvacuity_proof.log](/audit-output/evidence/06_nonvacuity_proof.log).
This is the expected unmet result-content obligation, not a parser error,
timeout, missing import, or unrelated crash.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied `MPY` definition and candidate-local equations, for every
finite `ValSeq` whose elements are finite `str(IntSeq)` values containing only
ASCII codes 48 through 57:

- if the submitted `odd_count` call terminates normally,
- it returns a fresh reference to a list of equal length and order,
- and each list element is the fixed template with all four `i` occurrences
  replaced by the decimal text of the number of codes 49, 51, 53, 55, or 57
  in the corresponding input string.

This is a universal partial-correctness theorem, not a termination or resource
bound.

### Trust ledger

| Boundary | Influence | Dependents | Assessment/evidence |
|---|---|---|---|
| supplied read-only `MPY` operational semantics | binding, order, calls, allocation, heap, loop, return | all claims | required fixed model; exact tree integrity and fresh builds checked |
| supplied `cntSub`, `allDigit`, `seqConcat`, `valSeqConcat` | counts, domain, output values | loop and entry postconditions | equations structurally reviewed; local and differential evidence agree |
| K `Int2String`/String hooks used by `str(int)` | decimal output text | `oddLine`, all nonempty outputs | fixed primitive outside theorem; counts 0, 1, 4, 5, 8, 9, 10, 11, 12 and larger random cases exercised |
| guarded `applyMethod` acceleration and `stringCodes` projection | each of five counts | loop and cons entry | ground-sound and constructor-universal connection; exact predicate-shaped connection remains informal/machine-unclosed, producing the concern |
| K compiler, LLVM/Haskell backends, SMT/backend implementation, host runtime | proof/execution trust | all machine results | standard toolchain trust; version and exact logs recorded |
| normal termination | whether a final state is reached | theorem interpretation | explicit partial-correctness assumption, not a value assumption |
| ASCII digit-string reading | formal input domain | Gate B scope | defensible docstring reading; Unicode numeral divergence documented as an underdetermined v3 edge |

The differential and smoke runs are finite evidence for implementation intent
and trusted primitives only. They are not substituted for the K reachability
proof. Candidate `PROOF.md`, historical `#Top`, and generation traces were not
used as proof premises.

### Gate and benchmark mapping

- Real-program soundness: PASS on the ground constructor domain. The real
  translated body executes, state/control are preserved, result equations are
  truthful there, and body/result mutations are rejected.
- Intent adequacy: PASS. Empty/cons claims plus structural recursion cover
  every finite list and finite ASCII digit-string length admitted by the
  documented reading, with no chosen bound.
- Trust/evidence auditability: LIMITED. The exact predicate-shaped symbolic
  connection theorem for the guarded count acceleration is absent and an
  auditor-authored attempt remains stuck, although constructor-universal and
  ground evidence establish no false intended-domain conclusion.

The closest Kit status is `FORMALLY-SOUND-UNVALIDATED` because of that narrow
connection-evidence limitation. Under this benchmark's more specific mapping,
the proof remains legitimate and the limitation maps to `CONCERNS / LEGIT`,
not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
