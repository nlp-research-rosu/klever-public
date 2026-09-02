# Independent adversarial audit: 47-median

## Executive finding

The candidate contains a legitimate, unbounded partial-correctness proof of
the submitted `median` body under the supplied MPY semantics. I rebuilt the
definition from source, proved all ten positive claims independently, matched
the proof closure to the trusted translation at constructor level, exercised
every claim precondition with a concrete witness, changed the executed body
and observed the theorem fail, and separately observed a false result
postcondition fail only after execution reached the correct result.

The result is `CONCERNS / LEGIT`, not `PASS`, for two reasons. First, the
docstring contradicts itself: its second example says `15.0`, whereas the
ordinary meaning of median and its two sorted center elements give `8.0`.
The candidate explicitly reports that contradiction and defensibly follows
the ordinary definition, which is exactly the campaign's
canonical-vs-docstring exception. Second, the supplied proof model leaves
sorting, access into a symbolic sorted sequence, and floating-point operations
as fixed opaque primitives. The K proof threads their exact terms but does not
itself prove their CPython meanings. These are disclosed, non-fatal trust
boundaries, not candidate rules encoding the answer.

I used the mandatory `using-kit` workflow followed by `validating-proof`.
Their proof-extension, body-sensitivity, non-vacuity, and trust-boundary checks
determined the reconstruction and mutation tests below. I did not use
`writing-semantics`, because this is `SUPPLIED_SEMANTICS`.

The complete command/status index is
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3` and
`SUPPLIED_SEMANTICS`. The required trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
mount topology agree.

I independently read and hashed `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all seven required top-level generation-evidence
records, and the structured trace. Every launcher-recorded hash matched. The
campaign JSON in the lock is exactly equal to the campaign block in
`audit-input`, and the lock hash matches. The sole declared trace file is the
sole mounted trace file; all 487 JSONL records parse. No required record is
missing, unreadable, mistyped, or symlinked.

The candidate prompt and translator are byte-identical to the trusted mounted
versions. Recursive comparison found 25 entries in each supplied-semantics
tree, with identical paths, entry types, and bytes; there are no missing,
additional, changed, or symlinked entries. The common independent semantics
manifest SHA-256 is
`f4020fabc480d2694ef5ec4f342ac501a3b8612c8d6b2a324604bd41e331f406`.
No candidate semantic modification is therefore in the proof.

I read the generation logs, final report, prompt, and trace only as untrusted
claims. In particular, I did not reuse the compiled definition that the
generation trace says was reused during its resume. All later work used a
fresh scratch tree containing only copied source artifacts.

The intact candidate mount contains the required proof sources:
`solution.py`, `solution.mpy`, `program.k`, `verification.k`, and `spec.k`;
none is a symlink. Candidate-built definitions and its prose were present but
were not treated as proof evidence.

Evidence:

- [stage1_integrity.py](/audit-output/evidence/stage1_integrity.py)
- [stage1-integrity-rerun.log](/audit-output/evidence/stage1-integrity-rerun.log)

The preserved `stage1-integrity.log` is a reviewer-script failure caused by an
invalid `Path.lexists` call; the corrected authoritative rerun exited zero.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted docstring says: “Return median of elements in the list `l`.” Its
plain meaning for a nonempty, orderable list is the middle sorted element for
odd length and the average of the two middle sorted elements for even length.
It specifies neither empty-input errors nor behavior for incomparable or
exotic numeric objects.

The two examples conflict. `[3, 1, 2, 4, 5]` has median `3`. Sorting
`[-10, 4, 6, 1000, 10, 20]` gives
`[-10, 4, 6, 10, 20, 1000]`, whose center average is
`(6 + 10) / 2 = 8.0`, not the documented `15.0`.

The submitted [solution.py](/candidate/solution.py) sorts the input, computes
the length, selects the middle element for odd length, and computes the center
average for even length. This satisfies the natural-language median
description. The candidate also explicitly identifies the contradictory
example in [PROOF.md](/candidate/PROOF.md), so the campaign's second exception
applies. Failing only the self-contradicted literal `15.0` is not a candidate
defect, but it requires `CONCERNS`.

### Translation identity

Running the trusted `/reference/py2mpy.py` over the copied `solution.py`
exited zero. The regenerated file is byte-identical to submitted
`solution.mpy`; both have SHA-256
`657af2a0a65feb8c65a1c35ef4dc33c15ff5fed7e66204c569e46b88e9dd6e29`.

Evidence:

- [stage2-translation.log](/audit-output/evidence/stage2-translation.log)
- Preserved
  [translation driver](/audit-output/evidence/artifacts/stage2_translate.sh)

### Independent differential

My independently authored differential imports the copied candidate and
trusted canonical entry points and also uses `statistics.median` as a
behavioral cross-check. It ran 29 fixed cases and 240 deterministic generated
numeric cases. The fixed set covers both examples, empty input, lengths
one through several branch boundaries, every ordered pair of `int`, `bool`,
and `float` center types, signed zero, infinities, NaNs, odd strings,
incomparable values, `Fraction`, and `Decimal`.

All 240 generated numeric cases agree among candidate, canonical, and the
independent median oracle. The only candidate/canonical divergences are
defensible underdetermined cases:

- For two `Fraction` values, the candidate returns exact `Fraction(1, 2)`;
  canonical's `/ 2.0` returns `0.5`. The independent oracle agrees with the
  candidate.
- For two `Decimal` values, the candidate returns `Decimal('1.5')`;
  canonical raises on division by a float. The independent oracle again
  agrees with the candidate.

Candidate and canonical both raise `IndexError` on empty input, while the
oracle raises `StatisticsError`; the docstring does not specify an empty case.
These divergences do not violate docstring-determined behavior. The conflicting
example check records candidate result `8.0`, conventional result `8.0`, and
literal-example mismatch.

Evidence:

- [stage2_differential.py](/audit-output/evidence/stage2_differential.py)
- [stage2-differential.log](/audit-output/evidence/stage2-differential.log)

## 3. Clean proof reconstruction

I copied source files into `/tmp/audit-work/median47`; no candidate-generated
definition, cache, or compiled artifact was copied. With K version `7.1.293`,
I built a fresh Haskell proof definition from `verification.k` and the
byte-verified supplied semantics:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

The build exited zero. Its only messages were unused-variable warnings in
fixed `str.k`.

I also compiled the supplied top-level semantics independently with the LLVM
backend into `audit-runtime-stage3-kompiled` and ran the preserved translated
smoke module against it. Both concrete build and execution exited zero. The
compiler's non-exhaustiveness warnings are accounted for in Stage 5; none
prevented clean reconstruction.

I then selected and ran every positive target separately. All ten commands
exited zero and printed `#Top`:

1. `median-odd`
2. `median-even-int-int`
3. `median-even-int-bool`
4. `median-even-bool-int`
5. `median-even-bool-bool`
6. `median-even-float-float`
7. `median-even-int-float`
8. `median-even-float-int`
9. `median-even-bool-float`
10. `median-even-float-bool`

Evidence:

- [stage3-kompile.log](/audit-output/evidence/stage3-kompile.log)
- [stage3-concrete-kompile.log](/audit-output/evidence/stage3-concrete-kompile.log)
- [stage3-concrete-smoke.log](/audit-output/evidence/stage3-concrete-smoke.log)
- Ten
  [stage3-proof logs](/audit-output/evidence/stage3-proof-median-odd.log),
  with the full file list and exact invocations in the command index

This is a fresh successful dynamic reconstruction, independent of the
candidate's prior `#Top` reports.

## 4. Adequacy and real-program pinning

### Plain-language claims

The odd claim starts from a direct call to `median(list(VS))`. Its precondition
requires a positive odd length for `sortVS(VS)` and a fresh heap location. Its
postcondition requires exactly the middle value
`valSeqAt(sortVS(VS), (length - 1) / 2)`, allocates the sorted list at that
location, increments the heap allocator once, and restores the environment,
scope allocator, stack, return, exception, and exit-code cells.

The nine even claims have the same state conditions and require positive even
length. They additionally bind the two center values to each ordered pair in
the Cartesian product `{Int, Bool, Float}²`. Each postcondition is the exact
fixed-semantics term for Python promotion, addition, and true division for
that pair. Thus the result is constrained; it is neither free nor a
one-directional implication.

### Mechanical source-to-claim link

An independent reviewer script parsed `solution.py`, invoked the trusted
translator's AST emitter directly, reconstructed the complete expected K
module, and compared it with `program.k`. The files are byte-equal, with
module hash
`efa842f53b4f636abcd57639e0825f5e64f6b6f9ba0a7ee9d42d7152a54dba4f`
and exact translated body hash
`f59824fada527fcc30b294bfda3da92671491395d301f8faff25f86f0dbe83ea`.

The supplied `FuncDef` rule binds that same parameter and statement body to
`closureVal(PNS, BODY, L)`. The claim binds `"median"` to
`solutionMedianClosure`; its sole equation expands to that exact closure with
environment `0`. Normal fixed-semantics lookup and call rules then execute the
docstring expression, `sorted`, `len`, assignments, parity comparison, the
selected branch, indexing, arithmetic, return, and frame pop. There is no
helper claim or loop summary and no call interception.

### Satisfiability and concrete substitution

I supplied `HP = .Map` and `HL = 0` plus a concrete input for every entry
precondition. Examples include `[3,1,2,4,5]` for the odd claim and one input
for every ordered center-type pair. All ten preconditions are true, and every
substituted RHS equals both Python implementations on its witness.

Evidence:

- [stage4_pinning.py](/audit-output/evidence/stage4_pinning.py)
- [stage4-pinning-rerun.log](/audit-output/evidence/stage4-pinning-rerun.log)

The preserved first pinning log is another reviewer-script quoting error; the
corrected rerun is authoritative.

### Body sensitivity

I created a fresh module whose closure is identical except that the odd branch
returns `0`. A claim still requiring median `5` for `[9,1,5]` built and parsed
successfully, then failed with exit `1`, `WarnStuckClaimState`, and residual
`<k> 0 ~> .K </k>`. This changes the program term actually bound in the claim,
not merely an external Python file.

Evidence:

- Preserved
  [mutated program](/audit-output/evidence/artifacts/audit-program-mutated.k),
  [mutated verification module](/audit-output/evidence/artifacts/audit-verification-mutated.k),
  and
  [body-sensitivity claim](/audit-output/evidence/artifacts/audit-body-sensitivity-spec.k)
- [stage4-body-mutant-kompile.log](/audit-output/evidence/stage4-body-mutant-kompile.log)
- [stage4-body-mutant-dry-run.log](/audit-output/evidence/stage4-body-mutant-dry-run.log)
- [stage4-body-mutant-proof.log](/audit-output/evidence/stage4-body-mutant-proof.log)

The theorem therefore pins and depends on the real submitted body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The authoritative source inventory covers `semantics.k`, all 24 helper K files,
`program.k`, `verification.k`, and `spec.k`. It contains 1,026 complete
statements:

- 765 rules;
- 245 syntax declarations;
- 10 target claims;
- 5 evaluation contexts; and
- 1 configuration.

It identifies 161 `function` declarations, 114 `total` declarations, no
`functional` declarations, 24 `no-evaluators` opaque declarations, 48
priority rules, and no simplification rules. A comparison against the freshly
compiled `allRules.txt` found 773 local compiled rule entries. The 26 rules in
`MPY-CONCRETE` are deliberately absent from the proof module and were reviewed
as runtime-only rules. The fixed semantics contains no case-insensitive
occurrence of `median`.

Every inventory item has an explicit disposition. Counts are: 686 entries in
the load-bearing fixed-semantics cone, 272 fixed noninterfering entries, 24
opaque trust-boundary declarations, 32 runtime-only entries, the one local
syntax name, the one local defining equation, and ten targets that are not
assumptions. There are zero undisposed rows.

Evidence:

- [stage5_inventory.py](/audit-output/evidence/stage5_inventory.py)
- [stage5-rule-inventory-rerun.log](/audit-output/evidence/stage5-rule-inventory-rerun.log)
- [stage5_dispositions.py](/audit-output/evidence/stage5_dispositions.py)
- [stage5-rule-dispositions.log](/audit-output/evidence/stage5-rule-dispositions.log)

The earlier `stage5-rule-inventory.log` is superseded because its first parser
version omitted some trailing attributes; the corrected inventory is the one
used here.

### Used-construct map and operational review

The submitted body uses `FuncDef`, `Expr(Str(...))`, `Assign`, `Name`, `Call`,
`If`, `Compare`, `BinOp` with `%`, `//`, `-`, `+`, and `/`, `Subscript`, and
`Return`. Their load-bearing routes are:

- `syntax.k` declares the constructors and strictness/evaluation contexts;
  the explicit `Call`, comparison, and subscript contexts enforce the relevant
  left-to-right evaluation.
- `core.k` supplies configuration cells, scope lookup, builtins, argument
  collection, `vsLen`, fresh heap allocation, and value representations.
- `call.k` performs ordinary callee lookup, argument evaluation, builtin
  dispatch, reference dereference for read-only builtins, frame push, and
  closure execution. Its generic `Call` rule is used; no higher-priority local
  call rule exists.
- `functions.k` supplies exact parameter binding, `Return`, and `#pop`,
  restoring the caller environment, stack, return cell, and scope allocator.
- `controls.k` discards the docstring expression, writes assignments, and
  selects the branch from the evaluated guard.
- `builtins.k` maps `len(list(VS))` to `vsLen(VS)`.
- `sort.k` maps `sorted(list(VS))` to one fresh allocation containing
  `list(sortVS(VS))`.
- `subscript.k` dereferences that allocated list, normalizes the nonnegative
  indices, and produces `valSeqAt`.
- `int.k`, `bool.k`, and `float.k` implement parity, integer division and
  subtraction, Bool promotion, mixed numeric addition, and true division.
- `operators.k` evaluates operands in order and dispatches only after both
  values are available.

The active rules have compatible cell footprints. Freshness prevents the sort
allocation from overwriting `HP`. Call/pop scopes are LIFO and the returned
list reference is not the median result; the final heap deliberately retains
the allocated sorted list. The relevant priority rules specialize reference
dereference, cell assignment, and method/builtin routing. I found no overlap
that selects a task answer or bypasses the source body. Duplicate fixed float
dispatch rules have the same RHS and are harmless.

### Proof-local extension

`program.k` contributes only:

```text
syntax Val ::= solutionMedianClosure [function, total]
rule solutionMedianClosure => closureVal("l", <exact body>, 0)
```

The symbol is nullary; its one equation is exhaustive, terminating, pure,
non-overlapping, and independent of all configuration cells. It names the
exact reconstructed body and does not summarize or predict execution.
`verification.k` adds no rule. The ten `spec.k` claims are proof targets and
are not imported as equations. This extension is sound.

### Fixed opaque boundaries and concrete execution

The proof-relevant opaque primitives are:

- `sortVS`, interpreted as the ascending sorted sequence;
- `valSeqAt` when its first argument is an opaque symbolic sort;
- `divII`, `addF`, `intToF`, and `divFloatIntV`.

These declarations come from the byte-verified supplied semantics, not the
candidate. The claims retain their exact terms, so no candidate rule is
allowed to choose a convenient center or numeric result. Nevertheless, the K
reachability proof does not prove that `sortVS` is a stable ascending
permutation or that the opaque float symbols match all CPython edge behavior.
The comments' reference to an external Lean argument is not mounted evidence
and was not counted. Differential and LLVM runs support only the tested
bridge.

I freshly built the LLVM semantics and ran one translated module containing
normal and boundary checks for all ten witness shapes plus odd strings. The
build and run exited zero. The compiler also warned that several unrelated
helpers and `valSeqAt(.ValSeq, _)` are non-exhaustive despite total
declarations. The target preconditions select positive, median-index cases;
the warning exposes the fixed model's partial/opaque trust boundary but does
not yield a false target conclusion.

Evidence:

- [stage5-llvm-kompile.log](/audit-output/evidence/stage5-llvm-kompile.log)
- [stage5-smoke-translate.log](/audit-output/evidence/stage5-smoke-translate.log)
- [stage5-smoke-krun.log](/audit-output/evidence/stage5-smoke-krun.log)
- Preserved
  [smoke source](/audit-output/evidence/artifacts/audit-smoke.py) and
  [translated input](/audit-output/evidence/artifacts/audit-smoke.mpy)

I found no materially unsound candidate rule and therefore make no
false-conclusion accusation requiring a witness. The opaque observations above
are narrower trust/evidence gaps, not claims that a fixed rule proves a false
result on the material numeric domain.

### Supplied-model representation observation

A fresh concrete witness isolates one representation difference:
CPython returns `'b'` for `median(["é", "a", "b"])`, but the freshly built
LLVM model exits `113` stuck at `strToCodes("\xc3\xa9")`. This is
model-versus-CPython; the submitted Python program is faithful. The candidate
explicitly disclosed the supplied model's ASCII-oriented string boundary, and
the fresh witness makes it concrete.

The supplied `Val` syntax also has no `Fraction` or `Decimal` constructor.
The Stage-2 concrete witnesses show that the submitted Python returns
`Fraction(1, 2)` for `[Fraction(1, 3), Fraction(2, 3)]` and
`Decimal('1.5')` for `[Decimal('1.0'), Decimal('2.0')]`, matching the
independent median oracle. These cases cannot be encoded in the fixed K model;
the gap originates in the supplied representation, not in a candidate
precondition.

Non-ASCII inputs are expressly underdetermined by campaign v3 and are not part
of the material numeric median domain established by the examples and
description. I therefore record this only as a concern; it is not being used
to excuse candidate-caused narrowing.

Evidence:

- [stage5-unicode-gap.log](/audit-output/evidence/stage5-unicode-gap.log)
- Preserved
  [Unicode witness source](/audit-output/evidence/artifacts/unicode-gap.py),
  [translated input](/audit-output/evidence/artifacts/unicode-gap.mpy), and
  [driver](/audit-output/evidence/artifacts/stage5_unicode_gap.sh)

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` as proof. My fresh mutation executes
the real closure on `[9,1,5]`, preserves the correct final cells and sorted
heap allocation, but changes the required result from the true `5` to the
demonstrably false `6`.

The dry run exited zero, proving that the mutation parses and builds against
the fresh definition. The real proof exited `1` with
`WarnStuckClaimState`; the residual has `<k> 5 ~> .K </k>` and the expected
final operational state. It failed at exactly the changed result obligation,
not at parsing, lookup, execution, or an unrelated cell.

Evidence:

- Preserved
  [false-result mutation](/audit-output/evidence/artifacts/audit-false-spec.k)
- [stage6-false-dry-run.log](/audit-output/evidence/stage6-false-dry-run.log)
- [stage6-false-proof.log](/audit-output/evidence/stage6-false-proof.log)

This is meaningful non-vacuity evidence.

## 7. Proven versus assumed accounting

### Formally established

Under the fixed supplied MPY semantics, from every configuration satisfying a
target precondition:

- the exact submitted function body executes through normal language rules;
- for every positive odd symbolic length, the return is the middle
  `valSeqAt` of `sortVS(VS)`;
- for every positive even symbolic length whose two center values have any of
  the nine `Int`/`Bool`/`Float` type pairs, the return is the exact supplied
  numeric-average term for that pair;
- `VS`, initial `HP`, and fresh `HL` are symbolic, so the theorem is not a
  bounded unrolling or a finite collection of sizes;
- exactly one sorted list is allocated, `heapLoc` advances once, and the other
  specified operational cells are restored; and
- changing either the executed body or the result constraint is detected.

### Trusted or informal boundaries

| Boundary | Influence | Assessment |
|---|---|---|
| K `7.1.293`, the Haskell backend, SMT reasoning, and reachability-logic implementation | Establish all ten `#Top` results | Necessary platform trust; fresh rebuild and discriminating failures reduce, but cannot eliminate, this boundary |
| Byte-verified supplied MPY semantics | Defines all execution behavior | Authorized fixed model; no candidate tampering |
| Trusted `py2mpy.py` AST translation | Links Python syntax to MPY constructors | Byte identity plus independent constructor reconstruction pins the submitted source; semantic faithfulness remains a translator trust boundary |
| `sortVS` and length of the opaque sort | Determines parity, center positions, result, and allocated list | Load-bearing supplied primitive; exact term is proved, ascending-permutation meaning is assumed and finitely tested |
| `valSeqAt(sortVS(VS), i)` | Selects odd result and even operands | Load-bearing supplied total/opaque boundary; median indices are in bounds under the sort/length contract |
| `divII`, `addF`, `intToF`, `divFloatIntV` | Determines even numeric values | Exact fixed terms are proved; CPython numeric meaning, NaNs, infinities, and rounding edges remain primitive trust |
| Differential and LLVM smoke suites | Tests ordinary source/model correspondence | Empirical support only; not substituted for the universal K proof |
| Unicode and unrepresented Python classes such as `Decimal`, `Fraction`, and custom objects | Fixed model cannot represent or execute all CPython cases; concrete witnesses are `'b'`, `Fraction(1, 2)`, and `Decimal('1.5')` as detailed above | Supplied-model representation boundary, explicitly recorded with divergence witnesses; candidate Python is faithful and adds no narrowing, so at most a concern |
| Contradictory `15.0` example | Prevents simultaneous satisfaction of literal example and ordinary median meaning | Candidate explicitly chose and implemented the defensible ordinary-median resolution; campaign exception requires `CONCERNS / LEGIT` |

### Decision

The proof is reconstructed, sound relative to the fixed semantics,
result-constraining, non-vacuous, sensitive to the real function body, and
unbounded over the material numeric source-contract domain. Its odd claim and
nine even numeric claims cover every positive-result input class representable
by the fixed model; the candidate adds no narrower size or value bound. The
candidate did not add an answer rule, oracle, or operational shortcut.
Underdetermined exotic inputs and fixed-model representation gaps do not show
a violation of docstring-determined behavior.

The self-contradicted example and load-bearing supplied opaque primitives
remain documented limitations. They warrant concerns but do not invalidate
the proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
