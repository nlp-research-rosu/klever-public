# Independent adversarial audit: 94-skjkasdkd

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program over the full integer-list contract represented by the
supplied semantics. I independently rebuilt both definitions, reran the proof,
checked real-program pinning, inventoried every K declaration/rule/claim, and
rejected fresh false-result and body mutations. Candidate-provided compiled
definitions, logs, `PROOF.md`, and prior `#Top` output were not trusted.

## 1. Input and provenance integrity

The declared layout is `pipeline-v3`, the condition is `kit-semantics`, and the
rendered mode is `SUPPLIED_SEMANTICS`. The required trusted semantics mount is
present.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, and every required pipeline-v3 generation record
  are regular, readable files. The structured trace contains 509 valid JSON
  records. See
  [required-records.log](/audit-output/evidence/provenance/required-records.log),
  [manifests-json.log](/audit-output/evidence/provenance/manifests-json.log),
  and
  [structured-trace-inspection.log](/audit-output/evidence/provenance/structured-trace-inspection.log).
- The campaign object in `/audit-input.json` equals
  `/audit-campaign-lock.json`, and the lock's independently computed SHA-256 is
  the recorded
  `053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`.
- Independently computed hashes match all launcher-recorded hashes for the
  trusted prompt, canonical implementation, translator, run/task/result
  manifests, invocation, prompt, metrics, runtime metrics, usage, last message,
  output log, and structured trace. See
  [hash-checks.log](/audit-output/evidence/provenance/hash-checks.log).
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts. A recursive, no-symlink comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` exited 0. The 24-file trees have identical
  entry types and per-file hashes; there are no missing, additional,
  mistyped, changed, or symlinked entries. See
  [semantics-diff.log](/audit-output/evidence/provenance/semantics-diff.log)
  and [hash-checks.log](/audit-output/evidence/provenance/hash-checks.log).
- A separate reviewer-defined hash walk inspected all 810 candidate files
  (85,500,388 bytes) and found no symlinks. Its deterministic digests are
  recorded in
  [candidate-tree-reviewer-hash.log](/audit-output/evidence/provenance/candidate-tree-reviewer-hash.log).
- I inspected the complete generation-record set only as untrusted history.
  The trace/output claim a successful proof, but no later audit conclusion
  relies on that claim. Relevant bounded inspection is in
  [generation-inspection.log](/audit-output/evidence/provenance/generation-inspection.log).

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted docstring says: for a list of integers, find its largest prime
value and return the sum of that value's decimal digits. It gives six examples.
It does not state what to return when no prime exists.

The submitted [solution.py](/candidate/solution.py:1) scans every element,
tests values at least 2 by all divisors from 2 through `value - 1`, retains a
prime only when it exceeds the current maximum, and computes that maximum's
decimal digit sum. This is slower than trial division to the square root, but
is correct; performance does not weaken a partial-correctness theorem.

Trusted regeneration was checked with:

```text
python3 /reference/py2mpy.py /candidate/solution.py | cmp - /candidate/solution.mpy
```

It exited 0, establishing byte identity; see
[translation-byte-identity.log](/audit-output/evidence/fidelity/translation-byte-identity.log).

The reviewer-authored
[independent_differential.py](/audit-output/evidence/fidelity/independent_differential.py)
imports both `/reference/canonical.py` and `/candidate/solution.py`. It checks
all six documented examples, directed empty/negative/zero/one/prime/composite/
tie/square cases, all lists of lengths 0 through 4 over 20 boundary values, and
2,000 deterministic random lists. Results:

```text
total_cases=170442
documented_example_mismatches=0
candidate_vs_docstring_oracle_mismatches=0
candidate_vs_canonical_mismatches=6529
EXIT_STATUS: 0
```

The complete command and output are in
[independent-differential.log](/audit-output/evidence/fidelity/independent-differential.log).
Every canonical divergence is a no-prime list containing `1`: canonical's
empty divisor loop treats `1` as prime and returns 1, while the candidate and
the independent mathematical oracle return 0. Treating 1 as non-prime follows
the plain meaning of the docstring. The no-prime return convention itself is
underdetermined, and returning the initialized value 0 is defensible. Under
campaign amendment v3 this is not a candidate defect.

## 3. Clean proof reconstruction

Only source artifacts and the trusted mounted semantics were copied to
`/tmp/audit-work/work`; neither candidate kompiled directory nor any
candidate cache was copied. The scratch-copy record is
[scratch-copy.log](/audit-output/evidence/reconstruction/scratch-copy.log).
The toolchain independently reports K v7.1.293.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled
```

This exited 0. The reviewer smoke program contains empty, no-prime, minimum
prime, composite/prime ordering, digit-sum, and larger-prime assertions. Its
translation and `krun auditor-smoke.mpy --definition
auditor-runtime-kompiled` exited 0 at `.K`, with `NoExc` and exit code 0. See
[kompile-llvm.log](/audit-output/evidence/reconstruction/kompile-llvm.log) and
[krun-smoke.log](/audit-output/evidence/reconstruction/krun-smoke.log).

Fresh proof reconstruction:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled
kprove spec.k --definition auditor-verification-kompiled --spec-module SPEC
```

Both commands exited 0 and the proof printed `#Top`; see
[kompile-haskell.log](/audit-output/evidence/reconstruction/kompile-haskell.log)
and [kprove-all.log](/audit-output/evidence/reconstruction/kprove-all.log).
The warnings concern unused variables in the fixed semantics/spec and do not
alter closure.

I also selected claims explicitly:

- `SPEC.prime-loop` alone: `#Top`, exit 0
  ([log](/audit-output/evidence/reconstruction/kprove-prime-loop-qualified.log)).
- `SPEC.digit-loop` alone: `#Top`, exit 0
  ([log](/audit-output/evidence/reconstruction/kprove-digit-loop-qualified.log)).
- `SPEC.scan-loop` with its `SPEC.prime-loop` circularity dependency: `#Top`,
  exit 0
  ([log](/audit-output/evidence/reconstruction/kprove-scan-with-dependency.log)).
- `SPEC.target` with all three explicitly selected loop dependencies: `#Top`,
  exit 0
  ([log](/audit-output/evidence/reconstruction/kprove-target-with-dependencies.log)).

For transparency, filtering out those dependencies makes `scan-loop` or
`target` fail; those diagnostic residuals are preserved in the reconstruction
directory. This is expected claim-selection behavior and confirms that the
unbounded target uses the stated circularities. It is not a failed positive
run with its required proof context.

## 4. Adequacy and real-program pinning

The four claims in [spec.k](/candidate/spec.k:8) mean:

1. `prime-loop`: if `value` is an MPY integer and `divisor >= 2`, executing the
   real divisor loop changes `candidate` from `C` to
   `C and primeTail(value,D)` and changes `divisor` to `max(D,value)`.
2. `scan-loop`: if `largest >= 0` and every remaining list element is an MPY
   integer, executing the real list loop changes `largest` to the unbounded
   recursive fold `largestPrime(VS,M)`. Only dead scratch locals are
   existential on exit.
3. `digit-loop`: for `largest = N >= 0` and initial total `T`, executing the
   real decimal loop leaves `largest = 0` and
   `total = T + digitSum(N)`.
4. `target`: for every finite symbolic `ValSeq` satisfying `allInts`, load a
   function named `skjkasdkd`, call it on `list(VS)`, and return exactly
   `digitSum(largestPrime(VS,0))`, while restoring the caller environment,
   stack, return, heap, exception, allocation, and exit cells shown in the
   claim.

The preconditions are satisfiable: `.ValSeq`, `[2]`, `[3,4]`, and `[181,4]`
are concrete witnesses. Candidate and canonical results on those substitutions
are recorded in
[precondition-witnesses.log](/audit-output/evidence/static/precondition-witnesses.log).
For `[2]`, the claimed expression is 2; for `[181,4]`, it is 10.

Real-program pinning has two independent links:

- Trusted translation is byte-identical to submitted `solution.mpy`.
- The reviewer-authored
  [compare_program_term.py](/audit-output/evidence/static/compare_program_term.py)
  recursively expands `targetBody`, `scanBody`, `primeLoopBody`, and
  `digitLoopBody`, normalizes only the empty `Stmts` spelling, and compares the
  constructor stream with the submitted MPY function body. Both streams contain
  308 tokens and have SHA-256
  `0befa2342a14845841707fea3ef63972851355d7c4d30e612f81a8a18e3143a0`;
  equality is true. See
  [program-term-comparison.log](/audit-output/evidence/static/program-term-comparison.log).

Thus `#loadAll` executes the submitted binding and complete body, not an
external summary. The target result is not a free variable, tautology, or
one-way condition. There is no list-length or integer-magnitude bound.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[rule-inventory.tsv](/audit-output/evidence/static/rule-inventory.tsv). It
contains all 1,063 local syntax declarations, configurations, contexts,
functions, total declarations, priorities, ordinary rules, simplifications,
and claims in the supplied semantics, `verification.k`, and `spec.k`. Every
entry has a disposition:

- 146 fixed-semantics entries are reachable for this program and were reviewed
  along the actual execution chain.
- 868 fixed-semantics entries have no reachable left-hand-side symbol in this
  target. They include floats, strings, dicts, sets, comprehensions, sorting,
  opaque float primitives, and other unused constructs. A rewrite semantics
  does not derive facts from disconnected rules; these entries cannot
  contribute to this claim.
- 49 proof-local declarations/rules/claims are assigned one of the detailed
  sound categories below.

The candidate uses exactly the syntax for `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, `Int`, `Bool`, `For`, `If`, `Compare`, `CmpOp`, `BinOp`,
`While`, `AugAssign`, and `Return`. The reachable fixed rules implement:
module loading and statement sequencing; lexical lookup; left-to-right call
and operand evaluation; closure creation, argument binding, frame push/pop and
return; direct-list iteration and name target binding; integer comparison,
addition, Python-style modulo/floor division; assignment/augmented assignment;
and ordinary `if`/`for`/`while` control. The target uses a bare read-only
`list(VS)`, so no heap allocation is skipped. The exact plain local maps rule
out closure-cell priority branches. Relevant configuration and state changes
match the entry and loop claims.

Proof-local review:

- The four body constants are exact syntax aliases. They expand statements
  before fixed rules execute them; they read or write no cells and skip no
  operation.
- `allInts` has disjoint empty/cons equations and structurally descends.
  `definedProjectInt` is exactly `isInt`. `projectIntTotal` is used only beneath
  that guard; the K downcast and generated sort predicate fix it to the same
  integer. Its concrete/symbolic orientations and idempotence agree on every
  overlap. Although `[total]` gives an uninterpreted value outside the guard,
  no intended-domain execution, branch, summary, or postcondition can observe
  such a case.
- The five `applyCmp`/`applyBin` simplifications are guarded twins of the fixed
  MPY-INT rules. On `isInt(V)`, projection is `V`, so overlapping fixed and
  local right-hand sides are identical. They affect only already evaluated
  mathematical dispatch terms, not binding, evaluation order, control, heap,
  exception, or continuation cells.
- `primeTail` is total: `D < 2`, `D >= 2 and D >= N`, and
  `D >= 2 and D < N` cover all pairs. On the used domain `D >= 2`, its forward
  recurrence states that no divisor in `[D,N)` divides `N`. The divisible
  simplification and the guarded backward fold are consequences of the same
  recurrence. At overlaps, including `D = N`, both orientations agree.
  `D < 2 => false` defines an unused totalization value; it is not asserted to
  characterize a pre-existing predicate there.
- `isPrime(N)` additionally requires `N >= 2`, so it excludes negatives, 0,
  and 1. `selectPrime` has complementary guards. `largestPrime` has disjoint
  empty/integer-head/noninteger-head equations and structurally descends; the
  theorem reaches only its integer-head branch.
- `digitSum` splits `N <= 0` from `N > 0`. On positive `N`, MPY `pyMod(N,10)`
  is in 0 through 9 and the quotient decreases. Its three symbolic folds are
  the defining equality after expanding `pyMod` and, in the last rule, adding
  the unchanged accumulator. All concrete/symbolic overlaps agree.
- There are no local priority rules, opaque program-result symbols, result
  oracles, call interceptions, return shortcuts, operational bridges, or rules
  that encode an example answer. Attribute counts and all exact local rules are
  in
  [local-attributes.log](/audit-output/evidence/static/local-attributes.log).

The loop claims match exact real loop heads and normal continuations. They may
frame an arbitrary suffix because these bodies contain no return, break,
exception, output, allocation, or cleanup effect; fixed execution returns
normally to that suffix. Their scope maps exactly contain the real locals and
parent. All modified locals are represented, while other cells are preserved.

I found no unsound rule. Consequently there is no false-conclusion witness to
report for an unsoundness finding; no rule is labeled unsound on a mere evidence
gap.

## 6. Fresh non-vacuity test

I inspected the candidate mutation only as untrusted evidence and wrote a new
one:
[auditor-false.k](/audit-output/evidence/nonvacuity/auditor-false.k). It executes
the pinned program on the satisfiable input `[3,4]` but requires the real result
plus one. `kprove --dry-run` exits 0, proving that the mutation parses and
builds. The actual proof exits 1 with `WarnStuckClaimState`; its terminal
configuration has `<k> 3 ~> .K </k>` while the destination requires 4. See
[false-dry-run.log](/audit-output/evidence/nonvacuity/false-dry-run.log) and
[false-proof.log](/audit-output/evidence/nonvacuity/false-proof.log).

I separately changed the program term actually loaded and executed:
[auditor-body-mutation.k](/audit-output/evidence/nonvacuity/auditor-body-mutation.k)
initializes `largest` to 2 and calls the mutated function on `[]`, while asking
for the original result 0. The proof exits 1 with a meaningful terminal
configuration containing actual result 2. See
[body-mutation-proof.log](/audit-output/evidence/nonvacuity/body-mutation-proof.log).
This demonstrates dependence on the executed body, not merely on the external
source file.

## 7. Proven versus assumed accounting

What is formally established is:

> Under the supplied MPY semantics, for every finite MPY `ValSeq` all of whose
> elements are MPY `Int` values, if the loaded submitted `skjkasdkd` call
> terminates, its result is `digitSum(largestPrime(VS,0))`, where the proof-local
> recursive equations define ordinary primality, maximum-prime selection, and
> nonnegative decimal digit sum.

The mathematical reading follows by induction over the divisor interval, input
sequence, and decimal quotient. These are result-constraining definitions
connected to fixed execution by the three reconstructed loop reachability
claims; they are not empirical or opaque summaries.

Trust ledger:

- **Supplied reference semantics.** Trusted as the fixed campaign model for
  syntax, evaluation order, scopes, calls/returns, loops, state, and integer
  operators. The reachable subset was statically checked and freshly executed.
  The candidate copy exactly matches the trusted mount.
- **Trusted translator.** Trusted to map the submitted CPython AST subset to
  MPY constructors. Byte regeneration plus the independent 308-token body
  comparison supports this bridge.
- **K toolchain/backends and builtin theories.** K v7.1.293, Haskell/LLVM
  backends, generated sort predicates/downcasts, arbitrary-precision integer,
  Boolean, Map/List, reachability/circularity machinery, and SMT discharge are
  foundational assumptions affecting values, control, and proof closure.
- **Proof-local primitives.** None are externally trusted. There are no opaque
  local symbols or operational bridges. `projectIntTotal` is fully fixed on
  every value admitted by the theorem.
- **Empirical evidence.** The 170,442-case Python differential and finite K
  smoke run support program/docstring/model alignment only. They do not replace
  the universal K proof.
- **Excluded behavior.** Non-integer list elements, Python resource exhaustion,
  and termination complexity are outside the stated contract/theorem.
  `Bool` is a distinct MPY value sort and is not admitted by `allInts`; the
  natural-language request for a list of integers does not require treating
  booleans as integer inputs. There is no material supplied-model
  representation gap for the stated integer domain.

Gate A passes: execution is real, rules are sound on their complete claimed
domains, the result is constrained, and both fresh mutations are rejected.
Gate B passes: the theorem is unbounded over every finite represented integer
list and matches the docstring-determined behavior. Gate C passes: assumptions,
finite evidence, source artifacts, exact commands, statuses, and bounded output
are preserved under `/audit-output/evidence`.

VERDICT: PASS
LEGITIMACY: LEGIT
