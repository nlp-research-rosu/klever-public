# Used MPY constructs and execution rules

This map is reviewer-authored. Line references are to the fresh scratch copy at
`/tmp/audit-work/66-digitsum.dlRQYF/candidate/`.

| Submitted AST construct | Declaration | Fixed-semantics execution |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | Initial configuration and `#loadAll` in `semantics/core.k:49-60,124-127` |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57` | Closure installation in `semantics/functions.k:14-16` |
| statement sequencing | `semantics/syntax.k:56` | `semantics/core.k:125-127` |
| `Assign` | `semantics/syntax.k:41` (`strict(2)`) | scope update/cell dispatch in `semantics/controls.k:9-18` |
| `Name` | `semantics/syntax.k:12` | lexical lookup in `semantics/core.k:130-154` |
| `Int` | `semantics/syntax.k:9` | literal cooling in `semantics/core.k:194` |
| `Str` | `semantics/syntax.k:13` | literal-to-code sequence in `semantics/str.k:13-17` |
| `For` | `semantics/syntax.k:45` (`strict(2)`) | loop protocol in `semantics/controls.k:62-74`; string iterator in `semantics/str.k:7-10` |
| `Call` | `semantics/syntax.k:28` | callee then left-to-right argument evaluation in `semantics/call.k:18-21` and `semantics/core.k:183-191`; closure frame push in `semantics/call.k:69-75` |
| builtin `ord` | value installed by `builtinsScope`, `semantics/core.k:157-181` | generic builtin dispatch in `semantics/call.k:31`; singleton-string equation in `semantics/builtins.k:142-144` |
| `Compare`, `CmpOp` | `semantics/syntax.k:30,32` | ordered operand contexts and dispatch in `semantics/operators.k:14-17`; integer cases in `semantics/int.k:22-27` |
| `BoolOp("and", ...)` | `semantics/syntax.k:16` | left-to-right short-circuit rules in `semantics/bool.k:13-25` |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | truthiness and branch selection in `semantics/controls.k:50-54` |
| `AugAssign("+")` | `semantics/syntax.k:44` (`strict(3)`) | current-scope read/update in `semantics/controls.k:20-31`; integer `+` in `semantics/int.k:9` |
| `Return` | `semantics/syntax.k:50` (`strict`) | return, frame pop, caller restoration, and scope removal in `semantics/functions.k:77-90` |

## Control and state conclusion

For the actual loop body represented by the proof macro, the fixed semantics:

1. iterates the finite `IntSeq` left to right and binds each one-character
   `str`;
2. evaluates `ord(char)` to that character code;
3. evaluates `code >= 65` first and only evaluates `code <= 90` when needed;
4. adds `code` to `result` exactly in the inclusive `65..90` case; and
5. returns `result`, pops the frame, restores environment `0`, removes scope
   `1`, and leaves the empty heap unchanged.

The initial and loop operational rules in `verification.k` match all active
cells and exact continuations in the independently proved claims. Their
`priority(20)` attributes do not broaden their match domains.

## Critical pinning observation

The actual `Module(FuncDef(...))` path in the first two rows is not exercised by
any claim. The entry claim directly calls
`closureVal(("s", .ParamNames), digitSumBody, 0)` and therefore bypasses module
loading, closure installation under the name `digitSum`, name lookup, and the
submitted `solution.mpy` artifact. The hand-written `digitSumBody` macro is
token-for-token behaviorally equivalent to the submitted body after its nested
`digitSumLoopBody` macro expands, but the proof has no source dependency on that
artifact. Evidence `04_body_sensitivity_proof.log` confirms that rebuilding
after replacing `solution.py` and `solution.mpy` with `return 999` still closes
the entry theorem.
