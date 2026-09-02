# Independent adversarial review: 145-order-by-points

The candidate reconstructs cleanly and all eight submitted reachability claims
produce `#Top`. It nevertheless does **not** contain a legitimate proof of the
requested sorting property. The only generic entry claim ends in the
equation-free term `sortKeyVS(VS, digitSumClosure)`. In the proof definition,
that operation never calls the program-defined `digit_sum` body and no theorem
connects the opaque term to stable sorting by the body's returned values. This
is a result-bearing oracle at exactly the property the task asks to prove.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
mode/mount infrastructure contradiction.

I treated all candidate material as untrusted and checked file types before
copying source artifacts to `/tmp/audit-work/145-order-by-points`.

- Recursive `diff -ru --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exited 0. The trees have identical entries and
  contents; no entry in either tree is a symlink. See
  [01-semantics-integrity.log](evidence/01-semantics-integrity.log).
- The candidate prompt and translator are byte-identical to the trusted
  versions (`cmp`, exit 0). See
  [02-prompt-integrity.log](evidence/02-prompt-integrity.log) and
  [03-translator-integrity.log](evidence/03-translator-integrity.log).
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and the semantic
  sources are regular files. The candidate contains an untrusted
  `__pycache__`, but no cache or compiled definition was copied or used.
- `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log` are all
  missing. No structured generation trace is present. These are provenance
  gaps, recorded in
  [04-file-types-and-required-metadata.log](evidence/04-file-types-and-required-metadata.log);
  they are not the reason for the verdict.
- Source hashes, including the regenerated `.mpy` hash, are recorded in
  [21-source-hashes.log](evidence/21-source-hashes.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a list of integers, return a stable ascending ordering by digit sum. For a
negative integer, the canonical implementation negates the most significant
decimal digit, so, for example, the key of `-123` is `-1 + 2 + 3 = 4`.
Elements with equal keys retain their original relative order. The empty list
returns the empty list.

The submitted implementation uses ordinary integer arithmetic. After taking
`abs(n)`, its loop adds all decimal digits and retains the most significant
digit as the last remainder encountered. For an originally negative input it
subtracts twice that digit, changing its contribution from positive to
negative. Zero is handled by the initialized values. `sorted(...,
key=digit_sum)` supplies stability. This is a different but faithful algorithm
on the intended integer domain.

The trusted translator regenerated the submitted constructor program in
scratch, and the result is byte-identical to the submitted `solution.mpy`
(`cmp`, exit 0):
[05-regenerate-solution-mpy.log](evidence/05-regenerate-solution-mpy.log) and
[06-solution-mpy-identity.log](evidence/06-solution-mpy-identity.log).

The independent differential test imports
`/reference/canonical.py:order_by_points` and the scratch copy of the submitted
entry point. It covers the two documented cases, zero and sign/decimal
boundaries, ties and duplicates, large integers, every list of lengths 0
through 3 over a 23-value boundary pool, and 5,000 deterministic generated
lists of lengths 0 through 30. All 17,733 cases agree. The script and complete
scope/result are
[differential_test.py](evidence/differential_test.py) and
[07-differential-test.log](evidence/07-differential-test.log).

This establishes strong finite program-fidelity evidence, not a universal K
proof.

## 3. Clean proof reconstruction

Only source files were copied to scratch. Candidate-built definitions and
caches were neither copied nor referenced. The available toolchain is K
v7.1.337; see [08-toolchain.log](evidence/08-toolchain.log).

Fresh builds succeeded:

- LLVM concrete definition:
  `kompile reference-semantics/semantics.k --backend llvm --main-module
  MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`
  (exit 0), in
  [09-build-concrete-llvm.log](evidence/09-build-concrete-llvm.log).
- Haskell proof definition:
  `kompile verification.k --backend haskell --main-module
  ORDER-BY-POINTS-VERIFICATION --syntax-module MPY-SYNTAX
  --output-definition verification-kompiled` (exit 0), in
  [10-build-proof-haskell.log](evidence/10-build-proof-haskell.log).

The LLVM build warned about several non-exhaustive total functions in unrelated
semantic modules. None occurs on this program's used execution path. The
concrete submitted program then completed four embedded assertion suites with
`.K`, `NoExc`, and exit code 0:
[11-concrete-semantics-tests.log](evidence/11-concrete-semantics-tests.log).

The byte-faithful candidate spec proved as a whole with exit 0 and `#Top`:
[12-kprove-all-positive.log](evidence/12-kprove-all-positive.log). I then made
a reviewer-only labeled copy, [spec-labeled.k](evidence/spec-labeled.k), and
ran every original positive target independently:

- seven `digit_sum` targets:
  [digit-0](evidence/13-kprove-digit-0.log),
  [digit-1](evidence/13-kprove-digit-1.log),
  [digit-11](evidence/13-kprove-digit-11.log),
  [digit-neg-1](evidence/13-kprove-digit-neg-1.log),
  [digit-neg-11](evidence/13-kprove-digit-neg-11.log),
  [digit-neg-12](evidence/13-kprove-digit-neg-12.log), and
  [digit-neg-123](evidence/13-kprove-digit-neg-123.log);
- the generic entry target:
  [order-generic](evidence/13-kprove-order-generic.log).

Every run exited 0 and printed `#Top`. Closure is genuine under the submitted
theory, but closure alone does not validate that theory's result-bearing
abstraction.

## 4. Adequacy and real-program pinning

### Claims in plain language

The first seven claims all have one concrete argument. Starting with environment
0, `initialScopes`, empty heap/stack, location counters 1 and 0, no pending
return, and no exception, they load both submitted definitions and call
`digit_sum`. They require the results:

| Input | Claimed result |
|---:|---:|
| 0 | 0 |
| 1 | 1 |
| 11 | 2 |
| -1 | -1 |
| -11 | 0 |
| -12 | 1 |
| -123 | 4 |

These are seven ground executions, not a quantified characterization of
`digit_sum`.

The eighth claim has no `requires` clause. For every K `ValSeq`—not merely
integer elements—it starts from the same concrete initial state, calls
`order_by_points(list(VS))`, returns fresh reference 0, and requires heap
location 0 to contain:

```k
list(sortKeyVS(VS, digitSumClosure))
```

with heap allocation advanced to 1, module definitions loaded, empty
call stack, no pending return, and no exception. The omitted `exit-code` cell is
framed.

Every entry precondition is satisfiable. Examples include `VS = .ValSeq`,
`VS = vCons(1, .ValSeq)`, and
`VS = vCons(11, vCons(1, .ValSeq))`, together with the explicitly stated
initial cells.

### Program identity

The two proof-local bodies are exact constructor abbreviations for the trusted
translator output. `solutionModule` contains those two definitions in the same
order. The `#run...` rules perform `#loadAll(solutionModule)` and then an
ordinary named call; they do not directly manufacture a return value.

I added a reviewer-only inert wrapper and proved that K normalizes
`solutionModule` to the explicit, parser-normalized constructor tree from
`solution.mpy`. The fresh identity definition built successfully and the
identity claim produced `#Top` (reported as a trivial normalization claim):
[identity-verification.k](evidence/identity-verification.k),
[spec-program-identity.k](evidence/spec-program-identity.k),
[19a-build-program-identity-definition.log](evidence/19a-build-program-identity-definition.log),
and
[19b-program-identity-proof.log](evidence/19b-program-identity-proof.log).
Together with the trusted translation byte comparison, this pins the executed
module to the real submitted program.

### Material result-adequacy failure

The generic return is syntactically constrained, but not to a mathematically
defined output. `sortKeyVS` has no proof-side equations. Its only proof-side
use is both:

1. the result manufactured by the abstract `sorted(..., key=KV)` transition,
   and
2. the term repeated in the postcondition.

Consequently the theorem does not show which permutation is returned, that
keys were evaluated, that ordering is ascending, or that ties are stable. Most
importantly, it does not connect the program-defined `digit_sum` body to the
key values used by the generic result.

Ground substitution makes the separation explicit. Both Python
implementations return `[1, 11]` for `[11, 1]` and
`[-1, -11, 1, -12, 11]` for the documented example, while the formal RHS
remains an irreducible `sortKeyVS` term:
[ground_claim_substitution.py](evidence/ground_claim_substitution.py) and
[20-ground-claim-substitution.log](evidence/20-ground-claim-substitution.log).

The formal domain is also broader than the intended list-of-integers domain.
The abstract sort transition returns an opaque term even for values on which
the actual key body would not execute successfully. That over-breadth reinforces
the bypass, although the integer-domain oracle gap alone is decisive.

## 5. Rule-by-rule static soundness review

The exhaustive source-linked inventory is
[rule-inventory.md](evidence/rule-inventory.md), generated by
[build_rule_inventory.py](evidence/build_rule_inventory.py) with the command
and exit status in
[14-build-rule-inventory.log](evidence/14-build-rule-inventory.log). It
enumerates 951 declarations/contexts/configuration/rules/claims: 233 syntax
entries, 704 rules, 5 contexts, 1 configuration, and 8 claims. There are no
candidate simplification rules or `functional` declarations.

### Module assessment

| Source group | Exhaustive assessment |
|---|---|
| `semantics.k`, `syntax.k`, `iter.k` | Assembly/imports and grammar/protocol declarations. The submitted constructors all have unambiguous declarations. No result equation is introduced here. |
| `core.k` | Configuration, loading, sequencing, lookup, left-to-right argument evaluation, literal evaluation, allocation, and list helper equations were checked. On the used path they preserve all cells and match the submitted program. Priority-40 rules concern heap/cell dereference; they do not preempt a used plain-value operation incorrectly. |
| `operators.k`, `int.k`, `bool.k` | The used `<`, `%`, `+`, `-`, `*`, `//`, truthiness, and comparison routing match integer/Python behavior on the actual path. `n` is made nonnegative before `% 10` and `// 10`; division by zero is unreachable. Guards are disjoint for the used cases. |
| `controls.k` | Used assignment, augmented assignment, `If`, and `While` rules evaluate in the right order and update the current scope. While repeats the real condition/body. Return handling is in `functions.k`. No loop summary or proof shortcut is present. |
| `functions.k`, `call.k` | Module definitions create the exact closures, parameter binding creates/restores a fresh scope, return unwinds the exact saved continuation, and calls resolve the callee and arguments before dispatch. The `sorted` and `abs` names are selected through the real builtins scope. |
| `builtins.k` | The used `abs(Int)` equation is ordinary integer absolute value. Other folds, conversions, `eval`, and `md5hexCodes` are unused. `md5hexCodes` and several broad total declarations are explicit trust/incompleteness boundaries, but they cannot contribute to this program's conclusion. |
| `sort.k` | Concrete unkeyed insertion rules, reverse helpers, and unkeyed abstractions are not used. The used keyed rule at lines 61–62 is the decisive operational bridge: it replaces a call that should invoke `KV` on every element with allocation of `list(sortKeyVS(VS, KV))`. `sortKeyVS` at line 49 is `[function,total,symbol,no-evaluators]` with no equations. |
| `concrete.k` | Only `MPY-KRUN` imports this module. Its used keyed-sort rules really call `KV` and stable-insert each `(key,value)` pair, which explains the successful concrete tests. The proof module imports `MPY`, not `MPY-CONCRETE`, so these rules and calls do not justify proof closure. |
| `range.k`, `float.k`, `str.k`, `set.k`, `list.k`, `tuple.k`, `subscript.k`, `comprehension.k`, `methods.k`, `assert.k`, `dict.k` | Every declaration and rule is inventoried. Except for shared declarations already identified above, these constructs are absent from the submitted function bodies and do not contribute to the target proof. Several files deliberately model restricted subsets or opaque float/digest operations. I found no rule from these modules that can enable a false conclusion on this submitted program's intended integer-list executions, so I do not label those unused limitations unsound. |
| `verification.k` | `digitSumBody`, `orderByPointsBody`, both closures, `solutionModule`, and the scope constants are terminating definitional abbreviations with exact RHSs. The two `#run...` rules are faithful entry wrappers and preserve framed cells. There are no local priorities or simplifications. Their truth does not supply the missing meaning of `sortKeyVS`. |
| `spec.k` | The seven helper claims are truthful ground executions. The generic claim repeats the opaque sort result and has no mathematical sortedness/digit-sum postcondition. |

### Used-construct map

`Module` and statement sequencing map to `syntax.k` plus
`core.k:#loadAll`; `FuncDef`, call frames, parameter binding, and return map to
`functions.k`/`call.k`; `Name`, `Int`, and `KwArg` map to lookup/literal/argument
rules in `core.k`; `Assign`, `AugAssign`, `While`, and `If` map to `controls.k`;
`Compare`, `BinOp`, and truthiness map through `operators.k`, `int.k`, and
`bool.k`; `abs` maps to `builtins.k`; and the final keyed call maps to
`sort.k:61-62`. Thus every submitted constructor is declared and reaches a
rule. The gap is not missing syntax—it is the deliberate replacement of the
property-bearing keyed computation.

### False-conclusion and body-sensitivity witnesses

The issue is not merely that a connection theorem was omitted from the prose.
The proof is insensitive to the key body's meaning:

- I replaced the entire `digitSumBody` with `Return(Int(0))`, rebuilt from
  source, and reran only the generic order claim. It still exited 0 with
  `#Top`: [verification-key-body-mutant.k](evidence/verification-key-body-mutant.k),
  [15-build-key-body-mutant.log](evidence/15-build-key-body-mutant.log), and
  [16-prove-order-with-wrong-key-body.log](evidence/16-prove-order-with-wrong-key-body.log).
- The satisfying input `[11, 1]` is a concrete false-conclusion witness.
  Correct digit sums are 2 and 1, so the required result is `[1, 11]`; a
  constant-zero key stably returns `[11, 1]`. See
  [key_body_counterexample.py](evidence/key_body_counterexample.py) and
  [17-key-body-counterexample.log](evidence/17-key-body-counterexample.log).
- To test the opaque value directly, I supplied the otherwise-admissible
  opposite interpretation `sortKeyVS(VS, _) => VS`. Because the original
  symbol has no equations, this selects a behavior its proof theory does not
  rule out. The extended definition built, and a ground claim that the real
  submitted entry returns the wrong `[11, 1]` produced `#Top`:
  [opposite-verification.k](evidence/opposite-verification.k),
  [spec-opposite.k](evidence/spec-opposite.k),
  [22-build-opposite-sort-model.log](evidence/22-build-opposite-sort-model.log),
  and
  [23-prove-false-opposite-result.log](evidence/23-prove-false-opposite-result.log).

The Python `sorted` implementation itself could reasonably be an external
trusted primitive. This abstraction is broader: it also skips execution of a
program-defined, result-bearing key function and then carries that same closure
symbol into the postcondition. A name and finite tests do not fix the value.
No bridge-free universal theorem establishes that fixed execution yields
`sortKeyVS`, and no universal helper theorem establishes the intended digit
sum. This is an illegitimate task-answer oracle, not an acceptable low-level
arithmetic or library trust boundary.

## 6. Fresh non-vacuity test

I created a fresh spec that keeps the real entry execution but changes the
final heap obligation to `0 |-> list(.ValSeq)`. It is demonstrably false for
the satisfying input `[1]`, whose real result is `[1]`.

The mutation is [spec-vacuity.k](evidence/spec-vacuity.k). `kprove` successfully
parsed and executed it to the result state, then exited 1 with
`WarnStuckClaimState`; the residual explicitly requires the unmet equality
`.ValSeq == sortKeyVS(VS, digitSumClosure)`. This is the expected proof
failure—not a parser error, missing import, timeout, or unrelated crash:
[18-false-result-mutation.log](evidence/18-false-result-mutation.log).

Therefore the submitted generic claim does discriminate its opaque result from
an arbitrary constant. This passes the narrow non-vacuity test but does not
repair the missing meaning of the opaque result.

## 7. Proven versus assumed accounting

### What the successful proof actually establishes

Under the supplied Haskell proof semantics and its uninterpreted
`sortKeyVS`, loading the exact submitted module and calling
`order_by_points(list(VS))` allocates a fresh list whose sequence is the term
`sortKeyVS(VS, digitSumClosure)`. It also establishes seven concrete executions
of `digit_sum`.

It does **not** establish that the generic sequence is a permutation of `VS`,
that it is ordered by any key, that key calls occur, that ties are stable, or
that `digitSumClosure` returns the canonical digit sum for every integer.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 compiler/prover and standard INT/BOOL/MAP/LIST hooks | All machine results | Normal toolchain trust. Fresh builds and exact statuses are recorded. |
| Supplied core/call/control/integer semantics | Real-module loading, helper ground claims, entry execution up to `sorted` | Acceptable for the used path after static review and concrete reconstruction. |
| Proof-local body/scope constants | Program identity and exact bindings | Acceptable definitional abbreviations; independently normalized against the translator output. |
| `sortKeyVS(ValSeq, Val)` plus `sort.k:61-62` | Entire generic result | Illegitimate. It is equation-free, result-bearing, bypasses program-defined key execution, and is repeated in the postcondition. |
| `MPY-CONCRETE` keyed insertion sort | LLVM smoke tests only | Reasonable concrete bridge evidence, but excluded from the Haskell proof definition and therefore not a proof premise or connection theorem. |
| Seven ground `digit_sum` claims | Only those seven inputs | Valid but far too weak to characterize the key over all integers. They are not used to close the generic sort claim. |
| Trusted canonical Python implementation and 17,733-case differential run | Source-to-intent confidence | Strong finite evidence only. It cannot define the opaque K symbol universally or replace a K connection proof. |
| Informal mathematical argument for the submitted digit loop | Human understanding of source correctness | Plausible and supported by tests, but absent as a quantified K theorem and bypassed by the generic K claim. |

The candidate therefore proves a conditional execution shape under an
unconstrained oracle, not the requested partial-correctness property of the
real generated program. Clean `#Top`, source fidelity, differential success,
and a valid false-postcondition rejection do not cure that material adequacy
and trust-boundary failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
