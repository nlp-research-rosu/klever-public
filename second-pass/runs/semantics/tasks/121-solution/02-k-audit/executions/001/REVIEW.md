# Independent adversarial audit: 121-solution

## Audit outcome

The candidate contains a legitimate partial-correctness proof of the submitted
integer-list program, but it has two auditability limitations. First, the three
proof-local arithmetic bridge rules rely on the ground meaning of `isInt` to
refine an abstract `Val` to `Int`; bridge-free theorems over the rules' exact
symbolic match domain do not close, although the equivalent typed-`Int`
theorems do. Second, the entry claim calls a manually embedded closure rather
than loading `solution.mpy`; an independent AST comparison pins that closure to
the submitted program, but the pin is external to the reachability claim.

Neither limitation supplies a false conclusion witness on the intended domain.
For every ground value admitted by `isInt`, `intProjection(I) => I` fixes the
value; typed bridge-free connection claims close; distinct ground results are
obtained; and an opposite ground projection is rejected. I therefore judge the
proof sound but not fully self-justifying: `CONCERNS / LEGIT`.

Scratch work was confined to `/tmp/audit-work/121-audit`. The candidate tree
was never modified. Reviewer-authored sources and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists. A recursive
`diff -ruN --no-dereference` between it and
`/candidate/reference-semantics` exited 0. Both trees contain the same
`semantics.k` and 23 helper files. There are no missing, additional, changed,
mistyped, or symlinked entries in the candidate semantics tree. All required
proof sources are regular files, and no candidate-provided K compiled
definition was present or copied.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted counterparts:

- `prompt.py`:
  `f5c091f79c729b97c5ed96f86e84d4d3ebee2ccae5b5ab192e98f6e265df18d5`
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The requested untrusted generation metadata is absent:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and a
structured generation trace were not present. Those are provenance gaps, not
substitutes for source reconstruction. Ancillary candidate artifacts
(`prove.sh`, concrete tests, and a Python `__pycache__`) were treated as
untrusted and were not used as proof authority.

Evidence: [stage1-integrity.log](evidence/stage1-integrity.log) and
[stage2-source-inspection.log](evidence/stage2-source-inspection.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and algorithms

The trusted prompt requires, for a non-empty list of integers, the sum of the
odd elements at even zero-based indices. The trusted canonical implementation
filters `enumerate(lst)` by `idx % 2 == 0` and `x % 2 == 1`.

The candidate starts `even_position = True`, toggles it after every element,
and, at even positions, adds:

```text
value * (value % 2)
```

For every Python integer, including negative integers, `% 2` is 0 for an even
integer and 1 for an odd integer. The candidate therefore adds exactly the odd
value at indices 0, 2, 4, ... and zero otherwise. It also returns 0 on the
out-of-contract empty-list boundary.

### Trusted translation

Running the trusted translator afresh produced a 536-byte MPY file byte-equal
to the submitted `solution.mpy`; both have SHA-256
`08c172cf52537618813be163e51562de009226cb6cb528e3b723fd9e4b8f5440`.
Evidence: [stage2-translation.log](evidence/stage2-translation.log).

### Independent differential test

The reviewer-authored
[differential_test.py](evidence/differential_test.py) independently imports
`/reference/canonical.py:solution` and the scratch copy of
`solution.py:solution`. It checks:

- all three documented examples;
- the empty-list boundary;
- singleton, sign, zero, parity, and very-large-integer cases;
- every list of lengths 0 through 5 over
  `[-100, -3, -2, -1, 0, 1, 2, 3, 100]`; and
- 2,000 deterministic generated lists, seed 121, lengths 1 through 20, values
  in `[-10^9, 10^9]`.

The exact run checked 68,443 inputs and found zero mismatches
([stage2-differential.log](evidence/stage2-differential.log)). This is finite
fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

K was independently available as v7.1.337. From source-only scratch copies:

1. The concrete definition was rebuilt with LLVM from the supplied
   `reference-semantics/semantics.k`, main module `MPY-KRUN`, syntax module
   `MPY-SYNTAX`. Exit status: 0.
2. The proof definition was rebuilt with Haskell from `verification.k`, main
   module `VERIFICATION`, syntax module `MPY-SYNTAX`. Exit status: 0.
3. Reviewer-authored concrete assertions were translated with the trusted
   translator and executed under the fresh LLVM definition. The final
   configuration had `.K`, `NoExc`, and exit code 0. The cases include the
   examples, empty input, negative odd values, mixed branches, and large
   values.

Build and execution evidence:
[stage3-kompile-concrete.log](evidence/stage3-kompile-concrete.log),
[stage3-kompile-proof.log](evidence/stage3-kompile-proof.log),
[k_concrete_tests.py](evidence/k_concrete_tests.py), and
[stage3-concrete-execution.log](evidence/stage3-concrete-execution.log).

The two positive claims were reconstructed as follows:

- `SPEC.loop-invariant`, selected alone, printed `#Top` and exited 0
  ([stage3-proof-loop-invariant.log](evidence/stage3-proof-loop-invariant.log)).
- The complete `SPEC` dependency set, which proves `solution-correct` using
  `loop-invariant` as its circularity, printed `#Top` and exited 0
  ([stage3-proof-all.log](evidence/stage3-proof-all.log)).

An additional diagnostic selected `solution-correct` while filtering out its
loop circularity. It kept symbolically unrolling and was reviewer-terminated
with status 130; it is not treated as a failed positive proof. Its purpose and
termination are recorded in
[stage3-proof-solution-correct.log](evidence/stage3-proof-solution-correct.log).
The successful complete run is the applicable entry proof, and the invariant
was also proved independently.

The concrete compiler reported non-exhaustiveness warnings for several
supplied functions (`mapStrVS`, float conversions, `joinCodes`, and
out-of-bounds `valSeqAt`). None occurs in the submitted program or its claims.
The proof build itself exited 0.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-invariant` says: in a function frame containing `total`,
`even_position`, and `value`, executing the real loop over an all-integer
remaining sequence `VS` consumes the loop and preserves the arbitrary
continuation. The final `total` is
`oddAtEvenAcc(VS, EVEN, TOTAL)`. The loop's final flag and iteration variable
are existential because the following `Return(Name("total"))` cannot observe
them. Other scopes and the frame parent are preserved.

`solution-correct` says: from the exact clean call configuration, calling the
solution closure with an all-integer list `VS` returns exactly
`oddAtEvenPositions(VS, true)`. It also requires the scope, allocation,
stack, return, exception, and exit-code cells to be restored. The destination
is an exact `Int` term, not a free variable, implication-only property, or
tautology.

### Satisfying states and concrete substitution

A satisfying loop state is obtained with `VS = [5, 8, 7, 1]`, `L = 1`,
`TOTAL = 0`, `EVEN = true`, `OLD = 0`, `LIST = list(VS)`,
`P = parent(0)`, and `KONT = .K`; `allInts(VS)` is true. A satisfying entry
state is the exact initial configuration in `spec.k` with the same `VS`.

The reviewer substituted that entry input in
[spec-witness.k](evidence/spec-witness.k). Both the ground summary and the
ground program call prove `12` with `#Top`; both Python implementations also
return 12. Evidence:
[stage4-summary-witness.log](evidence/stage4-summary-witness.log),
[stage4-entry-witness.log](evidence/stage4-entry-witness.log), and
[stage4-python-witness.log](evidence/stage4-python-witness.log).

### Real-program identity

The reachability claim calls `solutionClosure` directly rather than loading
the MPY module. This is not accepted on prose assertion alone. The reviewer:

1. parsed the trusted-translator-regenerated `solution.mpy` with `kast`;
2. expanded `solutionClosure` with the fresh proof definition; and
3. structurally compared the parsed `FuncDef` name, parameters, body, and
   closure parent.

The module has exactly one top-level statement, the function is named
`solution`, its parameter list and entire body AST equal the expanded closure,
and the closure parent is scope 0. Evidence:
[check_program_pin.py](evidence/check_program_pin.py) and
[stage4-program-pin.log](evidence/stage4-program-pin.log).

The claim uses the supplied semantics' supported unboxed read-only
`list(VS)` input representation rather than a heap reference created by a list
literal. This program only iterates and reads the argument; it does not mutate
it or observe identity. The supplied `For` rules make the boxed and unboxed
paths agree for this body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[k-rule-inventory.tsv](evidence/k-rule-inventory.tsv), generated by
[inventory_k.py](evidence/inventory_k.py) with the command recorded in
[stage5-inventory-generation.log](evidence/stage5-inventory-generation.log),
contains one line-addressed record
for every local declaration in `semantics.k`, all 23 supplied helper K files,
`verification.k`, and `spec.k`. Its 949 records exactly equal the raw
declaration-start count:

- 708 rules, 233 syntax declarations, 5 contexts, 2 claims, and 1
  configuration;
- 149 function attributes, 112 total attributes, 48 priority attributes, 35
  concrete attributes, 26 `owise` attributes, 25 symbol attributes, and 22
  `no-evaluators` opaque declarations;
- no `functional` or `simplification` attribute occurs.

Every row records its module, line span, complete normalized declaration,
attributes, proof role, and disposition. The 22 explicitly opaque supplied
symbols are float, sort, or MD5 facilities and are dormant here. The
`MPY-CONCRETE` rules are not imported by the Haskell proof. Imported rules
outside the execution slice use disjoint constructors, labels, or sorts and
cannot rewrite this program or its claims. I found no concrete or symbolic
false-conclusion witness for an inventoried supplied rule on the intended
integer-list domain.

The used construct map is:

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Int`, `Bool`, `For`, `If`, `Return`, `UnaryOp`, `BinOp`, `Call` | `semantics/syntax.k` |
| module/statement sequencing, literals, lookup, argument evaluation, values, scopes, configuration | `semantics/core.k` |
| closure creation, parameter binding, return, frame pop | `semantics/functions.k` and `semantics/call.k` |
| assignment, branch, for-loop control, continuation | `semantics/controls.k` |
| name-target loop binding | `semantics/tuple.k` |
| list iteration protocol | `semantics/iter.k` and `semantics/list.k` |
| operator dispatch and boolean `not` | `semantics/operators.k` and `semantics/bool.k` |
| integer `+`, `*`, Python-style `%` | `semantics/int.k`, aided symbolically by the three reviewed proof-local bridges |

Evaluation order is left-to-right through strictness and `#evalArgs`. The call
pushes one frame, binds `lst`, runs the exact body, and restores the caller
cells on `#pop`. The loop evaluates the iterable once, binds each `value`,
executes the branch and parity toggle, then recurs. The submitted body allocates
nothing and has no output or exceptions on integer inputs. The three bridge
rules preserve the entire continuation and touch only `<k>`, so they do not
discard control, frames, heap changes, allocation, exceptions, or output.

### Every proof-local extension

1. **`solutionLoopBody`, `solutionBody`, and `solutionClosure` macros.**
   These are syntactic abbreviations, not execution summaries. Macro expansion
   exactly matches the submitted AST as established in stage 4.

2. **`allInts`.** The empty sequence is true; a cons sequence is true exactly
   when its head satisfies the fixed sort predicate `isInt` and its tail is
   all-integer. The equations are constructor-complete, disjoint, and
   structurally decreasing.

3. **`intProjection`.** It is declared total, with
   `intProjection(I:Int) => I`. For non-integer `Val` terms it is an
   unconstrained total value, but all result-bearing uses in the entry and loop
   claims are protected by `allInts`, and every operational bridge is guarded
   by `isInt(V)`. Thus it is fixed to identity on every intended ground use.
   It is concerning because the backend does not derive that type refinement
   for an abstract `Val` automatically.

4. **Three priority-40 `BinOp` bridges.** They replace `%`, `+`, and `*` when
   an abstract operand satisfies `isInt`, returning the corresponding fixed
   integer operation over `intProjection`. They are operational bridges, not
   merely equations. Their match accepts any continuation and frames all other
   cells; their justification also covers arbitrary continuations because the
   displaced fixed rules are pure value rewrites. The `%` bridge is broader
   than this program in its divisor (`I:Int` rather than literal 2), but even at
   divisor 0 it reaches the same undefined `pyMod` residual as fixed semantics;
   the real program always uses 2.

5. **`oddAtEvenPositions` and `oddAtEvenAcc`.** These are definitional
   summaries. The empty equation returns the accumulator. The `true` cons case
   adds `V * pyMod(V, 2)` and toggles false; the `false` case skips the value
   and toggles true. Constructor and Boolean cases are disjoint, recursive
   calls strictly shorten the sequence, and on `allInts` inputs every
   projection is identity. No summary rule bypasses program execution; the
   loop claim connects the real `#loop` control state to the summary.

### Bridge connection and value-sensitivity experiments

The reviewer built
[verification-bridgefree.k](evidence/verification-bridgefree.k), which imports
the fixed supplied semantics and the projection equation but omits all three
operational bridges. The connection claims are in
[spec-bridge-connections.k](evidence/spec-bridge-connections.k), and the clean
build is recorded in
[stage5-kompile-bridgefree.log](evidence/stage5-kompile-bridgefree.log).

Exact universal claims over the candidate rules' symbolic domain
(`V:Val` plus `isInt(V)`) all get a genuine stuck implication: fixed semantics
leaves `applyBin(..., V, ...)` because the backend cannot turn the predicate
into a syntactic `Int`. Evidence:
[stage5-bridge-mod-connection.log](evidence/stage5-bridge-mod-connection.log),
[stage5-bridge-add-connection.log](evidence/stage5-bridge-add-connection.log),
and [stage5-bridge-mul-connection.log](evidence/stage5-bridge-mul-connection.log).

The corresponding bridge-free typed-`Int` theorems, with arbitrary
continuations, all print `#Top`:
[stage5-bridge-mod-typed.log](evidence/stage5-bridge-mod-typed.log),
[stage5-bridge-add-typed.log](evidence/stage5-bridge-add-typed.log), and
[stage5-bridge-mul-typed.log](evidence/stage5-bridge-mul-typed.log).

Ground projections 3→3 and 4→4 close, while the opposite interpretation 3→4
gets `WarnStuckClaimState`:
[stage5-projection-three.log](evidence/stage5-projection-three.log),
[stage5-projection-four.log](evidence/stage5-projection-four.log), and
[stage5-projection-opposite.log](evidence/stage5-projection-opposite.log).
The reviewer concrete suite also completes under the bridge-enabled Haskell
definition ([stage5-bridge-ground-execution.log](evidence/stage5-bridge-ground-execution.log)).

Accordingly, I do **not** label these rules unsound: no intended ground witness
can make them produce a false value, and the opposite ground interpretation is
rejected. The narrower evidence gap is that the candidate does not contain a
bridge-free, machine-checked connection theorem over its exact symbolic
`Val + isInt` match syntax. The proof therefore trusts the standard initial-
algebra meaning of the sort predicate as a type-refinement fact.

## 6. Fresh non-vacuity test

The reviewer-authored [spec-vacuity.k](evidence/spec-vacuity.k) calls the exact
solution closure on `[5, 8, 7, 1]` but changes the result-constraining
destination from the true result 12 to the false result 13.

- `kprove ... --dry-run` exited 0, demonstrating that the mutation parses and
  builds ([stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log)).
- The actual proof exited 1 with `WarnStuckClaimState`. Its residual
  configuration has `<k> 12 ~> .K </k>` and cannot unify with destination 13
  ([stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log)).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. It demonstrates that the entry proof is
reachable and result-discriminating.

## 7. Proven-versus-assumed accounting

### What the successful reachability proof establishes

Under the supplied K semantics, for every finite `ValSeq` whose elements
satisfy `isInt`, starting from the entry configuration in `spec.k`, execution
of the exact submitted solution body returns:

```text
oddAtEvenPositions(VS, true)
```

The loop proof establishes this by a circular invariant over the actual
`#loop` control state. Expanding the summary gives the initial accumulator 0,
alternating even/odd position state, and addition of
`x * pyMod(x, 2)` only at even positions. The proof also restores the listed
scope, stack, allocation, return, exception, and exit-code cells. This is a
partial-correctness theorem; it does not use differential tests as a proof
rule.

For Python integers and divisor 2, `pyMod(x, 2)` is 1 exactly for odd `x` and
0 for even `x`. Therefore the K result equals the prompt's sum of odd elements
at even positions. The formal precondition permits the empty list, so it is
slightly stronger than the prompt's non-empty domain rather than weaker.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 frontend, Haskell reachability backend, and builtin integer/Boolean theory | all machine results | Normal low-level proof-tool trust. |
| The recursively identical supplied reference semantics | execution of the MPY body | Authorized fixed semantics. The used subset was traced rule by rule and tested concretely; dormant opaque facilities do not influence this theorem. |
| Trusted `/reference/py2mpy.py` | Python-to-MPY source bridge | Accepted trusted input; fresh output is byte-identical to the submitted MPY. |
| Ground meaning of `isInt` and `intProjection(I) => I` | all three arithmetic bridges and the result summary | Sound on intended ground inputs, supported by typed connection and opposite-value tests, but the exact symbolic universal connection theorem is absent. This is the principal concern. |
| External AST equality between `solutionClosure` and parsed `solution.mpy` | real-program identity | Mechanically checked and exact, but not itself a claim in the candidate proof. |
| Mathematical equivalence of the alternating fold to the natural-language contract | intent bridge | Simple informal parity argument plus 68,443 differential cases; not misrepresented as a K theorem about `canonical.py`. |

No supplied float, sorting, keyed sorting, MD5, or other opaque symbol reaches
the control flow or result. `intProjection` is the only proof-local total
abstraction affecting the result, and it is fixed on every admitted ground
element.

Excluded behavior includes non-integer elements, arbitrary Python iterables,
custom operator overloading, mutation/identity observations of the argument,
and Python behaviors outside the supplied MPY subset. Those exclusions do not
weaken the stated problem domain. Missing generation metadata limits
provenance auditability but does not replace or invalidate the reconstructed
source proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
