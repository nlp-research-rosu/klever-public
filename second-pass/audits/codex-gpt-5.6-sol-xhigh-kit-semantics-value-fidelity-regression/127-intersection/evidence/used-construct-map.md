# Used-construct and rule map

The complete 947-item inventory is `rule-inventory.tsv`. This file maps every
constructor in the submitted `solution.mpy` to the supplied declarations and
the rules exercised by the entry proof.

| Submitted construct | Declaration / fixed-semantics behavior | Audit result |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequences | `syntax.k:54-62`; module sequencing `core.k:124-127`; closure installation `functions.k:14-16` | The entry claim starts in the exact post-load closure state rather than re-running module load. `body_pinning.py` proves syntactic identity of the translated body, parameters, and defining environment; the skipped load/definition steps only install that closure. |
| `Call` | `syntax.k:26`; callee then arguments `call.k:20-21`; argument order `core.k:189-191`; closure frame `call.k:69-74` | Callee lookup occurs first, arguments are evaluated left-to-right, and the exact looked-up closure is invoked. No Call interception or proof-local operational bridge exists. |
| `Name` | `syntax.k:12`; `core.k:130-154` | Lookup starts at `<env>`, uses the current scope when bound, and otherwise follows the parent. All function locals and the module binding are present. Cell-specific priority rules are inapplicable because these are plain frames. |
| `TupleExpr` | `syntax.k:19`; `tuple.k:14-16`; `core.k:189-191,217-219` | Each two-element tuple is evaluated left-to-right and becomes the exact `tuple(vCons(...))` consumed by parameter binding. |
| `Int` | `syntax.k:9`; `core.k:194` | K mathematical integers faithfully represent the task's integer domain. |
| `Assign(Name(...), ...)` | strict RHS in `syntax.k:38`; `controls.k:9-11` | RHS evaluates before the scope write. Cell/ref alternatives and their priorities cannot match the plain integer locals. |
| `Subscript(tuple, Int)` | `syntax.k:20,34-35`; ordered contexts `subscript.k:27-28`; dispatch `subscript.k:35`; tuple index `subscript.k:39`; helpers `subscript.k:11-23`, `core.k:223-225` | The tuple evaluates before the index. Indices are exactly `0` and `1` on two-element tuples, so the total-but-underdefined out-of-bounds cases cannot arise. |
| `If` | strict condition in `syntax.k:45`; `controls.k:51-54` | Only the selected branch executes. Integer truthiness comes from `core.k:202`; all actual conditions cool to Bool values through comparison. |
| `Compare` / `CmpOp` | `syntax.k:28-30`; ordered contexts and dispatch `operators.k:15-17`; integer cases `int.k:22-27` | Left operand then comparator operand are evaluated. Operators used are `>`, `<`, and `==`; all dispatch to ordinary integer relations. Ref-dereference priority rules cannot match. |
| `BinOp` | left-to-right `seqstrict(2,3)` in `syntax.k:14`; dispatch `operators.k:12`; integer `+`, `-`, `*`, `%` in `int.k:9,13-15` | All operands are integers. `%` becomes `pyMod`; the only program use has divisor `length >= 2`, so division by zero is excluded. |
| `While` | `syntax.k:42`; `controls.k:65-67,77-85` | The guard is re-evaluated before each iteration, the two assignments execute in sequence, and `#loopLbl` restores the loop. There is no break, continue, return, exception, output, heap write, or allocation in the body. |
| `Return` | strict result in `syntax.k:46`; `functions.k:78-90` | The result is stored in `<ret>`, the active computation is discarded exactly as Python return requires, and `#pop` restores caller environment, stack, scope map, and allocation pointer. |
| `Str` | `syntax.k:13`; `str.k:13-16` | The only literals are ASCII `"YES"` and `"NO"`, fully covered by `strToCodes`. The destination uses the identical code sequences. |

## Priority, opacity, and generated evaluation rules

- The supplied tree contains 34 declarations/rules mentioning `priority`, all
  listed in `rule-inventory.tsv`. None match the entry path: they concern heap
  references, closure cells, float/math interception, sort, dict/list
  operations, or assertion dereferencing.
- The supplied tree contains 25 `symbol(...), no-evaluators` opaque function
  declarations. They are confined to floats, sorting, and MD5, none of whose
  syntax appears in the program, claim, or result summaries.
- The only generated heating/cooling rules relevant here come from
  `seqstrict` on integer `BinOp`, `strict` on assignment RHS / condition /
  return, and the explicit comparison and subscript contexts. Their orders are
  recorded in the table above.
- There are no `[simplification]` rules and no `[functional]` declarations in
  the supplied or proof-local source. There are no proof-local priorities,
  opaque symbols, concrete-only rules, or operational rewrites.

## Configuration and state footprint

The fixed configuration is `core.k:49-60`. The entry claim pins all nine cells.
A call temporarily creates one local scope/frame; assignment changes only that
scope; the loop changes only `factorial` and `i`; return/pop removes the local
scope and restores `<env>`, `<scopeLoc>`, `<stack>`, and `<ret>`. The program
does not touch `<heap>`, `<heapLoc>`, `<exc>`, or `<exit-code>`. The destination
therefore correctly leaves every non-`<k>` entry cell unchanged.
