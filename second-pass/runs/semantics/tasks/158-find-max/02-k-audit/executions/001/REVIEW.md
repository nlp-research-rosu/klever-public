# Independent adversarial audit: 158-find-max

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MiniPy semantics. Fresh reconstruction closes both
positive claims, the proof executes an exact normalization of the trusted
translator output, the proof-local iterator accelerators have independent
connection theorems, and both a body mutation and a false-result mutation are
rejected.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for three
non-fatal limitations:

1. Four requested generation/provenance records and any structured trace are
   absent.
2. The recursive K summary is clearly the max-by-distinct-count/tie-by-lex
   algorithm, but that summary-to-English argmax fact is justified by an
   ordinary induction in this review rather than a separate K theorem.
3. The prose does not explicitly exclude `[]`, while the trusted canonical
   implementation raises on `[]`; the candidate and formal claim instead
   return `""`. On the canonical nonempty distinct-word domain there was no
   observed or formal mismatch.

No materially unsound or execution-bypassing candidate rule was found.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted directory
[/reference/reference-semantics](/reference/reference-semantics) exists as a
real directory, so the mount does not contradict that mode.

The integrity script and complete output are
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log). Its results
were:

- [/candidate/prompt.py](/candidate/prompt.py) is byte-identical to
  [/reference/prompt.py](/reference/prompt.py).
- [/candidate/py2mpy.py](/candidate/py2mpy.py) is byte-identical to
  [/reference/py2mpy.py](/reference/py2mpy.py).
- A recursive, no-symlink `diff` between the candidate and trusted
  `reference-semantics/` trees exited 0. A relative-path SHA-256 inventory also
  matched exactly. There are no missing, additional, changed, mistyped, or
  symlinked entries in that tree.
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k` are all regular, non-symlink files.
- `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log` are missing.
  No structured generation trace was present. This removes provenance evidence
  but not any source needed for independent reconstruction.
- The extra top-level `__pycache__/`, `concrete-tests.*`, and `prove.sh` are
  outside the supplied-semantics integrity tree and were not trusted as proof
  results.

All executable sources were copied to
`/tmp/audit-work/reconstruction`. No candidate-built definition or cache was
copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical function, the intended entry domain is a
nonempty list of pairwise different strings. The result is a list member with
the largest number of distinct characters; among equal scores, it is the
lexicographically smallest word.

The nonempty condition is implicit rather than explicit in the prose:
[/reference/canonical.py](/reference/canonical.py:16) computes
`sorted(...)[0]`, which raises `IndexError` for `[]`.

### Submitted algorithm

[/candidate/solution.py](/candidate/solution.py) maintains `(best,
max_unique)`. It replaces both on a strictly larger `len(set(word))`, replaces
only `best` on an equal score and lexicographically smaller word, and otherwise
retains the accumulator. For every nonempty string, the first iteration has a
positive score; the empty-string boundary is also handled consistently. This
is a different but faithful implementation of the canonical sort-based
algorithm.

### Trusted translation

The exact command is in
[stage2-translation.log](/audit-output/evidence/stage2-translation.log):

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py
cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy \
    /tmp/audit-work/reconstruction/solution.mpy
```

The translator exited 0 and `cmp` exited 0. Both MiniPy files have SHA-256
`1540848d93ea1f97b3b2355a5bd995a986cba1613b6dba2020b0ab9d8b65d947`.

### Independent differential test

The reviewer-authored test is
[differential_test.py](/audit-output/evidence/differential_test.py). Complete
inputs and outcomes are preserved in
[differential-inputs.json](/audit-output/evidence/differential-inputs.json) and
[differential-results.json](/audit-output/evidence/differential-results.json);
the bounded command output is
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

It independently imports `/reference/canonical.py` and the scratch copy of
`solution.py`. It covers:

- all three documented examples;
- empty list, one-element, empty-string, repeated-character, duplicate-word,
  and Unicode boundaries;
- the `>`, `<`, equal-and-lex-smaller, and equal-and-not-smaller branches;
- all 3,609 ordered distinct selections of length 1 through 4 from a
  nine-word small pool;
- 500 seeded, generated, nonempty distinct-word lists.

Command:

```text
env PYTHONHASHSEED=0 python3 /audit-output/evidence/differential_test.py
```

It exited 0. Of 4,123 cases, 4,121 were on the inferred intended domain and
had zero mismatches. The sole result difference was the deliberately tested
out-of-domain/underspecified empty list: canonical raised `IndexError`;
candidate returned `""`. The duplicate-word probe was also outside the stated
pairwise-different domain, but both returned `"ab"`.

## 3. Clean proof reconstruction

The installed tools are K version `v7.1.337`. Every build used source from the
clean scratch copy.

### Concrete definition

Exact command:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0; see
[stage3-kompile-runtime.log](/audit-output/evidence/stage3-kompile-runtime.log).
The compiler reported non-exhaustive-totality warnings for six families
unreachable from this program; they are accounted for in stages 5 and 7.

The independently built runtime then executed the five submitted smoke cases:

```text
krun concrete-tests.mpy --definition runtime-kompiled --output pretty
```

It exited 0 with `<k> .K </k>`, `NoExc`, and exit code 0; see
[stage3-krun-concrete-tests.log](/audit-output/evidence/stage3-krun-concrete-tests.log).
This concrete run is supporting evidence only, not a substitute for `kprove`.

### Proof definition

Exact command:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0; see
[stage3-kompile-verification.log](/audit-output/evidence/stage3-kompile-verification.log).

The positive claims were checked three ways:

| Target | Isolation command | Result |
|---|---|---|
| Loop invariant | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.find-max-loop-invariant` | exit 0, `#Top` |
| Entry contract, with the separately proved loop claim available as its helper | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.find-max-loop-invariant,SPEC.find-max-contract --trusted SPEC.find-max-loop-invariant` | exit 0, `#Top` |
| Both claims together, with neither trusted | `kprove spec.k --definition verification-kompiled --spec-module SPEC` | exit 0, `#Top` |

The corresponding logs are
[stage3-kprove-loop.log](/audit-output/evidence/stage3-kprove-loop.log),
[stage3-kprove-contract-with-verified-helper.log](/audit-output/evidence/stage3-kprove-contract-with-verified-helper.log),
and
[stage3-kprove-all-claims.log](/audit-output/evidence/stage3-kprove-all-claims.log).

Filtering to the entry claim while deleting its loop circularity was stopped
after 10 seconds with exit 124 and a user-interrupt diagnostic; see
[stage3-kprove-contract-only.log](/audit-output/evidence/stage3-kprove-contract-only.log).
This is a diagnostic showing the expected helper dependency, not a failed
candidate target: the loop claim closes independently and the untrusted
two-claim run closes.

There was no timeout, container failure, or infrastructure uncertainty in any
command used to establish the candidate verdict.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim at [/candidate/spec.k:6](/candidate/spec.k:6) says:

- Start at the real `#loop` control point with any remaining `WordSeq`, any
  string `BEST`, and any integer `SCORE`, in the exact function scope.
- Execute the real translated loop body and then resume the arbitrary
  continuation `KONT`.
- On reaching that continuation, `best` and `max_unique` equal the recursive
  accumulator `findMaxWords(WORDS, BEST, SCORE)`. The final `word` and `unique`
  locals exist but are intentionally not specified.

This is stronger than the reachable entry invariant because it does not assume
that `SCORE` already equals `BEST`'s distinct-character count.

The entry claim at [/candidate/spec.k:50](/candidate/spec.k:50) says:

- Start from the fresh supplied configuration.
- Load the `find_max` definition, call it on a list whose every element is a
  `str(IntSeq)`, and execute the function.
- Return exactly
  `str(bestWord(findMaxWords(WORDS, .IntSeq, 0)))`.
- Restore the caller environment and stack, remove the call scope, preserve an
  empty heap, leave no return/exception state, and retain exit code 0.

There is no implication-only or free-result postcondition.

### Exact program identity

The `<k>` cell embeds `findMaxFunctionBody` rather than reading a filename at
runtime. That alias is not a substitute program:

- the trusted translator regenerated the submitted `solution.mpy` byte for
  byte;
- `findMaxLoopBody` and `findMaxFunctionBody` at
  [/candidate/verification.k:23](/candidate/verification.k:23) and
  [/candidate/verification.k:37](/candidate/verification.k:37) contain the
  same AST;
- reviewer-authored normalization checks compare each alias to the fully
  expanded submitted AST and close with exit 0 and `#Top`.

The pinning definitions and claims are
[audit-pinning-definition.k](/audit-output/evidence/audit-pinning-definition.k)
and [audit-pinning-claims.k](/audit-output/evidence/audit-pinning-claims.k).
Their successful logs are
[stage4-kprove-pinning-loop-v2.log](/audit-output/evidence/stage4-kprove-pinning-loop-v2.log)
and
[stage4-kprove-pinning-function-v2.log](/audit-output/evidence/stage4-kprove-pinning-function-v2.log).
`WarnTrivialClaim` is expected: the aliases normalize to the compared AST
before an operational step.

An initial attempt to state bare functional reachability claims was rejected
because this Haskell backend does not support functional claims; that
reviewer-artifact error is preserved in
[stage4-kprove-pinning-loop.log](/audit-output/evidence/stage4-kprove-pinning-loop.log)
and was replaced by the successful configuration claims above.

### Satisfiable preconditions and concrete substitution

[audit-ground-witness.k](/audit-output/evidence/audit-ground-witness.k) gives
fully ground states for both claims:

- Loop state: the full input is `["ba", "ab"]`, the remaining iterator is
  `["ab"]`, and the current accumulator is `("ba", 2)`. Execution reaches
  `("ab", 2)`.
- Entry state: a fresh configuration calls the actual function on
  `["ba", "ab"]` and requires the exact return `"ab"`.

Both ground claims exited 0 with `#Top`; see
[stage4-kprove-ground-loop.log](/audit-output/evidence/stage4-kprove-ground-loop.log)
and
[stage4-kprove-ground-entry.log](/audit-output/evidence/stage4-kprove-ground-entry.log).
The differential results independently show both Python implementations also
return `"ab"` for this tie-and-lex-smaller input.

The universal formal domain does not require pairwise distinctness or
nonemptiness. That is an over-broad but sound theorem: duplicates do not break
the accumulator, and `.WordSeq` reduces to the empty string result. It does not
make a false conclusion provable on the intended nonempty distinct-word domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-generated inventory is available in full as
[k-rule-inventory.md](/audit-output/evidence/k-rule-inventory.md) and
[k-rule-inventory.json](/audit-output/evidence/k-rule-inventory.json). The
reviewer script and generation log are
[inventory_k.py](/audit-output/evidence/inventory_k.py) and
[stage5-inventory.log](/audit-output/evidence/stage5-inventory.log).

It inventories 27 modules and 958 top-level declarations:

- 234 syntax declarations;
- 716 ordinary/semantic/simplification rules;
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims.

Attribute counts include 151 `function`, 110 `total`, 47 priority, 8
simplification, 22 `no-evaluators`, 25 `symbol`, 26 `owise`, 2 `strict`, and 1
`seqstrict`. There are no local `functional` declarations.

Every one of the 958 entries has an explicit decision and rationale in
[k-rule-assessment.md](/audit-output/evidence/k-rule-assessment.md) and the
machine-readable
[k-rule-assessment.csv](/audit-output/evidence/k-rule-assessment.csv).
The assessment was generated by the reviewer-authored
[assess_inventory.py](/audit-output/evidence/assess_inventory.py); its count
check is in [stage5-assessment.log](/audit-output/evidence/stage5-assessment.log).

The supplied tree contributes the fixed semantics, not candidate proof
extensions. Its unused syntax and rules were still inventoried. For those
entries, `ACCEPT_FIXED_UNREACHABLE` means only that no target-proof execution
can select the rule; it does not claim full Python coverage for unrelated
programs.

### Used-construct map

| Submitted construct | Selected semantics |
|---|---|
| `Module`, statement sequencing, literal `Int`/`Str`, `Name` | `syntax.k`; `core.k` load, sequencing, lookup, literals |
| `FuncDef`, call, parameter bind, `Return` | `functions.k` closure/return/pop; `call.k` callee/argument/frame rules |
| `Assign`, `If`, `For` | `syntax.k` strictness; `controls.k` assignment, branch, `#loop`, bind-target, loop continuation |
| list input and iteration | `list.k` `#iterNext`; proof-local `wordVals` representation and two connected iterator accelerators |
| `set(word)` and `len(...)` | `call.k` builtin resolution; `builtins.k`; `set.k` `dedupCodes`; `core.k` `isLen` |
| integer `>`, `==` and string `<` | ordered comparison contexts in `operators.k`; `int.k`; constructor-defined `strLt` in `str.k` |

Evaluation order is preserved: assignment and branch conditions use strictness;
calls evaluate the callee first and arguments left-to-right; comparison
contexts evaluate the left operand before the wrapped right operand. `set` and
`len` are resolved through the real builtins scope, so the proof does not
bypass name binding.

The call allocates function scope 1, binds `words`, executes the exact body,
and pops back to scope 0. No heap allocation occurs in the target theorem:
the symbolic input is already an unboxed list value and `set(str)` yields the
pure `setV` representation. The claims correctly pin environment, scopes,
scope location, heap, heap location, stack, return state, exception state, and
exit code. Cells omitted from the loop claim are framed and none is changed by
the loop path.

### Candidate-local rules

The 28 declarations in
[/candidate/verification.k](/candidate/verification.k) were checked
individually:

1. `WordSeq`, `wordVals`, and its two constructor equations are an inductive
   typed representation of lists containing only strings. The equations are
   disjoint, exhaustive, and structurally decreasing.
2. The two priority-40 iterator rules are operational accelerators. They
   preserve the arbitrary continuation and touch no state cell. They are
   exactly the empty/nonempty compositions of `wordVals` with the supplied
   list iterator rules.
3. `findMaxLoopBody` and `findMaxFunctionBody` are nullary definitional aliases
   for the exact submitted AST; they do not summarize or skip its execution.
4. `findMaxWords` is a definitional mathematical accumulator. Its empty rule
   and four nonempty guarded rules are pairwise disjoint and exhaustive:
   distinct count is greater, smaller, or equal; the equal case is split by
   `strLt` versus `notBool strLt`. Every recursive call consumes one
   `wCons`.
5. `bestWord` and `bestScore` project the final `bestState`. Their totality is
   valid because total `findMaxWords` normalizes every finite `WordSeq` to that
   constructor.
6. The eight simplification rules repeat the same four guarded summary steps
   under the two projections. Their guards and right-hand sides exactly match
   the underlying equations; overlaps are disjoint.

`dedupCodes`, `isLen`, and `strLt` are fully constructor-defined supplied
functions, not unconstrained candidate oracles. `strLt` remains symbolic when
given an unconstructed `IntSeq`, but its six constructor cases define ordinary
lexicographic order and the program branch and mathematical summary use that
same fixed operation.

The accumulator encodes the requested answer in the postcondition, but it does
not replace program execution. The independently proved loop claim connects
the real loop body and all relevant state changes to that accumulator.

### Operational-bridge validation

The first bridge-free attempt correctly got stuck because ordinary `wordVals`
rules do not reduce under `list(...)`; see
[stage5-kprove-bridge-empty.log](/audit-output/evidence/stage5-kprove-bridge-empty.log).
This established that the candidate rules are genuine accelerators, not
decorative rewrites.

The final bridge-free definition
[audit-bridge-free.k](/audit-output/evidence/audit-bridge-free.k) uses the same
two complete `wordVals` equations, explicitly declared as a total mathematical
function, imports no candidate bridge, and otherwise uses only the supplied
semantics. Its claims in
[audit-bridge-claims.k](/audit-output/evidence/audit-bridge-claims.k) quantify
over the complete arbitrary continuation `KONT`. Both the empty and nonempty
universal connections exited 0 with `#Top`; see
[stage5-kprove-bridge-empty-v2.log](/audit-output/evidence/stage5-kprove-bridge-empty-v2.log)
and
[stage5-kprove-bridge-nonempty-v2.log](/audit-output/evidence/stage5-kprove-bridge-nonempty-v2.log).

An operational-sensitivity mutation changed the mapped word `"a"` to `""`.
The connection artifact built, but its proof exited 1 with
`WarnStuckClaimState`, preserving the observable `Int(7)` continuation; see
[audit-bridge-mutated.k](/audit-output/evidence/audit-bridge-mutated.k) and
[stage5-kprove-bridge-mutated.log](/audit-output/evidence/stage5-kprove-bridge-mutated.log).

### Body sensitivity

A second independent mutation removed the `best = word` update from the
strictly-greater branch. The mutated definition built successfully, but the
loop proof exited 1. Its residual specifically failed to equate summaries
starting from old `BEST` and new `WORD` on the greater-count path. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[stage5-kompile-body-mutated.log](/audit-output/evidence/stage5-kompile-body-mutated.log),
and
[stage5-kprove-body-mutated-loop.log](/audit-output/evidence/stage5-kprove-body-mutated-loop.log).
Thus the connection is sensitive to the executed program body.

### Supplied-semantics limitations

The fresh LLVM build reported incomplete-totality warnings around
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. The detailed
ledger marks every associated declaration/rule `EVIDENCE_GAP_UNUSED`. None is
reachable from `solution.mpy`: the program has no `map`, float operation,
`join`, or subscript. Consequently there is no intended-domain false-conclusion
witness and this review does not label those rules unsound.

The 22 supplied `no-evaluators` opaque symbols are also unreachable:

- `sortVS`, `sortKeyVS`;
- `md5hexCodes`;
- `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.

No candidate-local opaque symbol, fabricated result, answer-returning
operational rule, or unconstrained result-bearing oracle contributes to either
claim.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present or trusted. The fresh mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It retains the real
program and exact fresh entry configuration, fixes the satisfying input to
`["a"]`, and changes only the result obligation from `"a"` to `""`.

The mutation parsed and built successfully:

```text
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-empty-result-for-a \
  --dry-run
```

This exited 0; see
[stage6-mutation-dry-run.log](/audit-output/evidence/stage6-mutation-dry-run.log).

The real mutation proof command omitted `--dry-run`. It exited 1 with
`WarnStuckClaimState`. The residual showed the completed real result
`str(iCons(97, .IntSeq))` (`"a"`) unable to unify with the required
`str(.IntSeq)` (`""`), while all other destination cells matched. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. See
[stage6-mutation-proof.log](/audit-output/evidence/stage6-mutation-proof.log).

The independent witness script
[mutation_witness.py](/audit-output/evidence/mutation_witness.py) confirms that
both Python implementations return `"a"` on `["a"]`; it exited 0 and is
recorded in
[stage6-mutation-witness.log](/audit-output/evidence/stage6-mutation-witness.log).

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MiniPy semantics, for every finite `WordSeq` of `IntSeq`
strings, starting in the exact fresh configuration, if the exact submitted
`find_max` body terminates then it returns:

```text
str(bestWord(findMaxWords(WORDS, .IntSeq, 0)))
```

The helper theorem proves the more general accumulator transition from any
remaining sequence, initial string `BEST`, and integer `SCORE`. The entry
theorem additionally proves the specified environment/scope/heap/stack/return/
exception/exit-code post-state. This is partial correctness; termination is
not the theorem reported here.

By inspection and ordinary induction on `WordSeq`, `findMaxWords` retains the
word with maximum `isLen(dedupCodes(word))` and selects the `strLt`-smallest
word on equal scores. That induction is straightforward and all equations are
in the checked proof theory, but the candidate does not contain a separate K
claim phrased as membership plus a quantified maximum/tie property. This is
the principal intent-bridge concern.

### Trust and assumption ledger

- **Supplied MiniPy semantics:** trusted because it is the required,
  byte-identical `/reference/reference-semantics` baseline. The used path was
  nevertheless inspected for binding, evaluation order, control, allocation,
  state, and return behavior. The unused coverage gaps and opaque symbols are
  listed in stage 5.
- **K implementation and mathematical hooks:** integer, Boolean, string, map,
  list, equality, and reachability-logic backend behavior are the ordinary
  low-level tool trust boundary. Fresh builds and discriminating mutations
  support, but cannot eliminate, that boundary.
- **Trusted translator:** `/reference/py2mpy.py` is an authorized bridge from
  Python source to MiniPy. Its output is byte-identical to the submission.
- **String model:** formal inputs are arbitrary integer-code sequences and
  `strLt` compares integers lexicographically. This agrees with Python's
  code-point ordering on tested Unicode inputs, but the audit does not provide
  a universal Python-runtime encoding theorem. The program's only source
  string literal is ASCII `""`.
- **Recursive-summary meaning:** the max/tie interpretation is an informal
  induction over truthful, complete equations, not a separately named K
  theorem.
- **Finite empirical bridge:** 4,121 intended-domain differential cases give
  zero mismatches. This supports Python implementation equivalence only on
  those cases and is not used as a replacement for the K proof.
- **Generation provenance:** the four requested metadata/log files and any
  structured trace are missing. Independent source comparisons and clean
  reconstruction compensate for theorem legitimacy, but not for generation
  auditability.

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent
adequacy) is substantively met but has the explicit summary-to-argmax and empty
boundary limitations above. Gate C has reproducible reviewer evidence, but the
candidate-supplied provenance record is incomplete. These limitations justify
`CONCERNS` while leaving the proof `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
