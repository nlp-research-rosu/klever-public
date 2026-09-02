# Proof-extension review

The machine inventory is `rule-inventory.tsv`: it contains all 695 supplied
rules, 227 supplied syntax declarations, the supplied configuration and five
contexts, all 13 proof-local rules, all nine proof-local syntax declarations,
and all three reachability claims. The inventory count exactly matches direct
`rg` counts for supplied `rule` and `syntax` lines.

## Proof-local declarations and rules

| Lines | Extension | Class | Domain/context and state footprint | Review |
|---|---|---|---|---|
| verification.k:7-25 | `scanBody` declaration/equation | Definitional summary | Nullary `Stmts` function; no cells. One exhaustive equation. | Sound. Its RHS is the exact loop body from regenerated `solution.mpy`; `source-pinning-spec.k` checks constructor equality. |
| verification.k:26-33 | `isNestedBody` declaration/equation | Definitional summary | Nullary `Stmts` function; no cells. One exhaustive equation. | Sound. Exact assignments, loop, and return from regenerated `solution.mpy`. |
| verification.k:34-38 | `isNestedClosure` declaration/equation | Definitional summary | Nullary `Val` function; no cells. One exhaustive equation. | Sound. Exact parameter list, body, and defining scope location 0. |
| verification.k:39 | `BSeq ::= bNil \| bOpen \| bClose` | Proof-domain representation | Free algebraic datatype. | Sound and unbounded: a bijective representation of all finite strings over `[` and `]`. |
| verification.k:43 | `bCodes(BSeq)` | Proof-domain representation | Fresh `IntSeq` constructor. | Sound as a representation when paired with the three iterator rules below. It is not an opaque result oracle and carries no answer. |
| verification.k:44 | iterator of `bCodes(bNil)` | Definitional operational rule | Exact `#iterNext(str(...))` redex; arbitrary continuation is preserved; no cells touched. | Sound: the empty encoding produces `#iterDone`. Fresh constructor means no fixed rule is displaced. |
| verification.k:45-46 | iterator of `bCodes(bOpen(BS))` | Definitional operational rule | Same context; yields one-character string code 91 and preserves the suffix as `bCodes(BS)`. | Sound, exhaustive for the open constructor, and matches ASCII `[`. |
| verification.k:47-48 | iterator of `bCodes(bClose(BS))` | Definitional operational rule | Same context; yields one-character string code 93 and preserves the suffix. | Sound, exhaustive for the close constructor, and matches ASCII `]`. The three iterator LHSs are disjoint and exhaustive over `BSeq`. |
| verification.k:51-54 | `openStep` declaration/equation | Definitional summary | Total on `Int`; one conditional equation. | Sound: increments exactly when `I < 2`; no overlap or uncovered input. |
| verification.k:55-58 | `closeStep` declaration/equation | Definitional summary | Total on `Int`; one conditional equation. | Sound: increments exactly when `1 < I < 4`; no overlap or uncovered input. |
| verification.k:59-63 | `scanState` declaration/three equations | Definitional summary | Total on `Int × BSeq`; structural recursion. | Sound: the equations are constructor-disjoint, exhaustive, and decrease the `BSeq`. |
| verification.k:64-65 | `nested` declaration/equation | Definitional summary | Total on `BSeq`; one equation. | Sound: exactly `scanState(0, BS) == 4`, the `[[]]` subsequence automaton. |
| verification.k:74-115 | `proved-scan-loop` priority-40 rule | Operational bridge | Reads/replaces the entire loop, return, and `#endcall`; reads local state and arbitrary `_REST`; deletes local scope; restores env/scopeLoc/stack; returns `scanState(I,BS)==4`; requires `0<=I<=4`; heap/ret/exc/exit are exact. | **Unsound.** Its alleged connection theorem, `scan-loop`, fixes scopes 0 and -1 to the exact `is_nested` and builtins scopes. The installed rule instead accepts every `_REST:Map`, including globals that shadow `ord`. This violates context containment. |

There are no candidate simplification rules, no `[functional]` declarations,
and no candidate opaque/no-evaluator symbols. `proved-scan-loop` is the only
candidate priority rule.

## False-conclusion witness for `proved-scan-loop`

Use `I=2`, `BS=bClose(bClose(bNil))`, and the exact bridge control/stack state,
but let the `_REST` map contain a normal global source-language closure:

```text
0 |-> scope(
  "ord" |-> closureVal(("x", .ParamNames), Return(Int(91)) .Stmts, 0),
  parent(-1))
-1 |-> builtinsScope
```

This satisfies the installed rule's complete match and has the intended-domain
suffix consisting of two closing brackets.
Under the supplied semantics without the bridge, name
lookup selects the global closure. Both calls return 91; from state 2, the two
characters take the "open" branch and leave state 2, so the actual return is
`false`. `BRIDGE-WITNESS-FIXED-SPEC.fixed-shadowed-ord` proves that ground
execution to `false` with `#Top`.

The priority rule ignores that binding and rewrites directly to
`scanState(2,bClose(bClose(bNil))) == 4`, namely `true`.
`BRIDGE-WITNESS-EXTENDED-SPEC.bridge-shadowed-ord` proves that contradictory
bridge-enabled result with `#Top`. Thus the rule can enable a false
partial-correctness conclusion; this is not merely an untested edge.

The target entry state happens to contain the exact builtins namespace covered
by the narrower helper theorem. That does not repair the global rule:
`validating-proof` Gate A requires the bridge's entire match domain to lie
inside the bridge-free theorem's justification domain, and rejects globally
false rules even when their bad cases are off the target path. Narrowing
`_REST` back to the exact proven scopes (or proving a genuinely universal
connection theorem with a binding guard) would be required.

## Supplied-semantics rule review

The supplied tree is immutable under this condition and the candidate copy is
entry-for-entry and byte-for-byte identical. The 928 supplied declarations in
`rule-inventory.tsv` are therefore classified `ACCEPTED_SUPPLIED_BASELINE`.
The complete inventory was reviewed by module:

- `syntax.k` and `core.k`: constructor grammar, configuration, allocation,
  sequencing, lexical lookup, literal evaluation, truthiness, and structural
  list helpers.
- `iter.k`, `range.k`, `list.k`, `tuple.k`, `str.k`, and `set.k`: disjoint
  iterator cases and structurally descending sequence helpers.
- `operators.k`, `int.k`, `bool.k`, and `float.k`: strict evaluation,
  domain-disjoint dispatch, integer arithmetic/comparisons, short-circuit
  control, and the explicitly opaque/concrete float boundary.
- `controls.k`, `functions.k`, and `call.k`: assignment, conditional and loop
  control, left-to-right calls, frame allocation, binding, return, and pop.
- `builtins.k`, `methods.k`, `subscript.k`, `sort.k`, `dict.k`,
  `comprehension.k`, `assert.k`, and `concrete.k`: their declarations and
  rules are recorded individually in the inventory; their special primitives
  and deliberate partiality are outside this program's used path.

The 25 supplied opaque/symbol declarations are listed individually by the
inventory (MD5, float operations/conversions, and sort primitives). None can be
reached from this program or any claim. There are no supplied simplification
rules or `[functional]` declarations. Compiler warnings identify deliberately
partial totalized helpers in unused float/method/subscript paths; they do not
affect this theorem.

## Used-constructor mapping

| Submitted constructor/effect | Declaration and rules |
|---|---|
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll`, statement sequencing, `.Stmts` |
| `FuncDef`, `Call`, parameter and return frames | `functions.k` `FuncDef`, `#bindP`, `Return`, `#endcall`, `#pop`; `call.k` callee/argument evaluation and `closureVal` dispatch |
| `Assign(Name, ...)`, `AugAssign` | strict declarations in `syntax.k`; local-map rules in `controls.k`; integer `applyBin("+",Int,Int)` in `int.k` |
| `For` and character binding | strict `For` declaration; `controls.k` `For/#loop/#loopStep`; `tuple.k` `#bindTgt(Name,Val)`; proof-local `bCodes` iterator rules |
| `If` | strict declaration; `controls.k` `If/#branch`; `core.k` `truthy(Bool)` |
| `Name` | `core.k` local/parent lookup rules and exact `builtinsScope` |
| `Int`, `Str`, comparisons | `core.k` integer literal; `str.k` ASCII `Str/strToCodes`; `operators.k` comparison contexts/dispatch; `int.k` integer `==`, `<`, `>` |
| `ord(char)` | `call.k` call routing; `core.k` builtins lookup; `builtins.k` one-character `ord` equation |
| `Return` and observable result | strict declaration and `functions.k` return/pop rules; all heap, exception, exit, and control cells are pinned by the claims |

All material operations in the real body execute under those fixed rules before
the loop bridge is used. The only failing extension is the over-broad installed
loop rule described above.
