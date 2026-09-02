# Static soundness assessment

This assessment is keyed to the complete source-block inventory in
`05_rule_inventory.md` and the one-row-per-anchor ledger in
`05_rule_decisions.csv`. The ledger classifications are:

- `F-USED`: a supplied fixed-semantics declaration/rule on the submitted
  execution path, or an overlap/priority declaration that must be considered
  on that path. These rules were checked against the real control and state
  transition below.
- `F-UNREACHED`: a rule or declaration in the authoritative supplied semantics
  which cannot be reached from the submitted AST and exact entry state. No
  target claim depends on it. This is not a claim of universal Python fidelity;
  it is a narrower theorem-local decision and no unsoundness is alleged.
- `P-MATH`: a proof-local declaration or equation in `verification.k`. Each is
  separately justified below.

## Source-wide inventory decision

The inventory covers the assembly file, all 23 supplied helper modules, and
`verification.k`: 230 syntax declarations, one configuration, five contexts,
and 701 rules (937 declaration anchors total). It also enumerates all
attributes: 148 `function`, 110 `total`, zero `functional`, 25 `symbol`, zero
literal `opaque` attributes, 22 `no-evaluators`, 45 priority, zero
simplification, 35 concrete, 26 owise, four macro, two strict, and one
seqstrict-containing declaration block. Attribute counts are
containing-declaration-block counts; the full blocks prevent a multiline
attribute from being lost.

All 25 symbolic opaque candidates are in the supplied fixed semantics:
`md5hexCodes`; 22 float conversion/arithmetic/comparison operations; and
`sortVS`/`sortKeyVS`. None is reachable: the verified program performs no
arithmetic, comparison, hashing, sorting, float conversion, or operations on
its elements. Merely carrying an arbitrary `Val` through list iteration and
append does not invoke an operation on that value. Thus no opaque value can
affect a branch or the result summary here. The concrete-only module is used
only by the independent LLVM run; the Haskell proof module imports `MPY`, not
`MPY-CONCRETE`.

The fixed-semantics modules with no reachable declaration for this program are:
`assert.k`, `bool.k`, `builtins.k`, `comprehension.k`, `concrete.k`, `dict.k`,
`float.k`, `int.k`, `methods.k`, `operators.k`, `range.k`, `set.k`, `sort.k`,
`str.k`, and `subscript.k`. The irrelevant portions of the partly used modules
(`core.k`, `controls.k`, `functions.k`, `list.k`, `call.k`, `tuple.k`, and
`syntax.k`) are likewise marked individually as `F-UNREACHED` in the CSV.
No target configuration can synthesize their redexes.

## Construct-to-rule map and state/control check

| Submitted construct | Declaration and active fixed rules | Decision |
|---|---|---|
| `Module` / statement list | `syntax.k:56,61`; `core.k:124-127` | Loads and sequences the exact AST left-to-right; empty statements vanish. |
| `ImportFrom("typing","List")` | `syntax.k:41`; `controls.k:36` (`owise`) | No-op is faithful for this type-only import; it cannot affect the function. |
| `FuncDef` / `Params` | `syntax.k:41,57`; `functions.k:14` | Binds the exact body and two parameters in module scope as `closureVal`. |
| `Call(Name("intersperse"), list(NUMBERS), D)` | `call.k:19-21,69`; `core.k:130-132,185-191`; `functions.k:63-64` | Resolves the module binding, evaluates callee then arguments left-to-right, allocates a scope-1 frame, binds both arguments, and saves the caller continuation/environment. |
| `Assign(result,ListExpr())` | `syntax.k:41` strict RHS; `list.k:13-15`; `core.k:117-118,213-219`; `controls.k:9` | Allocates a fresh heap list at location 0, advances `heapLoc`, and binds `result` to `ref(0)`. |
| `For(number,numbers,body)` | `syntax.k:41` strict iterable; `controls.k:65,69,71-73`; `iter.k:8`; `list.k:9-10`; `tuple.k:31-32` | Looks up the unboxed input list once, yields its head in order, binds `number`, executes the body, and loops on the tail. Empty input terminates immediately. |
| `If(result, append delimiter, empty)` | `syntax.k:41` strict condition; `controls.k:95,51-54`; `core.k:199,204` | Dereferences `ref(0)` before list truthiness. Empty accumulator skips the delimiter; nonempty accumulator takes the delimiter branch. Priority 40 correctly preempts treating the ref itself as a generic value. |
| `Attribute(...,"append")` / `Call` / `Expr` | `syntax.k:9,41`; `call.k:16,20-21`; `list.k:18-20,53`; `controls.k:48` | Cools the receiver to a bound method, evaluates the one argument, and the priority-40 exact `append` rule mutates the same heap location by right-appending one value. The generic method route is lower priority; the ref-dereference route is guarded false by `isMutMethod("append")`. `Expr` discards only the returned `noneV`, preserving the mutation. |
| `Return(result)` | `syntax.k:41` strict expression; `core.k:130-132`; `functions.k:78,85` | Reads `ref(0)`, records it as the return value, discards the rest of the callee body, restores env 0, removes scope 1, restores `scopeLoc=1`, preserves heap 0, and resumes the saved continuation. |

The configuration cells match this story: `<k>` holds control; `<env>` selects
scope; `<scopes>` holds module/builtin/callee maps; `<scopeLoc>` allocates the
callee frame; `<heap>` contains the fresh mutable output list; `<heapLoc>`
allocates it; `<stack>` saves the caller continuation; `<ret>` transfers the
value; and `<exc>`/`<exit-code>` remain normal. The entry postcondition
constrains every one of those cells material to this execution.

The relevant ordinary-rule overlaps are benign and correctly prioritized:

1. `If(ref(H),...)` at priority 40 runs before generic `If(C:Val,...)`, exposing
   the heap list whose truthiness is tested.
2. Exact list `append` at priority 40 runs before the generic bound-method
   dispatch; the separate nonmutating-receiver dereference rule is guard-false
   because `isMutMethod("append")` is true.
3. Plain name target binding wins in the ordinary frame. The cell-target rule
   requires a `$cells` marker absent from this closure frame.
4. Plain name lookup applies because the frame contains direct values and no
   `$cells` marker; cell lookup cannot overlap.

No exception-producing construct is used. No input mutation occurs: iteration
uses the unboxed input `list(NUMBERS)`, while only fresh heap location 0 is
updated.

## Proof-local inventory

`verification.k` contains no configuration, semantic `<k>` rewrite,
simplification, concrete rule, priority, symbol, opaque value, lemma, or claim.
It adds exactly three total functions and six equations:

1. `intersperseAcc(ACC,.ValSeq,D) = ACC`. This is the empty-remainder base
   case.
2. `intersperseAcc(.ValSeq,vCons(V,REST),D)` starts with `V` and recurses on
   the strictly shorter `REST`; no delimiter precedes the first item.
3. `intersperseAcc(vCons(A,AS),vCons(V,REST),D)` appends `D` then `V` and
   recurses on the strictly shorter `REST`.
4. `intersperseVS(NUMBERS,D)` is exactly the empty-accumulator call.
5. `lastNumber(OLD,.ValSeq) = OLD`.
6. `lastNumber(_,vCons(V,REST))` recurses with `V` on the strictly shorter
   `REST`.

Items 2 and 3 are disjoint by the accumulator constructor; together with item
1 they cover all `ValSeq` remainders. The two `lastNumber` equations are
disjoint and exhaustive. All recursion structurally decreases.

These functions name mathematical sequences without replacing any program
redex. Their values are fully determined by exhaustive equations; none is an
oracle. The entry and loop claims then constrain the heap to those values.
There is no candidate rule for which an operational-bridge connection theorem
is required.

## Claim/circularity review

The empty-loop claim is exact and preserves all cells. The first-iteration
claim starts from a fresh empty result, executes one or more real iterations,
sets `number` to `lastNumber(V,REST)`, and produces
`intersperseAcc(.ValSeq,vCons(V,REST),D)`. The recurrent claim starts from a
nonempty accumulator and appends `D,V` for every remaining element. It is the
guarded loop circularity used by the first and entry claims.

Every loop claim quantifies over the full `CONT`; this is not an unjustified
bridge with a broader continuation. `kprove` proves the claim under that
arbitrary continuation and the fixed state footprint. The freshness conditions
on `L` and `H` make the map decompositions well formed and are satisfiable.

The entry claim embeds the parsed submitted program exactly and returns
`ref(0)` whose heap value is `list(intersperseVS(NUMBERS,D))`; the result is not
free and there is no one-way implication in place of equality. No rule encodes
a shortcut to that postcondition.

## Static conclusion

Every declaration anchor has a decision in `05_rule_decisions.csv`. No
materially unsound proof or used-semantics rule was found, so no false-rule
witness is asserted. For unreachable supplied facilities, the narrower evidence
statement is that their universal Python fidelity was not needed or established
by this theorem.
