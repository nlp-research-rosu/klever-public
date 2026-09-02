# Submitted constructor coverage

The trusted translator regenerated `/tmp/audit-work/candidate/solution.mpy`
byte-for-byte. Its constructor term is:

```text
Module(
  FuncDef("flip_case", Params("string"),
    Return(Call(Attribute(Name("string"), "swapcase"), ))))
```

| Used constructor/form | Declaration | Operational path |
|---|---|---|
| `Module(Stmts)` | `semantic.k:6` | module load/invoke rule at line 55 |
| singleton `Stmts` containing `FuncDef` | `semantic.k:8` | direct `Stmt` injection; the multi-statement sequencing rule at line 58 is not needed |
| `FuncDef(String,Params,Stmts)` | `semantic.k:11` | installs exact parameters/body at line 60 |
| `Params(String,.Strings)` | `semantic.k:14-15` | destructured by invocation at lines 63-65 |
| `Return(Expr)` | `semantic.k:12` | evaluates expression and appends `#return` at line 67 |
| `Call(Expr,.Exprs)` | `semantic.k:17,21` | zero-argument evaluation at line 78 and swapcase dispatch at lines 79-80 |
| `Attribute(Expr,String)` | `semantic.k:20` | receiver-first evaluation at lines 74-76 |
| `Name(String)` | `semantic.k:19` | exact environment lookup at lines 69-70 |
| K `String` tokens (`"flip_case"`, `"string"`, `"swapcase"`) | imported `STRING-SYNTAX` | preserved as function keys, parameter keys, and method names |

The runtime path additionally uses `function`, `strVal`,
`boundStringMethod`, `#invoke`, `#attribute`, `#callNoArgs`, `#return`, and
`#endCall`, all declared at `semantic.k:34-43`. It does not use the extra
`Str(String)` expression rule or multi-statement sequencing.
