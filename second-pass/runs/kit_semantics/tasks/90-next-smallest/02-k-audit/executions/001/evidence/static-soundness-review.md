# Static soundness review notes

## Inventory scope

`k-rule-inventory.txt` lexically inventories every declaration start in all 24
trusted supplied-semantics K files, `verification.k`, and `spec.k`: 978 records
(243 syntax declarations, one configuration, five contexts, 727 rules, and two
claims). It includes complete source chunks and attribute flags. No candidate
semantic helper K file exists outside `verification.k`; the candidate mutation
files are negative probes and are not imported by the positive definition.

The 930 records before `verification.k` belong to the immutable supplied model.
They are classified as the selected semantics/trust boundary. Unused rules do
not contribute to this theorem. The used subset was checked below against the
program's complete constructor vocabulary and state footprint.

## Used constructor-to-semantics map

- `Module`, `FuncDef`, `Params`, statement-list syntax: `syntax.k`; `#loadAll`
  and statement sequencing in `core.k`; function installation in `functions.k`.
- `Call`, `Name`, one positional list argument: callee lookup and left-to-right
  argument evaluation in `core.k` and `call.k`; closure dispatch, frame push,
  parameter bind, `Return`, and frame pop in `call.k`/`functions.k`.
- `Expr(Str(...))`: ASCII literal conversion in `str.k`, then discard in
  `controls.k`. The submitted docstring is ASCII, so the fixed model's ASCII
  boundary is not reached.
- `Assign`, `If`, `For`: `controls.k`. Iteration of the already-evaluated bare
  `list(ValSeq)` uses `#iterNext` rules in `list.k`. The body has no exception,
  break, continue, return, allocation, output, or other abrupt effect.
- `Int`, `Bool`, `NoneVal`, `truthy`: `core.k`; `not` and short-circuit `and`/`or`
  in `bool.k`; `+`, `<`, and `!=` dispatch in `operators.k` and `int.k`.
- The ten-cell configuration is the one in `core.k`. The theorem pins module
  and builtins scopes, starts with empty heap/stack and no return/exception,
  pushes exactly one function frame, deletes it on pop, restores `env` and
  `scopeLoc`, and neither allocates nor mutates heap state because the input is
  a read-only bare `list(VS)` and the source performs no list mutation.

Strictness/context declarations establish the needed order: assignment RHS,
`For` iterable, `If` guard, unary operand, binary operands, comparison operands,
and call callee/arguments evaluate before their consumers. Boolean `and`/`or`
short circuit in source order. No priority rule added by `verification.k`
changes operational control.

## Every `verification.k` declaration and rule

The detailed source for all 48 records is in inventory records 931--978. Their
soundness decisions are:

1. `nextSmallestLoopBody`, `nextSmallestBody`, and `solutionProgram` (three
   function declarations and three equations) are constructor aliases only.
   They neither intercept `<k>` nor summarize execution. Trusted regeneration,
   K parsing, and `stage4-constructor-pinning-final.log` mechanically establish
   that `solutionProgram` is the exact regenerated `solution.mpy` module. The
   first two aliases are the corresponding literal subterms. Decision: sound
   definitional aliases.
2. `allInts` and its two equations structurally recurse over every finite
   `ValSeq`; the head/tail cases are disjoint and complete. It is true exactly
   when all elements have the K `Int` subsort. Decision: sound domain predicate.
3. `definedProjectInt` and its equation merely name `isInt`. Decision: sound.
4. `projectIntTotal` is the only `no-evaluators` symbol. Off the theorem domain
   its interpretation is unconstrained, but every use is guarded by `isInt`.
   The `#Ceil` equation states the ordinary definedness condition for the K
   `Val`-to-`Int` sort projection; the concrete/symbolic pair equates the helper
   with that projection under exactly the same guard; the `Int` identity and
   nested-projection equations follow. On `allInts`, its value is therefore the
   unique represented integer, not an oracle. The equations overlap only where
   their right sides are equal. Decision: sound guarded projection; off-domain
   opacity has no dependent positive claim.
5. The three guarded `applyBin("+")`, `applyCmp("<")`, and
   `applyCmp("!=")` simplifications are sort-refined versions of the fixed
   `int.k` equations. Their guards require both operands to be `Int`; the
   projection equations then yield exactly `+Int`, `<Int`, and `=/=Int`.
   They affect value but not binding, evaluation order, continuation, or any
   other cell, because they simplify only the already-dispatched pure function.
   Decision: sound derived lemmas, not operational bridges.
6. `scanState` is a constructor. `scanStep` plus its six equations exactly
   implements one source-body iteration. The cases split first on the two
   Boolean flags, then on integer trichotomy (`X<A`, `X==A`, `X>A`) and, when
   needed, `X<B` versus `X>=B`. Guards are disjoint and exhaustive and recursive
   descent is not involved. Direct branch comparison shows the same updates to
   `smallest`, `found_smallest`, `second`, and `found_second` as the source.
   Decision: sound and complete.
7. `scanAfter`/`scanVS` and their four equations are a structural fold over the
   finite suffix. Empty and cons cases descend. The non-`Int` totalization is
   disjoint from the `isInt` case and unreachable under `allInts`; it defines a
   harmless off-domain value and does not claim source behavior there.
   Decision: sound definitional summary on the theorem domain.
8. The four scan-field projection declarations/equations select the four
   `scanState` fields. They are complete on normalized `ScanState` results and
   mutually independent. Decision: sound.
9. `lastInt` and its three equations structurally return the last represented
   integer, or the supplied initial value for an empty suffix. Its off-domain
   stop rule is disjoint and unreachable under `allInts`. This matches the loop
   variable after the source's `x = x + 0`. Decision: sound.
10. `nextSmallestSpec` and its equation run `scanVS` from both flags false and
    return the second field iff it was found, else `noneV`. It does not replace
    program execution; it is the result-constraining RHS. The elementary fold
    invariant is: after each prefix, `HA` iff the prefix is nonempty; when true,
    `A` is its minimum; `HB` iff a distinct value greater than `A` exists; when
    true, `B` is the least such value. Every `scanStep` case preserves this
    invariant, including moving the old minimum to `B` when a new minimum is
    seen. Thus the final value is exactly the second-smallest distinct integer.
    Decision: sound total summary of the docstring contract.

There are no candidate ordinary operational rules, call interceptions,
priority rules, abrupt-control bridges, unconstrained fresh values, proof-local
claims hidden in `verification.k`, or rules that replace execution with the
answer. No false-conclusion witness exists for an inventoried candidate rule.

## Claim review

- `loop-invariant` accepts any finite all-`Int` suffix and arbitrary accumulator
  flags/values. It consumes the real `#loop` with the exact real body and updates
  only the five local bindings described by `scanVS`/`lastInt`. A satisfying
  instance is `VS=.ValSeq`, `HA=HB=false`, `A=B=X0=0`, with any valid scope
  location. Its arbitrary continuation framing is safe because this body has no
  abrupt control or observable side effects.
- `next-smallest` starts from the complete fixed initial configuration, loads
  and binds the exact regenerated module, calls that closure on any all-`Int`
  finite `ValSeq`, and requires the returned `<k>` value to equal
  `nextSmallestSpec(VS)`. `VS=.ValSeq` and `VS=vCons(1,vCons(2,.ValSeq))` are
  concrete satisfying inputs. The result is not free and no implication weakens
  equality.

Fresh body sensitivity changed `Assign(second,x)` to
`Assign(second,smallest)` inside `nextSmallestLoopBody`, hence inside the
executed `solutionProgram`; the definition rebuilt, and the original proof
failed on its loop obligation (`stage4-body-mutation-kprove.log`).
