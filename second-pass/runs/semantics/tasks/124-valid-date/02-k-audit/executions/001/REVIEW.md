# Independent adversarial review: 124-valid-date

## Decision summary

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted `solution.mpy` under the supplied semantics. Both entry claims
were rebuilt from source and independently closed with exit 0 and `#Top`. The
proof executes the full submitted function body through the fixed semantics;
its local equations neither intercept execution nor provide an opaque result.
A fresh opposite-result mutation reached the prover and failed on the expected
semantic obligation.

The result is not an unqualified pass for two evidence/intent reasons. Four
required generation-provenance files are missing, and the generated program
materially disagrees with `/reference/canonical.py`. The latter disagreement
is unusual: on the tested strict `mm-dd-yyyy` domain, the generated program
agrees with the prompt while the canonical implementation exhibits
precedence/format behaviors contrary to the prompt. I therefore treat this as
a documented canonical-to-intent bridge limitation, not as proof
unsoundness.

All candidate artifacts were treated as untrusted. `/candidate` was never used
for a compiled definition or cache and was not modified. Reconstruction took
place under `/tmp/audit-work/reconstruction`; reviewer evidence is under
`/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent
with that mode: `/reference/reference-semantics` exists. There is no
infrastructure-mode breach.

The following required candidate provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present. The candidate's `prove.log`,
`prove-final.log`, and `prove.sh` were inspected only as untrusted historical
claims. Their claimed `#Top` did not contribute to this decision.

Integrity results:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `71bb688daf8e872a52f7dfb4d4a09c07db640afd5fc1f8845baa1470a2930b78`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Recursive `diff -r --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exited 0. Their directory and regular-file
  entries match exactly. There are no missing, additional, mistyped, changed,
  or symlinked entries in the candidate semantics tree.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. The top-level `__pycache__`, old proof logs, and `prove.sh` are extra
  non-source evidence, not additions to the protected semantics tree.

The integrity script deliberately exits 1 because the four required
provenance files are missing; all byte/tree comparisons within it pass. Exact
commands, types, hashes, and statuses are in
[`stage1-integrity.log`](evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py:3-20` requires a nonempty date in `mm-dd-yyyy` format,
month 1-12, and day 1 through 31 for months
1/3/5/7/8/10/12, 1 through 30 for 4/6/9/11, and 1 through 29 for February. It
does not impose a numeric year range or leap-year rule. The documented
`04-0-2040` false example supports fixed-width month/day syntax.

`/candidate/solution.py:1-41` implements the literal fixed-width reading:
length 10, ASCII hyphens at offsets 2 and 5, ASCII digits in all other
positions, the stated month/day bounds, and any four-digit year. It
short-circuits before indexing when the length is not 10.

The trusted canonical implementation is not behaviorally identical:

- `/reference/canonical.py:27-29` strips whitespace and uses `split`/`int`, so
  it accepts variable-width fields, surrounding whitespace, signs, and some
  non-ASCII decimal digits that do not have literal `mm-dd-yyyy` shape.
- The unparenthesized conditions at lines 32-36 parse as
  `(month-in-group and day<1) or day>limit`. In particular, the final
  `or day > 29` applies to every month, so the canonical implementation rejects
  every day 30 or 31.

### Translation fidelity

The trusted translator was run on the scratch copy of `solution.py`; `cmp`
against the submitted `solution.mpy` exited 0. See
[`stage2-translation.log`](evidence/stage2-translation.log).

### Independent differential evidence

[`differential_test.py`](evidence/differential_test.py) independently imports
the trusted canonical entry point and the scratch generated entry point. It
also contains a separate direct implementation of the strict prompt
contract. With seed 124 it ran:

- 5 documented examples;
- 36 explicit empty, formatting, Unicode, separator, digit, month, day, and
  length boundaries;
- all 1,386 combinations of months 00-13, days 00-32, and years
  0000/2000/9999 in strict fixed-width form;
- 1,781 unique seeded malformed strings.

All documented expectations passed. There were zero
generated-versus-strict-contract mismatches. There were 70 recorded
canonical-versus-generated mismatches across the categorized evaluations
(categories intentionally overlap). Examples include:

- `04-30-2000`: canonical `False`, generated/contract `True`;
- `01-31-2000`: canonical `False`, generated/contract `True`;
- `1-1-2000` and `" 03-11-2000 "`: canonical `True`,
  generated/contract `False`.

The command exited 0 because the generated implementation matched the
independent prompt oracle on every tested case. The full scope, first 70
mismatches, oracle identities, and status are in
[`stage2-differential.log`](evidence/stage2-differential.log).

Judgment: the candidate is faithful to the literal prompt contract, including
cases such as `04-30-2000` where the trusted canonical code is not. The
canonical disagreement is material and prevents claiming equivalence to that
Python implementation. It does not falsify the theorem about the submitted
program or show a prompt-contract violation; it remains a documented intent
bridge concern.

## 3. Clean proof reconstruction

K v7.1.337 was available as an independent system installation. The scratch
tree contains only copied source artifacts, the trusted semantics/translator,
and reviewer-generated files. No candidate compiled definition or cache was
copied.

Fresh commands and outcomes:

| Purpose | Command summary | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| CPython boundary driver | `python3 concrete_tests.py` | exit 0 |
| Supplied-semantics boundary driver | `krun concrete_tests.mpy --definition runtime-kompiled` | exit 0, final `.K`, no exception |
| Proof definition | `kompile verification.k --backend haskell --main-module VALID-DATE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Original two-claim spec | `kprove spec.k --definition verification-kompiled --spec-module VALID-DATE-SPEC` | exit 0, `#Top` |
| Non-ten claim alone | `kprove spec-claim1.k ... --spec-module VALID-DATE-SPEC-CLAIM1` | exit 0, `#Top` |
| Ten-code claim alone | `kprove spec-claim2.k ... --spec-module VALID-DATE-SPEC-CLAIM2` | exit 0, `#Top` |

The exact commands and outputs are preserved in
[`stage3-runtime-kompile.log`](evidence/stage3-runtime-kompile.log),
[`stage3-krun-corrected.log`](evidence/stage3-krun-corrected.log),
[`stage3-verification-kompile.log`](evidence/stage3-verification-kompile.log),
[`stage3-kprove-all.log`](evidence/stage3-kprove-all.log),
[`stage3-kprove-claim1.log`](evidence/stage3-kprove-claim1.log), and
[`stage3-kprove-claim2.log`](evidence/stage3-kprove-claim2.log).

The LLVM build warns about non-exhaustive total functions in unused map/float/
join/list-index operations. The proof build warns only about unused variables
in `strLt`. None is in the task's dependency cone; Stage 5 accounts for the
opaque/total boundaries.

For audit transparency, the first reviewer-authored concrete driver used
Python `is True` assertions. The supplied subset models Boolean equality but
only models identity against `None`, so that driver stuck at
`applyCmp("is", true, true)` (exit 113). It was corrected to `== True` and
then both CPython and K runs passed. The failed diagnostic remains in
[`stage3-krun.log`](evidence/stage3-krun.log); it is not candidate evidence.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Claim 1 (`/candidate/spec.k:8-30`) starts from the exact clean module
configuration, loads `valid_date`, and calls it on an arbitrary
`str(CS:IntSeq)`. Its precondition is `isLen(CS) != 10`. It requires the call
to return Boolean `false`; it also constrains the module scope, heap,
allocation counter, stack, return state, exception state, and exit code.

Claim 2 (`/candidate/spec.k:34-77`) starts from the same exact state and calls
the function on exactly ten symbolic integer codes. It has no additional
precondition. It requires the return value to equal `validDate10` of those
same ten codes. `validDate10` is an equivalence-valued Boolean expression, not
a free variable or one-way implication: it checks both separators, all eight
ASCII digits, month 1-12, day at least 1, and the exact month-dependent upper
bound.

Together the claims cover every finite `IntSeq`: length 10 is covered by Claim
2, and all other lengths by Claim 1. There are no loop or helper claims.

### Satisfiable states and substitutions

The initial cells displayed in both claims are realizable: they are exactly
the supplied configuration with empty module scope/heap/stack and the fixed
builtins frame.

- Claim 1 witness: `CS = .IntSeq`, representing `""`; both Python
  implementations and the formal destination return `False`.
- Claim 2 true witness: codes
  `[48,51,45,49,49,45,50,48,48,48]` (`03-11-2000`);
  `validDate10`, generated Python, and canonical Python are all `True`.
- Claim 2 false witness: `02-30-2000`; all three are `False`.
- Prompt-boundary witness: `04-30-2000`; the formal destination and generated
  Python are `True`, while canonical Python is `False`, exposing the already
  documented bridge disagreement.

Exact results are in
[`claim_witnesses.py`](evidence/claim_witnesses.py) and
[`stage4-claim-witnesses.log`](evidence/stage4-claim-witnesses.log).

### Actual program pinning

`validDateBody` does not summarize a call. It is a nullary definitional name
for the complete submitted statement tree. `validDateModule` expands to a
one-function module containing that body. The fixed `#loadAll`, `FuncDef`,
call, frame, statement, builtin, assignment, branch, and return rules then
execute it.

Pinning was checked three ways:

1. Trusted regeneration is byte-identical to submitted `solution.mpy`
   (Stage 2).
2. The program subtree in
   [`program-pinning-spec.k`](evidence/program-pinning-spec.k) was mechanically
   compared to the regenerated file after the sole parser normalization
   `..., )` to explicit `.Stmts`; `cmp` exited 0 in
   [`stage4-pinning-normalized-compare.log`](evidence/stage4-pinning-normalized-compare.log).
3. The same normalized module was used as the destination of the ordinary
   configuration reachability claim in
   [`program-pinning-reachability-spec.k`](evidence/program-pinning-reachability-spec.k).
   It exited 0 with `#Top` in
   [`stage4-pinning-reachability-kprove.log`](evidence/stage4-pinning-reachability-kprove.log).
   `WarnTrivialClaim` is expected here because K normalizes the nullary
   definitional functions before a rewrite step, making both sides identical.

A prior bare functional version was parsed but rejected because this Haskell
backend does not support functional claims. That diagnostic is preserved in
`stage4-pinning-kprove-corrected.log` and is not counted as proof evidence.

The formal claims therefore pin the regenerated/submitted real program term,
not a substituted algorithm. The destination constrains the returned Boolean
and all observable modeled cells.

## 5. Rule-by-rule static soundness review

[`inventory_k.py`](evidence/inventory_k.py) generated an exhaustive inventory
of the trusted semantics tree, `verification.k`, and `spec.k`. The
guard-preserving output is
[`stage5-rule-inventory-with-guards.log`](evidence/stage5-rule-inventory-with-guards.log):

- 944 total entries;
- 234 syntax declarations;
- 702 rules;
- 5 contexts;
- 1 configuration;
- 2 claims.

[`rule-assessment.md`](evidence/rule-assessment.md) assigns every inventory
entry 0001-0944 to an exhaustive source range, records whether it is
task-reachable, maps every `solution.mpy` constructor to its declarations and
rules, and inventories all opaque/special declarations.

### Relevant fixed execution

The checked dependency chain is:

- configuration, module loading, statement sequencing, scopes, lookup, values,
  left-to-right argument evaluation, and sequence length in `core.k`;
- plain function installation, parameter binding, return, caller restoration,
  and callee-frame removal in `functions.k` and `call.k`;
- `len(str(IS)) = isLen(IS)` and one-character `ord` in `builtins.k`;
- nonnegative string indexing through `intSeqAt` in `subscript.k`;
- strict condition/RHS evaluation, assignment, `If`, short-circuit `or`,
  integer arithmetic, and integer/Boolean comparisons in `controls.k`,
  `bool.k`, `operators.k`, and `int.k`.

The non-ten branch returns before any index. The ten-code branch makes all
indices 0-9 provably in bounds, so partial `intSeqAt` never reaches an
unmodeled case. The program has no loops, allocation, mutation, methods,
collections, floats, sorts, imports, comprehensions, or exceptions.
Relevant priority rules concern heap references/cell closures absent from
these states, or are sort-disjoint. Evaluation order and frame/state changes
match the real control flow, and the claims constrain every modeled cell.

### Proof-local entries

`verification.k` adds exactly seven syntax declarations and seven equations:

- `validDateBody`, `validDateClosure`, and `validDateModule` are complete
  definitional names for the actual program term and its fixed-semantics
  closure/module.
- `digitCode(C)` is exactly `48 <= C <= 57`.
- `dateNumber(T,O)` is exactly `(T-48)*10 + (O-48)`.
- `dateLimit(M)` is 29 for 2, 30 for 4/6/9/11, and 31 otherwise.
- `validDate10` is the full fixed-width contract conjunction.

Each is a nonrecursive catch-all equation, so each `[total]` declaration is
covered. There is no overlap, inconsistent guard, priority, simplification,
`owise`, ordinary operational rewrite, call interception, opaque local
symbol, or auxiliary execution claim. In particular, `validDate10` occurs
only in the destination; it is not used to drive or replace program execution.

The supplied tree has no `[functional]` or `[simplification]` declarations.
Its 25 explicit opaque `symbol(...)` functions are listed in Stage 7. None is
reachable from this program or final result. The fixed total-but-
underspecified `valSeqAt` is likewise unused; strings use in-bounds
`intSeqAt`.

No candidate or relevant fixed rule was classified unsound. Accordingly this
review makes no unsoundness allegation requiring a false-conclusion witness.
The narrower evidence boundary is that unused parts of the supplied language
are accepted as the selected fixed semantics, not claimed to be a universal
model of CPython.

## 6. Fresh non-vacuity test

The reviewer-created
[`spec-vacuity.k`](evidence/spec-vacuity.k) keeps the complete ten-code entry
claim but changes the result destination from
`validDate10(...)` to `notBool validDate10(...)`. This is false for the
satisfying witness `03-11-2000`: the real program/formal contract return
`true`, while the mutation requires `false`. It is also false on rejected
inputs because it then requires `true`.

Command:

`kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY`

The spec parsed and reached the backend. `kprove` exited 1 with
`WarnStuckClaimState`; the residual shows the real `false` result on the
reachable `SEP1 != 45` branch cannot imply the negated destination. It was not
a timeout, parser error, missing import, or unrelated crash. Full residual and
status are in
[`stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log).

For transparency, a separate attempt to use `kompile` directly on the spec
exited 113 because K definitions are not allowed to contain claims. That is an
invalid reviewer build method, preserved in
`stage6-vacuity-build.log` and excluded from the non-vacuity evidence. The
valid `kprove` path necessarily compiled the spec before reaching the semantic
backend failure.

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditional on the supplied MPY semantics and K's trusted implementation, the
fresh reachability proof establishes:

1. For every finite `IntSeq CS` with length other than 10, executing the
   submitted `valid_date` from the displayed clean entry state returns
   Boolean `false` and reaches the displayed clean final state.
2. For every ten-code `IntSeq`, the same execution returns exactly
   `validDate10` of those codes, with the displayed scope, heap, stack,
   allocation, return, exception, and exit cells.

This is a partial-correctness result for calls on the modeled string domain.
It does not specify calls on non-string Python values or arbitrary preexisting
state/builtin shadowing. It models strings as finite integer-code sequences;
the theorem is actually broader than Unicode code-point well-formedness at
the K level, while the English bridge interprets literal ASCII
`mm-dd-yyyy`.

### Trust ledger

| Boundary | Influence and judgment |
|---|---|
| K v7.1.337 frontend, Haskell/LLVM backends, and builtin Int/Bool/String/Map/List/K-equality operations | Trusted low-level verification infrastructure. They affect parsing, symbolic execution, arithmetic, and cells. This is the ordinary acceptable K trust boundary. |
| `/reference/reference-semantics` | Trusted selected language semantics by problem condition and independently integrity-checked against the candidate copy. Used call/return/index/branch/builtin rules were statically reviewed and concretely exercised. Acceptable. |
| Trusted `py2mpy.py` | Syntactic bridge from `solution.py` to `solution.mpy`; candidate copy matches it and fresh output is byte-identical. Acceptable. |
| `validDate10` to English prompt | Informal mathematical reading, supported by direct equation review and zero mismatches against an independent strict oracle over the recorded finite scope. It is not used as an execution oracle. Acceptable for the literal prompt, but not a formal theorem about prose. |
| CPython generated implementation to K execution | Supported by byte pinning, the fixed semantics path, 26 corrected concrete boundary assertions under both CPython and K, and broader Python-only differential testing. Finite tests support rather than replace the K proof. |
| Trusted canonical implementation | Not assumed by the K proof. Differential evidence finds material disagreement. Its code conflicts with the literal prompt on fixed width and day 30/31, so equivalence to canonical is explicitly not established. Concerning intent/evidence boundary. |
| Missing generation provenance | Does not alter reconstructed proof soundness, but prevents full audit of how the candidate was produced. Concerning evidence limitation. |

The supplied semantics' explicit opaque symbols are:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. All are fixed-semantics primitives for
unused float/sort/hash functionality. None affects control, state, returned
value, or postcondition here. There is no proof-local opaque symbol or
empirical oracle.

Candidate `PROOF.md` is absent, and old logs/traces were not used as proof.
Differential and concrete tests support only the source/intent and
Python-to-semantics bridges described above; the successful fresh `kprove`
runs establish the formal reachability claims.

Gate A (real-program soundness and non-vacuity) passes. Prompt adequacy passes
under the literal strict-format reading, but equivalence to the trusted
canonical implementation does not. Evidence auditability is limited by the
missing provenance records. Those limitations justify concerns while leaving
the reconstructed proof legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
