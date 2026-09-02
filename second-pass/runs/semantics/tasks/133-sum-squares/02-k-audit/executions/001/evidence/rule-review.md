# Exhaustive rule-review disposition

The exact text, source span, attributes, and classification of all 1,225
top-level declarations are in `13-exhaustive-rule-inventory.log`. That inventory
contains 700 rules, 229 syntax declarations, five contexts, one configuration,
and two claims. Of the rules, 695 belong to the byte-identical fixed supplied
semantics and five are candidate-local.

## Fixed supplied semantics

The following table accounts for every fixed-semantics inventory item and every
one of its rules. `Relevant` identifies the dependency slice of the submitted
program and the two claims. `Fixed/unreached` means the declarations are part of
the selected trusted semantics but no top symbol, continuation, value, or cell
used in either successful claim can invoke them before the target is reached.
No rule in this latter group contributes to claim closure.

| File (inventory items) | Rules | Disposition |
|---|---:|---|
| `semantics.k` (0001–0050) | 0 | Import graph only; `MPY` is the Haskell proof module and `MPY-KRUN` adds `MPY-CONCRETE` only for LLVM execution. |
| `assert.k` (0051–0058) | 3 | Fixed/unreached by the positive claims; reached only by reviewer concrete smoke programs. |
| `bool.k` (0059–0083) | 13 | Fixed/unreached. |
| `builtins.k` (0084–0288) | 137 | Fixed/unreached; the program's `math.ceil` uses the special syntactic interception in `float.k`, not builtin dispatch. |
| `call.k` (0289–0321) | 21 | Relevant generic callee/argument evaluation, closure invocation, frame push, and argument binding are faithful to the exact direct-closure call. Other builtin/method/annotated-closure cases are fixed/unreached. |
| `comprehension.k` (0322–0338) | 7 | Fixed/unreached. |
| `concrete.k` (0339–0367) | 16 | LLVM-only fixed support; none is imported into the Haskell `MPY` proof dependency slice. |
| `controls.k` (0368–0418) | 34 | Relevant rules implement assignment, integer augmented assignment, `For` creation, iterator stepping, target binding, body sequencing, and loop continuation. `Import` handling is relevant only to the separately executed module. Branch/while/break/ref cases are fixed/unreached. |
| `core.k` (0419–0519) | 46 | Relevant configuration, module load, statement sequencing, local lookup, left-to-right argument evaluation, integer literals, algebraic sequence helpers, and builtin-scope normalization are faithful. Heap/cell/keyword/truthiness/unreached helper cases do not contribute. |
| `dict.k` (0520–0569) | 28 | Fixed/unreached. |
| `float.k` (0570–0736) | 121 | Relevant rules are float literal evaluation, no-op plain import, priority-40 `math.ceil` interception, `#mathCeil`, and `ceilF`. The interception is exact for this unshadowed `math.ceil` call but intentionally broader than full Python binding semantics. All other float operations are fixed/unreached. |
| `functions.k` (0737–0761) | 15 | Relevant function definition for the module-to-closure bridge, ordinary parameter binding, return, and frame pop are faithful. Annotated closure/cell cases are fixed/unreached. |
| `int.k` (0762–0781) | 16 | Relevant integer `+` and nonnegative exponentiation implement the accumulator and square. Other integer operators are fixed/unreached. |
| `iter.k` (0782–0785) | 0 | Iterator control syntax used by `For`. |
| `list.k` (0786–0826) | 27 | The two list-iterator rules are relevant, disjoint, exhaustive on algebraic `ValSeq`, and preserve left-to-right order. Literal allocation and list operations are fixed/unreached in the formal claims. |
| `methods.k` (0827–0940) | 75 | Fixed/unreached. |
| `operators.k` (0941–0959) | 10 | Generic binary dispatch is relevant; `seqstrict(2,3)` in `syntax.k` fixes left-to-right operand evaluation. Ref and comparison cases are fixed/unreached. |
| `range.k` (0960–0976) | 6 | Fixed/unreached. |
| `set.k` (0977–0999) | 12 | Fixed/unreached. |
| `sort.k` (1000–1030) | 19 | Fixed/unreached. |
| `str.k` (1031–1069) | 28 | Fixed/unreached. |
| `subscript.k` (1070–1145) | 40 | Fixed/unreached. |
| `syntax.k` (1146–1167) | 0 | All submitted constructs are declared: `Module`, `Import`, `FuncDef`, `Params`, `Assign`, `For`, `Name`, `AugAssign`, `BinOp`, `Call`, `Attribute`, `Int`, and `Return`. Strictness attributes cover the expression evaluation order. |
| `tuple.k` (1168–1200) | 21 | The ordinary `#bindTgt(Name,V)` rule is relevant to the loop target; tuple/unpacking/cell cases are fixed/unreached. |

The fixed semantics contains no `[simplification]` or `[functional]`
declaration. Its proof-domain opaque or concrete-only symbols are inventoried
with `opaque=yes`/their attributes in the exhaustive log. Only `ceilF` can
influence this theorem.

## Candidate-local declarations and rules

| Inventory item | Extension | Class and decision |
|---|---|---|
| 1204 | `sumSquaresFrom(Int,ValSeq) [function,total]` | Definitional summary. No opacity. |
| 1205 | empty `sumSquaresFrom` equation | True base equation. |
| 1206 | cons `sumSquaresFrom` equation | True left fold equation; constructor-disjoint from 1205 and strictly descends on `REST`. Its value uses the same fixed `ceilF` and integer square executed by the program. |
| 1207 | `lastFrom(Val,ValSeq) [function,total]` | Definitional summary. No opacity. |
| 1208 | empty `lastFrom` equation | True base equation. |
| 1209 | cons `lastFrom` equation | True last-element recursion; constructor-disjoint from 1208 and strictly descends. |
| 1213–1214 | priority-40 loop rewrite | Operational bridge/derived lemma. Its normalized contract is byte-identical to the independently proved base loop claim except for priority. The base proof closed with `#Top`; its domain includes the arbitrary continuation and the same framed cells. Base and extended ground executions with an observable following assignment both closed. It updates only `number` and `result` and introduces no abrupt control. |

There are no candidate-local simplification rules, opaque symbols, or
unconstrained fresh results. The two candidate total functions have exhaustive
constructor coverage and no overlapping equations. The priority attribute only
selects the already-proved loop lemma before unrolling; it does not broaden the
match.

## Program/control mapping

The actual module concretely loads as an environment-0 closure with exactly the
body embedded in the function claim. The formal entry claim starts one step
later from a direct call of that closure. Its body executes:

`Call` → closure frame push/bind → `Assign(result,0)` → evaluate `lst` once →
`For/#loop` → list iterator → bind `number` → evaluate `math.ceil(number)` →
integer `** 2` → integer `result +=` → loop → `Return`/frame pop.

The loop lemma does not match the function's initial nonempty loop state because
`number` is not bound yet. Fixed semantics executes the first iteration, binds
`number`, and only then can the lemma summarize the remaining suffix. The empty
input exits by fixed semantics. This matches the real control flow and prevents
the lemma from fabricating the initial target binding.
