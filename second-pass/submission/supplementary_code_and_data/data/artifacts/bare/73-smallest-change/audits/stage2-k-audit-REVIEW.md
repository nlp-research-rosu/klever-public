# Adversarial review: 73-smallest-change

The candidate's fresh `#Top` is reproducible, and the submitted program body is
not substituted. However, the claims do not prove partial correctness of
`smallest_change` for the source-contract domain. They prove three single-step
case transitions, three definitional recurrences, and three fixed examples.
There is no claim connecting a complete execution on a symbolic input to
`minimumPalindromeChanges(L)` (or to any other result-specifying expression).
This is a material theorem-adequacy failure.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. The generated
semantics boundary is consistent: `/reference/reference-semantics` does not
exist. No hidden or inferred reference semantics was used.

I independently inspected `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, all records required for
the selected legacy layout, the optional recorded `usage.json`, the complete
structured trace, and the candidate/reference trees. Historical runtime metrics
are not required for this layout and were not reconstructed.

The following integrity checks passed:

- `/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block in
  `/audit-input.json`, and its SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required mounted record exists, is readable, and is not a symlink.
  Every launcher-declared individual file hash checked by the reviewer matches.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The one trace file has its declared SHA-256 and all 528 lines parse as JSON.
  The generation-result and invocation evidence maps agree, including all
  hashes for the trace, prompt, usage, legacy records, final message, and output
  log.
- Every candidate entry was independently enumerated and hashed. There are no
  candidate symlinks. The launcher does not document the serialization used for
  its aggregate directory hashes, so the audit relies on the stronger
  per-entry inspection plus every declared per-file/evidence hash rather than
  guessing an aggregate-tree serialization.

The generation log's claims of `#Top`, concrete examples, and 4,000 tests were
treated only as untrusted history. The audit reconstructed them independently.
Full integrity output is in
[`01-provenance.log`](/audit-output/evidence/01-provenance.log); tool versions
are in [`01-tool-versions.log`](/audit-output/evidence/01-tool-versions.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for the minimum number of element replacements needed
to make a finite integer array palindromic. Equivalently, the answer is the
number of mirrored index pairs whose current elements differ. The trusted
canonical implementation iterates over the first half and counts those
mismatches.

The candidate implements the same recurrence: return zero for length at most
one; otherwise strip the two endpoints, add zero if they agree, and add one if
they differ. Trusted regeneration with:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/73-smallest-change-fresh/solution-regenerated.mpy
cmp /tmp/audit-work/73-smallest-change-fresh/solution-regenerated.mpy /candidate/solution.mpy
```

exits 0, establishing byte identity
([`02-translator-regeneration.log`](/audit-output/evidence/02-translator-regeneration.log)).

The independent differential test covers the three documented examples, nine
explicit boundary/branch cases, every list over `{-1,0,1}` at lengths 0 through
9, and 10,000 deterministic random lists of lengths 0 through 80 with large
integers. Those 39,536 ordinary cases have no mismatch. The final test also
adds unbounded-domain length probes. At CPython's recorded recursion limit
1,000, a length-1,990 all-zero list still agrees, while both length-2,000 probes
diverge:

- canonical returns `0` for 2,000 zeros; candidate raises `RecursionError`;
- canonical returns `1000` for a length-2,000 alternating list; candidate
  raises `RecursionError`.

The exact deterministic script and result are
[`differential_test.py`](/audit-output/evidence/differential_test.py) and
[`02-differential.log`](/audit-output/evidence/02-differential.log). The earlier
small-only zero-mismatch run is preserved rather than hidden in
[`02-differential-small-only.log`](/audit-output/evidence/02-differential-small-only.log).
For partial correctness this exceptional boundary does not by itself refute a
theorem conditional on normal termination, but it is a real implementation and
language-model boundary because the source contract states no maximum length.

## 3. Clean proof reconstruction

Only source files were copied to
`/tmp/audit-work/73-smallest-change-fresh`; no candidate-built definition or
cache was copied. K 7.1.293 was used.

Fresh Haskell builds both exit 0:

- generated semantics:
  [`03-kompile-semantic.log`](/audit-output/evidence/03-kompile-semantic.log);
- proof definition:
  [`03-kompile-verification.log`](/audit-output/evidence/03-kompile-verification.log).

Thirteen concrete executions of the actual regenerated `solution.mpy` under the
fresh generated semantics cover empty/singleton lists, equal and unequal
length-two and length-three boundaries, negative and arbitrary-precision
integers, and all prompt examples. Every `krun` exits 0, and every K result
equals both Python implementations
([`semantic_differential.py`](/audit-output/evidence/semantic_differential.py),
[`03-semantic-differential.log`](/audit-output/evidence/03-semantic-differential.log)).
The reviewer's initial parser expected bare `0` rather than K's `0 ~> .K`
rendering; that reviewer-script failure and the corrected rerun are both
preserved.

A length-2,000 K probe was killed with exit 137 while K's Java parser processed
the 24,007-character configuration argument
([`03-semantic-long-boundary.log`](/audit-output/evidence/03-semantic-long-boundary.log)).
This is a resource/infrastructure-limited probe. It is not treated as a
candidate proof failure and contributes nothing to the verdict.

The exact submitted proof run exits 0 and prints `#Top`
([`03-kprove-all.log`](/audit-output/evidence/03-kprove-all.log)). It also emits
`WarnTrivialClaim` for all three mathematical-recurrence claims. I made a
metadata-only labelled copy of the nine exact claims and ran each separately.
Every individual command exits 0 and prints `#Top`; the logs are
`03-kprove-claim-*.log`, and the labelled source is
[`spec-labelled.k`](/audit-output/evidence/spec-labelled.k).

Thus reconstruction succeeds for exactly the claims the candidate submitted.
The defect is what those claims say, not a failure to reproduce their closure.

## 4. Adequacy and real-program pinning

### Submitted claim meanings

The nine claims in `/candidate/spec.k` state:

| Claims | Preconditions | Postcondition actually proved | Satisfying witness |
|---|---|---|---|
| Program base | `size(L) <= 1` | one body execution reaches `finish(0)` | `[]` |
| Program equal | `size(L) > 1` and endpoints equal | one body execution reaches `recur(body, range(L,1,1), body)` | `[7,7]` |
| Program unequal | `size(L) > 1` and endpoints unequal | one body execution reaches that `recur` followed by `addResult(1)` | `[7,8]` |
| Mathematical base/equal/unequal | the same three case guards | `minimumPalindromeChanges` rewrites by its own defining equation | `[]`, `[7,7]`, `[7,8]` |
| Three examples | fixed prompt lists | concrete execution reaches `finish(4)`, `finish(1)`, or `finish(0)` | the fixed list in each claim |

The witness values agree with both Python functions
([`04-claim-witnesses.log`](/audit-output/evidence/04-claim-witnesses.log)).

The body abbreviation is honest. A reviewer-authored mechanical comparison
normalizes whitespace and explicit empty `.Stmts` lists, reconstructs
`Module(FuncDef("smallest_change", Params("arr"), BODY))` from the
`#smallestChangeBody` equation, and obtains exact constructor equality with
submitted `solution.mpy`
([`constructor_compare.py`](/audit-output/evidence/constructor_compare.py),
[`04-constructor-compare.log`](/audit-output/evidence/04-constructor-compare.log)).
A body-sensitivity mutation changing the executed unequal branch from
`1 + recurse` to `2 + recurse` builds, but its corresponding claim fails at an
`addResult(2)` residual
([`verification-body-mutation.k`](/audit-output/evidence/verification-body-mutation.k),
[`05-body-mutation-kprove-expected-failure.log`](/audit-output/evidence/05-body-mutation-kprove-expected-failure.log)).
There is therefore no substituted-program defect in the local claims.

The fatal gap is result adequacy. The equal and unequal general claims stop
before the recursive call executes. They neither constrain a final `<result>`
cell nor reach `finish(minimumPalindromeChanges(L))`. The separate mathematical
claims do not mention `run`, `recur`, the program body, or a returned value; K
warns that they prove trivially because their RHS is already installed as a
simplification equation. No circularity or auxiliary connection claim relates
recursive program execution to that mathematical function.

To expose the exact missing obligation, I added a diagnostic claim—outside the
candidate—that starts at the mechanically identical complete
`Module/FuncDef`, consumes the program, and requires
`<result> minimumPalindromeChanges(L) </result>`. It parses successfully but
fails with `WarnStuckClaimState` at a symbolic recursive `run` and an unchanged
`.K` result:
[`spec-intended-audit.k`](/audit-output/evidence/spec-intended-audit.k) and
[`04-intended-claim-kprove-expected-failure.log`](/audit-output/evidence/04-intended-claim-kprove-expected-failure.log).
This diagnostic failure is not substituted for the audit of the submitted
claims; it documents the residual their theorem set leaves.

## 5. Rule-by-rule static soundness review

There are no generated helper K files besides `semantic.k`. Numbered source
copies are preserved in `05-semantic-numbered.log`,
`05-verification-numbered.log`, `05-spec-numbered.log`, and
`05-solution-mpy-numbered.log`.

### Syntax, configuration, and attributes

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- list sorts `Stmts`, `Exprs`, `Strings`, and `CmpOps`;
- statements `FuncDef`, `If`, and `Return`;
- `Params` and `CmpOp`;
- expressions `Int`, `Name`, `Call`, `Compare`, `Subscript`, `Slice`,
  `UnaryOp`, `BinOp`, and `NoBound`.

This covers every constructor in submitted `solution.mpy`: module/function
binding, two `If`s, returns, `len`, comparisons, indexing at `0` and `-1`,
the `[1:-1]` slice, recursive calls, and integer addition. Missing syntax for
other Python constructs is acceptable in generated-semantics mode because the
program does not use it.

The configuration has exactly `<k>`, immutable `<input>`, and `<result>` under
`<mpy>`. Runtime symbols are `run`, `recur`, `finish`, `addResult`,
`eval [function]`, `truth [function]`, and `concatStmts [function]`.
Verification adds `minimumPalindromeChanges(List) [function,total]` and
`#smallestChangeBody [function]`. There are no local opaque/oracle symbols,
priority rules, `functional` declarations, or other proof modules. The sole
strategy attribute is `[concrete]` on recursive continuation; the three
mathematical equations are `[simplification]`.

### Exhaustive operational and equational rule inventory

| ID and source | Rule | Assessment |
|---|---|---|
| S1, semantic 63 | `concatStmts(.Stmts,S2) => S2` | Sound empty-list equation. |
| S2, semantic 64 | prepend the head and recurse on statement tail | Sound, descending, and disjoint from S1. |
| S3, semantic 66–68 | exact submitted module/function/parameter binding starts `run(BODY,L,BODY)` | Sound for the closed submitted module; it deliberately does not model a general Python environment. |
| S4, semantic 72–75 | length guard true: prepend `THEN` | Sound and preserves the arbitrary K continuation. |
| S5, semantic 76–79 | length guard false: prepend `ELSE` | Sound; guard is complementary to S4 for finite K lists. |
| S6, semantic 80–85 | endpoint equality: prepend `THEN` | Sound for integer elements and reached only after length exceeds one. |
| S7, semantic 86–91 | endpoint inequality: prepend `ELSE` | Sound and complementary to S6 on the intended integer-list domain. |
| S8, semantic 93 | `Return(Int(I))` discards remaining statements and yields `finish(I)` | Sound return control for the used body. |
| S9, semantic 94–95 | exact recursive return evaluates its slice and yields `recur` | Sound for the closed self-binding used here; global rebinding and Python exceptions are outside this model. |
| S10, semantic 96–99 | exact `I + recursive-call` schedules `addResult(I)` | Correct left integer and continuation behavior for the submitted expression. |
| S11, semantic 102 | ground `[concrete]` `recur` resumes the same body | Ground execution is body-faithful. The attribute intentionally prevents symbolic recursion; it fabricates no value, but leaves the needed general theorem unproved. |
| S12, semantic 103 | `finish(I) ~> addResult(N)` yields `finish(N+I)` | Sound integer continuation equation. |
| S13, semantic 104–105 | terminal `finish(I)` writes result `I` | Sound and only matches an empty result cell and no remaining K continuation. |
| S14, semantic 108 | evaluate integer literal | Sound. |
| S15, semantic 109–110 | evaluate unary minus | Sound for integer-valued operand. |
| S16, semantic 111–112 | evaluate integer `+` | Sound for integer-valued operands. |
| S17, semantic 113 | `len(arr)` is K-list size | Sound for the list input. |
| S18, semantic 114–115 | list subscript uses K indexing | Sound for the used valid indices `0` and `-1`; out-of-range Python exceptions are not modeled but are unreachable in the submitted body after its length guard. |
| S19, semantic 116–119 | slice becomes `range(L,LOW,0-HIGH)` | Sound for the only submitted form `[1:-1]`, yielding `range(L,1,1)`. Its syntactic match is broader than its justification: arbitrary positive upper bounds and Python's clamping behavior are not generally modeled. No input to the fixed submitted program can change the slice constructor, so there is no intended-domain false-result witness; this is recorded as a reuse/evidence gap, not labelled a material unsoundness. |
| S20, semantic 122–123 | integer `<=` truth | Sound where the integer projections are defined; unused by the specialized statement rules. |
| S21, semantic 124–125 | integer equality truth | Sound where the integer projections are defined; unused by the specialized statement rules. |
| V1, verification 11–12 | minimum changes is zero at sizes 0/1 | Mathematically sound. |
| V2, verification 13–16 | equal endpoints contribute zero and strip one from each side | Mathematically sound, strictly descending, and guard-disjoint from V1/V3 on integer lists. |
| V3, verification 17–20 | unequal endpoints contribute one and strip one from each side | Mathematically sound: each mismatched disjoint mirrored pair needs at least one edit and one edit suffices. |
| V4, verification 25–38 | `#smallestChangeBody` expands to the literal submitted body | Sound exact abbreviation, mechanically checked above. |

The `[total]` declaration on `minimumPalindromeChanges` is justified by V1–V3
for the intended domain of lists whose elements are integers, with descent by
two. At the broader raw K sort `List`, non-integer endpoint projections are not
covered. Because such lists violate the source contract, this creates no false
conclusion witness on the intended domain; it is nevertheless an over-broad
formal declaration and a reuse limitation.

The nine claims were also inventoried. Program claims P1–P3 are the three sound
local transitions described in Stage 4; M1–M3 merely replay V1–V3 and are
reported by K as trivial; E1–E3 are sound fixed concrete executions. There is
no hidden lemma, simplification, operational bridge, or oracle connecting either
P2/P3 or E1–E3 to a universal final result.

No materially unsound local rule on the intended integer-list executions is
asserted in this review. The rejection rests on the missing theorem, for which a
false-rule witness is neither necessary nor fabricated.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so none was trusted. The fresh
mutation changes the first documented example's required terminal value from
`finish(4)` to the demonstrably false `finish(5)`.

The mutation source is
[`spec-vacuity-audit.k`](/audit-output/evidence/spec-vacuity-audit.k).
`kprove --dry-run` exits 0, establishing successful parsing/build
([`06-vacuity-dry-run.log`](/audit-output/evidence/06-vacuity-dry-run.log)).
The real proof exits 1 with `WarnStuckClaimState`; its residual is exactly
`finish(4)` against the required `finish(5)`
([`06-vacuity-kprove-expected-failure.log`](/audit-output/evidence/06-vacuity-kprove-expected-failure.log)).

This proves that the concrete example claim is result-constraining and
non-vacuous. It cannot compensate for the absence of a symbolic final-result
claim.

## 7. Proven versus assumed accounting

What the successful reachability proof establishes:

1. For a symbolic list satisfying one of the three outer guards, one execution
   of the exact submitted body reaches the corresponding base result or
   recursive cutpoint.
2. The locally defined mathematical function obeys its own three recurrence
   equations.
3. The three prompt examples execute to `4`, `1`, and `0` under this generated
   semantics.

What it does **not** establish:

- that symbolic recursion ever reaches a result;
- that a normally terminating symbolic execution returns
  `minimumPalindromeChanges(L)`;
- that `minimumPalindromeChanges` is connected to program execution at all;
- a result theorem for every finite integer list;
- CPython exception/control behavior at recursion-depth boundaries.

Trust and evidence ledger:

| Boundary | Dependents | Status |
|---|---|---|
| K 7.1.293 `INT`, `BOOL`, `LIST`, `K-EQUAL`, including arithmetic, size, indexing, `range`, projections, and the Haskell prover | all semantics and claims | Ordinary low-level trusted primitives; version recorded, not reproved locally. |
| Trusted `/reference/py2mpy.py` | source-to-`solution.mpy` identity | Acceptable: byte identity was independently regenerated. |
| Generated minimal Python subset semantics | all program claims | Informally audited rule-by-rule and supported by 13 short concrete K/Python comparisons; not a universal Python-semantics connection theorem. |
| Closed self-binding and absence of Python recursion-limit exceptions | recursive K execution | A model boundary. The actual Python length-2,000 witness raises `RecursionError`; the attempted matching K probe was resource-killed and is not used as proof evidence. |
| Informal combinatorial meaning of `minimumPalindromeChanges` | only the mathematical recurrence claims, because the program claims never reference it | The recurrence is ordinary mathematics and appears truthful, but its human-facing meaning is not machine-proved here. |
| Differential tests | implementation/semantics bridge on tested inputs only | Finite evidence: 39,536 ordinary Python cases agree, two unrestricted-length Python cases diverge, and 13 short K cases agree. It never substitutes for a K theorem. |

Under the Kit terminology, the submitted theorem set is locally sound but
materially limited: it contains no unrestricted final-result theorem. The
benchmark's decision boundary explicitly maps such material HumanEval
source-contract narrowing/omission to `FAIL / NOT_LEGIT`, not to a concern-only
verdict. The primary failure is therefore theorem adequacy, even though the
candidate's narrower claims genuinely print `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
