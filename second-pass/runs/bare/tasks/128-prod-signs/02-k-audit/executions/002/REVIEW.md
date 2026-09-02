# Independent adversarial review: 128-prod-signs

The candidate does not contain a K reachability theorem establishing the
HumanEval result for arbitrary nonempty integer lists. Its submitted claims are
sound, close cleanly, execute the real translated program, and reject a false
fixed-example result. But the only symbolic nonempty entry claim stops at loop
initialization with `noResult`; the loop claims prove one iteration at a time
and an exit from arbitrary accumulators without a formal invariant connecting
those accumulators to the original input. Complete entry-to-result claims cover
only the empty input and three fixed nonempty examples.

That is a material narrowing of an unrestricted source contract. Under the
benchmark-specific decision boundary, the corresponding Kit status would be
`SOUND-BUT-LIMITED`, and it maps to `FAIL / NOT_LEGIT`, not to a concern-level
legitimate proof.

## 1. Input and provenance integrity

Infrastructure integrity passed; there is no audit-error condition.

- `/audit-input.json` is readable and declares problem `128-prod-signs`,
  condition `bare`, `record_layout` `legacy-selected-stage1`, and
  `semantics_mode` `GENERATED_SEMANTICS`. Container paths, not host-only paths,
  were used.
- `/audit-campaign-lock.json` is a regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed content exactly equals the `audit_campaign` block.
- All records required for `legacy-selected-stage1` are present and regular:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` is present and was
  checked. The never-recorded `runtime-metrics.json` is absent, which is
  permitted for this historical layout.
- Every declared regular-file hash checked in
  [01-provenance.log](/audit-output/evidence/01-provenance.log) matches.
  Independent recursive generation-workspace hashing of `/candidate` gives
  `f332312aed44c82c7d4c1f812a8d530f83ddd6657f3b3ac70ff7aae3ef09fcf1`,
  matching both `generation-result.json` and `invocation.json`. The trace tree
  digest is
  `fdefc470aa8ba88b0e1076d5b8cbe3bfd6ac1f90fe418ce629554cfb5d6f6190`,
  matching `usage.json`; its sole JSONL file also matches the independently
  checked per-file digest in the invocation records.
- The structured trace contains 135 parseable JSON records. The complete
  generation output and last-message files were read and hash-checked. Their
  `KPROVE_PASSED` assertion was treated only as an untrusted historical claim.
- No linked or unsupported entry occurs under `/candidate`,
  `/generation-evidence`, or `/reference`. The candidate contains one
  `__pycache__` file; it was inventoried but never copied into or used by the
  reconstruction.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The generated-semantics boundary is consistent:
  `/reference/reference-semantics` does not exist. No hidden or inferred
  reference semantics was used.
- The mandated `/kit-skills` copies of `using-kit`, `validating-proof`, and
  `writing-semantics` are byte-identical to the loaded approved skill files.

The reproducible checker is
[provenance_check.py](/audit-output/evidence/provenance_check.py). The
candidate, generation evidence, and launcher manifests remained read-only.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract is: for an arbitrary finite list of integers, return
`None` when the list is empty; otherwise return the sum of all absolute values
multiplied by the product of each element's sign, where a sign is `-1`, `0`, or
`1`. The domain has no stated list-length or integer-magnitude bound.

[solution.py](/candidate/solution.py:1) uses `total` for the sum of magnitudes
and `sign` for the product of signs. Its negative, zero, and positive branches
implement the trusted formula. It is a different but faithful algorithm from
[canonical.py](/reference/canonical.py:6).

Trusted regeneration:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/regenerated-solution.mpy
```

exited 0. Both the submitted and regenerated files have SHA-256
`f89ded5d120c6c7181dbb71b22dbf7bb07017c9989de832e6b7c9a820ff683d0`,
and `cmp` exited 0. See
[02-translation.log](/audit-output/evidence/02-translation.log).

The independent differential test imports the trusted canonical entry point
and the candidate entry point separately. It checked the documented examples,
empty input, each sign-branch singleton, zero placement, odd/even negative
parity, very large unbounded integers, all lists of lengths 0 through 5 over
`[-3,3]` (19,608 cases), and 2,000 seeded lists of lengths 0 through 40.
There were 21,620 comparisons and zero mismatches against both canonical
Python and an independently written mathematical formula. See
[differential_test.py](/audit-output/evidence/differential_test.py) and
[03-differential.log](/audit-output/evidence/03-differential.log). This is
strong finite fidelity evidence, not a universal proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/fresh`. Candidate compiled
definitions and caches were not present or reused. The observed K toolchain is
K v7.1.293.

The generated concrete semantics was rebuilt with:

```text
kompile semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --backend llvm \
  --output-definition semantics-kompiled
```

Exit was 0
([04-kompile-semantics.log](/audit-output/evidence/04-kompile-semantics.log)).
Fresh `krun` executions terminated with `.K` and the Python-matching results
`none`, `-1`, `0`, `1`, `-9`, `0`, `3`, and `-6` for the recorded empty and
branch/boundary cases
([05-krun-boundaries.log](/audit-output/evidence/05-krun-boundaries.log)).
A second executable checker decoded the K `<result>` cell and compared it
directly with trusted Python on 12 normal/boundary cases, including a
35-digit-magnitude case; all `krun` exits were 0 and there were zero
mismatches. See
[k_semantics_diff.py](/audit-output/evidence/k_semantics_diff.py) and
[06-k-semantics-differential.log](/audit-output/evidence/06-k-semantics-differential.log).

The proof definition was rebuilt with:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition verification-kompiled
```

Exit was 0
([07-kompile-verification.log](/audit-output/evidence/07-kompile-verification.log)).
The submitted aggregate command

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`
([08-kprove-all.log](/audit-output/evidence/08-kprove-all.log)).

For independent per-claim checking, audit-only labels were added without
changing any claim. Normalized source equivalence is recorded in
[09a-labeled-claim-equivalence.log](/audit-output/evidence/09a-labeled-claim-equivalence.log).
Each of all nine claims was selected separately with `--claims`; each exited 0
and printed `#Top`
([09-kprove-individual.log](/audit-output/evidence/09-kprove-individual.log)).
Thus clean reconstruction succeeds for exactly the claims the candidate
submitted.

## 4. Adequacy and real-program pinning

Program pinning passes. `solutionProgram` expands to `solutionBody`, which
expands to `solutionLoopBody`; parsing the fully expanded term and the
trusted-regenerated `solution.mpy` gives identical constructor ASTs. See
[program_term_compare.py](/audit-output/evidence/program_term_compare.py) and
[10-program-term-compare.log](/audit-output/evidence/10-program-term-compare.log).
The differences are only explicit empty-list nonterminal spellings
(`.Exprs`/`.Stmts`) versus their empty concrete constructor slots.

A body-sensitivity mutation changed the positive branch inside
`solutionLoopBody` from addition to subtraction. This changes the program term
actually executed by the claims, rather than merely changing an external
source file. The mutated proof definition built successfully, but `kprove`
exited 1 with `WarnStuckClaimState` at the positive-step obligation
`T -Int X = T +Int X` under `X >Int 0`. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k)
and [11-body-sensitivity.log](/audit-output/evidence/11-body-sensitivity.log).

The nine submitted claims say:

| Claim | Preconditions and postcondition | Satisfying witness |
|---|---|---|
| Empty entry | Fresh state and `input()` execute the real program to `result(contract(.Ints)) = result(none)` | `[]`; both Python implementations return `None` |
| Nonempty initialization | Fresh state and `input(X,IS)` reach the real loop with `total=0`, `sign=1`, `x=0`, still `noResult` | `[2]` |
| Negative step | At a loop head with `X<0`, one iteration adds `magnitude(X)` and multiplies by `integerSign(X)` | Reachable head for `[-2]` |
| Positive step | The analogous one-iteration relation under `X>0` | Reachable head for `[2]` |
| Zero step | The analogous one-iteration relation under `X=0` | Reachable head for `[0]` |
| Loop exit | From an empty tail and arbitrary `T,S`, the actual return expression produces `T*S` | State after `[2]`, `T=2`, `S=1` |
| Fixed example 1 | Exact input `[1,2,2,-4]` returns `contract(...)=-9` | Both Python implementations return `-9` |
| Fixed example 2 | Exact input `[0,1]` returns `contract(...)=0` | Both Python implementations return `0` |
| Fixed example 3 | Exact input `[-1,-2,-3]` returns `contract(...)=-6` | Both Python implementations return `-6` |

The detailed precondition/postcondition and witness accounting is in
[claim-adequacy.md](/audit-output/evidence/claim-adequacy.md).

The critical omission is an entry claim for arbitrary `IS:Ints` that reaches
`result(contract(IS))`. The symbolic initialization claim stops before even
one iteration. The step claims forget the original list and do not state an
invariant relating the consumed prefix, remaining suffix, `total`, and `sign`.
The exit claim permits arbitrary `T,S`. Those true local facts can validate
each chosen finite unrolling, but the submitted K proof contains no induction
or circularity connecting an unrestricted number of iterations to the
contract.

An audit-authored statement of the missing unrestricted theorem,
[spec-intended.k](/audit-output/evidence/spec-intended.k), dry-runs
successfully but does not close: `kprove` exits 1 with a genuine
`WarnStuckClaimState`
([12-missing-universal-target.log](/audit-output/evidence/12-missing-universal-target.log)).
That failed audit probe is not used as evidence that the true theorem is
false; it demonstrates that the submitted definition and claims do not contain
its proof.

Therefore the result is constrained only for the empty list and three exact
nonempty lists. For example, Python and fresh K all return `2` on `[2]`, but no
submitted complete entry claim states that result. This is a material
finite-example restriction of the source-contract domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). It enumerates
every local syntax declaration and configuration cell, all 14 internal
computation forms, all 36 `semantic.k` rules, and all 14 `verification.k`
equations. It also maps every constructor in `solution.mpy` to syntax and
behavior.

Static findings:

- The configuration has only the state this program needs: computation,
  external integer-list input, the selected function, local bindings, and
  result.
- Module boot, single-function selection, entry binding, statement order,
  assignment, conditionals, finite list iteration, returns, lookup, integer
  literals, `None`, empty-list comparison, unary minus, arithmetic, and integer
  comparison all have faithful used-domain rules.
- Evaluation is left-to-right. Loop state is threaded in order. Existing-map
  update and missing-key insertion guards are disjoint. Return evaluates its
  expression, records the value, and discards the single-frame continuation,
  which is the correct abrupt effect for this generated single-function
  language.
- Deliberately unsupported unused language forms get stuck. In generated
  semantics mode this is acceptable minimal coverage, not a defect.
- `magnitude`, `integerSign`, `sumMagnitudes`, `productSigns`, and `contract`
  are fully defined mathematical functions. Their guarded cases are
  exhaustive and pairwise disjoint; list recursion structurally descends.
- `solutionLoopBody`, `solutionBody`, and `solutionProgram` are transparent
  constructor constants, not execution shortcuts. Their equations do not
  inject a result.
- There are no local priorities, simplification rules, `[functional]`
  declarations, opaque symbols, result-bearing oracles, task-answer rules, or
  operational bridges that bypass material program execution.

No materially false local rule was found. Consequently no unsoundness label is
made and no false-conclusion witness is required for a rule. The failure
verdict rests on the missing unrestricted theorem, not on an alleged semantic
inconsistency.

## 6. Fresh non-vacuity test

The candidate supplied no mutation that was relied on. The fresh mutation
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) preserves the real
program and the satisfying input `[1,2,2,-4]` but changes the required result
from the true `-9` to the false `-8`.

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, establishing that the mutation builds. The corresponding proof
command exited 1 with `WarnStuckClaimState`; its residual completed
configuration contains actual `result(-9)` and cannot unify with required
`result(-8)`. See
[13-false-result-mutation.log](/audit-output/evidence/13-false-result-mutation.log).
This is meaningful non-vacuity evidence for the fixed example's result
constraint. It does not create the absent all-input claim.

## 7. Proven versus assumed accounting

What the successful reachability proofs formally establish, under the submitted
generated semantics and K built-ins:

- Empty input executes the pinned program and returns `none`.
- Every symbolic nonempty input executes the entry prefix and reaches the
  initial loop state.
- One loop iteration has the stated accumulator transition separately for
  negative, positive, and zero heads.
- Once the tail is empty, the program returns the product of whatever
  accumulator values are present.
- The three fixed nonempty inputs execute end to end and return `-9`, `0`, and
  `-6`.

What they do not formally establish:

- For every arbitrary nonempty finite integer list, the final accumulators
  equal `sumMagnitudes(input)` and `productSigns(input)`.
- Consequently, there is no submitted K theorem that the unrestricted
  nonempty entry returns `contract(input)`.
- An informal induction that composes the one-step facts is not encoded or
  machine checked and cannot substitute for the missing reachability claim.

Trust and evidence ledger:

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 compiler/prover and imported `INT`, `BOOL`, `STRING`, `MAP` theories | All executions and claims | Ordinary low-level proof trust boundary; acceptable. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Accepted trusted input; byte regeneration proves exact submitted-term identity. |
| `input(IS)` represents an external Python list of integers as `listVal(IS)` | All entry claims | Explicit generated-language entry boundary. Static representation is exact for ordered integer lists; finite K/Python comparisons support it. |
| Generated semantics corresponds to the used CPython subset | Program-level interpretation of K results | Audited rule by rule and supported by 12 direct K/Python boundary cases. No material used construct is omitted. |
| Candidate Python corresponds to trusted canonical Python | Rewrite-to-reference bridge | Supported by 21,620 independent finite tests and direct algorithm review; tests alone are not treated as universal proof. |
| Mathematical `contract` corresponds to the English prompt | Claimed result meaning | Direct transparent definitions using magnitude sums and sign products; acceptable ordinary mathematics. |

There are no opaque or empirical result primitives. Differential tests,
constructor comparison, and mutation tests support only their stated bridges;
none is counted as a substitute for the absent universal K claim.

Gate summary:

- Clean verification of submitted claims: PASS.
- Real-program pinning and local proof-extension soundness: PASS.
- Generated semantics coverage and soundness for every used construct: PASS.
- Non-vacuity of submitted fixed result obligations: PASS.
- HumanEval intent/domain adequacy: FAIL, because the unrestricted nonempty
  entry-to-result theorem is missing and only finitely many complete nonempty
  executions are proved.
- Evidence auditability: PASS.

The precise command list and exit statuses are preserved in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md). Because the adequacy failure
materially narrows the HumanEval contract to finitely many complete cases, the
benchmark requires the following terminal classification.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
