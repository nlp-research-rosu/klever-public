# Static rule review

This is the reviewer-authored disposition for the exhaustive inventory in
`rule_inventory.tsv`. The inventory contains 1,110 declarations/directives:
700 `rule` declarations, 229 `syntax` declarations, 5 contexts, one
configuration, two claims, 25 `requires`, 90 imports, 29 modules, and their
29 end markers. No `[functional]`, `[simplification]`, or `[simplifier]`
declaration occurs.

The supplied tree is fixed evidence in `SUPPLIED_SEMANTICS` mode and was
recursively byte-compared with the trusted mount before this review. The
dispositions below still inspect whether its rules can affect this proof.

## Rule-by-rule disposition by file

Every row in the inventory belongs to exactly one row below.

| File | Rules | Syntax | Disposition for this theorem |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Assembly only; the proof imports `MPY`, while LLVM imports `MPY-KRUN`. Import closure is correct. |
| `syntax.k` | 0 | 16 | Declares every constructor in `solution.mpy`; strictness is checked in the construct map below. |
| `core.k` | 46 | 37 | Relevant load, statement sequencing, scope lookup, literals, argument evaluation, list helpers, and configuration preserve the declared cells. Remaining disjoint value/heap helpers never match the reachable terms. |
| `iter.k` | 0 | 1 | Declares the iterator protocol used by `For`. |
| `range.k` | 6 | 2 | Inert: no `rangeObj` occurs in the program or claims. |
| `operators.k` | 10 | 0 | Relevant generic `BinOp` dispatch is faithful; heap-ref paths are disjoint because the accumulator, ceilings, and exponent are `Int`. Comparison/unary rules are inert. |
| `int.k` | 16 | 1 | Relevant `+` and nonnegative `**` equations are ordinary unbounded integer arithmetic. Other operator cases are disjoint. |
| `bool.k` | 13 | 0 | Inert: the body has no boolean operation or guard. |
| `float.k` | 121 | 34 | Relevant `Import` no-op, exact `math.ceil` interception, `#mathCeil`, and `ceilF` are reviewed separately below. Other float/math patterns are constructor- or operator-disjoint. |
| `str.k` | 28 | 5 | Inert: no string value or operation is reachable. |
| `set.k` | 12 | 6 | Inert: no set value or operation is reachable. |
| `list.k` | 27 | 5 | The two `#iterNext(list(...))` equations exactly implement left-to-right iteration. Literal, equality, mutation, and membership rules are inert. |
| `tuple.k` | 21 | 4 | The generic `#bindTgt(Name,V)` rule is relevant and updates only the current scope. Cell and unpacking rules are guard- or constructor-disjoint. |
| `subscript.k` | 40 | 15 | Inert: the program has no subscript or slice. |
| `comprehension.k` | 7 | 3 | Inert: the program has no comprehension. |
| `methods.k` | 75 | 27 | Inert: the exact `math.ceil` call is intercepted before generic method dispatch. |
| `controls.k` | 34 | 3 | Relevant name `Assign`, name `AugAssign`, `For`, `#loop`, `#loopStep`, and loop-label rules have the expected evaluation and state footprint. Other control forms are disjoint. |
| `functions.k` | 15 | 4 | Relevant unannotated `FuncDef`, parameter binding, `Return`, `#endcall`, and `#pop` correctly establish and remove one frame. Annotated-closure rules are disjoint. |
| `builtins.k` | 137 | 38 | Only the fixed `builtinsScope` value imported from `core.k` is present in the entry state; no builtin call in this file matches because `math.ceil` is intercepted in `float.k`. All fold/eval/digest rules are inert. |
| `call.k` | 21 | 3 | Generic call evaluates the closure and one argument left-to-right, allocates a child scope, pushes the exact continuation, executes `BODY`, then pops. Builtin/method/type cases are value-disjoint. |
| `sort.k` | 19 | 6 | Inert: no `sorted` or sort method occurs. |
| `assert.k` | 3 | 0 | Inert in both proof definitions; used only by the independently rebuilt LLVM smoke program. |
| `dict.k` | 28 | 12 | Inert: no dictionary term occurs. |
| `concrete.k` | 16 | 5 | LLVM-only; keyed-sort/deep-equality LHSs are disjoint. It cannot contribute to either Haskell proof. |
| `verification.k` | 5 | 2 | All seven proof-local declarations are individually justified below. |
| `spec.k` | 0 | 0 | The two claims are reviewed for adequacy and satisfiability below. |

No inactive rule has an LHS capable of unifying with a reachable term of the
submitted body after its guards and sorts are considered. Consequently those
rules do not contribute to claim closure; this does not assert full-Python
adequacy for unused constructs.

## Construct-to-rule map

| Submitted constructor | Declaration and operational path |
|---|---|
| `Module` | `syntax.k`; `core.k` configuration starts at `#loadAll`, then `#loadAll(Module(SS)) => SS`. |
| `Import("math")` | `syntax.k`; `float.k` removes imports. For this module the omission is inert because the only use is the exact intercepted `math.ceil` syntax. |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` stores `closureVal(PNS,BODY,L)` in the current scope. |
| `Assign(Name("result"),Int(0))` | RHS strictness; `Int` reduces in `core.k`; `controls.k` writes the current scope. |
| `For(Name("number"),Name("lst"),B)` | Iterable position is strict, `Name` uses `#look`, then `controls.k` creates `#loop`; `list.k` yields elements left-to-right; `tuple.k` binds the target. |
| `AugAssign(Name("result"),"+",E)` | RHS is strict; the non-reference rule reads and updates the existing current-scope integer with `applyBin("+",...)`. |
| `Call(Attribute(Name("math"),"ceil"),Name("number"))` | Exact priority-40 `float.k` interception evaluates only the argument, then produces `ceilF(V)`. It preempts generic call/attribute lookup only for this exact arity and name. |
| `BinOp("**",...,Int(2))` | `seqstrict(2,3)` preserves operand order; `operators.k` dispatches to the `int.k` rule `I1 ^Int I2` with guard `I2 >= 0`. |
| `Return(Name("result"))` | Strict lookup, `functions.k` stores `retV`, pops the frame, restores the continuation/environment, and yields the value. |

The active path allocates only the function scope. The input is the semantics'
documented bare read-only `list(VS)` claim representation, so the loop does not
allocate or mutate heap state. It changes only local `number` and `result`.
`env`, heap, heap counter, exception, exit code, and the continuation are
preserved across the loop summary.

## Proof-local extensions

1. `sumSquaresFrom : Int × ValSeq -> Int` is a definitional summary. Its
   `.ValSeq` and `vCons` equations are exhaustive, disjoint, decrease the
   sequence, and exactly state the left-to-right accumulator update
   `ACC + ceilF(V)^2`.
2. `lastFrom : Val × ValSeq -> Val` is a definitional summary. Its two equations
   are exhaustive, disjoint, decreasing, and give the last bound target, or
   preserve the prior target on an empty sequence.
3. The priority-40 `#loop` rule is an operational bridge, but it is not assumed
   without a connection theorem. `SUM-SQUARES-LOOP-SPEC.loop-correct` is the
   same complete K/scopes/env pattern with arbitrary `CONT`, `INPUT`,
   `PARENT`, and disjoint `GLOBAL`; it was proved against
   `SUM-SQUARES-VERIFICATION-BASE`, which does not import the bridge. Mechanical
   comparison confirms constructor identity. Its priority only preempts fixed
   iteration inside that proved match domain.

The loop bridge accepts any continuation, exactly as the bridge-free theorem
does. Its body has no return, break, continue, exception, allocation, output,
or other abrupt effect. There is therefore no wider continuation or omitted
state footprint than the connection theorem justifies.

## Opaque and total symbols

The fixed tree declares these named symbols:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

Only `ceilF` can affect this theorem. It is a fixed external primitive rather
than a proof-local program summary: exact program execution and the
postcondition are interpretation-parametric in that same operation. The
supplied semantics gives concrete equations `ceilF(I)=I` and
`ceilF(F)=Float2Int(ceilFloat(F))`; LLVM executed the prompt's positive and
negative fractional examples. The Haskell backend deliberately leaves
symbolic `ceilF(V)` opaque. The other named symbols have no reachable
dependent in either positive proof.

Compiler warnings identify non-exhaustive totalization on values outside the
used numeric cases. For the intended list of finite Python integers/floats,
`ceilF` covers both relevant value constructors. No rule in the active path is
labelled unsound, so no false-conclusion witness is asserted.

## Claims

The loop claim is satisfiable, for example with `L=1`, `GLOBAL=.Map`,
`INPUT=list(.ValSeq)`, `CURRENT=7`, `ACC=0`, and any parent; its empty instance
preserves `number=7` and `result=0`.

The function claim is satisfiable with `VS=.ValSeq` in its explicitly stated
module/builtins configuration. It executes the mechanically matched closure
body and returns `sumSquaresFrom(0,VS)`. The target is a value equality in the
`<k>` cell, not a free result variable or implication-only condition.

Ground K claims close for `[] -> 0` and `[1,2,3] -> 14`; the LLVM assertion
program also closes for `[1.4,4.2,0] -> 29` and `[-2.4,1,1] -> 6`.
