# Independent adversarial review: 104-unique-digits

The candidate contains a legitimate partial-correctness proof of the submitted
program, reconstructed from source. The proof is result-constraining and pins
the trusted translator's exact program body. I assign `CONCERNS / LEGIT`,
rather than `PASS / LEGIT`, because the natural-language conclusion still
depends on the supplied semantics' opaque `sortVS` contract and on an informal
arithmetic interpretation of the digit summary. Neither limitation makes a
false result provable, but neither is a K theorem in this submission.

All candidate prose, logs, traces, and compiled directories were treated as
untrusted. Builds and experiments used only the scratch copy under
`/tmp/audit-work/104-unique-digits-audit`; candidate compiled definitions and
caches were not copied or used. The evidence index is
[`evidence/README.md`](evidence/README.md).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is present, is a real directory, and therefore
does not contradict the rendered mode. There is no infrastructure breach.

The following checks all passed with status 0
([log](evidence/stage1_integrity.log)):

- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `verification.k`,
  `spec.k`, `prove.sh`, and `PROOF.md` are regular, non-symlink candidate files.
- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` are regular, non-symlink trusted files.
- Neither `/candidate` nor `/reference` contains any symlink.
- `cmp /reference/prompt.py /candidate/prompt.py` exited 0.
- `cmp /reference/py2mpy.py /candidate/py2mpy.py` exited 0.
- Recursive `diff -qr --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exited 0. Thus there is no missing, additional,
  changed, mistyped, or symlinked semantics entry.

Candidate-built `*-kompiled/` directories and `__pycache__/` are additional
top-level generated material, not required source artifacts. They were
deliberately ignored. They are not additions inside the integrity-protected
semantics tree.

I read the four required provenance files and the complete structured JSONL
trace strictly as claims. The trace has 845 parseable records and no malformed
record. The candidate claims a successful, non-timeout generation, `VALIDATED`
status, positive `#Top` runs, passing differentials, and expected negative
tests. None of those claims was used as a verdict premise. Hashes, record
counts, and bounded claim summaries are preserved in
[`stage1_untrusted_claims.log`](evidence/stage1_untrusted_claims.log).

**Stage 1 result: PASS.** No integrity or infrastructure failure was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For any finite list of positive integers, return a new list containing exactly
those input elements whose base-10 representation contains no even digit,
preserving multiplicity, sorted in increasing order. The prompt examples are:

- `[15, 33, 1422, 1] -> [1, 15, 33]`
- `[152, 323, 1422, 10] -> []`

The trusted canonical implementation converts each positive integer to decimal
text, tests every character's parity, retains matching elements, and calls
`sorted`.

### Submitted implementation

`solution.py` uses an equivalent arithmetic algorithm on the intended domain.
For each positive integer it repeatedly checks the current least-significant
digit's parity via `number % 2 == 1`, then removes one decimal digit with
`number // 10`. It appends only values whose checks all remain true, then
sorts the result in place. Empty input, duplicates, and arbitrary-size positive
integers are handled. Behavior for zero, negative integers, and non-integers is
outside the stated domain and outside the formal precondition.

The trusted translator regenerated
`/tmp/audit-work/104-unique-digits-audit/regenerated-solution.mpy`; a byte
comparison with the submitted `solution.mpy` exited 0
([command and status](evidence/stage2_translation.log)).

The independent differential script imports
`/reference/canonical.py` and the scratch copy of the submitted
`solution.py`. It covers both documented examples, empty input, one-digit and
decimal-transition boundaries, true/false digit branches, short-circuit after
an earlier even digit, embedded zero, sorting, duplicates, very large integers,
every singleton `1..2000`, and 1,000 deterministic `Random(104)` lists.
All 3,018 cases agreed; mismatch count was zero
([script](evidence/stage2_differential.py),
[log](evidence/stage2_differential.log)). The script completely determines the
inputs and records their aggregate SHA-256.

This differential result is finite evidence of implementation fidelity. It is
not substituted for the K proof.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

The installed tools are K `v7.1.293` and Python `3.10.12`
([versions](evidence/toolchain_versions.log)).

I copied only source artifacts and the candidate's integrity-checked semantics
tree into scratch. I then built these fresh definitions:

| Definition | Source/main module | Backend | Result |
|---|---|---|---|
| `runtime-fresh-kompiled` | supplied `semantics.k` / `MPY-KRUN` | LLVM | exit 0 |
| `connection-fresh-kompiled` | `connection-verification.k` / `CONNECTION-VERIFICATION` | Haskell | exit 0 |
| `verification-fresh-kompiled` | `verification.k` / `VERIFICATION` | Haskell | exit 0 |
| `audit-fresh-kompiled` | `audit-verification.k` / `AUDIT-VERIFICATION` | Haskell | exit 0 |

Exact commands and outputs are in the four
[`stage3_kompile_*.log`](evidence/) files. Compiler warnings concern unused
variables and known non-exhaustive supplied functions such as float/cell-marker
helpers. None of those function heads occurs on the submitted program's
reachable path.

The reviewer concrete harness contains the submitted function's first 15 lines
byte-for-byte ([identity log](evidence/stage3_concrete_source_identity.log)).
It was translated with the trusted translator and run using the fresh LLVM
definition. Assertions cover empty, documented, branch-boundary, duplicate,
sorting, and very-large-integer cases. `krun` ended with `.K`, `NoExc`, and exit
code 0 ([source](evidence/fresh-concrete.py),
[translated program](evidence/fresh-concrete.mpy),
[run](evidence/stage3_krun_concrete.log)).

Every positive suite was independently invoked from the scratch source:

| Suite and included claims | Result |
|---|---|
| `CONNECTION-SPEC`: `digit-loop-general`, `digit-loop-positive-connection`, `assign-number-projection` | `#Top`, exit 0 |
| `SPEC`: `digit-loop`, `outer-loop`, `unique-digits` | `#Top`, exit 0 |
| `AUDIT-SPEC`: `bridge-one-true`, `bridge-two-false` | `#Top`, exit 0 |

The decisive bounded logs are
[`stage3_connection_suite.log`](evidence/stage3_connection_suite.log),
[`stage3_target_suite.log`](evidence/stage3_target_suite.log), and
[`stage3_ground_bridge_suite.log`](evidence/stage3_ground_bridge_suite.log).
The single `#Top` from each command is K's success result for all claims loaded
from that spec module.

An early diagnostic selected
`digit-loop-positive-connection` while excluding its general circularity; that
dependency-stripped invocation was interrupted with SIGINT after producing no
result. It is not a candidate timeout or verdict input. The partial log and
explanation are retained in
[`stage3_diagnostic_interruption.md`](evidence/stage3_diagnostic_interruption.md).
The correct complete suite subsequently closed in nine seconds.

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

| Claim | Preconditions | Postcondition |
|---|---|---|
| `CONNECTION-SPEC.digit-loop-general` | Exact digit loop and plain five-local frame; `number=N`, `valid=B`, `N >= 0` | Loop finishes with `number=0`, `valid=digitsOddFrom(N,B)`; arbitrary continuation and other cells are preserved |
| `CONNECTION-SPEC.digit-loop-positive-connection` | Same complete loop/frame domain; `number=N`, `valid=true`, `N > 0` | `number=0`, `valid=allOddResult(N)` |
| `CONNECTION-SPEC.assign-number-projection` | Exact assignment/frame domain; assigned `V` equals `projectIntTotal(V)` | The same local assignment writes `projectIntTotal(V)` and preserves the continuation/state |
| `SPEC.digit-loop` | Same positive loop domain | Same `allOddResult` post-state, discharged through the connected bridge |
| `SPEC.outer-loop` | Exact list loop, result reference `H`, accumulator `ACC`, and `positiveIntSeq(VS)` | Heap `H` becomes `appendOddDigits(ACC,VS)`; only scratch locals are existential |
| `SPEC.unique-digits` | Exact module binding, empty heap/stack, and `positiveIntSeq(VS)` | Returns `ref(0)`; heap 0 is `list(sortVS(oddDigitFilter(VS)))`; frame, stack, return, exception, allocation, and exit cells have the stated final values |
| Two `AUDIT-SPEC` claims | Ground counters 1 and 2 plus a trailing assignment | Respectively `valid=true` and `valid=false`, and the trailing assignment executes |

The formal domain is exactly finite `ValSeq` input whose elements are K
integers greater than zero. It imposes no size, ordering, uniqueness, or
magnitude restriction. Empty input satisfies the precondition vacuously.

### Exact program body

The entry claim invokes a genuine `Call(Name("unique_digits"), ...)` through
the module binding and the normal call/frame/return semantics. It does not
replace the whole function with a summary. The binding's `uniqueDigitsBody`
macro expands to the translated constructor body.

I independently wrote a pinning claim whose left side contains the normalized
literal body regenerated from `solution.mpy`. Using only fixed module-loading
and `FuncDef` rules, it proves that this literal is bound as the exact
`uniqueDigitsBody` closure used by the entry claim. It printed `#Top` and exited
0 ([claim](evidence/reviewer-pinning-spec.k),
[log](evidence/stage4_pinning_retry.log)). Combined with the Stage 2 byte
identity, this rules out proving a substituted program.

### Result constraint and satisfying witnesses

The returned value is not free: it is `ref(0)`, and heap location 0 is fixed to
`sortVS(oddDigitFilter(VS))`. `sortVS` is an opaque function, not an existential
variable. The helper claim's existential `?VF`, `?NF`, and `?BF` are only dead
scratch locals; they do not influence the heap or returned reference.

Concrete satisfying witnesses are recorded in
[`stage4_witnesses.md`](evidence/stage4_witnesses.md). In particular:

- `N=1` satisfies the digit-loop precondition and yields `valid=true`;
  `N=2` yields `valid=false`.
- `.ValSeq` satisfies the whole-function precondition and yields `[]`.
- Substituting `[15,33,1422,1]` gives filter order `[15,33,1]` and claimed
  sorted output `[1,15,33]`.
- Substituting `[152,323,1422,10]` gives `[]`.
- Substituting `[33,1,33,2,1]` preserves multiplicity and gives
  `[1,1,33,33]`.

Both Python implementations and fresh concrete K execution agree on those
values. The sorting step in the formal substitution is conditional on the
supplied `sortVS` contract, accounted for in Stage 7.

**Stage 4 result: PASS.** The proof pins the actual submitted program and its
observable result.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.tsv`](evidence/rule_inventory.tsv) inventories every
declaration, rule, context, configuration, and claim in the 2,211-line supplied
semantics tree and every candidate-local K source used for proof or validation.
The reviewer-authored generator is
[`inventory_k.py`](evidence/inventory_k.py). The inventory has 971 entries:

- 239 syntax declarations;
- 714 rules: 695 supplied-semantics rules and 19 candidate-local rules;
- 12 claims, five contexts, and one configuration;
- 154 entries carrying `function`, 116 carrying `total`, 23 carrying
  `no-evaluators`, 47 carrying `priority`, 36 carrying `concrete`, eight
  carrying `macro`, and 26 carrying `owise`;
- no `functional` or `simplification` rule.

Counts and per-entry dispositions are reproducible in
[`stage5_inventory_counts_retry.log`](evidence/stage5_inventory_counts_retry.log).
Each row records source location, complete flattened text, attributes, decision,
and rationale. Unused fixed-semantics heads are explicitly separated from the
132 fixed entries reachable from the submitted construct/value domain. They
cannot rewrite any term, guard, or postcondition in this proof. The 15
sort-related entries are separately identified as the supplied trusted
primitive boundary.

### Construct-to-semantics map

Every constructor in `solution.mpy` is covered:

| Program construct | Declaration | Operational path used |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`, `core.k:124-127` | `#loadAll`, left-to-right statement sequencing |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16`; exact closure captures module env 0 |
| `Call`, `Name` | `syntax.k:12,28` | `core.k:130-154`; `call.k:20-21,69-75`; left-to-right callee/argument evaluation |
| `Assign` | `syntax.k:41` | fixed `controls.k:9-18`; candidate projection bridge only on exact `"number"` frame |
| `ListExpr` | `syntax.k:17` | `list.k:13-15`, `core.k:117-121`; fresh result allocation |
| `Int`, `Bool` | `syntax.k:9,11` | `core.k:193-196` |
| `For` and target `Name` | `syntax.k:45` | `controls.k:65-74`, list iterator `list.k:9-10`, target binding `tuple.k:31-41` |
| `While` | `syntax.k:46` | fixed `controls.k:76-82`; connected candidate bridge on the exact body |
| `BoolOp("and")` | `syntax.k:16` | short-circuit contexts/rules `bool.k:16-25` |
| `BinOp("%","//")` | `syntax.k:15` | dispatch `operators.k:12`; `int.k:15-20`; denominators are fixed positive 2 and 10 |
| `Compare(">","==")`, `CmpOp` | `syntax.k:30,32` | evaluation/dispatch `operators.k:14-17`; integer cases `int.k:24-26` |
| `If` | `syntax.k:49` | truthiness `core.k:198-205`; branching `controls.k:50-54` |
| `Attribute`, `append`, `sort` | `syntax.k:29` | bound method `call.k:16,24`; mutator routing `call.k:52-60`; heap writes `list.k:53-55` and `sort.k:40-42` |
| `Expr` | `syntax.k:52` | evaluated for effect then discarded by `controls.k:46-48` |
| `Return` | `syntax.k:50` | `functions.k:77-90`; returned `ref(0)` escapes while the local frame is popped |

Evaluation order is left-to-right where relevant. The list input is dereferenced
once for `For`; the implementation never mutates it. The result list allocates
at heap location 0, append mutates that exact heap entry, sort mutates the same
entry, and the return preserves the reference. The entry postcondition fixes
environment restoration, scope counter, heap counter, stack, return state,
exception state, and exit code.

### Candidate-local definitions, one rule family at a time

- The four `program-fragments.k` macro declarations and four macro equations are
  pure syntax abbreviations. The successful pinning claim confirms exact
  expansion; they do not bypass execution.
- `projectIntTotal(I) => I` and the guarded non-integer
  `projectIntTotal(V) => 0` cases are disjoint and exhaustive. Equality with
  this projection therefore forces a symbolic `Val` in the theorem domain to
  be an integer.
- `positiveIntSeq` has the exact empty/cons structural cases. It terminates and
  says every element is an integer greater than zero.
- `hasOnlyOddDigits` is one total equation. On the formal domain its first two
  conjuncts are true and its result is `allOddResult(I)`.
- The two `addIfOdd` rules have complementary Boolean guards and agreeing types;
  exactly one applies. `appendOddDigits` has disjoint empty/cons cases and
  structurally descends. `oddDigitFilter` starts that fold at empty. These
  equations preserve order and multiplicity before sorting.
- `digitsOddFrom` has disjoint and exhaustive guards `N <= 0` and `N > 0`.
  The positive case replaces `N` by Python floor division by 10 and accumulates
  its parity. With positive divisor 10, the recursive argument is a
  nonnegative integer strictly smaller than `N`.
- `allOddResult(N) => digitsOddFrom(N,true)` is present only in the
  connection theory. It fixes the otherwise opaque symbol for all integers.
  The dependency check confirms the connection definition does not import
  `verification.k` ([log](evidence/stage5_dependency_check_retry.log)).

### Operational bridge: assignment projection

The priority-40 bridge matches only
`Assign(Name("number"),V)` in an exact plain five-binding local frame, parent 0,
with `V ==K projectIntTotal(V)`. It reads `<k>`, `<env>`, and `<scopes>`, writes
only `"number"`, frames the arbitrary continuation and every omitted cell, and
writes a value equal to fixed assignment's value.

`CONNECTION-SPEC.assign-number-projection` has the same computation, binding,
frame, guard, continuation generality, and state footprint and is proved without
the bridge. Independent fixed and bridge-enabled ground claims both execute a
trailing assignment and end with `number=7`, `value=8`
([fixed](evidence/stage5_fixed_control.log),
[bridge](evidence/stage5_bridge_control.log)). The priority resolves the overlap
with fixed assignment but does not change its effect.

### Operational bridge: positive digit loop

The priority-40 bridge matches only the exact translated loop in the exact
plain five-binding frame, parent 0, with `number=N`, `valid=true`, and `N>0`.
It writes only `number=0` and `valid=allOddResult(N)`. The loop body has no
return, break, continue, exception, cleanup, allocation, heap write, or output.

The bridge-free positive connection claim has the same loop, guard, frame,
binding, arbitrary continuation, and framed cells. Its general circularity
executes the fixed condition/body and derives the truthful recursive summary.
The complete connection suite printed `#Top`.

Independent sensitivity evidence goes beyond the candidate's tests:

- Fixed and bridge-enabled execution both give `1 -> true` and `2 -> false`
  and both run a trailing `value=7` assignment
  ([specs](evidence/reviewer-fixed-control-spec.k),
  [bridge spec](evidence/reviewer-bridge-control-spec.k)).
- The opposite `1 -> false` interpretation produces a stuck final state whose
  actual `"valid"` is `true`
  ([mutation](evidence/reviewer-opposite-spec.k),
  [log](evidence/stage5_opposite_value.log)).
- A fresh mutation changing the body to test for an even digit parses
  successfully, then gets stuck with actual `"valid" = false` rather than
  `allOddResult(1) = true`
  ([mutation](evidence/reviewer-body-mutation.k),
  [dry run](evidence/stage5_body_mutation_dry_run.log),
  [failure](evidence/stage5_body_mutation_proof.log)).

Thus the same symbol's appearance in the bridge and postcondition is not the
only support for its value: a bridge-free universal connection theorem and
body/value/control sensitivity checks independently fix it.

### Supplied sort boundary and priority/overlap checks

`sortVS` is supplied, not candidate-defined. It is a total opaque function for
symbolic proof. On concrete integer sequences, the supplied rules implement
insertion sort: empty and cons cases are structural; insertion's `X <= Y` and
`X > Y` guards are disjoint and exhaustive; each recursive call descends. The
priority-40 `.sort()` rule exactly preempts generic bound-method routing and
writes only the receiver's heap entry.

Because `positiveIntSeq` excludes non-integers, the theorem never needs the
unmodeled heterogeneous sort cases. The concrete equations and LLVM run are
consistent with ascending, multiplicity-preserving sorting. Nevertheless, the
symbolic target proof has no K lemma stating that opaque `sortVS` is an
ascending permutation. This is an explicit trusted primitive, not a
candidate-local shortcut, and is the principal concern recorded in Stage 7.

The other 21 imported `no-evaluators` symbols concern floats, MD5, and keyed
sorting. Their heads never occur in the submitted program, summaries,
preconditions, guards, or postconditions. There are no proof-local
`simplification` rules. Relevant priority overlaps are the two connected
bridges, fixed cell-vs-plain assignment/target rules (the exact frame has no
`"$cells"` marker), append, and sort; guards/priorities select the intended
rules without conflicting right-hand sides.

No materially unsound rule was found. Accordingly, I do not label any rule
unsound and do not manufacture a false-conclusion witness. The opposite-value
and body-mutation residuals above are validation evidence, not witnesses of an
unsound accepted rule.

**Stage 5 result: PASS for real-program soundness.** The supplied opaque sort
contract remains an adequacy/trust limitation, not a proof-local unsoundness.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation fixes the
satisfying input to `[1]` but requires the returned heap list to be `[2]`.
Both Python implementations and concrete K execution return `[1]`.

The mutation is
[`reviewer-spec-vacuity.k`](evidence/reviewer-spec-vacuity.k). Its `kprove
--dry-run` command parsed and built the claim successfully with exit 0
([dry-run log](evidence/stage6_mutation_dry_run.log)). The actual proof command
then exited 1 with `WarnStuckClaimState`. The residual is a reachable returned
`ref(0)` state and an unmet result condition involving `allOddResult(1)`; it is
not a parser error, missing import, timeout, or unrelated crash
([proof log](evidence/stage6_mutation_proof.log)).

This demonstrates that changing a result-bearing obligation is detected.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What the successful proof establishes

Under the supplied `MPY` semantics plus the two externally validated
proof-local operational bridges, for every finite `ValSeq` satisfying
`positiveIntSeq`, if the exact submitted `unique_digits` call terminates, it:

1. returns the fresh reference `ref(0)`;
2. leaves heap 0 equal to `list(sortVS(oddDigitFilter(VS)))`;
3. restores the module environment and scope counter;
4. leaves an empty call stack, `noRet`, `NoExc`, heap counter 1, and exit code 0.

`oddDigitFilter` retains each input occurrence exactly when the connected real
digit loop returns true. The bridge-free connection suite establishes the loop
summary over every positive integer in the bridge's match domain. The outer
claim establishes the complete filtering fold. The whole-function claim
executes allocation, iteration, append, in-place sort, return, and frame pop.

This is partial correctness. The target claim is not a general termination
theorem.

### Trust and assumption ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Supplied `MPY` semantics and K built-in integer/collection hooks | All parsing, evaluation, state, allocation, and control | Authorized fixed semantics; candidate tree is exactly the trusted tree; used rules were statically mapped and fresh LLVM/Haskell builds succeeded |
| K compiler, Haskell prover, LLVM runtime | Every machine result | Ordinary toolchain trust; exact version and commands recorded |
| Trusted `py2mpy.py` | Program-to-AST identity | Trusted mount equals candidate copy; fresh translation is byte-identical; pinning claim connects normalized AST to the proof body |
| `allOddResult` | Inner-loop result, filter branch, final membership | Not left as an oracle: its truthful equations and bridge-free universal connection close; opposite values and a body mutation are rejected |
| `sortVS` | Final order and permutation | Legitimate supplied external primitive for `.sort()`, but opaque in symbolic proof; concrete insertion-sort equations, K execution, and differential tests support it finitely. This is a documented concern |
| Arithmetic-to-decimal intent bridge | Meaning of “every decimal digit is odd” | Informal ordinary mathematics: `% 2` gives the last decimal digit's parity because 10 is even, and `// 10` removes that digit. Differential coverage supports but does not universally prove this interpretation. Documented concern |
| Positive digit-loop termination | Operational bridge does not fabricate a terminating result | Informal descent argument: for every `N>0`, `0 <= N // 10 < N`; no machine-checked liveness theorem is included. The rule is true on the intended domain, so this is an evidence limitation, not an unsoundness witness |
| Trusted canonical Python implementation | Differential oracle only | 3,018 finite comparisons; not used to close any K claim |
| Unused opaque symbols | `md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`; `sortKeyVS` | No reachable term or proof condition contains these heads; they have no dependent claim in this audit |

The natural-language result follows conditionally on the supplied `sortVS`
contract and the stated arithmetic interpretation. These are transparent,
non-circular boundaries. The candidate did not encode the filtering answer in
an unconstrained oracle, skip the whole program, prove a free result, or exploit
an inconsistent rule.

### Final decision

The reconstructed K proof is sound, discriminating, and pinned to the real
generated program. The fresh connection, control, body-sensitivity, opposite
value, and false-result checks all behave as required. The opaque supplied sort
contract and informal summary-to-decimal bridge prevent an unqualified `PASS`,
but they do not invalidate legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
