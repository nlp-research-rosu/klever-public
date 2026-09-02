# Independent adversarial audit: 110-exchange

## Decision

The candidate contains a legitimate, freshly reconstructible partial-correctness
proof of the submitted program for non-empty lists of K/Python integers. The
proof executes the submitted function body, computes both loop counts, and
constrains the returned value to `YES` exactly when the number of odd elements
in `lst1` is at most the number of even elements in `lst2`.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, for three bounded
limitations:

1. The prompt says lists of “numbers,” but the theorem is explicitly restricted
   to integers. The generated function and the trusted canonical function
   disagree on fractional values such as `([0.5], [1.0])`.
2. `verification.k` introduces `intVals(IntSeq)` as a proof-only symbolic input
   representation. Its two iterator equations are exact for the only operation
   the program performs on its inputs, but the candidate supplies no separate
   universal connection theorem to the native `.ValSeq`/`vCons` representation.
   The representation is not globally interchangeable with native lists; a
   fresh probe exhibits the difference for empty-list truthiness. This does not
   affect the submitted program's non-empty integer execution path.
3. The candidate omits all four requested generation-record artifacts. The
   independent reconstruction compensates for the missing evidence, but the
   provenance record is incomplete.

No candidate-local rule was found that can prove a false exchange result on the
formal non-empty integer domain. No candidate-local opaque result, answer
oracle, simplification, priority rule, or execution-bypassing rewrite exists.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as required. There is no
infrastructure contradiction, so this is a candidate audit rather than an
`AUDIT_ERROR`.

The non-following integrity checker in
`evidence/integrity_check.py` recursively compared entry names, entry types,
modes, and file bytes. It found:

- `/candidate/reference-semantics` and
  `/reference/reference-semantics` have exactly the same directories and files;
- all entries are regular directories/files, with no symlinks;
- all modes and bytes match;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`; and
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

The independent recursive `diff` also exited 0. See
`evidence/05-integrity-check.txt` and `evidence/06-semantics-diff.txt`.
Candidate and trusted manifests, including SHA-256 hashes, are in
`evidence/02-candidate-manifest.txt` and
`evidence/03-reference-manifest.txt`.

No missing, extra, changed, mistyped, or symlinked entry exists inside the
required supplied-semantics tree. The trusted baseline establishes the selected
fixed semantics; it does not bless the proof-local rules in `verification.k`,
which are reviewed in stage 5.

### Missing and untrusted generation evidence

The following requested artifacts are absent from `/candidate`:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`; and
- `codex-output.log`.

There is no separate structured model-generation trace. The candidate does
contain `kore-exec.tar.gz`, which is a K diagnostic archive, not source. It was
listed without extraction and not reused. Its untrusted logs report an SMT
adapter error from a prior run; that claim has no bearing on the fresh
reconstruction. See `evidence/34-candidate-trace-archive-list.txt` and
`evidence/35-candidate-trace-claims.txt`.

Candidate `__pycache__`, `kore-exec.tar.gz`, and any candidate-generated
concrete tests were not used as proof evidence. The source files needed for
execution were copied to `/tmp/audit-work/exchange-110-fresh`; the scratch
manifest is `evidence/07-scratch-source-manifest.txt`. No candidate compiled
definition or cache was copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For two non-empty lists, arbitrary exchanges may replace odd elements of
`lst1` with even elements from `lst2`. Such an exchange is possible exactly
when:

```text
count_odd(lst1) <= count_even(lst2)
```

If the inequality holds, pair each odd element in `lst1` with a distinct even
donor from `lst2`; all other elements of `lst1` are already even. If it does
not hold, at least one odd element lacks an even donor. The requested return is
`"YES"` in the first case and `"NO"` in the second. The prompt expressly
excludes empty inputs.

The trusted canonical implementation counts `i % 2 == 1` in `lst1` and
`i % 2 == 0` in `lst2`. The submitted implementation counts
`number % 2 != 0` and `number % 2 == 0`. These are equivalent for all Python
integers, including negative integers, because modulo 2 is either 0 or 1. Both
then test the same non-strict count inequality.

### Translator fidelity

`solution.py` compiled successfully. Regeneration with the trusted translator:

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
```

produced SHA-256
`0a7ce271d769befb3c9f4c307998e9d32975d9d190b9f537e254a0c5f711c6eb`,
the same hash as the submitted `solution.mpy`; `cmp` exited 0 and printed
`BYTE_IDENTICAL`. See `evidence/08-translation-identity.txt` and
`evidence/09-python-compile.txt`.

### Independent differential testing

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of `solution.py`. It does not
reuse proof equations. The recorded command exited 0 with zero mismatches over:

- both documented examples;
- 12 boundary cases, including the equality, just-below, just-above, zero,
  negative, large-integer, and empty cases;
- all 159,201 pairs of non-empty integer lists of lengths 1 through 3 over
  `{-3,-2,-1,0,1,2,3}`; and
- 5,000 deterministic seeded pairs of non-empty integer lists, each of length
  1 through 8 with values between `-10^9` and `10^9`.

Complete scope and results are in `evidence/10-differential-test.txt`.

The same test also records five exploratory fractional cases outside the K
theorem's domain. Three differ:

```text
([0.5],  [1.0])  canonical YES, generated NO
([1.5],  [3.0])  canonical YES, generated NO
([-0.5], [5.0])  canonical YES, generated NO
```

This is a real implementation/domain limitation. It is not hidden as proof
evidence and is one reason for `CONCERNS`.

## 3. Clean proof reconstruction

The installed independent toolchain is K
`v7.1.337` (build date 2026-06-18); see
`evidence/01-toolchain.txt`.

### Concrete definition

From source in the scratch directory:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
```

exited 0. The complete bounded log is
`evidence/11-kompile-runtime.txt`.

`evidence/k_concrete_probe.py` contains an exact copy of the submitted function
body and independent assertions for documented, branch-boundary, negative,
empty, and large-integer cases. The trusted translator produced the MPY probe,
and:

```text
krun k-concrete-probe.mpy --definition runtime-fresh-kompiled --output pretty
```

exited 0 with `.K`, `NoExc`, an empty stack, and exit code 0. See
`evidence/12-concrete-probe-translation.txt` and
`evidence/13-krun-concrete-probe.txt`.

### Proof definition and positive claims

The fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module EXCHANGE-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

exited 0; see `evidence/14-kompile-verification.txt`.

The complete three-claim proof:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module EXCHANGE-SPEC --output pretty
```

exited 0 and printed `#Top`; see `evidence/16-kprove-all.txt`. This invocation
proves both loop circularities and the entry claim together, which is required
because the entry proof depends on the two loop circularities.

The loop claims were also independently selected with K's required fully
qualified labels:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module EXCHANGE-SPEC --claims EXCHANGE-SPEC.odd-loop --output pretty

kprove spec.k --definition verification-fresh-kompiled \
  --spec-module EXCHANGE-SPEC --claims EXCHANGE-SPEC.even-loop --output pretty
```

Both exited 0 and printed `#Top`; see
`evidence/20-kprove-qualified-odd-loop.txt` and
`evidence/21-kprove-qualified-even-loop.txt`.

For transparency, logs 17–19 preserve rejected unqualified-label diagnostics.
Log 22 preserves a diagnostic attempt to select only `exchange-correct`; that
filter removes the two loop circularities the entry needs and was interrupted
after approximately 90 seconds. It is not treated as a proof run or candidate
failure. The valid independent entry proof is the complete fresh invocation in
log 16.

Compiler warnings concern unused pattern variables or non-exhaustive
fixed-semantics functions for constructs absent from this program. They do not
change any successful exit status or enter the proof's execution slice.

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Preconditions | Postcondition |
|---|---|---|
| `odd-loop` | Current computation is the real first `#loop` over a non-empty `intVals` integer sequence; the current scope has exact bindings for both inputs, `odd`, `even`, and `number`; current scope location is disjoint from the framed rest of the scope map. | The loop terminates at the same arbitrary continuation; `odd` becomes its initial value plus the number of odd sequence elements; `even`, inputs, and parent are preserved; only the dead final value of `number` is existential. |
| `even-loop` | Analogous real second `#loop`, non-empty integer sequence, exact local bindings, and disjoint map decomposition. | The loop reaches the same continuation; `even` becomes its initial value plus the number of even sequence elements; `odd`, inputs, and parent are preserved; only the dead final `number` value is existential. |
| `exchange-correct` | Exact initial MPY configuration; two non-empty integer sequences encoded as `list(intVals(iCons(...)))`; empty heap/stack; no exception or return state; exit code 0. | The exact returned K value is `exchangeResult` of the two complete sequences; environment, allocation counters, heap, stack, return state, exception state, and exit code satisfy the unchanged cells. Only the final scope map is existential. |

A satisfying helper-claim state is obtained with `L = 1`, `SC` containing the
module and builtins scopes, a five-binding local map, and a singleton sequence.
`notBool L in_keys(SC)` is then true. The entry precondition is satisfied, for
example, by `A=1`, `AS=.IntSeq`, `B=2`, `BS=.IntSeq` and the exact initial
configuration written in the claim.

### Exact program identity

The entry `<k>` cell starts with:

```text
#loadAll(Module(exchangeDef)) ~> Call(Name("exchange"), ...)
```

`exchangeDef` is a compile-time macro whose expanded `FuncDef` contains, in
order, the three assignments, both submitted `For` loops and exact loop bodies,
the `odd <= even` branch returning `"YES"`, and the fallback returning `"NO"`.
That AST is the byte-verified submitted `solution.mpy` AST. The macro names code;
it does not replace a call or a return with a summary.

The fixed semantics loads that `FuncDef`, resolves the real closure, evaluates
and binds both arguments, pushes the call frame, executes assignments and both
loops, evaluates the final comparison, executes the selected `Return`, and
pops the frame. The only loop summaries are reachability claims anchored at the
real `#loop` control point. Each non-empty induction step must execute
`#iterNext`, target binding, the exact body, and the loop label before
circularity can recur.

The final value is not free. `exchangeResult` has two disjoint and exhaustive
guards and reduces to the concrete ASCII code sequence for `YES` or `NO`.
Existential `?FINALSCOPES` does not weaken the returned value, stack, exception,
or exit-code obligations.

### Ground substitutions

`evidence/ground-witness-spec.k` substitutes two satisfying ground inputs into
the complete entry execution:

- `([1],[2])` reaches concrete `"YES"` at the equality boundary;
- `([1,3],[2])` reaches concrete `"NO"` just beyond the boundary.

The fresh K proof exited 0 with `#Top`; see
`evidence/25-ground-witness-proof.txt`. Both trusted canonical Python and the
generated Python return the same respective values; see
`evidence/26-ground-witness-python.txt`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` generated
`evidence/k-rule-inventory.tsv`. The inventory covers all 26 selected K source
files (the supplied semantics tree, `verification.k`, and `spec.k`) and
enumerates every top-level source item. It contains:

- 708 rules: 695 supplied fixed-semantics rules and 13 rules in
  `verification.k`;
- 234 syntax declarations;
- 149 declarations with `function`, 110 with `total`, 25 explicit symbolic
  declarations, 45 priority-bearing items, 36 concrete items, 26 `owise`
  items, 7 macros, and 1 recursive macro;
- 5 contexts, 1 configuration, and all 3 reachability claims; and
- no `functional` or simplification rule.

`evidence/k_rule_review.py` adds a disposition and rationale for every one of
the 1,118 inventoried records in `evidence/k-rule-review.tsv`. Its summary is:

- 42 fixed rules reviewed on the submitted solution's execution slice;
- 653 fixed rules for unused constructs, which cannot contribute to this
  proof's closure;
- all 13 candidate-local rules individually classified as sound operational
  extensions, definitions, or macros;
- both auxiliary claims sound; and
- the entry claim sound and result-constraining.

The selected fixed semantics is a trusted input, not candidate-authored theory.
Nevertheless, its relevant load, lookup, argument evaluation, call/frame,
binding, sequencing, strictness, loop, integer, string, and return rules were
read in source. The source excerpt log is
`evidence/23-relevant-semantics-source.txt`, and the exhaustive per-rule
locations remain in the TSV inventory.

### Construct-to-rule map

| Submitted construct | Declaration/evaluation path |
|---|---|
| `Module`, statement sequence | `MPY-SYNTAX`; `#loadAll` and statement sequencing in `core.k` |
| `FuncDef`, `Call`, parameters, return | `syntax.k`; closure creation and return/pop in `functions.k`; callee/argument and closure application in `call.k` |
| `Assign`, `AugAssign` | strict RHS syntax plus the current-scope map updates in `controls.k` |
| `For` over a name | strict iterable evaluation, name lookup, `#loop`, `#loopStep`, and `#bindTgt` in `controls.k`/`tuple.k` |
| Symbolic integer list iteration | exactly the two `intVals` rules at `verification.k:10-12` |
| `If` | strict condition plus `#branch` true/false rules in `controls.k` |
| `%`, `+` | sequential operand evaluation and dispatch in `operators.k`; `pyMod` and integer addition in `int.k` |
| `!=`, `==`, `<=` | comparison contexts/dispatch in `operators.k`; integer comparisons in `int.k` |
| `Name` and `Int` | lookup and literal rules in `core.k` |
| `Str("YES")`, `Str("NO")` | strict return evaluation and `strToCodes` rules in `str.k` |

This path evaluates operands in the submitted order, uses the current call
scope, changes only the expected scope bindings, and restores the caller frame.
No allocation occurs because the claim supplies read-only bare list values,
which the supplied semantics explicitly permits for claim inputs.

### Candidate-local rules

The 13 rules in `verification.k` have the following complete assessment:

1. The two `#iterNext(list(intVals(...)))` rules are operational extensions for
   a fresh constructor. Empty yields `#iterDone`; non-empty yields the exact
   integer head and structurally smaller tail. They change no cell, preserve
   the active continuation, cover both `IntSeq` constructors, and do not overlap
   the fixed `.ValSeq`/`vCons` list rules.
2. `oddAcc` has one base equation and complementary
   `pyMod(I,2) == 0` / `=/= 0` recursive equations. The guards are disjoint and
   exhaustive, and recursion decreases the sequence.
3. `evenAcc` has the analogous base and complementary equations.
4. `exchangeResult` uses complementary `<=` and `>` guards and exact ASCII
   `YES`/`NO` values.
5. `ODD-BODY`, `EVEN-BODY`, and `exchangeDef` are compile-time macros exactly
   reproducing submitted AST fragments. They do not preempt operational rules.

There is no candidate-local `priority`, `owise`, `concrete`,
`no-evaluators`, opaque result, simplification, or ordinary execution rewrite
for `Call`, `Return`, `For`, or the function body.

### Operational sensitivity and abstraction boundary

`evidence/abstraction-probe-spec.k` checks that the empty iterator rule,
followed by the real `#loopStep` consumer, preserves and executes an observable
trailing assignment. The corrected probe exited 0 with `#Top`; see
`evidence/29-abstraction-probe-proof-corrected.txt`. Log 28 preserves the
reviewer's first malformed probe, which omitted the required protocol consumer
and therefore stuck at `#iterDone`; it is not candidate evidence.

The same corrected artifact documents a narrower evidence gap. Under the fixed
truthiness function:

```text
truthy(list(.ValSeq))             = false
truthy(list(intVals(.IntSeq)))    = true
```

Thus `intVals` is not a globally substitutable native-list representation.
This is a concrete conclusion witness for the abstraction limitation, not an
unsoundness claim against the two iterator equations. The submitted program
never tests list truthiness, equality, length, indexing, or mutation; it only
iterates, where the extension is exact. Both entry inputs are non-empty, and
the internal empty tail is consumed only by `#iterNext`. No false exchange
conclusion is enabled on the formal domain.

No rule is labelled unsound in this audit, so there is no unsupported
unsoundness allegation requiring a false-result witness.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is
`evidence/spec-vacuity.k`. Relative to `spec.k`, it changes only the module and
entry label/comments and replaces the result-constraining
`exchangeResult(A,B)` postcondition with concrete `"NO"` for every input. The
exact diff is `evidence/30-vacuity-mutation-diff.txt`.

The mutation is demonstrably false at the satisfying input `([2],[1])`: both
Python implementations return `"YES"`, while the mutation demands `"NO"`.
See `evidence/31-vacuity-witness-python.txt`.

The dry run:

```text
kprove spec-vacuity.k --definition verification-fresh-kompiled \
  --spec-module EXCHANGE-SPEC-VACUITY --dry-run --output pretty
```

exited 0 and emitted a valid `kore-exec` command, establishing that the mutation
parsed and built; see `evidence/32-vacuity-dry-run.txt`.

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual has
concrete returned `YES` and the satisfiable branch condition:

```text
oddAcc(0, iCons(A,AS)) <=Int evenAcc(0, iCons(B,BS))
```

which cannot unify with the demanded `NO`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. See `evidence/33-vacuity-proof-failure.txt`. The positive theorem is
therefore non-vacuous and discriminates its result.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the selected MPY supplied semantics and the proof-local transparent
integer-list representation, for every two finite, non-empty `IntSeq` values:

```text
if execution of the exact submitted exchange function reaches a return,
the returned value is
  "YES" iff oddAcc(0,lst1) <= evenAcc(0,lst2),
  "NO"  iff oddAcc(0,lst1) >  evenAcc(0,lst2).
```

The loop claims establish that `oddAcc` counts nonzero modulo-2 elements of the
first sequence and `evenAcc` counts zero modulo-2 elements of the second.
Within integer arithmetic, this is the intended odd/even count. This is a
partial-correctness result under the requested proof interpretation; no
stronger claim about fractional values, native CPython internals, or arbitrary
Python programs is made.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Byte-identical supplied MPY semantics | Entire K execution | Acceptable and required by `SUPPLIED_SEMANTICS`; relevant rules were still reviewed. |
| K compiler, Haskell/LLVM backends, reachability engine, SMT integration | Fresh builds and `#Top` | Standard toolchain trust; exact version and outcomes recorded. |
| K built-in unbounded integers, Booleans, maps/lists, string hooks, integer arithmetic/comparison | Counts, scope updates, branch guards, returned strings | Acceptable low-level primitives. `pyMod` itself is defined in supplied source and divisor 2 is nonzero. |
| `intVals(IntSeq)` plus two iterator equations | All symbolic input traversal | Transparent and structurally exact for iteration; concerning only because the candidate lacks a native-list connection theorem and the representation is not globally substitutable. |
| `oddAcc`, `evenAcc`, `exchangeResult` | Loop postconditions and final result | Fully defined by terminating, disjoint, exhaustive equations; not opaque assumptions. |
| Equivalence of odd-donor count inequality to exchange feasibility | Natural-language intent bridge | Ordinary finite matching argument, stated in stage 2; not substituted for program execution. |
| Candidate-versus-canonical integer equivalence | Intent/fidelity evidence | Supported by arithmetic reasoning and finite differential evidence; tests are not treated as a universal K proof. |
| Fractional “number” behavior | Prompt-to-theorem bridge | Excluded by the theorem and demonstrably divergent; documented concern. |

The selected semantics imports 25 explicit symbolic declarations:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
`roundFN`, `sqrtF`, `sortVS`, and `sortKeyVS`. All are fixed supplied
semantics, not candidate additions. None occurs in `solution.mpy`, the entry
claim, its loop claims, its summaries, or the execution slice that closed the
proof. They therefore have no value, control, state, termination, or
postcondition influence here.

The candidate introduces no opaque or empirical result primitive. Differential
testing supports only the implementation-to-canonical bridge over its recorded
inputs. Concrete `krun` probes support only the tested fixed-semantics
executions. Neither is used as a substitute for the successful K reachability
proof.

### Gate and verdict rationale

- Real-program soundness: **PASS**. Exact program body, fixed execution,
  transparent/counting extensions, reachable preconditions, ground witnesses,
  result constraint, and false-mutation rejection all hold.
- Intent adequacy: **LIMITED**. The integer theorem matches the ordinary
  odd/even interpretation and canonical integer behavior, but the prompt's
  broader word “numbers” admits a documented fractional ambiguity/divergence.
  The proof-only input representation also lacks a separate universal
  native-representation connection theorem.
- Evidence auditability: **PASS with provenance concern**. All reviewer
  artifacts, scripts, commands, statuses, and outputs are preserved under
  `evidence/`; `evidence/37-final-evidence-manifest.txt` indexes statuses and
  hashes. The candidate's own four generation-record artifacts are missing.

These limitations narrow the bridge from the sound theorem to the broadest
reading of the prompt, but they do not make a false result provable, replace the
program, or vacate the postcondition. The correct decision is therefore
`CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
