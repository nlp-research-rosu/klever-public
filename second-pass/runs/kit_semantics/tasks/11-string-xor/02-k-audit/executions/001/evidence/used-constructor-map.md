# Submitted-term constructor and rule map

The exact regenerated term is:

```text
Module
  FuncDef / Params
    Assign(Name("result"), Str(""))
    Assign(Name("x"), Str(""))
    Assign(Name("y"), Str(""))
    For(TupleExpr(Name("x"), Name("y")), Call(Name("zip"), Name("a"), Name("b")),
      If(Compare(Name("x"), CmpOp("==", Name("y"))),
        AugAssign(Name("result"), "+", Str("0")),
        AugAssign(Name("result"), "+", Str("1"))))
    Return(Name("result"))
```

The entry theorem begins after module loading, with the exact function closure
already bound at scope 0. Module loading and `FuncDef` are nevertheless covered
by concrete execution of the regenerated module.

| Submitted constructor / runtime form | Declaration | Material rules on the theorem path | Review |
|---|---|---|---|
| `Module`, statement list | `semantics/syntax.k:56,61`; `semantics/core.k:124` | `core.k:125-127` | Ordered module/statement execution; used by concrete reconstruction. |
| `FuncDef`, `Params` | `syntax.k:41,57,60`; closure values at `core.k:25` | `functions.k:14` | Binds the exact parameter list/body/defining scope. The entry claim mechanically pins the resulting closure rather than reloading the module. |
| `Name` | `syntax.k:9`; `#look` at `core.k:130` | `core.k:131-132,145-155` | Current-frame lookup, then parent lookup. The cell-deref priority rule is disabled because the exact plain frame has no `"$cells"` key. |
| `Str`, `str`, `IntSeq` | `syntax.k:9`; `core.k:13,15` | `str.k:14-16` | ASCII literal conversion; only `""`, `"0"`, and `"1"` are used. |
| `Assign` | `syntax.k:41` with strict RHS | `controls.k:9-18` | RHS first, then current-frame update. Cell-write priority case is disabled in the exact plain frame. |
| `Call` | `syntax.k:9`; call continuation at `call.k:19` | `call.k:20-21`; argument loop `core.k:185-191` | Callee evaluated first, then arguments left-to-right. |
| user-closure call | closure values at `core.k:25`; frame at `functions.k:8` | `call.k:69-75`; parameter binding `functions.k:63-75` | Creates a fresh plain callee frame, pushes the complete caller continuation, and binds `a`, then `b`. |
| builtin `zip` lookup/dispatch | `builtinV` at `core.k:25`; registry `core.k:157-181`; `applyBuiltin` at `builtins.k:17` | generic builtin call `call.k:31`; string zip `builtins.k:164` | Normal name lookup selects the fixed `zip` binding; no proof-local call interception exists. |
| `zipObjS` iteration | iterable declaration `core.k:18-23`; iterator protocol `iter.k:8` | `builtins.k:171-174` | Produces pairs of one-character strings and stops when either input is empty. |
| `For`, `#loop` | `syntax.k:41`; loop forms `controls.k:65-67` | `controls.k:69,71-74` | Iterable evaluated once; each yield binds target, executes body, then recurs. |
| tuple target / unpack | `TupleExpr` and `Exprs` at `syntax.k:9,37`; `#bindTgt`/`#unpackSeq` at `tuple.k:31,49` | `tuple.k:42,55,57`, plus name binding `tuple.k:32-41` | Binds `x` then `y` from the two-element tuple yielded by `zipObjS`. Cell-target priority is disabled in the plain frame. |
| `Compare(...,"==",...)` | `CmpOp` at `syntax.k:32`; comparison contexts `operators.k:15-16`; `applyCmp` at `core.k:210` | dispatch `operators.k:17`; string equality `str.k:25` | Left then right evaluation; exact code-sequence equality. |
| `If` | `syntax.k:41` with strict condition; branch form `controls.k:51` | `controls.k:52-54`; boolean truth at `core.k:199-200` | Chooses exactly one branch from the comparison boolean. |
| `AugAssign(...,"+",...)` | `syntax.k:41` with strict RHS; `applyBin` at `core.k:209` | update `controls.k:20-31`; string addition `str.k:20-24` | Literal RHS first; reads current `result`, concatenates, and writes it. Ref-specific priority case is disabled for `str`. |
| `Return` and call pop | `syntax.k:41`; return/frame forms `core.k:42`, `functions.k:8` | `functions.k:78-89` | Evaluates `result`, records it, restores caller state, deletes the callee frame, and resumes the saved continuation. |
| proof bridge | local `#loop` rule `verification.k:66-94` | exact text of `spec.k:6-33` loop theorem | Only the exact loop/body/plain five-key frame matches; it preserves arbitrary continuation and all omitted cells and changes exactly `result`, `x`, and `y`. |

Generated heat/cool rules from the `strict` and `seqstrict` declarations are
part of the trusted K elaboration. For this term they enforce RHS-before-write,
iterable-before-loop, condition-before-branch, return-expression-before-pop,
and the explicit comparison contexts enforce left-to-right operand evaluation.
