# Reviewer static rule disposition

This document accompanies the mechanically exhaustive 945-entry inventory in
`05_rule_inventory.md`. Inventory IDs 1–928 are the supplied, byte-verified
fixed semantics. IDs 929–945 are candidate-controlled declarations, rules, and
claims.

## Fixed-semantics dependency slice

The exact translated body uses these constructors:

`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Bool`, `Int`, `For`, `If`,
`Compare`, `CmpOp("==", ...)`, `CmpOp(">", ...)`, `Call`, `Attribute`,
`UnaryOp("-")`, `Return`, statement/argument sequence units, and the semantic
input value `list(ValSeq)`.

The material fixed-semantics declarations and rules are:

- `semantics/syntax.k:9-61`: declarations and evaluation attributes for every
  constructor above. `Assign` evaluates its RHS, `For` evaluates its iterable,
  `If` evaluates its condition, `Return` evaluates its value, `Attribute`
  evaluates its receiver, and `UnaryOp` evaluates its operand. `Compare` uses
  explicit contexts in `operators.k`.
- `semantics/core.k:13-42,49-60`: value/sequence sorts and the complete
  configuration. The entry claim fixes every configuration cell.
- `semantics/core.k:124-127`: module loading and left-to-right statement
  sequencing.
- `semantics/core.k:130-181`: lexical lookup and the fixed builtins scope.
  Lookup selects the function installed in module scope; no proof-local rule
  selects a binding by name.
- `semantics/core.k:185-196,213-225`: left-to-right argument evaluation,
  integer/Boolean literals, and sequence helpers.
- `semantics/core.k:199-205`: Boolean truthiness used by `If`.
- `semantics/core.k:208-210`: the fixed operator dispatch declarations.
- `semantics/functions.k:8-16,62-90`: function installation, parameter binding,
  return, frame restoration, scope deletion, and return-value propagation.
- `semantics/call.k:15-24,69-75`: receiver cooling, callee evaluation, argument
  evaluation, bound-method dispatch, and exact unannotated-closure invocation.
- `semantics/controls.k:8-18,50-54,62-74,85`: local assignment, branching, the
  `For` iterator loop, target binding, and normal loop continuation.
- `semantics/tuple.k:31-34`: `#bindTgt(Name(...), V)` writes the loop variable
  in the active scope.
- `semantics/list.k:8-10`: list iteration yields the head and structural tail.
- `semantics/methods.k:9-10,63-68`: `list.count` dispatches to the structurally
  recursive `cntOccVS`; its equality and inequality guards are complementary.
- `semantics/operators.k:10,14-17`: unary dispatch and left-before-right
  comparison evaluation.
- `semantics/int.k:7,22-27`: mathematical-integer unary minus and comparisons,
  including the used `==` and `>` cases.

These rules preserve the material source behavior: the input list is read but
not mutated; `found` and `x` are the only body-written bindings; `count` is
pure; calls push and pop one frame; return discards the remaining function-body
continuation exactly as Python return does; and no exception, output, or
allocation occurs for the unboxed read-only input used by the symbolic entry
claim.

All other fixed-semantics inventory entries have a left-hand constructor,
operator tag, callable, value sort, or control marker absent from the exact
program and from the material rules above. They are therefore outside the
theorem dependency slice. In particular, the 22 `no-evaluators` float/sort/md5
symbols and all concrete-only rules are unreachable and cannot influence the
claim result. This is a reachability disposition, not a claim that the reviewer
reproved every unused language feature against CPython.

## Candidate-controlled inventory, rule by rule

### IDs 929–931: `intProj`

- ID 929 declares a total mathematical projection from `Val` to `Int`.
- ID 930 is identity on the injected `Int` subsort.
- ID 931 returns `0` only under `notBool isInt(V)`.
- The equations cover `Val`, their guards are disjoint, and neither recurses nor
  touches state. The arbitrary off-Int value cannot enter either bridge because
  both bridge guards require `isInt(V)`. It also cannot affect `anyInverse` on
  the entry domain because `allInts(FULL)` supplies `isInt` for every head.

Disposition: sound definitional summary.

### IDs 932–933: `hasInverse`

The single unconditional equation is exhaustive. For `X == 0`, a distinct
zero partner exists exactly when the fixed `cntOccVS(FULL, 0)` is greater than
one. For `X =/= 0`, a distinct partner exists exactly when `-X` occurs at least
once; it cannot be the same position because `X` is nonzero. The two Boolean
cases are complementary and use mathematical unbounded integers.

Disposition: sound, terminating definitional summary of the requested
distinct-position property.

### IDs 934–936: `anyInverse`

The empty and `vCons` equations are constructor-disjoint and exhaustive. The
recursive call strictly descends the first `ValSeq`. On integer-only inputs the
head conjunct reduces to `hasInverse(head, FULL)`; the explicit `isInt` check
and total projection merely define harmless behavior outside the theorem
domain. The result is the finite disjunction of `hasInverse` over all
occurrences.

Disposition: sound, terminating definitional summary.

### IDs 937–939: `allInts`

The empty and `vCons` equations are constructor-disjoint, exhaustive, and
structurally descending. They say exactly that every semantic list element is
in the `Int` subsort.

Disposition: sound input-domain predicate.

### ID 940: integer-equality simplification

Complete match domain: pure term `applyCmp("==", V:Val, I:Int)` under
`isInt(V)`, in an arbitrary term context. It reads or writes no configuration
cell and introduces no control effect. The guard means `V` is an injected
integer. `CONNECTION-SPEC.int-equality`, built without `VERIFICATION`, proves
universally that fixed semantics yields `intProj(V) ==Int I`. This agrees with
the overlapping fixed `semantics/int.k:26` equation. The fresh opposite ground
interpretation leaves `true` and is rejected.

Disposition: sound operational/equational bridge over its full guard.

### ID 941: integer-unary-minus simplification

Complete match domain: pure term `applyUn("-", V:Val)` under `isInt(V)`, in an
arbitrary term context. It has no state or control footprint. The guard selects
the injected-Int domain. `CONNECTION-SPEC.int-unary-minus`, built without
`VERIFICATION`, proves the universal fixed-semantics equality, agreeing with
`semantics/int.k:7`. The fresh opposite ground interpretation leaves `-2` and
is rejected.

Disposition: sound operational/equational bridge over its full guard.

### IDs 942–943: bridge-free connection claims

Both claims quantify over all mathematical integers, preserve the arbitrary
continuation and all omitted cells, import no bridge rule, and close from the
fixed integer equations plus the `intProj` identity equation. They are
supporting theorems, not axioms imported into the target definition.

Disposition: valid derived lemmas.

### ID 944: loop invariant claim

Precondition: `FULL` and `REM` are finite integer-only semantic sequences;
`found` is Boolean; `l` is the unboxed semantic list `FULL`; and execution is
at the exact `#loop` head for the translated body. `REM` need not be a suffix
of `FULL` for the claim to be true: the loop intentionally iterates `REM` while
each body count reads `FULL`.

Postcondition: the loop is removed from the active continuation, `found`
becomes its incoming value OR `anyInverse(REM, FULL)`, `l` is unchanged, and
`x` may have any final `Val`. Other scopes and every omitted cell are framed.

The base case preserves `found`. In the cons case, fixed iteration binds the
head to `x`; fixed comparison/count execution sets `found` precisely when
`hasInverse(head, FULL)`; the circularity applies to the structural tail.
There is no abrupt effect in the loop body, so framing an arbitrary continuation
does not broaden beyond the derived behavior.

Disposition: valid circular reachability lemma with complete material state
footprint.

### ID 945: entry claim

Precondition: a clean fixed configuration and any finite `FULL` satisfying
`allInts(FULL)`. This is satisfiable, e.g. `FULL = .ValSeq` and
`FULL = vCons(1, vCons(-1, .ValSeq))`.

The `<k>` term loads the exact mechanically compared translated function,
then performs only a wrapper assignment calling the installed binding. Fixed
lookup, call, parameter binding, body execution, return, and assignment all
execute. The postcondition existentially names the final module map but
constrains its `$result` entry to the Boolean `anyInverse(FULL, FULL)`. It is
neither a free result nor a one-way implication.

The final configuration pins scope, heap, stack, return, exception, and exit
cells. No task-answer rule rewrites the invocation, no opaque symbol reaches
the result, and no proof-local rule bypasses function lookup or body execution.

Disposition: adequate, result-constraining partial-correctness entry theorem.

## Static conclusion

No inventoried candidate-controlled rule admits a false conclusion on the
intended integer-list domain, so there is no false-conclusion witness to
report. The only proof-local execution accelerations are IDs 940–941, and each
has a bridge-free universal connection theorem over its complete guard plus a
fresh rejected opposite-value witness.
