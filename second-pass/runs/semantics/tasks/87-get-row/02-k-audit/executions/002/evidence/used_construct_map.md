# Submitted-program constructor and rule map

This map is reviewer-authored. Source line numbers refer to the trusted
`/reference/reference-semantics` tree and the immutable candidate.

| Submitted constructor/operation | Declaration and fixed execution rules | Audit conclusion |
|---|---|---|
| `Module(FuncDef(...))` | `semantics/syntax.k:61`; module load in `core.k:120-123`; function definition in `functions.k:14-16` | The entry claims install the same closure directly instead of loading the module. The separately checked `getRowBody`/`getRowClosure` constructor identity makes the skipped load inert for this one-definition module. |
| `Call(Name("get_row"), ...)` | `syntax.k:27`; lookup `core.k:126-153`; argument evaluation `core.k:183-188`; call routing and closure entry `call.k:18-20,63-69`; param binding and return/pop `functions.k:63-89` | The actual closure body is entered, arguments bind left-to-right, and the function frame is popped normally. No proof-local call interception exists. |
| `Assign(Name("result"), ListExpr())` | strict assignment `syntax.k:41`; list evaluation/allocation `list.k:14-17`; name assignment `controls.k:8-10`; allocation `core.k:114-117` | Allocates the returned list and binds its ref in the callee scope. |
| outer `For(..., enumerate(lst), ...)` | `syntax.k:43`; builtin lookup/call above; enumerate `builtins.k:124-129`; heap-iterable dereference and loop protocol `controls.k:50-61,101-104`; list iterator `list.k:8-10` | Enumerate eagerly creates `(row_index,row)` tuples in row order; the loop consumes all rows in that order. |
| tuple loop target | tuple literal and target binding/unpacking `tuple.k:14-16,31-57` | Binds `row_index` and `row` to the two tuple fields on each iteration. |
| `len(row) - 1` and unary `-1` | len/`seqLen` `builtins.k:17-24`; heap argument dereference `call.k:38-43`; unary/binary dispatch `operators.k:9-11`; integer rules `int.k:7-17` | For each finite row of length `n`, produces `n-1`, `-1`, `-1`. |
| `range(n-1,-1,-1)` | builtin range `builtins.k:177-180`; range membership/iteration `range.k:8-25` | Yields exactly `n-1,...,0`; empty rows yield no index. Step is the fixed nonzero integer `-1`. |
| `row[column_index]` | subscript evaluation/deref and `applyIndex` `subscript.k:24-38`; `valSeqAt`, `normIdx`, `vsLen` `subscript.k:9-22`, `core.k:223-226` | All generated indices are in bounds. Access returns the selected integer. The semantics' underspecified out-of-bounds totality is unreachable here. |
| integer `== x` and `If` | compare contexts/dispatch `operators.k:13-16`; integer equality `int.k:26`; branch rules `controls.k:42-46` | Branches exactly on integer equality. |
| `result.append((row_index,column_index))` | attribute/call routing `call.k:15-20`; tuple construction `tuple.k:14-16`; append mutation `list.k:45-48`; expression discard `controls.k:37` | Appends each matching coordinate to the result list in traversal order and preserves the list ref. |
| `Return(Name("result"))` | strict return and frame pop `functions.k:77-89` | Returns the allocated list ref and restores the caller state. |

The used path is entirely integer/list/tuple control flow. The fixed semantics'
opaque float, sort, MD5, keyed-sort, and similar primitives cannot match any
submitted term and do not contribute to either positive claim.
