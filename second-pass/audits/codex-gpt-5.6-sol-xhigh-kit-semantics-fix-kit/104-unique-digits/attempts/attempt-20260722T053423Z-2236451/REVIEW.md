# Adversarial review: 104-unique-digits

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program, but the proof-to-intent bridge has material, explicit trust limits. A
fresh reconstruction proves that the exact translated function returns
`list(sortVS(filterOdd(VS)))` for every finite K list of positive integers. The
function body executes; the loop claim matches its real loop; the returned
reference and heap object are constrained; and a fresh false-result mutation is
rejected for the expected unmet result equality.

The concern is not an unsound proof rule. It is that `decimalCodes` is opaque on
symbolic integers and the supplied semantics intentionally treats `sortVS` as
an opaque trusted primitive. Thus the K proof itself does not universally prove
that `sortVS` is an ascending permutation or prove the complete mathematical
bridge from decimal code membership to the English “all digits odd” predicate.
Independent Python and concrete-K tests support those bridges finitely, but do
not turn them into K theorems. Under the requested decision boundary, this is
`CONCERNS / LEGIT`, not a soundness failure.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount contains
`/reference/reference-semantics` as required. There is no mode/mount
contradiction and therefore no infrastructure breach.

I treated all candidate reports and traces as claims only. The generation trace
was read in full by a bounded summarizer: 613 JSONL records, zero parse errors,
with its messages and tool calls inventoried in
[`01b-structured-trace-summary.log`](evidence/01b-structured-trace-summary.log).
`run-input.json`, `metrics.json`, `codex-last.txt`, and bounded result-bearing
portions of `codex-output.log` are recorded in
[`01a-untrusted-generation-claims.log`](evidence/01a-untrusted-generation-claims.log).
Their prior assertions of `#Top`, validation, mutations, and zero mismatches
were not used as proof evidence.

Independent integrity results:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`; `cmp`
  exited 0 ([`01d-prompt-integrity.log`](evidence/01d-prompt-integrity.log)).
- `/candidate/py2mpy.py` is byte-identical to the trusted translator; `cmp`
  exited 0 ([`01e-translator-integrity.log`](evidence/01e-translator-integrity.log)).
- The candidate and trusted supplied-semantics trees each have the same 26
  recursively inventoried entries (including the root), with identical entry
  types and file hashes. There were zero missing, additional, changed,
  mistyped, or symlinked entries
  ([`01c-semantics-tree-integrity.log`](evidence/01c-semantics-tree-integrity.log)).
- All required candidate artifacts checked at this stage are regular,
  non-symlink files; neither the semantics tree nor trace tree contains a
  symlink ([`01f-required-artifact-types.log`](evidence/01f-required-artifact-types.log)).
- Trusted/candidate hashes are recorded in
  [`01g-trusted-hashes.log`](evidence/01g-trusted-hashes.log). The prompt and
  translator hashes also agree with the corresponding untrusted run-input
  claims.

Candidate-provided `runtime-kompiled`, `verification-kompiled`, Python caches,
`proof-run.log`, `PROOF.md`, mutation files, and validation scripts were not
reused. Because this is supplied-semantics mode, I did not invoke the
generated-semantics workflow.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is: for a finite list of
positive integers, retain every occurrence whose ordinary decimal digits are
all odd, preserve duplicates, and return the retained integers in increasing
order. The empty list is in-domain. Zero, negative integers, non-integers, and
Python `bool` values are outside the stated/formal domain.

The trusted canonical implementation converts each positive integer to decimal
text, requires every character's numeric value to be odd, appends qualifying
elements, and sorts the result. The submitted `/candidate/solution.py` uses an
equivalent predicate: its decimal text must contain none of `0`, `2`, `4`, `6`,
or `8`; it then appends and calls `sorted`. This is equivalent on the intended
positive-integer domain. It is not claimed equivalent outside that domain.

In `/tmp/audit-work/reconstruction`, I regenerated the translation using the
trusted translator. The fresh and submitted files both have SHA-256
`74c6da322fd59858bbee6a26a661d6022e59f51e65d5546a7f1952ec76d54fef`,
and an independent `cmp --verbose` exited 0
([`02a-translation-identity.log`](evidence/02a-translation-identity.log),
[`02b-translation-byte-compare.log`](evidence/02b-translation-byte-compare.log)).
Thus `solution.mpy` is the exact trusted translation of the submitted Python,
not a substituted K program.

The reviewer-authored differential
[`differential_test.py`](evidence/differential_test.py) independently imports
`/reference/canonical.py:unique_digits` and
`/candidate/solution.py:unique_digits`. Its input scope is documented in
[`differential-input-scope.md`](evidence/differential-input-scope.md): both
examples; empty and minimum cases; all five even-character branches; digit
position, duplicate, sorting, and large-integer cases; every singleton from 1
through 10,000; deterministic sliding windows; and 1,000 seeded generated
lists. Result: 11,288 cases, zero documented-example failures, zero mismatches,
exit 0 ([`02c-python-differential.log`](evidence/02c-python-differential.log)).
This is strong finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/reconstruction`. Fresh output directories were named
`runtime-fresh-kompiled` and `verification-fresh-kompiled`; no candidate-built
definition or cache was placed on either command line. The independently
installed tools are K v7.1.293
([`00-toolchain.log`](evidence/00-toolchain.log)).

Fresh builds and proofs were:

| Target | Exact recorded command summary | Result |
|---|---|---|
| Concrete definition | `timeout 900 kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-fresh-kompiled` | exit 0 ([`03a-fresh-llvm-kompile.log`](evidence/03a-fresh-llvm-kompile.log)) |
| Proof definition | `timeout 900 kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled` | exit 0 ([`03b-fresh-haskell-kompile.log`](evidence/03b-fresh-haskell-kompile.log)) |
| Loop claim alone | `timeout 900 kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.filter-loop` | `#Top`, exit 0 ([`03d-kprove-filter-loop.log`](evidence/03d-kprove-filter-loop.log)) |
| Every positive label, explicitly selected | `timeout 900 kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.filter-loop,SPEC.unique-digits` | `#Top`, exit 0 ([`03g-kprove-explicit-all-labels.log`](evidence/03g-kprove-explicit-all-labels.log)) |
| Complete spec, unfiltered | `timeout 900 kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC` | `#Top`, exit 0 ([`03f-kprove-all-positive-claims.log`](evidence/03f-kprove-all-positive-claims.log)) |

The entry proof legitimately depends on `filter-loop` as a circularity, so the
two claims must be present together for that target. For transparency, an
auditor diagnostic that selected only the entry label was interrupted after it
removed that needed circularity; it is marked status 130 in
[`03e-kprove-unique-digits.log`](evidence/03e-kprove-unique-digits.log) and is
not the reconstruction result. An earlier wrong short label produced only an
`Unused filtering labels` CLI error
([`03c-kprove-filter-loop.log`](evidence/03c-kprove-filter-loop.log)); the
correct fully qualified run above replaced it. Neither diagnostic is a
candidate proof failure.

Concrete execution was also rebuilt from source. A reviewer file whose first 11
lines were byte-compared with the exact candidate function was freshly
translated and run against the LLVM definition. Six empty/example/branch/
duplicate/order assertion groups completed with exit 0
([`k_concrete_checks.py`](evidence/k_concrete_checks.py),
[`04a-k-concrete-checks.log`](evidence/04a-k-concrete-checks.log)). A broader
independent arithmetic-digit/insertion-sort generator produced 151 concrete K
cases; all assertions completed, with zero runtime mismatches and exit 0
([`generate_k_differential.py`](evidence/generate_k_differential.py),
[`07a-independent-k-differential.log`](evidence/07a-independent-k-differential.log)).

## 4. Adequacy and real-program pinning

### Claim meanings

`filter-loop` precondition, in plain language: execution is at the real `For`
loop head with remaining iterator `list(VS)`; `VS` consists only of positive K
integers; the loop target and body are exactly those from the submitted
function; the current local scope has `x`, `result`, `n`, and `text`; `result`
points to heap list `ACC`; the global frame does not shadow `str`; and built-ins
are present. The local `x` value is named independently as `INPUT`, which makes
the invariant broader but does not affect the already-evaluated loop iterator
or result. Its postcondition says the loop control is consumed and the same
heap object contains `valSeqConcat(ACC, filterOdd(VS))`; final `n` and `text`
are existential because they are not observable in the returned result.

`unique-digits` precondition: `VS` is a finite sequence of positive K integers;
the module scope binds `unique_digits` to a plain closure with parameter `x`,
definition environment 0, and the submitted function body; built-ins are the
fixed scope; heap and stack are empty; and allocation begins at zero. Its
postcondition: normal execution returns `ref(1)`; heap location 0 is the
program's accumulator `list(filterOdd(VS))`; heap location 1 is the returned
fresh object `list(sortVS(filterOdd(VS)))`; `heapLoc` is 2; the caller
environment/scope counter are restored; stack and return state are clear; and
exception/exit state remains `NoExc`/0.

The result is not free, tautological, or guarded by a one-way implication. Both
the returned reference and its exact heap payload are fixed. Allocation order
is pinned by the empty initial heap: the literal `result = []` allocates 0 and
`sorted(result)` allocates 1.

### Exact program identity

The entry claim begins after module loading, but this does not substitute a
different program: the fixed `FuncDef` rule creates exactly the closure state
used by the claim. To check this structurally rather than visually, I freshly
parsed both `solution.mpy` and `spec.k`, then compared their K ASTs. There is one
submitted `FuncDef`, one spec closure, and their parameter AST and entire body
AST are exactly equal; the closure environment is 0
([`04c-emit-program-and-spec-ast.log`](evidence/04c-emit-program-and-spec-ast.log),
[`compare_program_spec_ast.py`](evidence/compare_program_spec_ast.py),
[`04d-program-spec-ast-pinning.log`](evidence/04d-program-spec-ast-pinning.log)).
The loop claim likewise reproduces the exact translated `For` target and body.

### Satisfying witnesses and substitution

The empty sequence satisfies `positiveInts(.ValSeq) = true`. A more informative
witness is `VS = [15, 33, 1422, 1]`: all four values are positive integers,
`filterOdd(VS) = [15, 33, 1]`, and the named sort contract gives
`sortVS(filterOdd(VS)) = [1, 15, 33]`. The claim therefore predicts `ref(1)`
pointing to `[1, 15, 33]`. The trusted canonical and submitted Python both
return that list. Empty, minimum, example, and duplicate witnesses were
substituted into the claim-side summary and both Python implementations; all
four satisfied the precondition and all results agreed
([`witness_compare.py`](evidence/witness_compare.py),
[`04b-concrete-witnesses.log`](evidence/04b-concrete-witnesses.log)).

## 5. Rule-by-rule static soundness review

The corrected exhaustive inventory
[`05b-exhaustive-k-inventory-corrected.log`](evidence/05b-exhaustive-k-inventory-corrected.log)
lists every declaration with source line, normalized text, attributes, and file
hash. It covers 26 K files, 1,116 declarations: 231 syntax declarations, one
configuration, five contexts, 710 rules, and two claims. The rule population is
593 ordinary, 36 concrete, 26 `owise`, 43 priority-40, three priority-45, one
priority-39, and eight simplification rules (attribute categories can overlap).
There are 111 `total` declarations, no `functional` declarations, and 24 opaque
`no-evaluators` symbols. The preliminary inventory is preserved as `05a`; the
corrected inventory fixes association of indented `requires`/attributes with
their owning rule.

The reviewer-authored disposition
[`static-rule-review.md`](evidence/static-rule-review.md) accounts for all 695
supplied rules module by module, maps every submitted constructor to its
declaration and operational rules, enumerates the opaque/priority/total trust
surface, and assesses every one of the 15 proof-local rules. Key findings are:

- The trusted supplied tree is exact and candidate-unmodified. The used path is
  module/closure load, name lookup, left-to-right calls, list allocation and
  iteration, local assignment, short-circuit `and`, string `not in`, list
  append, return/frame restoration, and unkeyed `sorted`. Unused float, dict,
  set, range, comprehension, slice, MD5, keyed-sort, and related rules cannot be
  reached from the submitted AST/configuration.
- Configuration and cell effects on the used path are coherent: the plain call
  allocates/deletes its local scope, preserves the module and built-in scopes,
  appends in place to heap location 0, allocates the returned sorted list at 1,
  restores caller control, and leaves normal status.
- Evaluation/binding are pinned. `str` is not locally or globally shadowed in
  the helper's exact scope, and the entry module has only `unique_digits`, so
  lookup reaches the built-in `typeV("str")`. The local `str` bridge fires only
  after callee and argument evaluation.
- `intProj(I) => I` is exact. `positiveInts` descends over the sequence. The
  integer-list iterator bridge produces the same head/rest as the fixed rule
  because `isInt(V)` entails `intProj(V) = V`; it touches only `<k>`.
- `decimalCodes` has the exact ground equation
  `strToCodes(Int2String(N))`. Its positive-Int operational bridge has the same
  value/control/state footprint as the fixed `str` path, but keeps symbolic
  codes opaque.
- The six recursive `filterOdd` cases cover the intended predicate. The five
  rejection guards may overlap only with identical right sides; the keep guard
  is disjoint from every rejection guard; all cases descend on the tail.
- The two `valSeqConcat` simplifications are true right-identity and
  associativity lemmas. Their orientation descends/reassociates rightward, and
  overlaps agree with the fixed recursive equations.
- No rule intercepts a whole `unique_digits` call, returns an oracle result,
  fabricates a reference, skips the body, or unconstrains a result/state cell.
- The relevant supplied opaque primitive is `sortVS`. The operational
  `sorted` rule really executes and allocates, but ascending-permutation meaning
  is intentionally outside symbolic proof. Nineteen float opaque symbols,
  `md5hexCodes`, and `sortKeyVS` are unreachable. The other two relevant opaque
  symbols are the guarded `intProj` and ground-linked `decimalCodes` above.

The LLVM compiler warned that six supplied `total` helpers are non-exhaustive:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is on the
submitted path. These are coverage warnings, not false equations, and I found
no concrete or symbolic false conclusion they enable for a finite list of
positive integers. I therefore record the narrower off-path evidence gap and
do not label those rules unsound.

No inventoried rule is judged unsound on the intended domain. Consequently
there is no required false-conclusion witness for an unsoundness allegation.
The opaque decimal/sort meanings are trust limitations, not globally false
rules.

## 6. Fresh non-vacuity test

I did not reuse `/candidate/spec-vacuity.k`. Starting from the submitted spec in
scratch, I created
[`reviewer-false-result.k`](evidence/reviewer-false-result.k), changed the module
name, and changed only the entry result payload from
`list(sortVS(filterOdd(VS)))` to
`list(vCons(0, sortVS(filterOdd(VS))))`. The exact two-line semantic diff is
recorded with `diff` exit 1 in
[`06c-false-mutation-diff.log`](evidence/06c-false-mutation-diff.log).

This mutation is demonstrably false for the satisfying witness
`VS = .ValSeq`: the real post-state holds an empty returned list, while the
mutation demands `[0]`. It is result-constraining and reachable.

- `kprove ... --dry-run` emitted a valid backend command and exited 0, proving
  that the mutation parsed/built
  ([`06a-false-mutation-dry-run.log`](evidence/06a-false-mutation-dry-run.log)).
- The actual proof exited 1 with `WarnStuckClaimState`, normal final control and
  heap, and the precise failed implication
  `sortVS(filterOdd(VS)) = vCons(0, sortVS(filterOdd(VS)))`
  ([`06b-false-mutation-kprove.log`](evidence/06b-false-mutation-kprove.log)).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unreachable mutation, or unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

For every finite algebraic `ValSeq` whose elements are K integers strictly
greater than zero, under the supplied MPY semantics plus the audited local
extensions, any terminating execution of the exact submitted `unique_digits`
closure returns normally with a fresh reference to
`list(sortVS(filterOdd(VS)))`. The accumulator contains
`list(filterOdd(VS))`; allocation, caller control, scope restoration, stack,
return state, exception state, and exit code have the concrete values stated in
the entry claim. The loop circularity establishes the accumulator invariant for
arbitrarily many iterations. This is partial correctness; it does not prove
termination.

### Trust ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| K v7.1.293 compiler, Haskell prover/backend, LLVM backend, and hooked Int/Bool/Map/List operations | All machine-checking and execution | Foundational accepted tool trust. Fresh builds, positive `#Top`, and a discriminating negative proof were observed. |
| Trusted translator `/reference/py2mpy.py` | Python-to-MPY identity | Authorized trusted input; fresh output is byte-identical. Translator correctness beyond that mount is assumed. |
| Exact supplied MPY semantics | Meaning of every used AST/control/state operation | Authorized semantics boundary and byte/type-identical candidate copy. Used constructs were statically mapped and concretely exercised; it is a subset semantics, not full CPython. |
| `intProj` | Symbolic Int head/value | Acceptable derived projection: exact equation on Int injections and guarded uses. |
| `decimalCodes` plus the positive-Int `str` bridge | Branch control, `filterOdd`, and thus final value | Exact for every ground K Int by equation; universal symbolic correspondence is assumed. Supported by 151 independent concrete-K cases and Python differentials, not proved universally. |
| Supplied opaque `sortVS` | Final ordering and permutation | Explicit trusted primitive. Ground insertion rules and 151 independent concrete-K cases support it; the reachability proof itself does not prove ascending-permutation semantics. This is the principal concern. |
| `filterOdd` summary-to-English bridge | “No even digit” meaning | Equations literally mirror the program's five checks. For positive decimal notation, absence of `0,2,4,6,8` iff every digit is odd is ordinary but informal mathematics here; 11,288 Python cases and the concrete K cases support it finitely. |
| Trusted canonical implementation | Differential oracle for intent | Authorized trusted input and independent of proof equations. Testing supports implementation/intent alignment only on tested inputs. |
| Termination | Whether the loop/call completes | Not established and not needed for the stated partial-correctness theorem. Inputs are finite, so termination is plausible operationally, but remains outside the proof result. |

The proof does not rely on candidate `PROOF.md`, its old traces, or differential
tests as substitutes for `kprove`. The tests support only the program/canonical,
decimal, and sort bridges they execute.

Gate A (real-program soundness) passes: body identity, state footprints,
binding/control, equations, satisfiable witnesses, and non-vacuity all pass.
Gate B (intent adequacy) passes on the stated positive-integer-list domain, with
the documented conditional/empirical decimal and sorting bridge. Gate C
(auditability) passes: reviewer scripts, input scopes, exact commands, statuses,
and bounded outputs are preserved below `/audit-output/evidence`.

This is not `FAIL`: no substituted program, vacuity, failed reconstruction, or
materially unsound rule was found. It is not an unqualified `PASS` because the
K theorem stops at opaque `sortVS` and symbolic decimal summaries whose full
human-facing interpretation is assumed/empirically supported rather than
formally derived.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
