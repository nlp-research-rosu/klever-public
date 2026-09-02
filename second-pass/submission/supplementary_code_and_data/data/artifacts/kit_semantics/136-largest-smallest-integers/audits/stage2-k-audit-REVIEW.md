# Independent adversarial review: 136-largest-smallest-integers

This review treats every candidate artifact and every generation trace as
untrusted evidence. I rebuilt the definitions from source in
`/tmp/audit-work/review-136`, using a fresh copy of the trusted mounted
semantics, translator, prompt, and canonical implementation. I did not use any
candidate `*-kompiled` directory, cache, binary, or claimed `#Top`.

The completed audit finds a legitimate, result-constraining partial-correctness
proof of the submitted generated program over the full stated domain of finite
integer lists.

## 1. Input and provenance integrity

### Declared layout and infrastructure

`/audit-input.json` declares:

- problem `136-largest-smallest-integers`;
- condition `kit-semantics`;
- record layout `pipeline-v3`; and
- semantics mode `SUPPLIED_SEMANTICS`.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` is present as a real directory. The candidate,
generation-evidence, trace, and reference mounts are also real directories, and
all launcher-required records are readable regular files. No required
provenance mount or pipeline-v3 record is absent, unreadable, or mistyped.
There is therefore no infrastructure breach requiring `AUDIT_ERROR`.

The independent checker and its exact output are
[verify_provenance.py](/audit-output/evidence/verify_provenance.py) and
[stage1-provenance.log](/audit-output/evidence/stage1-provenance.log). It:

- deep-compared the campaign block in `/audit-input.json` with
  `/audit-campaign-lock.json`;
- recomputed the lock SHA-256 as
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the launcher-recorded hash;
- recomputed all declared file hashes for the trusted inputs, run/task/result
  manifests, invocation, metrics, runtime metrics, usage, prompt, last
  response, transcript, and structured trace;
- checked the invocation and generation-result evidence maps for equality; and
- checked all trace entries against the per-file hashes recorded by the
  launcher.

All checks passed.

### Required pipeline-v3 generation records

I inspected `/run.json`, `/task.json`, `/generation-result.json`, and all
required files under `/generation-evidence`: `invocation.json`,
`metrics.json`, `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured JSONL trace. These remain
untrusted historical claims and were not used to establish proof success.

The structured trace has 724 valid JSON records from
`2026-07-25T08:06:06.561Z` through `2026-07-25T08:40:27.510Z`; its complete
type/tool summary is in
[stage1-trace.log](/audit-output/evidence/stage1-trace.log). The transcript
reader consumed all 71,406 lines (2,417,194 bytes) of `codex-output.log`;
marker counts and endpoints are in
[stage1-generation-log.log](/audit-output/evidence/stage1-generation-log.log).
The numerous historical `#Top`, stuck-claim, error, and `VALIDATED` strings in
those records were treated only as claims.

### Prompt, translator, and supplied-semantics identity

The candidate [prompt.py](/candidate/prompt.py) and
[py2mpy.py](/candidate/py2mpy.py) are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Their recomputed hashes are,
respectively:

```text
9dd2a92d4b141565a666931ff044c4c6109db09520ed710c3651e9ae51d80ec8
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
```

I recursively compared `/candidate/reference-semantics` with
`/reference/reference-semantics`, including relative names, entry types, and
file bytes. Both trees have the same 25 entries; there are no missing,
additional, changed, mistyped, or symlinked entries. An independently defined
manifest digest was identical for both trees:

```text
c5c09ab0e89570b1c8b9d4233634d7bbeff8c2eb47c5ca8a65e793cce544d946
```

This establishes semantics integrity. It does not bless the candidate-local
rules reviewed in stage 5.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires `largest_smallest_integers(lst)` to return a
two-element tuple:

1. the largest negative integer (the negative value closest to zero), or
   `None` if the list has no negative integer; and
2. the smallest positive integer, or `None` if the list has no positive
   integer.

Zero belongs to neither side. The documented examples cover a positive-only
list, the empty list, and `[0]`.

The trusted [canonical.py](/reference/canonical.py:6) filters the negative and
positive elements, then uses `max` and `min`. The submitted
[solution.py](/candidate/solution.py:1) uses zero sentinels and one loop. For
each element it replaces the negative sentinel/candidate exactly when the
element is negative and larger than the current candidate, and dually replaces
the positive candidate exactly when the element is positive and smaller. This
is a different but contract-equivalent algorithm for integer lists.

### Trusted regeneration

In scratch I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands together exited 0; see
[stage2-translate.log](/audit-output/evidence/stage2-translate.log). The
preserved regenerated file is
[regenerated-solution.mpy](/audit-output/evidence/regenerated-solution.mpy).
Thus the submitted [solution.mpy](/candidate/solution.mpy) is byte-identical to
trusted translation of the actual submitted `solution.py`.

### Independent differential test

I wrote a new test, independent of the candidate test:
[differential_test.py](/audit-output/evidence/differential_test.py). It loads
the trusted canonical and submitted generated Python entry points from explicit
paths. Its cases were:

- 15 named examples and boundary/branch cases: all prompt examples, empty,
  zero, negative-only, positive-only, first/later update and no-update orders,
  duplicates, mixed signs, zeros between candidates, and 100-digit integers;
- all 19,608 lists of lengths 0 through 5 over `[-3, -2, -1, 0, 1, 2, 3]`; and
- 500 deterministic random lists, seed 136, lengths 0 through 50, with values
  from `[-1,000,000, 1,000,000]`.

The exact run in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log)
exited 0:

```text
source=named checked=15
source=exhaustive[-3,3],len<=5 checked=19608
source=random(seed=136) checked=500
checked=20123 mismatches=0
```

Finite testing is used only as implementation/canonical bridge evidence, not as
a substitute for the universal K claim.

## 3. Clean proof reconstruction

### Fresh definitions and concrete execution

K, `krun`, and `kprove` independently reported version 7.1.293; see
[stage3-toolchain.log](/audit-output/evidence/stage3-toolchain.log).

I copied only source artifacts into scratch and copied the trusted
`/reference/reference-semantics` tree, rather than a candidate definition.
Every output definition used a new `audit-*` name. The fresh LLVM definition:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

exited 0; full bounded output is
[stage3-kompile-llvm.log](/audit-output/evidence/stage3-kompile-llvm.log).

I also created a fresh concrete program with six assertions covering the three
prompt examples, both update orders, mixed signs, zero, and very large
integers: [concrete-probe.py](/audit-output/evidence/concrete-probe.py), with
trusted translation preserved as
[concrete-probe.mpy](/audit-output/evidence/concrete-probe.mpy). `krun` exited
0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`;
see [stage3-krun-concrete-probe.log](/audit-output/evidence/stage3-krun-concrete-probe.log).

### Fresh Haskell builds

These clean builds all exited 0:

| Definition | Source/main module | Evidence |
|---|---|---|
| `audit-connection-kompiled` | `connection.k` / `CONNECTION` | [log](/audit-output/evidence/stage3-kompile-connection.log) |
| `audit-verification-core-kompiled` | `verification-core.k` / `VERIFICATION-CORE` | [log](/audit-output/evidence/stage3-kompile-core.log) |
| `audit-verification-kompiled` | `verification.k` / `VERIFICATION` | [log](/audit-output/evidence/stage3-kompile-verification.log) |

No candidate definition or cache was referenced.

### Every positive claim

I ran every positive labeled claim separately, then every complete spec module.
Each command exited 0 and printed `#Top`:

| Spec / claim | Result | Evidence |
|---|---:|---|
| `CONNECTION-SPEC.int-vals-empty-iterator` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-connection-empty.log) |
| `CONNECTION-SPEC.int-vals-cons-iterator` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-connection-cons.log) |
| all of `CONNECTION-SPEC` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-connection-all.log) |
| `LOOP-SPEC.loop-connection` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-loop-connection.log) |
| all of `LOOP-SPEC` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-loop-all.log) |
| `SPEC.loop-invariant` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-spec-loop.log) |
| `SPEC.entry` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-spec-entry.log) |
| all of `SPEC` | `#Top`, 0 | [log](/audit-output/evidence/stage3-prove-spec-all.log) |

The clean dynamic reconstruction gate therefore passes.

The compiler warned about several non-exhaustive fixed-semantics total
functions and unused fixed-semantics string variables. Those warnings are
accounted for in stages 5 and 7; none of the warned functions is reachable from
this integer-list program or its proof.

## 4. Adequacy and real-program pinning

### Claims in plain language

The two claims in
[connection-spec.k](/candidate/connection-spec.k:6) state the two constructor
observations of the proof-input representation:

- an encoded empty integer sequence iterates to `#iterDone`; and
- an encoded `iCons(I, IS)` yields `I` and the encoded tail.

The [loop-connection claim](/candidate/loop-spec.k:6) says that, whenever the
current negative candidate is non-positive and the current positive candidate
is non-negative, executing the exact remaining `lsiLoopBody` over encoded
`IS` consumes the loop and updates:

- `largest_negative` to `scanNeg(IS, N)`;
- `smallest_positive` to `scanPos(IS, P)`; and
- the loop target `value` to `lastValue(IS, CURRENT)`.

It preserves the arbitrary continuation and every omitted cell. The
`SPEC.loop-invariant` claim has the same transition under the final proof
definition.

The [entry claim](/candidate/spec.k:26) begins in the supplied initial module
state, loads a function named `largest_smallest_integers` with one parameter
`lst` and body `lsiBody`, calls that binding with an arbitrary finite encoded
integer list, and requires the returned value to be exactly:

```text
tuple(vCons(negativeResult(scanNeg(IS, 0)),
       vCons(positiveResult(scanPos(IS, 0)), .ValSeq)))
```

It also constrains the function binding, environment, scope allocator, empty
heap and heap allocator, empty call stack, return cell, exception cell, and
exit code after the call. There is no free result variable, implication-only
postcondition, or tautological destination.

### Mechanical body identity

Trusted regeneration first pins `solution.py` to `solution.mpy`. I then parsed
both:

1. the complete regenerated `solution.mpy`; and
2. a complete `Module(FuncDef(..., lsiBody))` term matching the entry claim,

with the fresh verification definition, module `VERIFICATION`, sort `Module`,
and `--expand-macros --output json`. The source probe is
[claimed-program.mpy](/audit-output/evidence/claimed-program.mpy); the expanded
constructor trees are
[solution-expanded.json](/audit-output/evidence/solution-expanded.json) and
[claimed-expanded.json](/audit-output/evidence/claimed-expanded.json).

The two `kast` commands exited 0, and byte comparison of the expanded JSON
trees exited 0:

- [solution parse log](/audit-output/evidence/stage4-kast-solution.log)
- [claim parse log](/audit-output/evidence/stage4-kast-claim.log)
- [constructor comparison](/audit-output/evidence/stage4-constructor-compare.log)

This is a mechanical constructor-level comparison, not a visual source
similarity claim. The entry theorem executes the submitted function binding
and body. The only normalization is expansion of the candidate's syntax
macros to that identical body.

The body then uses supplied rules for module loading, binding, lookup, argument
evaluation, call-frame push/pop, integer literals and comparisons, Boolean
short-circuiting, list iteration, assignments, branches, tuple construction,
`None`, and return. The loop operational summary is separately connected to
execution in stage 5.

There is no automatic source-to-proof regeneration script for `lsiBody`; that
is a maintenance observation. For this immutable candidate, trusted
regeneration plus the constructor comparison pins the body.

### Satisfiable entry state and concrete substitution

The entry precondition is satisfiable. I instantiated it with:

```text
IS = [-3, -1, 0, 4, 2]
```

under the exact initial cells in the entry claim. Both trusted canonical Python
and submitted Python return `(-1, 2)` (included in the independent
differential run). The fresh K ground claim
[ground-spec.k](/audit-output/evidence/ground-spec.k) requires the same
`(-1, 2)` value and closed with `#Top`, exit 0; see
[stage4-ground-entry.log](/audit-output/evidence/stage4-ground-entry.log).

The loop precondition is likewise satisfiable with the same sequence,
`N = 0`, `P = 0`, and `CURRENT = 0`. Its inequalities hold, and those are the
actual values after the program's three initializing assignments.

### Scope and domain

`IS:IntSeq` is an unrestricted recursive K sequence of arbitrary K `Int`
values. It is not length-bounded and does not fix examples or sizes. It
represents every finite mathematical-integer list, which is the source
contract. K integers are unbounded, matching the relevant Python integer
operations. Non-integer elements and non-list inputs are outside the stated
integer-list contract; no material source-contract domain was narrowed.

### Body sensitivity

I independently rebuilt the candidate source mutation under the trusted
semantics. It changes the negative update comparison from `>` to `<` in the
program term itself; it does not merely edit an external Python file. The fresh
build exited 0
([build log](/audit-output/evidence/stage4-kompile-body-sensitivity.log)).
The proof of the correct `(-1, None)` result for `[-3, -1]` then failed with
exit 1 and `WarnStuckClaimState`, exposing the actual mutant result
`(-3, None)`:
[stage4-body-sensitivity.log](/audit-output/evidence/stage4-body-sensitivity.log).

This demonstrates dependence on the material body and also confirms that the
loop bridge does not match a differently named/differently expanded loop body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory tool is
[inventory_k.py](/audit-output/evidence/inventory_k.py). Its full,
source-located inventory is
[stage5-rule-inventory.log](/audit-output/evidence/stage5-rule-inventory.log).
It covers all K sources in the supplied tree and all submitted proof sources
that contribute declarations, rules, or claims.

It enumerates 963 declarations:

```text
718 rules
234 syntax declarations
5 claims
5 contexts
1 configuration
```

Attribute inventory includes 150 function-bearing declarations, 111 total
declarations, 35 concrete occurrences, 46 priority occurrences, 26 `owise`
occurrences, six macro occurrences, 25 `symbol` occurrences, and the strictness
attributes. There are no submitted proof-local `simplification`,
`functional`, or opaque-symbol declarations.

The fixed-semantics per-file counts in the inventory include every rule and
syntax declaration in `assert.k` (3 rules), `bool.k` (13),
`builtins.k` (137), `call.k` (21), `comprehension.k` (7),
`concrete.k` (16), `controls.k` (34), `core.k` (46 plus the
configuration), `dict.k` (28), `float.k` (121), `functions.k` (15),
`int.k` (16), `list.k` (27), `methods.k` (75), `operators.k` (10),
`range.k` (6), `set.k` (12), `sort.k` (19), `str.k` (28),
`subscript.k` (40), and `tuple.k` (21), together with all syntax-only
declarations and iterator declarations. `semantics.k` only assembles/imports
these modules. The full record, rather than this summary, is the exhaustive
inventory.

### Construct-to-semantics map

Every material constructor in `solution.mpy` has a fixed declaration and
operational route:

| Submitted construct | Declaration / material rules |
|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k`; load/sequence in `core.k` 124–127; binding in `functions.k` 14–16 |
| `Call`, `Name` | lookup in `core.k` 130–154; callee/arguments and closure dispatch in `call.k` 19–21 and 69–75 |
| `Assign` | strict RHS from `syntax.k`; current-frame update in `controls.k` 9–18 |
| `For`, `#loop` | strict iterable from `syntax.k`; loop protocol in `controls.k` 65–74 |
| encoded integer-list iteration | `representation.k` 8–26; fixed list iterator in `list.k` 9–10 |
| `Int`, `NoneVal` | `core.k` 194–196 |
| `Compare`, `<`, `>`, `==` | contexts/dispatch in `operators.k` 14–17; integer cases in `int.k` 22–27 |
| `BoolOp("or", ...)` | left-to-right context and short-circuit rules in `bool.k` 16–25 |
| `If` and `IfExp` | strict condition plus `controls.k` 51–60 |
| loop-target name binding | `tuple.k` 31–41 |
| `TupleExpr` | left-to-right argument evaluation in `core.k` 183–191 and tuple application in `tuple.k` 14–16 |
| `Return`, frame cleanup | strict return plus `functions.k` 78–90 |

The configuration has the computation, current environment, scope map and
allocator, heap and allocator, call stack, return state, exception state, and
exit code. The entry claim pins all of them. Evaluation order is left-to-right
where it matters. The program performs no external call, output, exception,
mutable-list operation, or allocation within the loop.

### Submitted local declarations and rules

#### Input representation

[representation.k](/candidate/representation.k:8) introduces exactly one
syntax symbol, `intVals(IntSeq)`, with four rules:

1. `.IntSeq` maps to `.ValSeq`;
2. `iCons(I, IS)` maps structurally to `vCons(I, intVals(IS))`;
3. iteration of encoded empty exposes fixed list iteration of `.ValSeq`; and
4. iteration of encoded cons exposes fixed list iteration of
   `vCons(I, intVals(IS))`.

The two constructors are disjoint and exhaustive for `IntSeq`. The rules
preserve order and the exact integer `I`; they introduce no fresh value. The
iterator exposure rules preserve the whole continuation syntactically and read
or write no state cell. Fixed list rules then produce `#iterDone` or
`#iterYield`.

These exposure rules define how the proof's external mathematical input
encoding is observed; they do not replace any program-defined helper or encode
the task answer. The submitted `connection-spec.k` imports these rules, so its
two claims are behavioral constructor checks, not a bridge-free derivation of
the representation rules themselves. I tested this distinction explicitly:
after removing the two exposure rules, the new encoding is stuck because the
fixed semantics has no independent meaning for the newly introduced
`intValsNoIterBridge` symbol
([source](/audit-output/evidence/representation-no-iter-bridge.k),
[proof log](/audit-output/evidence/stage5-prove-no-iter-bridge.log)). This is
consistent with the rules' role as the definition of an input encoding, not
evidence of a hidden fixed-semantics computation.

The appropriate sensitivity test is whether the later bridge-free program
theorem detects a wrong encoding. I changed only the cons exposure to yield
zero instead of `I`; the mutated source is
[wrong-representation.k](/audit-output/evidence/wrong-representation.k). It
built successfully, but the bridge-free loop theorem failed with an unmet
condition relating `scanNeg`, `scanPos`, and `lastValue`; see
[stage5-wrong-representation-sensitivity.log](/audit-output/evidence/stage5-wrong-representation-sensitivity.log).
Thus the proof is value-sensitive to this low-level input bridge and does not
admit the opposite interpretation. The original rules are an acceptable,
exhaustive structural input boundary.

#### Body macros

`lsiLoopBody` and `lsiBody` are syntax macros whose two rules expand to the
loop body and function body. The mechanical comparison in stage 4 proves the
full `lsiBody` expansion is the submitted constructor tree. `lsiLoopBody` is
the exact body nested inside it. These are semantically inert normalization,
not execution bypasses.

#### Mathematical summaries

The proof-local total functions and every equation are:

- `takeNeg(X,N)`: exactly
  `X < 0 and (N == 0 or X > N)`;
- `takePos(X,P)`: exactly
  `X > 0 and (P == 0 or X < P)`;
- `nextNeg` and `nextPos`: one rule under the predicate and one under its
  Boolean negation;
- `scanNeg` and `scanPos`: base rule on `.IntSeq` and recursive rule on the
  strict sequence tail;
- `lastValue`: base returns the prior value; cons recurses with the current
  head;
- `negativeResult` and `positiveResult`: zero maps to `noneV`, while the
  disjoint nonzero guard maps to the integer.

The guarded pairs are exhaustive and disjoint. Every sequence recursion
strictly decreases. There are no inconsistent overlaps or unjustified totality
gaps. Induction on `IntSeq` gives:

- starting from 0, `scanNeg` is 0 iff no negative has occurred, otherwise the
  maximum negative seen;
- starting from 0, `scanPos` is 0 iff no positive has occurred, otherwise the
  minimum positive seen.

This is ordinary integer/order mathematics, not an opaque oracle. More
importantly, these symbols are not merely repeated in an execution shortcut
and postcondition: the separate loop theorem executes the fixed body and
connects its state updates to these exact summaries.

#### Loop operational bridge

The only submitted rule that summarizes program execution is the priority-40
rule in [verification.k](/candidate/verification.k:10).

Its complete match domain is:

- `#loop(list(intVals(IS)), Name("value"), lsiLoopBody)` with an arbitrary
  continuation;
- environment location 1;
- the exact local keys and types, including arbitrary `lst`;
- the exact module binding and `lsiBody`;
- an arbitrary builtins scope;
- `N <= 0` and `P >= 0`; and
- every omitted configuration cell framed.

It consumes only the loop and updates the three locals to `scanNeg`,
`scanPos`, and `lastValue`. It does not pop a frame, return, throw, allocate,
discard a suffix, or alter the heap, allocators, stack, return, exception, or
exit cells.

The universal connection theorem is
[loop-spec.k](/candidate/loop-spec.k:6), compiled against
`VERIFICATION-CORE`, which does not contain the loop summary rule. Its LHS,
RHS, guards, exact scope map, arbitrary continuation, and framed cells are the
same as the admitted rule. The clean proof exited 0 with `#Top`. Therefore the
bridge match domain is contained exactly in its justification domain, including
control context and all observable state.

The body mutation in stage 4 changes the displaced execution and is rejected.
The wrong-input-exposure mutation above also causes this connection theorem to
fail. These are independent control/value sensitivity checks, while stage 6 is
the separate result-postcondition check.

#### Claims

The five claims in the inventory are the two representation observations, the
bridge-free loop theorem, the final-definition loop claim, and the entry claim.
All have satisfiable instances. The loop claims correspond to the real
`#loop` control point produced by the fixed `For` rule. The entry claim executes
the actual module load, binding, call, loop, return, and frame cleanup.

### Supplied-semantics rules and opaque boundaries

I reviewed all fixed modules in the exhaustive inventory. For the target path,
the relevant rules have disjoint constructor/guard domains and preserve the
expected cells and evaluation order. No fixed priority rule preempts the
submitted path with a different binding or result.

The supplied tree also contains 25 explicitly symbolic/opaque declarations,
all enumerated in the inventory:

```text
intFloatDiv divII floatMod floatLt absF floorFI toF ceilF
subF divF addF mulF powF gtF eqF decStrToF divFloatIntV intToF
truncF roundF roundFN sqrtF sortVS sortKeyVS md5hexCodes
```

They belong to float, sorting, or MD5 support. The submitted syntax contains no
float, sorting, subscript, MD5, method, dict, set, string, range, or builtin
call, so none is reachable or appears in any result, branch, summary, or
postcondition.

The LLVM compiler's fixed-semantics non-exhaustiveness warnings concerned
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. They are
also outside the target path. I do not relabel these warnings as unsoundness:
there is no witness by which any warned rule can enable a false conclusion for
an intended integer-list input. They remain fixed-semantics limitations for
unrelated language fragments.

No submitted rule encodes the requested answer, substitutes a different
program, creates an unconstrained result-bearing oracle, or fabricates a value
for a used source construct. I found no unsound local rule and therefore make
no unsupported unsoundness allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on the candidate `spec-vacuity.k`. I wrote
[audit-false-spec.k](/audit-output/evidence/audit-false-spec.k), which starts
from the exact satisfiable entry configuration, calls the exact submitted body
on `[-1]`, and changes only the result obligation from the true
`(-1, None)` to the false `(None, None)`.

First:

```text
kprove audit-false-spec.k --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-SPEC --dry-run
```

exited 0, proving the mutation parses and builds; see
[stage6-false-dry-run.log](/audit-output/evidence/stage6-false-dry-run.log).

The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
contains:

```text
tuple(vCons(-1, vCons(noneV, .ValSeq)))
```

which cannot unify with the false destination. The failure is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unrelated crash. Full bounded output is
[stage6-false-proof.log](/audit-output/evidence/stage6-false-proof.log).

The proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### Precisely established theorem

Under the supplied K semantics and candidate-local definitions reviewed above,
for every finite `IS:IntSeq`, starting from the pinned initial module state:

1. the exact submitted translated function is loaded under the required name;
2. that binding is called with the integer list represented by `IS`;
3. the fixed operational semantics executes its initialization, lookup,
   call/return machinery, conditions, assignments, tuple construction, and
   frame cleanup;
4. the loop's exact operational transition is connected by a separately proved
   reachability theorem; and
5. execution reaches exactly
   `(negativeResult(scanNeg(IS,0)), positiveResult(scanPos(IS,0)))` with the
   pinned final cells.

By the exhaustive recursive equations and ordinary induction described in
stage 5, this is exactly the largest negative and smallest positive pair, using
`None` where the respective subset is empty.

This is a partial-correctness/reachability result in the Kit sense. It is not a
standalone mechanized theorem equating all of CPython with the supplied
semantics, nor a resource-exhaustion guarantee.

### Trust ledger

| Boundary | Influence | Assessment and support |
|---|---|---|
| Supplied `reference-semantics` | Defines the Python subset's control, state, and primitives | Required fixed execution model; candidate tree is byte/type-identical to trusted mount. Relevant rules were statically reviewed and concretely exercised. |
| K 7.1.293, Haskell/LLVM backends, SMT and builtin integer/Boolean/map theories | Proof checking and primitive mathematics | Standard machine-checking trust boundary; versions and fresh commands are recorded. |
| Trusted `py2mpy.py` | Connects submitted Python AST to `solution.mpy` | Launcher-trusted file, candidate copy identical, and regeneration is byte-identical. |
| `intVals` input representation | Connects arbitrary `IntSeq` to the list values observed by iteration | Exhaustive structural definition, no fresh value/oracle, no state effect; wrong-yield interpretation makes the bridge-free loop theorem fail. Acceptable low-level input boundary. |
| `scanNeg`/`scanPos` meaning | Connects recursively defined summaries to “largest negative/smallest positive” | Exhaustive terminating equations plus the explicit induction argument; actual execution-to-summary is machine checked by `loop-spec.k`. |
| Opaque float/sort/MD5 symbols listed above | None on this theorem | Imported but unreachable and absent from claims/results. They are not assumptions used by the proof. |
| CPython canonical differential evidence | Supports implementation/intent alignment on 20,123 cases | Independent finite evidence only; it does not replace any K claim. |
| Concrete LLVM assertions | Supports used-semantics behavior on six normal/boundary inputs | Finite evidence only; the universal result comes from the reconstructed Haskell proofs. |

There is no result-bearing external primitive, empirical oracle, or informal
program-helper contract on which claim closure depends. The only informal
mathematical step is the transparent induction connecting the exhaustive
`scanNeg`/`scanPos` equations to the natural-language extrema terminology.

### Gate and decision summary

- Real-program soundness: pass. The actual body is pinned, the only program
  operational bridge has an exact bridge-free theorem, body/input mutations
  are detected, and a false reachable result is rejected.
- Intent adequacy: pass. The theorem ranges over arbitrary finite integer lists
  and its recursively fixed result is exactly the prompt result.
- Trust/evidence auditability: pass. All assumptions, opaque symbols,
  commands, statuses, and finite evidence are separated and recorded.

The clean proof therefore satisfies the benchmark's `PASS / LEGIT` boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
