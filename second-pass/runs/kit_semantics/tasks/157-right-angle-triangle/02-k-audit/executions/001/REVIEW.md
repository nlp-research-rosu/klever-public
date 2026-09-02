# Independent adversarial audit: 157-right-angle-triangle

The candidate contains a genuine, result-constraining reachability proof of
the submitted program under the supplied MPY model. It does not substitute a
different body, bound the integer domain, or prove only examples. Two trust
limitations prevent an unqualified `PASS`: symbolic Float equality is connected
through an explicit low-level primitive contract rather than a bridge-free
universal theorem, and the fixed supplied model has a reproducible
mixed-Int/Float overflow/non-finite behavior gap from CPython. The latter meets
all four conditions of campaign amendment v2's documented supplied-model-gap
exception, so it is `CONCERNS / LEGIT`, not candidate-caused domain narrowing.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. I read `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, and every required pipeline-v3 generation record:
`invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
Generation prose and traces were treated only as untrusted claims.

The independent checker [provenance_check.py](/audit-output/evidence/provenance_check.py)
hashed the mounted files rather than host provenance paths. Its complete
[log](/audit-output/evidence/01-provenance.log) records:

- every launcher-recorded digest matched;
- the campaign lock digest matched and its content equaled the campaign block
  in `/audit-input.json`;
- candidate and trusted prompt copies were byte-identical;
- candidate and trusted translator copies were byte-identical;
- the required proof artifacts were regular, readable, non-symlink files;
- the trusted and candidate supplied-semantics trees each had the same 25
  path/type entries and the same reviewer tree digest
  `5fb440366297acb1e079d51d621aea5caa20e4df9af333a527ac39bb98a5c452`;
- there were no symlinks in either the candidate tree or structured trace.

The trace checker [trace_summary.py](/audit-output/evidence/trace_summary.py)
parsed all 419 JSONL records; the direct trace hash also matched both recorded
manifests ([log](/audit-output/evidence/01-trace-summary.log)). The supplied
semantics mount required by this mode is present. There is no provenance,
mount, record-layout, or supplied-semantics integrity breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: given three side lengths, return whether they form a
right-angled triangle; it gives `(3,4,5) -> True` and `(1,2,3) -> False`
([prompt](/reference/prompt.py:2)). The trusted canonical implementation defines
the benchmark result as the disjunction of the three possible Pythagorean
equalities ([canonical.py](/reference/canonical.py:6)).

The submitted [solution.py](/candidate/solution.py:1) has exactly that return
expression. The independent pinning checker compared parsed function ASTs
(ignoring only the canonical docstring), regenerated `solution.mpy` using the
trusted `/reference/py2mpy.py`, and mechanically compared the resulting
function binding, parameters, body constructor, and defining scope. The
regenerated MPY file was byte-identical to the submission
([commands and results](/audit-output/evidence/02-translation-pinning.log),
[checker](/audit-output/evidence/pinning_check.py)).

The independent differential harness
[differential_test.py](/audit-output/evidence/differential_test.py) imported the
trusted canonical and submitted entry points. It checked the documented
examples, empty/arity errors, branch and boundary cases, all 15,625 triples in
`[-12,12]^3`, 5,832 Float triples including subnormal and non-finite values,
1,331 mixed triples, and 10,000 deterministic generated mixed triples. All
32,807 outcomes matched
([log](/audit-output/evidence/02-differential.log)). This finite testing supports
the source bridge; it is not used as the universal proof.

A concrete fixed-model representation boundary is also recorded: canonical
and candidate both accept `Fraction(3,1), Fraction(4,1), Fraction(5,1)` and
return `True`, while MPY has no Fraction value representation. This is not a
candidate rewrite or restriction; the source implementations are identical.

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the trusted supplied semantics to
`/tmp/audit-work/reconstruction`. I did not copy or reuse candidate-compiled
definitions, caches, logs, or proof results. Tool versions are recorded in
[00-toolchain.log](/audit-output/evidence/00-toolchain.log).

The fresh Haskell proof definition was built with:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

It exited 0 ([build log](/audit-output/evidence/03-kompile-haskell.log)).
The only warnings were unused variables in the unchanged supplied `str.k`.
An aggregate proof run exited 0 and printed `#Top`
([log](/audit-output/evidence/03-kprove-all.log)). I then independently selected
and ran every entry claim:

| Claim | Domain | Result |
|---|---|---|
| `right-angle-iii` | Int, Int, Int | exit 0, `#Top` |
| `right-angle-iif` | Int, Int, Float | exit 0, `#Top` |
| `right-angle-ifi` | Int, Float, Int | exit 0, `#Top` |
| `right-angle-iff` | Int, Float, Float | exit 0, `#Top` |
| `right-angle-fii` | Float, Int, Int | exit 0, `#Top` |
| `right-angle-fif` | Float, Int, Float | exit 0, `#Top` |
| `right-angle-ffi` | Float, Float, Int | exit 0, `#Top` |
| `right-angle-fff` | Float, Float, Float | exit 0, `#Top` |

The first claim's command/output is preserved separately
([log](/audit-output/evidence/03-kprove-right-angle-iii.log)); the other seven
are in [03-kprove-selected-remaining.log](/audit-output/evidence/03-kprove-selected-remaining.log).
The count check confirms eight independently selected `#Top` results
([summary](/audit-output/evidence/03-proof-summary.log)).

I also freshly built the unchanged supplied semantics with LLVM
([build log](/audit-output/evidence/03-kompile-llvm.log)) and executed an
independently authored 14-assert source harness covering both examples, each
true branch, false and zero cases, negatives, large integers, Float, and mixed
values ([source](/audit-output/evidence/concrete_audit.py),
[translation](/audit-output/evidence/03-concrete-audit.mpy)). `krun` exited 0
with `.K`, `NoExc`, and exit code 0
([log](/audit-output/evidence/03-krun-fixed.log)).

## 4. Adequacy and real-program pinning

All eight claims have the same meaning, differing only in the three argument
sorts ([spec.k](/candidate/spec.k:9)):

- Precondition: there is no additional `requires`. The computation is a normal
  call to `right_angle_triangle` with three symbolic values; environment 0
  binds that name to the submitted closure; builtins are in parent scope -1;
  the heap and call stack are empty; return state is `noRet`; exception state
  is `NoExc`; and exit code is 0.
- Postcondition: execution returns a `Bool` equal to `ratExpected(A,B,C)`.
  `ratExpected` is exactly the disjunction of the three modeled squared-side
  equalities ([verification.k](/candidate/verification.k:92)). The return value
  is neither free nor guarded by a one-way implication.

The eight sort combinations cover all of the fixed model's `Int`/`Float`
triples, with no positivity, magnitude, enumeration, or unrolling restriction.
Each precondition is satisfiable. For every claim, independent ground
substitution with a sort-correct `(3,4,5)` produced `True`, and `(1,2,3)`
produced `False`; formal postcondition, canonical, and candidate agreed in all
16 checks
([checker](/audit-output/evidence/claim_witnesses.py),
[log](/audit-output/evidence/04-claim-witnesses.log)).

The claim term does not merely name the external `solution.mpy` file. The
nullary `rightAngleTriangleClosure` expands to a normal `closureVal` whose
parameter list, defining scope 0, and complete `Return(BoolOp(...))` body are
constructor-identical to the trusted regeneration
([verification.k](/candidate/verification.k:8),
[mechanical comparison](/audit-output/evidence/02-translation-pinning.log)).
Normal supplied rules still perform lookup, argument evaluation and binding,
frame allocation, body execution, short-circuiting, return, and frame
restoration.

For an independent body-sensitivity test, I changed the closure body actually
executed by a ground `(3,4,5)` claim to `return False` while retaining the true
obligation. The mutation parsed and built (`--dry-run` exit 0), then proof
failed with exit 1 and the expected stuck `false ~> .K`
([mutation](/audit-output/evidence/04-body-sensitivity-fresh.k),
[log](/audit-output/evidence/04-body-sensitivity.log)). This is sensitivity to
the claim's program term, not merely a changed external source file.

## 5. Rule-by-rule static soundness review

The exhaustive inventory
[05-k-inventory.tsv](/audit-output/evidence/05-k-inventory.tsv) contains one
row, source location, attributes, target-path classification, decision, and
reason for every local declaration/rule in the supplied semantics,
`verification.k`, and `spec.k`. The inventory command exited 0
([script](/audit-output/evidence/static_inventory.py),
[run log](/audit-output/evidence/05-inventory-run.log)).

There are 1,007 inventoried entries: 981 supplied, 18 proof-local, and 8 entry
claims. By source kind these are 245 syntax declarations, 748 rules, 5
contexts, 1 configuration, and 8 claims. The 748 rules divide into 507
equational and 241 operational rules. Attributes include 163 `function`, 115
`total`, 25 `no-evaluators`, 55 `concrete`, 48 priority, 28 `owise`, 4
`macro`, and 1 `macro-rec`; there are no local simplification rules or
`functional` declarations. The inventory identifies 156 entries on the
target's material execution/specification path and 851 constructor-disjoint
entries not used by this loop-free numeric function.

### Used source constructs and fixed rules

The submitted MPY body uses only `Call`, `Name`, `closureVal`, `Return`,
`BoolOp("or",...)`, `Compare`/`CmpOp("==",...)`, `BinOp("*",...)`,
`BinOp("+",...)`, and Int/Float values. Their declarations are in supplied
`syntax.k` and `core.k`; lookup is in `core.k`; call routing, left-to-right
argument evaluation, binding, frame push/pop, and restoration are in `call.k`
and `functions.k`; operand evaluation and dispatch are in `operators.k`;
short-circuit selection is in `bool.k`; and numeric operations are in `int.k`
and `float.k`. The initial and final cells used by the claims are exactly the
supplied configuration cells. No material allocation, mutation, output, or
exception rule is bypassed.

The complete row-by-row decisions are in the TSV. For the 851 unused supplied
entries, the decision is explicitly limited to the selected supplied-model
level: no constructor unifies them with the target path and no proof-local
lemma depends on them. I found no inconsistent proof-local overlap or
proof-enabling simplification through them. This is not a claim that the
supplied miniature Python model implements every unused CPython feature.

The material fixed-rule review found:

- Int multiplication, addition, and equality use K's mathematical integer
  operations and match canonical behavior on the unrestricted Int domain.
- Float operations use supplied opaque `mulF`, `addF`, `intToF`, and `eqIF`
  primitives with concrete LLVM equations. Sort cases are disjoint. The
  duplicated mixed `applyBin` equations in supplied `float.k` have identical
  right-hand sides, so their overlap is harmless.
- `BoolOp("or",...)` evaluates left-to-right and short-circuits using the
  supplied truthiness rules, matching the real control flow.

### Every proof-local extension

The 18 proof-local inventory rows reduce to these fully reviewed groups:

1. `rightAngleTriangleClosure` declaration/equation
   ([verification.k](/candidate/verification.k:8)) is a terminating,
   exhaustive nullary definitional name for the mechanically pinned closure.
   It does not summarize or intercept function execution.
2. `trustedFloatEq` declaration and concrete equation
   ([verification.k](/candidate/verification.k:56)) form an explicit external
   primitive contract. For concrete values the equation is exactly K
   `==Float`; it is opaque only to the symbolic Haskell prover.
3. The priority-40 Float-Compare rule
   ([verification.k](/candidate/verification.k:64)) is an operational bridge.
   Its operands are already evaluated Float values, it returns one Bool, and
   its `...` preserves the arbitrary continuation and every other cell. It
   preempts the supplied path
   `Compare -> applyCmp("==",...) -> ==Float` only because symbolic Haskell
   cannot execute that fixed hook. It cannot skip operand effects, lookup,
   return, an exception, or a frame transition.
4. `ratSquare`, `ratAdd`, `ratEq`, and `ratExpected` declarations/equations
   ([verification.k](/candidate/verification.k:74)) are postcondition-only
   definitions. Their Int/Float cases are sort-disjoint and exhaustive for all
   eight claims, and their right-hand sides are the corresponding supplied
   operations. They are nonrecursive except for finite composition and do not
   execute in place of the program.

There is no proof-local return shortcut, call interceptor, task-answer axiom,
free-result oracle, loop circularity, auxiliary execution claim, or
simplification lemma. The Float bridge and postcondition use the same named
primitive, so the Float claims are interpretation-parametric and conditional
on that primitive denoting fixed Float equality; they do not prove the
primitive contract itself. A bridge-free universal connection theorem is
absent. Because this is a fixed external operation rather than program-defined
code, the boundary is explicit and the concrete equation is correct, I classify
this as a non-fatal trust/evidence limitation, not an unsound task-result rule.

Fresh bridge tests support—but do not prove—the connection. The supplied-only
and extended LLVM definitions produced byte-identical complete final
configurations on the 14-case whole-function harness
([log](/audit-output/evidence/05-bridge-fixed-vs-extended.log)). A second
harness exercised true and false Float equality followed by observable
assignments and Boolean continuations; complete outputs were again
byte-identical
([source](/audit-output/evidence/bridge_context_audit.py),
[log](/audit-output/evidence/05-bridge-context.log)). The extended LLVM build
itself exited 0
([log](/audit-output/evidence/05-kompile-extended-llvm.log)).

### Concrete false-conclusion witness in the supplied model

I did find a material CPython-fidelity defect, but it is in the immutable
supplied semantics, not in a candidate-added rule. Supplied mixed arithmetic
promotes arbitrary K Int values through total `intToF`
([float.k](/reference/reference-semantics/semantics/float.k:131),
[float.k](/reference/reference-semantics/semantics/float.k:230)), while
non-finite mixed equality also compares through that conversion
([float.k](/reference/reference-semantics/semantics/float.k:165)). The model
does not represent CPython's `OverflowError` from converting an enormous Int
during mixed arithmetic, and an enormous Int can convert to positive infinity
for a non-finite comparison.

Concrete false conclusion:

```text
input = (10**308, 1.0e308, 1.0e308)
CPython canonical/candidate: raises OverflowError
unchanged supplied MPY LLVM: terminates normally, result = true, NoExc
```

The sides themselves are positive and finite, so this is not created by an
invalid K-only input. The fixed-definition reconstruction, source, translated
MPY, exact commands, statuses, and outputs are preserved in
[07-model-behavior-gap.log](/audit-output/evidence/07-model-behavior-gap.log),
[witness source](/audit-output/evidence/model_behavior_gap_witness.py),
[K output](/audit-output/evidence/07-model-gap-krun-output.txt), and
[CPython output](/audit-output/evidence/07-model-gap-cpython-output.txt).
An independent import-based check establishes that the submitted Python and
trusted canonical both raise the same `OverflowError`
([checker](/audit-output/evidence/model_gap_fidelity.py),
[log](/audit-output/evidence/07-model-gap-fidelity.log)).

This witness is against the fixed model's CPython fidelity. It is not a witness
that any candidate-local equation can prove a false result relative to that
fixed model: `ratExpected` deliberately uses the same supplied numeric
operations as execution.

## 6. Fresh non-vacuity test

I did not rely on the candidate's mutation files. The fresh mutation
[06-false-result-fresh.k](/audit-output/evidence/06-false-result-fresh.k)
executes the real submitted closure on the satisfying ground input `(3,4,5)`
but changes the result obligation from true to false. It therefore changes a
material, reachable, result-constraining obligation known false for that input.

`kprove ... --dry-run` exited 0, establishing that the mutation parsed and
built. The actual proof exited 1 with `WarnStuckClaimState`; its residual
contained `true ~> .K` while the destination required false
([complete command log](/audit-output/evidence/06-false-result.log)). The
failure is the expected unmet result obligation, not a parser error, import
failure, timeout, or unrelated crash. Together with the distinct executed-body
mutation in Stage 4, this establishes both result non-vacuity and body
sensitivity.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Conditional on the trust ledger below, for every K triple in
`{Int,Float}^3`, execution from the exact claimed normal call state of the
mechanically pinned submitted closure reaches a Boolean result equal to:

```text
(a*a == b*b + c*c)
or (b*b == a*a + c*c)
or (c*c == a*a + b*b)
```

where every operation has the supplied MPY numeric meaning. The reachability
claims restore the specified caller cells with `NoExc` and exit code 0. This
is a universal symbolic result in the fixed model, not finite testing or
bounded unrolling. Although the runs establish normal completion in that
model, the required benchmark classification is partial correctness.

### Trust ledger

| Boundary | Used by | Status and justification |
|---|---|---|
| Supplied `reference-semantics` operational rules | All claims | Trusted fixed model; candidate copy was recursively identical. Material target-path rules were reviewed. The documented mixed overflow/non-finite divergence below limits CPython fidelity. |
| K compiler, Haskell prover, LLVM executor, and builtin Int/Float hooks | Builds, proofs, concrete bridge evidence | Necessary toolchain trust. Fresh builds and both backends were used; no candidate cache was trusted. |
| K mathematical Int operations | `iii` and Int portions of mixed claims | Acceptable standard primitive; unbounded Int arithmetic matches the canonical operations before any mixed conversion. |
| Supplied opaque `mulF`, `addF`, `intToF`, and `eqIF` | Float/mixed claims and `ratExpected` | Explicit fixed-model primitives. Their symbolic meanings are assumed; concrete LLVM equations provide finite evidence. `intToF`/non-finite behavior has the concrete divergence witness in Stage 5. |
| Candidate `trustedFloatEq` contract | Seven Float-containing claims | Explicit low-level external primitive. Concrete equation and two fixed-vs-extended tests support it, but there is no bridge-free universal connection theorem. This is a non-fatal evidence limitation because the theorem is conditional and the primitive replaces fixed external equality, not program-defined computation. |
| Source-to-MPY/body constructor bridge | All claims | Acceptable and mechanically checked: trusted regeneration was byte-identical and the closure body/parameters/scope matched constructor-for-constructor. Fresh body mutation failed as required. |
| Pythagorean characterization of right triangles | Natural-language intent | Standard informal mathematical fact for positive side lengths. The formal result implements all three choices of hypotenuse and matches canonical ground truth. |
| CPython classes absent from MPY, such as `Fraction`, `Decimal`, complex, and overloaded numeric objects | Source-contract boundary | Supplied-model representation gap, not candidate narrowing. A concrete Fraction witness is recorded; candidate and canonical are identical on it. |
| CPython mixed huge-Int conversion/overflow behavior | Positive finite Int/Float inputs | Supplied-model behavior gap. Concrete witness: canonical and candidate raise `OverflowError`, while fixed MPY returns normal `true`. Explicitly documented here and in preserved evidence. |
| Differential and bridge test suites | Source and primitive bridges only | Finite empirical support. They are not treated as the K proof or as universal justification. |

### Decision

The clean proof, exact-body pinning, exhaustive target-path review, and fresh
mutations pass the proof legitimacy gates. No candidate-local rule encodes the
answer, bypasses program-defined computation, or introduces a demonstrated
false conclusion under the fixed model.

The unproven universal Float-equality bridge is an explicit, low-level
trust-boundary limitation. Separately, the supplied model cannot faithfully
represent all canonical CPython numeric classes or the demonstrated
mixed-huge-Int exception behavior. Campaign amendment v2 applies to the latter:

1. the restriction originates in the read-only supplied semantics, whose
   candidate copy is recursively identical;
2. the eight no-`requires` claims cover every `Int`/`Float` triple the fixed
   model represents, with no candidate-added magnitude or finiteness bound;
3. this trust ledger records both a representation witness and the concrete
   CPython-versus-fixed-MPY divergence;
4. the submitted Python is AST-equivalent to canonical and has exactly the
   same `OverflowError` behavior on the divergence witness.

Accordingly, these are documented, non-fatal model/evidence limitations under
the campaign mapping. They do not convert a faithful program and sound
fixed-model proof into `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
