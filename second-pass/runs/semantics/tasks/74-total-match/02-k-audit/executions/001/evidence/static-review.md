# Static rule and construct review

This note is reviewer-authored. The exhaustive sentence inventory is
`rule-inventory.tsv`; its generating script is `static_inventory.py`.

## Inventory coverage

The inventory parses all 25 supplied-semantics K files plus `verification.k`
and `spec.k`. It contains 1,093 source sentences:

- supplied semantics: 695 rules, 227 syntax declarations, five contexts, one
  configuration, and structural module/import sentences;
- proof-local `verification.k`: 11 rules and six syntax declarations;
- `spec.k`: three claims.

Across these sources there are 146 `[function]` declarations, 108 `[total]`
declarations, 47 priority rules (one at priority 39, 43 at priority 40, and
three at priority 45), 35 `[concrete]` declarations, no `[simplification]`
rules, and no `[functional]` declarations.

`opaque-symbol-inventory.tsv` identifies the only locally declared functions
without a direct local equation: supplied `md5hexCodes` and `sortKeyVS`, both
marked `no-evaluators`. Neither is reachable from `solution.mpy`. There is no
proof-local opaque or oracle symbol.

Because this audit is in `SUPPLIED_SEMANTICS` mode and the candidate semantics
tree is entry/type/byte identical to the trusted tree, every supplied-semantics
sentence is classified as part of the selected fixed baseline. The used subset
was manually traced below. Unused baseline rules cannot affect this submitted
program. The trusted baseline does not justify any proof-local rule.

## Used-construct mapping

| Submitted construct | Syntax and fixed rules | Observed role |
|---|---|---|
| `Module` | `semantics/syntax.k:61`; `semantics/core.k:124-127` | Loads top-level statements. The entry proof bypasses this path. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57,60`; `semantics/functions.k:14-16` | Creates and binds a closure. The entry proof bypasses the definition/binding step. |
| `Int` | `semantics/syntax.k:9`; `semantics/core.k:194` | Produces unbounded K integers, matching Python integers for this program. |
| `Name` | `semantics/syntax.k:12`; `semantics/core.k:130-154` | Lexical lookup through function, module, and builtins scopes. |
| `Assign` | `semantics/syntax.k:41`; `semantics/controls.k:9-18` | Strict RHS evaluation and current-frame update. |
| `For` | `semantics/syntax.k:45`; `semantics/controls.k:65-74`; `semantics/list.k:8-9`; `semantics/tuple.k:31-41` | Evaluates iterable once, iterates, binds the target each iteration, and runs the body. |
| `AugAssign` and integer `+` | `semantics/syntax.k:44`; `semantics/controls.k:20-32`; `semantics/int.k:9` | Strict RHS then accumulator update. |
| `Call(Name("len"), ...)` | `semantics/syntax.k:28`; `semantics/call.k:18-21,69-75`; `semantics/core.k:156-183`; `semantics/builtins.k:17-26`; `semantics/core.k:227-229` | Resolves `len`, evaluates the argument, and counts `IntSeq` elements. |
| `Compare(..., "<=")` | `semantics/syntax.k:30,32`; `semantics/operators.k:14-17`; `semantics/int.k:23` | Left-to-right operand evaluation followed by integer comparison. |
| `If` | `semantics/syntax.k:49`; `semantics/controls.k:50-54`; `semantics/core.k:198-205` | Chooses exactly one branch using integer-comparison truth. |
| `Return` | `semantics/syntax.k:50`; `semantics/functions.k:78-90` | Sets the return value, drops the remaining body, restores the caller frame, and deallocates the callee scope. |

The fixed configuration has `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>` cells.
The entry claims pin all material initial cells; the generated counter/exit
cell is framed and does not affect the result.

## Proof-local extension decisions

1. `StrSeq` (`verification.k:9-10`) is an algebraic sequence restricted by
   construction to `IntSeq` string values. Accepted as a proof-domain syntax.

2. `strVals` and its two rules (`verification.k:12-15`) are structurally
   recursive, disjoint, and exhaustive over `StrSeq`. Accepted.

3. total function `totalChars` and its two rules
   (`verification.k:17-20`) are structurally recursive, disjoint, exhaustive,
   and equal the sum of supplied `isLen` values. Accepted.

4. `nextStrings` and its three rules (`verification.k:25-38`) expose one
   symbolic `StrSeq` constructor to the fixed list iterator. The adapter
   returns `#iterDone` for empty and the same head/rest pair the fixed list
   iterator returns for nonempty. It changes only `<k>` and preserves the
   active continuation. Accepted as an operational adapter.

5. `readAccAndDrop` and its two guarded rules
   (`verification.k:42-74`) define a proof-only observer. The guards distinguish
   item-absent from item-present maps and require accumulator/item names to
   differ. It returns the integer accumulator and, in the second case, deletes
   the item binding. Accepted as the definition of a new observer, but its
   special continuation cannot justify an arbitrary-continuation loop bridge.

6. The priority-40 `For` rewrite (`verification.k:86-108`) is rejected as an
   unsound operational bridge. It matches an arbitrary continuation and
   arbitrary names `ACC`/`ITEM`, reads the current environment and accumulator,
   replaces the entire real loop by one mathematical accumulator update, and
   otherwise frames every cell. A real nonempty loop also writes `ITEM` on
   every iteration; this rule leaves an existing item binding unchanged or
   leaves an absent binding absent. Its only purported connection claim
   (`spec.k:10-37`) is for literal names `"acc"`/`"item"` followed by the exact
   `readAccAndDrop` continuation, whose purpose is to delete the item binding.
   It proves neither arbitrary continuations nor the bridge's preserved item
   state, and it is not imported as a connection theorem into the entry
   claims.

   Concrete false-conclusion witness: start with `acc=0`, `item="z"`, iterate
   the exact body over `["a"]`, then evaluate `item`. Fixed semantics reaches
   accumulator `1`, item `"a"`, result `"a"` and proves that outcome
   (`14-fixed-witness-proof.log`); it rejects result `"z"` with a residual
   showing item/result `"a"` (`16-fixed-false-witness-rejected.log`). The
   bridge-enabled theory proves accumulator `1`, retained item `"z"`, and
   result `"z"` (`15-bridge-false-witness-proof.log`). The input is a
   one-element list of strings, within the intended input domain.

7. `runTotalMatch` (`verification.k:112-138`) is a new wrapper whose rewrite
   constructs a direct `closureVal` with a manually copied body. The body text
   currently matches the translated function body, so the wrapper itself is
   deterministic and its result is not opaque. It is nevertheless rejected as
   real-program pinning: it never parses or loads `solution.mpy`, never executes
   its `Module`/`FuncDef`, and has no source identity premise. A clean rebuild
   after replacing `solution.mpy` by an always-return-second implementation
   still proves both entry claims (`17` through `19` logs).

## Claims

- `spec.k:10-37` executes the fixed `#loop` from a state containing integer
  `acc=I` and arbitrary old item value, then executes the special observer. It
  constrains the result and final accumulator, but its continuation/name/state
  scope is strictly smaller than the proof-local `For` rule's match domain.
- `spec.k:42-57` states that the wrapper returns `A` when
  `totalChars(A) <= totalChars(B)`.
- `spec.k:59-74` states that the wrapper returns `B` when
  `totalChars(A) > totalChars(B)`.

The entry guards are satisfiable, disjoint, and exhaustive. Their results are
strongly constrained, as confirmed by the rejected wrong-branch mutation.
They close only under a theory containing the rejected loop bridge and prove a
wrapper independent of the submitted program artifact.
