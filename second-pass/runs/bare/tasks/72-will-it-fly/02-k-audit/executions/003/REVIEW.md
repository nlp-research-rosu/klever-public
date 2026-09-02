# Independent adversarial review: 72-will-it-fly

## Executive conclusion

The candidate contains a freshly reproducible, non-vacuous K reachability proof
for a restricted theorem: for every finite list of mathematical integers and
every integer weight, the exact submitted constructor term returns whether the
list is a palindrome and its integer sum is at most the weight. The generated
semantics and proof-local definitions are sound for that formal domain, every
positive claim closes independently, and the program term is mechanically
pinned to trusted regeneration.

That is not the whole source contract. Neither `prompt.py` nor the trusted
canonical function restricts list elements or `w` to integers. Ordinary
floating-point weights and list elements are accepted by both trusted Python
executions, while the K configuration has only `pyList(IntList)` and
`pyInt(Int)`. This excludes a material numeric class rather than an exceptional
corner. Gate A therefore passes for the stated integer theorem, but Gate B fails
for source-domain alignment. Under the benchmark-specific decision rule, this
Kit `SOUND-BUT-LIMITED` result is `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

## 1. Input and provenance integrity

The launcher record declares:

- problem `72-will-it-fly`;
- condition `bare`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `GENERATED_SEMANTICS`; and
- no mounted reference-semantics tree.

This boundary is internally consistent: `/reference/reference-semantics` is
absent. I did not seek or use any hidden semantics.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. The required files for
`legacy-selected-stage1` are present, readable real regular files; the required
trees are real directories; and the mounted candidate, generation records,
manifests, and trusted inputs are read-only. No required candidate,
generation-evidence, or reference entry is a symlink. See
[stage1-provenance.log](evidence/stage1-provenance.log) and
[stage1-mounts.log](evidence/stage1-mounts.log).

All launcher-recorded direct hashes checked by
[provenance_check.py](evidence/provenance_check.py) reproduce, including the
canonical, trusted prompt, trusted translator, candidate prompt, candidate
translator, run/task/result manifests, invocation, metrics, usage, generation
prompt, `codex-last.txt`, and `codex-output.log`. The candidate prompt and
translator are byte-identical to their trusted mounts. A complete recursive
pipeline tree digest of `/candidate` is
`4d743293e0f748e7d267fffd69ece03191f91dc513099c1574d290e96d01eca0`,
matching both the generation result and invocation records. The analogous
trace-tree digest is
`aa38db9ba914a65a764f3a1834c9330496355e77c94715b6454ea0cf4ae66523`,
matching `usage.json`. Every per-file evidence hash in
`generation-result.json` also reproduces.

I read `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, the present `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the full structured
trace. Historical `runtime-metrics.json` is absent but is not required for this
legacy layout. The trace consists of 172 valid JSONL records, including 31 tool
calls and 31 outputs. Its bounded structural inventory is in
[stage1-generation-record-summary.log](evidence/stage1-generation-record-summary.log).
The prior `#Top` and `KPROVE_PASSED` statements were treated only as untrusted
generation claims.

Candidate source proof artifacts are present: `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. Candidate-provided
compiled/cached material, `spec.json`, logs, bytecode, and prose played no role
in reconstruction. There is no audit infrastructure breach.

The observed independent toolchain is K 7.1.293 and Python 3.10.12; see
[stage1-toolchain.log](evidence/stage1-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

In plain language, `will_it_fly(q, w)` returns true exactly when both conditions
hold:

1. `q` is balanced, meaning it is a palindromic list; and
2. the sum of its elements is less than or equal to maximum weight `w`.

The trusted canonical first rejects `sum(q) > w`, then checks mirrored elements
with two indices. The submitted implementation uses the equivalent direct
expression:

```python
return q == q[::-1] and sum(q) <= w
```

The different evaluation order is observationally irrelevant for ordinary
numeric lists and numeric weights, because both operations are pure and
defined there.

### Trusted regeneration

In scratch, the exact command

```text
python3 ../reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp solution.mpy regenerated-solution.mpy
```

exited 0. Both files have SHA-256
`7c0e0763451ba64ad5a942a7e0cf477e9755446d733bd21ae8221636efd7efa0`.
See [stage2-translation.log](evidence/stage2-translation.log).

### Independent differential execution

[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical and scratch-copied generated entry point. It covers:

- the four documented examples;
- empty and singleton lists;
- equality and one-below/one-above weight boundaries;
- mismatch positions in even and odd lists;
- negative and very large integers;
- every list over `{-2,-1,0,1,2}` through length 6 at every integer weight
  from -13 through 13; and
- 20,000 deterministic generated cases with lengths 0 through 64 and values up
  to \(10^{12}\) in magnitude.

The exact run made 547,353 comparisons, found zero mismatches, and exited 0.
See [stage2-differential.log](evidence/stage2-differential.log). This is finite
implementation-equivalence evidence, not a substitute for the K theorem.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/72-will-it-fly-audit`. No candidate-provided kompiled
definition or cache was copied or used.

### Fresh concrete semantics

The generated semantics was compiled from source with:

```text
kompile --backend llvm semantic.k \
  --main-module HUMAN-EVAL-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled-audit-llvm
```

It exited 0; see [stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).
[make_concrete_cases.py](evidence/make_concrete_cases.py) constructed each K
invocation around the trusted-regenerated module and first checked its expected
result with both Python implementations. See
[stage3-concrete-inputs.log](evidence/stage3-concrete-inputs.log).

Fresh `krun` calls covered empty-list zero and negative bounds, a singleton
threshold, unbalanced underweight input, palindrome over/at weight, negative
values and weights, and a longer palindrome. All nine exited 0 and returned the
same `pyBool` as both Python functions. The individual bounded logs are
`evidence/stage3-krun-*.log`.

### Fresh proof definition and every target claim

The proof definition was compiled from source with:

```text
kompile --backend haskell verification.k \
  --main-module HUMAN-EVAL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit-haskell
```

It exited 0; see
[stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).
Each positive claim was then selected and run separately:

| Claim | Exit | Output evidence |
|---|---:|---|
| `WILL-IT-FLY-SPEC.universal` | 0 | `#Top` in [log](evidence/stage3-kprove-universal.log) |
| `example-unbalanced` | 0 | `#Top` in [log](evidence/stage3-kprove-example-unbalanced.log) |
| `example-overweight` | 0 | `#Top` in [log](evidence/stage3-kprove-example-overweight.log) |
| `example-balanced` | 0 | `#Top` in [log](evidence/stage3-kprove-example-balanced.log) |
| `example-singleton` | 0 | `#Top` in [log](evidence/stage3-kprove-example-singleton.log) |

Thus clean reconstruction succeeds. The eventual negative verdict is not based
on a timeout, tool failure, stale cache, or failed positive proof.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiable preconditions

No claim has an explicit `requires`; its logical precondition is true together
with the typed variables and displayed configuration. The
`<generatedCounter> 0 </generatedCounter>` cell fixes generated bookkeeping and
does not restrict program inputs.

| Entry claim | Plain-language precondition | Exact postcondition | Satisfying state and Python/K result |
|---|---|---|---|
| `universal` | any `IS:IntList`, any `W:Int` | exact result `pyBool(canFly(IS,W))` | `IS=nil`, `W=0`: true |
| `example-unbalanced` | fixed `[1,2]`, `5` | exact result false | canonical/generated/K false |
| `example-overweight` | fixed `[3,2,3]`, `1` | exact result false | canonical/generated/K false |
| `example-balanced` | fixed `[3,2,3]`, `9` | exact result true | canonical/generated/K true |
| `example-singleton` | fixed `[3]`, `5` | exact result true | canonical/generated/K true |

The universal RHS is neither a fresh existential nor a tautological implication:
it constrains the returned `pyBool` to the conjunction of list-palindrome
equality and the sum bound.

### Mechanical program identity

The claim executes `run(solutionProgram, ...)`. Using K's own parser with macro
expansion, I parsed both the trusted-regenerated `solution.mpy` and the
`solutionProgram` macro under the fresh definition. `cmp` found the expanded
JSON constructor trees byte-identical; both have SHA-256
`c06a37d746b7b58a58b6f40596c28ee7cba6e4e6ddc857cf55ba39b6cdac6b93`.
The commands and output are in
[stage4-constructor-pinning.log](evidence/stage4-constructor-pinning.log).

The `run` rule structurally requires the exact binding name
`"will_it_fly"`, parameters `"q"` and `"w"`, and the actual `Return(E)` body;
it binds the two values in `env(Q,W)` and evaluates `E`. It does not replace
the submitted body with `canFly`.

### Body sensitivity

I changed the term actually executed by the claim, replacing the body's
`Name("w")` comparator operand with `Int(0)` while leaving the intended
postcondition unchanged. The mutant definition
[verification-body-mutant.k](evidence/verification-body-mutant.k) compiled
successfully. Its universal connection claim then exited 1 with
`WarnStuckClaimState`; the residual explicitly compares `sumInts(IS) <=Int 0`
against `sumInts(IS) <=Int W`. `IS=nil, W=-1` is a concrete false witness.
See [compile log](evidence/stage4-body-mutation-kompile.log) and
[proof log](evidence/stage4-body-mutation-kprove.log).

Therefore the successful claim depends on the submitted body, not merely an
external source filename or an oracle shared with the postcondition.

### Material adequacy failure

The formal universal domain is exactly `IntList × Int`. The trusted prompt has
no annotations and never says that elements or weights must be integers. The
trusted canonical and generated Python functions both execute normally on
ordinary float-valued instances. Concrete witnesses include:

```text
q=[0.25, 0.5, 0.25], w=1.0  -> True
q=[0.25, 0.5, 0.25], w=0.9  -> False
q=[1], w=1.5                 -> True
q=[-0.25, -0.25], w=-0.5    -> True
```

Both Python functions agree on every witness, as recorded in
[stage7-domain-gap.log](evidence/stage7-domain-gap.log). None has a K
representation: `Val` provides `pyInt`, `pyBool`, and `pyList(IntList)`, but no
float numeric value or float list. This is not a false semantic conclusion on
integers; it is a material strengthening of the source precondition. The
candidate therefore does not prove the full natural-language contract of the
real generated Python function.

## 5. Rule-by-rule static soundness review

There are no additional helper K files. The exhaustive numbered source and
attribute search is preserved in
[stage5-rule-inventory.log](evidence/stage5-rule-inventory.log).

### Local syntax and declarations

`MPY-SYNTAX` declares every following local production:

- `Pgm`: `Module(Stmts)`, `run(Pgm,Val,Val)`, and `programLoaded`;
- `Stmts`: one statement and statement followed by more statements;
- `Stmt`: `FuncDef(String,Params,Stmts)` and `Return(Expr)`;
- `Params`: exactly two string parameters;
- `Expr`: `Name`, `Int`, unary operation, binary `BoolOp`, single-operation
  `Compare`, single-argument `Call`, and `Subscript`;
- `CmpOp`, `Slice`, and `NoBound`;
- `IntList`: `nil` and `cons(Int,IntList)`; and
- `Val`: `pyInt`, `pyBool`, and `pyList(IntList)`.

`HUMAN-EVAL-SEMANTICS` additionally declares:

- immutable `env(Val,Val)`;
- function symbols `eval`, `negate`, `reverseVal`, `sumVal`, `compare`, and
  `boolAnd`;
- integer-valued functions `getInt` and `sumInts`;
- list-valued functions `reverseInts` and `reverseAcc`; and
- boolean-valued functions `equalVals` and `equalIntLists`.

`HUMAN-EVAL-VERIFICATION` declares the functions `balanced`,
`withinWeight`, and `canFly`, plus the `solutionProgram` macro.

Exactly 15 local symbols carry `[function]`: the 12 semantic functions and the
three verification summaries above. None is declared `[total]`. There is one
`[macro]`, `solutionProgram`. There are no local `functional`, `total`,
`opaque`, `priority`, `simplification`, or `concrete` declarations/rules.
Ordinary constructor productions carry `[symbol(...)]` only.

### Construct-to-rule coverage

Every source constructor in `solution.mpy` has both syntax and behavior:

| Submitted construct | Semantic path |
|---|---|
| `Module(FuncDef(...Params..., Return(E)))` | exact `run` structural match and `eval(E,env(Q,W))` |
| `Name("q")`, `Name("w")` | the two disjoint environment lookup rules |
| `Int(1)` and `UnaryOp("-",...)` | integer literal, `negate`, K integer subtraction |
| `Subscript(...,Slice(NoBound,NoBound,-1))` | `reverseVal` then `reverseInts/reverseAcc` |
| `Call(Name("sum"),q)` | `sumVal` then `sumInts` |
| `Compare(...,"==",...)` | `compare` then `equalVals/equalIntLists` |
| `Compare(...,"<=",...)` | `compare`, `getInt`, and K integer `<=` |
| `BoolOp("and",A,B)` | `boolAnd` and K boolean conjunction |

The concrete runs exercise every used construct, including recursion base cases
and nonempty recursive cases.

### Every ordinary rule and its justification

1. `Module(FuncDef(...Return(E))) => programLoaded` is a terminal loader marker
   in this intentionally tiny model. It discards no modeled observable cell
   because `<k>` is the only source-state cell and no invocation claim uses the
   marker as a result. It is not used to establish `will_it_fly`'s return value.
2. The `run` rule matches the sole exact target binding and evaluates its real
   returned expression under the two argument bindings. It preserves any K
   continuation because it is a local term rewrite and introduces no abrupt
   return, exception, or frame pop.
3. The eight `eval` equations—for `q`, `w`, integer literal, unary minus, exact
   `[::-1]`, builtin `sum`, comparison, and `and`—match the submitted AST and
   give their ordinary value semantics.
4. `negate`, `reverseVal`, `sumVal`, both `compare` equations, and `boolAnd`
   truthfully implement the used integer/list operations.
5. `getInt(pyInt(I))`, `sumInts(nil)`, and
   `sumInts(cons(I,IS))` are the projection, zero base case, and recursive
   mathematical integer sum.
6. `reverseInts(IS) => reverseAcc(IS,nil)`,
   `reverseAcc(nil,ACC) => ACC`, and the `cons` accumulator rule are the
   standard terminating reverse on finite inductive lists.
7. The three `equalVals` equations dispatch same-sort integer, boolean, and list
   equality. The four `equalIntLists` equations cover `nil/nil`,
   `nil/cons`, `cons/nil`, and `cons/cons`, with the recursive case comparing
   heads and tails.
8. `balanced`, `withinWeight`, and `canFly` are truthful definitional summaries:
   list equals its reverse, sum is at most weight, and their conjunction. They
   name the postcondition and do not replace source execution.
9. The `solutionProgram` macro is a constructor-level abbreviation. Its exact
   expansion was mechanically checked against trusted regeneration.

The lookup equations are disjoint by literal name. Comparison equations are
disjoint by operator. The `nil/cons` recursive equations are pairwise disjoint
and exhaustive on their declared inductive inputs. Recursion strictly removes
one list constructor. Same-sort `equalVals` equations do not overlap. Functions
are deliberately partial outside the small declared language; no false
`[total]` promise is present, and every function application reachable from the
target typed inputs is covered.

The generated semantics has no heap, allocation, mutation, output, exceptions,
or external state because this submitted body has none. K integers are
unbounded, matching Python integers. Reversal allocation/alias identity is
unobservable in the body. Treating the unshadowed name `sum` as the builtin is
sound for this exact module, which defines no such binding.

The `and` equation can evaluate both pure comparison operands instead of
modeling Python's short-circuit scheduling. On the formal `IntList × Int`
domain, both comparisons are total, side-effect free, boolean valued, and
exception free, so the returned value and all modeled state agree. This does
not enable a false conclusion on the theorem domain. It would be inadequate
for custom values with effects or exceptions, which are already outside the
model.

I found no locally unsound rule on the formal integer domain, so there is no
unsound-rule false-conclusion witness to report. The decisive problem is the
formal domain exclusion documented above, not a false equation.

## 6. Fresh non-vacuity test

I independently created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), which retains the real
program and satisfying concrete input `[3], 5` but changes the required result
from true to false.

First:

```text
kprove spec-vacuity-audit.k \
  --definition verification-kompiled-audit-haskell \
  --spec-module WILL-IT-FLY-SPEC-VACUITY-AUDIT \
  --claims WILL-IT-FLY-SPEC-VACUITY-AUDIT.false-singleton-result \
  --dry-run
```

exited 0, demonstrating successful parsing and proof-request construction; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log). Running the
same claim without `--dry-run` exited 1 with `WarnStuckClaimState`. The residual
is the reached configuration `<k> pyBool(true) ~> .K </k>`, which cannot unify
with the mutated false destination. See
[stage6-vacuity-kprove.log](evidence/stage6-vacuity-kprove.log). This is the
expected unmet result obligation, not a parser error, timeout, unrelated crash,
or unreachable mutation.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Conditioned on the fresh K definition and its mathematical builtins, the
successful universal reachability claim establishes:

> For every finite `IS:IntList` of K mathematical integers and every K
> integer `W`, executing the exact trusted-regenerated constructor body of
> `will_it_fly` in the submitted generated semantics reaches
> `pyBool(equalIntLists(IS,reverseInts(IS)) andBool
> sumInts(IS) <=Int W)`.

The four example claims are ground instances. Because the local recursive
functions are structurally descending, every concrete finite integer-list
instance also computes to a ground boolean. This is a valid partial-correctness
theorem for the formal subdomain.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, and builtin `INT`/`BOOL` mathematics | all compilation, execution, and proofs | Ordinary low-level proof trust boundary; version recorded and fresh builds used |
| Trusted `py2mpy.py` transliteration | source-to-constructor identity | Acceptable; byte regeneration and K constructor comparison reproduced |
| Generated `run`/`eval` semantics | binding, evaluation, control, and result for all claims | Audited rule by rule and tested concretely; sound for `IntList × Int` |
| Builtin `sum` binding | result of the second comparison | Acceptable for the exact structurally matched module, which cannot shadow `sum` |
| Pure/eager treatment of `and` | evaluation scheduling | Acceptable only on the formal pure typed domain; no state/result difference there |
| `balanced`, `withinWeight`, `canFly` | universal postcondition | Locally and truthfully defined; no opacity or oracle |
| Differential and concrete tests | implementation bridge for tested inputs | Finite empirical support only; not treated as a universal proof |
| Natural-language numeric domain mapped to `IntList × Int` | theorem adequacy | Illegitimate for completion: ordinary floats accepted by both Python implementations are excluded |

There are no local opaque symbols and no unconstrained fresh values affecting
the result. The K-level `sum`, reverse, equality, and bound values are all fixed
by explicit equations. No candidate prose, generation trace, differential test,
or prior `#Top` substitutes for the reconstructed K proof.

Excluded behavior includes float-valued inputs/weights, boolean-as-integer
elements, non-list sequences, custom equality/arithmetic objects, side effects,
exceptions, and alias-sensitive behavior. Most exclusions are normal for a
minimal generated semantics if outside the source contract; float numerics are
not harmless here because the prompt supplied no integer restriction and both
real Python functions support them.

### Gate and benchmark status

- Gate A, real-program soundness on the formal domain: **PASS**.
- Gate B, intent and source-domain adequacy: **FAIL** due material restriction
  from numeric lists/weights to integers.
- Gate C, evidence reproducibility and trust accounting: **PASS**.
- Generic Kit status: **SOUND-BUT-LIMITED**.
- Benchmark mapping: a material HumanEval domain narrowing is
  **FAIL / NOT_LEGIT**.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
