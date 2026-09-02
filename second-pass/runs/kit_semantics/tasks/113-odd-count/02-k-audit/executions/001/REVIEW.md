# Independent adversarial audit — 113-odd-count

## Audit conclusion

The K proof reconstructs successfully and is sound for a narrower theorem:
every finite list of finite strings whose codes are all ASCII `0` through `9`.
It does not prove the full behavior of the trusted canonical implementation.
More importantly, the submitted `solution.py` is itself not canonical-faithful
on canonical-valid non-ASCII decimal digits. For the satisfying source input
`["٣"]`, CPython's `int("٣")` is `3`, the canonical result uses count `1`, and
the candidate result uses count `0`.

This is a material source-domain narrowing and a real program-versus-canonical
divergence, not merely an unavailable representation in the supplied model.
The campaign's documented-supplied-model-gap exception therefore does not
apply. The candidate also did not record this boundary with a concrete
divergence witness in its trust ledger.

The proof-local rules are not being rejected as unsound. Gate A passes for the
formal ASCII theorem; intent/domain adequacy fails.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout = pipeline-v3`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- problem `113-odd-count`;
- candidate mount `/candidate`;
- trusted prompt, canonical, translator, and generation-record mounts under
  `/reference` and `/generation-evidence`.

There is no infrastructure breach.

The independent mounted-input check is
[`evidence/verify_provenance.py`](evidence/verify_provenance.py), with complete
output and command status in
[`evidence/01b-provenance-complete.log`](evidence/01b-provenance-complete.log).
It establishes:

- `/audit-campaign-lock.json` is a regular file with SHA-256
  `e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`,
  exactly the hash recorded by `/audit-input.json`.
- The decoded campaign lock is exactly equal to the `audit_campaign` object in
  `/audit-input.json`.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the one JSONL trace are present,
  regular, readable, and match their recorded file hashes.
- All JSON records parse. The pipeline records say generation `SUCCEEDED`,
  exit code `0`, no OOM, no timeout, and complete usage accounting. Those are
  untrusted generation claims, not proof evidence.
- The JSONL trace has 553 valid JSON records and no malformed line. Its sole
  file hash matches `/generation-result.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts. Their SHA-256 values are respectively
  `2e684f86c7166a064ce81c06ad2a26b4d974f41c507e6e65e4dccd32f2345bcd`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The candidate and trusted `reference-semantics/` trees have exactly the same
  25 relative entries, types, and per-file hashes. There are no missing,
  additional, changed, mistyped, or symlinked semantics entries.
- No entry anywhere in `/candidate` is a symlink. All required proof source
  artifacts are regular files.

I read every structured trace record and every byte of the generation output
log using
[`evidence/generation_record_summary.py`](evidence/generation_record_summary.py).
The bounded summary is
[`evidence/16-generation-record-summary.log`](evidence/16-generation-record-summary.log).
It records all 36 generation shell commands, tool/event counts, assistant
claims, and output markers. The prior `#Top` and `KPROVE_PASSED` statements
were treated only as claims to reconstruct below.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py` and `/reference/canonical.py`, `odd_count` accepts a
list of digit strings. For each string it counts the digits whose integer value
is odd, then substitutes that count for every `i` in:

```text
the number of odd elements in the string i of the input.
```

The trusted canonical expression is
`sum(int(d) % 2 == 1 for d in arr)` at
`/reference/canonical.py:20`. Thus canonical behavior, not an ASCII-only
reinterpretation, is the ground truth.

The candidate uses five literal substring counts at
`/candidate/solution.py:7`–`/candidate/solution.py:13`. That is equivalent on
ASCII digit strings, but it ignores non-ASCII decimal digits that CPython
`int(d)` accepts.

### Translation identity

In a clean scratch copy I ran:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
sha256sum solution.mpy solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

Both files have SHA-256
`c0b3fe37dcb86f08f41a30bb841afb5c294fc76bb6e7df2a914a0c758eef9639`;
`cmp` exited `0`. See
[`evidence/02-translation-identity.log`](evidence/02-translation-identity.log).

### Independent differential

[`evidence/differential.py`](evidence/differential.py) independently imports
the trusted canonical and candidate entry points. Its valid run covered:

- both documented examples;
- empty list and empty string;
- outer-loop empty/nonempty boundaries;
- zero, one, all-odd, mixed, multi-digit, and long counts;
- every ASCII decimal string through length four as a singleton input;
- 500 deterministic generated lists with strings up to length 160;
- four lists containing CPython-convertible Arabic-Indic, fullwidth,
  Devanagari, or mixed decimal digits.

The exact valid command exited `1` because it found genuine mismatches:

```text
DIFFERENTIAL_SUMMARY cases=11627 ascii_cases=11623 unicode_cases=4
mismatches=4 ascii_mismatches=0 unicode_mismatches=4
```

The smallest witness is:

```text
input     = ["٣"]
canonical = ["the number of odd elements 1n the str1ng 1 of the 1nput."]
candidate = ["the number of odd elements 0n the str0ng 0 of the 0nput."]
```

The full valid output is
[`evidence/03b-differential-valid.log`](evidence/03b-differential-valid.log).
The earlier `03-differential.log` is explicitly invalid evidence: the initial
reviewer harness accidentally added one nesting level and passed a list where
a string was expected. It was corrected before drawing any conclusion.

This mismatch is within the natural contract: U+0663 ARABIC-INDIC DIGIT THREE
is a decimal digit and `int("٣") == 3`. The canonical function terminates
normally on it.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/rebuild`.
Candidate-provided `*-kompiled` directories, caches, traces, and proof outputs
were not copied or used. K was independently identified as v7.1.293; see
[`evidence/04-tool-versions.log`](evidence/04-tool-versions.log).

### Fresh fixed-semantics connection definition

```bash
kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition fresh-reference-kompiled
```

This exited `0`
([`evidence/05-compile-reference-haskell.log`](evidence/05-compile-reference-haskell.log)).
The bridge-free supplied-semantics count claim was then run:

```bash
kprove projection-spec.k \
  --definition fresh-reference-kompiled \
  --spec-module PROJECTION-SPEC
```

It exited `0` and printed `#Top`
([`evidence/06-prove-projection.log`](evidence/06-prove-projection.log)).
`WarnTrivialClaim` is expected here: the fixed `str.count` equation simplifies
the claim before an operational rewrite.

### Fresh target definition and all positive claims

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

The compile exited `0`
([`evidence/07-compile-verification.log`](evidence/07-compile-verification.log)).
The complete target command:

```bash
kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
```

exited `0` and printed `#Top`
([`evidence/08-prove-target-all.log`](evidence/08-prove-target-all.log)).
This combined invocation is necessary because the nonempty entry claim uses
the loop claim as a circularity.

I also replayed every claim with the dependencies it requires:

```bash
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.outer-loop-cons

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.odd-count-empty

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.outer-loop-cons,SPEC.odd-count-cons
```

All three commands exited `0` and printed `#Top`; see
[`evidence/08a-prove-outer-claim.log`](evidence/08a-prove-outer-claim.log),
[`evidence/08b-prove-empty-claim.log`](evidence/08b-prove-empty-claim.log), and
[`evidence/08c-prove-cons-with-loop.log`](evidence/08c-prove-cons-with-loop.log).

### Fresh concrete execution

For additional fixed-model evidence, the reviewer-authored
[`evidence/auditor-concrete.py`](evidence/auditor-concrete.py) contains the
exact candidate body plus assertions for `[]`, `["1"]`, and both even-only and
odd-only strings. It was translated with the trusted translator. The fresh
LLVM definition command exited `0`
([`evidence/14-compile-concrete.log`](evidence/14-compile-concrete.log)), and:

```bash
krun auditor-concrete.mpy --definition fresh-runtime-kompiled
```

exited `0` with final `<k> .K </k>` and `<exit-code> 0 </exit-code>`
([`evidence/15-concrete-run.log`](evidence/15-concrete-run.log)).

The fresh dynamic gate therefore passes for the candidate's ASCII behavior.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`SPEC.outer-loop-cons` (`/candidate/spec.k:6`) says: from an exact function
loop-head state with a nonempty remaining input of ASCII digit strings, exact
call frame and counters, and accumulator `ACC` at heap location `0`, executing
the real loop to completion preserves the framed continuation and changes the
heap list to `oddLinesAcc(ACC, remaining)`.

`SPEC.odd-count-empty` (`/candidate/spec.k:43`) says: calling the bound
candidate closure on the empty list returns `ref(0)`, allocates exactly heap
location `0` containing the empty list, restores the caller state, and leaves
no exception.

`SPEC.odd-count-cons` (`/candidate/spec.k:68`) says: calling the same closure on
a nonempty list satisfying `allDigitStrings` returns `ref(0)`, whose exact heap
value is `oddLinesAcc(.ValSeq, input)`, with the caller state restored and no
exception.

The nonempty preconditions are not the unrestricted source precondition.
`allDigitStrings` uses the supplied `allDigit` predicate
(`/candidate/verification.k:84`–`/candidate/verification.k:88`), and supplied
`isDigitC` is exactly `48 <= C <= 57`
(`/reference/reference-semantics/semantics/methods.k:121`–`:122`).

### Satisfiable states and concrete substitutions

Every entry precondition is satisfiable:

- Empty entry: the exact LHS in `odd-count-empty`.
- Nonempty entry: `HEAD = str(iCons(49, .IntSeq))`, `REST = .ValSeq`. The
  predicate reduces to true.
- Loop claim: the same head/rest, `ACC = .ValSeq`, `COUNT = 0`,
  `COUNTSTRING = .IntSeq`, `S = str(.IntSeq)`, and `INPUT` equal to the
  singleton input in the exact displayed cells.

For `[]`, `odd-count-empty` yields an empty heap list, matching both Python
functions. For `["1"]`, `oddLinesAcc` reduces to one `oddLine` with count `1`;
the reviewer concrete K assertions and both Python functions produce
`"the number of odd elements 1n the str1ng 1 of the 1nput."`.

### Program identity

The claims do not execute an unrelated summary call. They bind
`closureVal("lst", ODD-COUNT-BODY, 0)` and execute that closure through the
fixed call, loop, method, append, and return semantics.

[`evidence/constructor_pinning.py`](evidence/constructor_pinning.py) expands
both macros and performs a constructor-token comparison against the trusted
regeneration of `solution.mpy`, allowing only K's explicit empty-list
terminators `.Stmts`/`.Exprs`. It reports identical SHA-256 values
`cadac0b93ca6d9eeafd50be2cd3ac35f8fa0d19559336fbd4191abdf2eb9fac6`;
see [`evidence/09-constructor-pinning.log`](evidence/09-constructor-pinning.log).
Combined with byte-identical trusted translation, this mechanically pins the
function binding and body. Omitting module loading is inert because the exact
resulting closure binding and parent scope are present in every entry state.

The reviewer body-sensitivity mutation changes the closure body actually bound
and executed by the claim to `result = []; return result`, while retaining the
original singleton destination. It reaches a final empty heap list and gets
stuck, exiting `1`; see Stage 6 and
[`evidence/12-body-sensitivity.log`](evidence/12-body-sensitivity.log).

The postconditions are result-constraining: they fix the returned reference and
its exact heap contents. They are not tautologies or one-way implications.

### Adequacy failure

The pinning result also pins the defect. For `["٣"]`, the actual submitted
program runs but counts only literal ASCII `"1"`, `"3"`, `"5"`, `"7"`, and
`"9"`. The theorem excludes the input, while canonical accepts it and returns
a different result. Thus correct pinning does not rescue full-contract
adequacy.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule_inventory.py`](evidence/rule_inventory.py) reads every K source
declaration in the supplied tree, `verification.k`, and `spec.k`. The complete
inventory is
[`evidence/10b-rule-inventory-valid.log`](evidence/10b-rule-inventory-valid.log):

```text
SOURCE_COUNT 26
DECLARATION_COUNT 1035
claim=3 configuration=1 context=5 rule=776 syntax=250
function=168 total=122 no-evaluators=28 priority=56
simplification=2 macro=5
```

The first 1,014 declarations are the byte-verified supplied fixed model. The
remaining 21 are candidate-local: six syntax declarations, twelve rules, and
three claims. Every declaration has source location, full text, and attributes
in the inventory.

For the supplied files, the per-module disposition covering the full inventory
is:

| Supplied module/file | Target relevance and static decision |
|---|---|
| `semantics.k` | Import aggregation for the fixed MPY proof model; accepted fixed boundary. `MPY-CONCRETE` is absent from Haskell proof builds. |
| `syntax.k` | Declares every used constructor. `BinOp` is left-to-right `seqstrict`; assignment, `For`, `Return`, `Expr`, and `Attribute` strictness matches the executed candidate. |
| `core.k` | Exact configuration, scope lookup, allocation, statement sequencing, literals, argument evaluation, builtins scope, integer/list helpers. Used rules preserve the displayed cells and evaluation order. |
| `iter.k` | Declares iterator control constructors used by `For`; no rewrite conclusion. |
| `list.k` | Empty/cons iteration, list allocation, concatenation, and in-place `append`. The priority-40 append rule updates exactly heap location `0`; sound on the tracked state. |
| `tuple.k` | Name-target binding used by the `For` loop. It updates the active local scope exactly. Other tuple rules are constructor-disjoint. |
| `controls.k` | Assignment, expression discard, `For/#loop/#loopStep`, and list-input dereference. The loop claim matches the actual loop head and preserves its continuation/frame. |
| `functions.k` | Exact function binding, parameter binding, `Return`, `#endcall`, and frame pop. Entry claims track scopes, stack, return state, and counters. |
| `call.k` | Callee then left-to-right argument evaluation, bound-method routing, builtin/type routing, and exact user-call frame creation. No candidate rule intercepts `Call` or frame control. |
| `operators.k` | Evaluated `BinOp` dispatches to `applyBin`; string and integer cases below are constructor-disjoint. |
| `int.k` | Integer addition for the five counts; ordinary unbounded integer arithmetic. |
| `str.k` | ASCII literal conversion, concatenation, and code-sequence helpers. Sound for the formal ASCII theorem; its explicit ASCII-only behavior is the material CPython model gap. |
| `methods.k` | Fixed `str.count` is `cntSub`; prefix/drop equations are disjoint and structurally descend. `isDigitC/allDigit` deliberately means ASCII codes 48–57. |
| `builtins.k` | `str(Int)` uses K's `Int2String` hook. The relevant result is nonnegative decimal ASCII. Its `int(str)` support is also explicitly ASCII and does not model canonical Unicode conversion. |
| `bool.k`, `float.k`, `range.k`, `set.k`, `dict.k`, `subscript.k`, `sort.k`, `comprehension.k`, `assert.k` | No constructor from these operational paths is executed by the proof target. Their rules and priority cases are inventoried but cannot contribute a target rewrite. Opaque float/sort symbols are not target dependences. |
| `concrete.k` | Used only by the fresh LLVM smoke definition. It is not imported by `MPY` in either Haskell proof definition and contributes no proof axiom. |

No candidate-local priority rule exists. All 28 `no-evaluators` declarations
are listed by the inventory; 27 are supplied float/sort/hash boundaries that
are unused here, and the one candidate symbol is `stringCodes`, discussed
below. The only two simplification rules are the two candidate rules at
`verification.k:82` and `verification.k:90`.

### Candidate-local syntax and rule decisions

| Local declarations | Class and soundness decision |
|---|---|
| `ODD-COUNT-BODY`, `ODD-COUNT-LOOP-BODY` syntax and rules (`verification.k:6`–`:7`, `:23`–`:77`) | Compile-time macros. The mechanical expanded constructor comparison is exact. They introduce no runtime state transition or oracle. |
| `isStringVal`, `allDigitStrings` syntax/equations (`:9`–`:10`, `:79`–`:88`) | Truthful constructor predicates. `isStringVal` has a string case and disjoint `[owise]`; the list predicate has empty/cons cases and descends on the tail. It defines an ASCII-only domain, which is sound but inadequate. |
| `stringCodes` declaration/equation (`:12`–`:13`, `:82`) | Result-bearing projection with one exact string-constructor equation. It is opaque off-domain despite `[total]`; every target-dependent use is under `allDigitStrings`, which entails a string constructor. It causes no false conclusion on the theorem domain. |
| Guarded `applyMethod(...,"count",...)` simplification (`:90`–`:93`) | Pure derived equation, not a `<k>` control bridge. `isStringVal(V)` entails `V = str(CS)`; `stringCodes` yields `CS`; the supplied equation yields the same `cntSub(CS,PATTERN)`. It overlaps the supplied exact-string equation only with an agreeing RHS. The bridge-free universal projection claim closes. |
| `oddDigitCount` (`:95`–`:100`) | Definitional summary: sum of the five single-ASCII-character occurrence counts. One unguarded equation; no overlap or recursion issue. |
| `oddLine` (`:102`–`:127`) | Definitional summary of the exact fixed string concatenations and decimal count conversion. One unguarded equation. It names the result but does not replace program execution. |
| `oddLinesAcc` (`:129`–`:133`) | Empty/cons equations are disjoint and recursion strictly descends on the second `ValSeq`. On the target domain its step is the exact heap `append` value. Off-domain `stringCodes(V)` remains opaque rather than proving a false value. |
| Three `spec.k` claims | The loop claim is a genuine circular invariant over the exact loop head. The two entry claims execute the pinned closure and constrain returned reference, heap, caller cells, exception, and exit code. Their soundness is supported by the fresh `#Top`, false-result, opposite-value, and changed-body runs. |

The guarded count equation was also value-tested against an opposite
interpretation under the fixed definition:

```bash
kprove auditor-count-opposite.k \
  --definition fresh-reference-kompiled \
  --spec-module AUDITOR-COUNT-OPPOSITE
```

It reduces `"11".count("1")` to `2`, gets stuck against destination `1`, and
exits `1`; see
[`evidence/13-count-opposite.log`](evidence/13-count-opposite.log).

I do not classify any proof-local rule as unsound, so there is no unsupported
unsoundness allegation. The concrete false-conclusion witness in this audit is
instead for the candidate's full-contract claim/program fidelity:
`["٣"]` proves that the ASCII restriction is material.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not used. I created the independent
[`evidence/auditor-vacuity.k`](evidence/auditor-vacuity.k). Its initial state
calls the exact candidate closure on satisfying input `["1"]`; its destination
deliberately requires an empty output heap list.

Exact command:

```bash
kprove auditor-vacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDITOR-VACUITY
```

The spec parses and builds, fixed execution terminates at `ref(0)` with the
nonempty expected text in heap location `0`, and implication to the false empty
destination fails with `WarnStuckClaimState`. Exit status is `1`. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. Full bounded output:
[`evidence/11-fresh-vacuity.log`](evidence/11-fresh-vacuity.log).

The distinct reviewer body-sensitivity claim is
[`evidence/auditor-body-mutation.k`](evidence/auditor-body-mutation.k). It
changes the closure body actually present in the starting scope. The proof
terminates with an empty heap list, fails against the original nonempty
destination, emits `WarnStuckClaimState`, and exits `1`
([`evidence/12-body-sensitivity.log`](evidence/12-body-sensitivity.log)).

These results show that the formal theorem is non-vacuous and body-sensitive
within its narrowed domain.

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the supplied MPY semantics and the K toolchain, the successful
reachability proof establishes partial correctness of the exact submitted
function body for:

```text
all finite ValSeq lists whose every element is str(CS)
and whose every code in CS is between 48 and 57 inclusive.
```

For every such input, normal completion returns a fresh `ref(0)` whose exact
heap list contains one template string per input element, in order, with `n`
equal to the sum of occurrences of ASCII `1`, `3`, `5`, `7`, and `9`.
The loop circularity is symbolic in both outer list length and inner string
length; this is not bounded unrolling.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied MPY configuration, call/return, scopes, allocation, loops, list mutation | Value, control, and heap state of all target claims | Fixed supplied-model trust boundary; relevant rules were statically traced and concretely smoke-tested. |
| `cntSub`, `seqConcat`, `valSeqConcat`, `allDigit` | Count, output strings, final list, formal domain | Fixed mathematical recursions; equations are constructor-disjoint and descending. |
| K `Int2String`/string hooks | Decimal text inserted four times | Fixed primitive outside the theorem. Tested on representative counts, but finite tests are not a universal proof. Counts are nonnegative, so their outputs are ASCII decimal. |
| Candidate `stringCodes` | Supplies symbolic codes to the count and result summary | Exact on string constructors; opaque off-domain; all target uses are guarded by the string/ASCII predicate. |
| Guarded count simplification | Determines each of the five count terms | Universally connected to the fixed exact-string equation without importing candidate verification rules; wrong ground interpretation rejected. |
| Loop circularity | Summarizes arbitrarily many remaining list elements | Machine-checked reachability claim in the same successful target invocation. |
| K compiler, Haskell/LLVM backends, SMT solver, host runtime | Compilation and proof validity | Standard unavoidable trusted toolchain boundary. |
| Termination | Whether Python/K execution completes | Not proven; the result is partial correctness. |
| Differential testing | Candidate/canonical bridge on tested inputs | Finite evidence only. It supports ASCII agreement and, decisively, exhibits a canonical-domain mismatch. |
| Unicode decimal behavior | Full source-contract fidelity | Not proven and in fact false for the submitted Python. |

### Gate and campaign mapping

- Gate A — **PASS for the formal theorem**: clean `#Top`, exact body pinning,
  sound local equations, satisfiable states, result constraint, and meaningful
  rejected mutations.
- Gate B — **FAIL**: the theorem and submitted implementation materially
  narrow canonical-valid digit strings to ASCII. The witness `["٣"]` changes
  the result.
- Gate C — **FAIL as a full-contract validation claim**: the candidate report
  labels Gate B as passing and does not disclose the Unicode model/program
  divergence with a concrete trust-ledger witness.

Under generic Kit terminology this is a sound-but-limited formal result. The
benchmark prompt explicitly maps material source-contract narrowing to
`FAIL / NOT_LEGIT`.

Campaign amendment v2 exception 1 does not change that result. Although the
supplied semantics explicitly has ASCII-only literal and `int(str)` behavior
(`/reference/reference-semantics/semantics/str.k:12`–`:17` and
`builtins.k:195`–`:197`), the submitted Python is not faithful to canonical
CPython behavior on the gap, and the candidate did not document the concrete
divergence. Exception 2 is irrelevant because the canonical implementation and
docstring examples agree.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
