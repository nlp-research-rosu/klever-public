# `solution.mpy` constructor-to-semantics map

The trusted-regenerated constructor census is:

```text
2 Assign; 1 Attribute; 8 BinOp; 2 Bool; 8 Call; 1 CellVars;
2 CmpOp; 2 CompFor; 2 Compare; 2 Expr; 1 FreeVars; 2 FuncDef;
1 If; 1 IfExp; 12 Int; 2 ListComp; 1 Module; 27 Name; 2 Params;
3 Return; 4 Slice; 3 Str; 6 Subscript; plus NoBound and list units.
```

| Constructor | Declaration | Operational rules | Target-proof use |
|---|---|---|---|
| `Module`, `Stmts` | `semantics/syntax.k:56,61` | `semantics/core.k:124-127` loads and sequences the module | The entry claim starts from the mechanically identical function binding rather than replaying module load; fresh `krun solution.regenerated.mpy` checks module load. |
| `FuncDef`, `Params` | `syntax.k:53-54,57` | `functions.k:14-16` binds the unannotated `decode_cyclic` closure; `functions.k:33-45` handles annotated defs | The manually written `decodeClosure` is mechanically KORE-identical to the regenerated unannotated target body/binding. |
| `CellVars`, `FreeVars` | `syntax.k:58-59` | `functions.k:33-60` and `call.k:80-94` capture/bind annotated closures/cells | Used only by the prompt-supplied `encode_cyclic` helper, not by `decode_cyclic`. |
| `Expr` | `syntax.k:50` | strictness evaluates its expression; `controls.k:44` discards the resulting value | Executes the target docstring before the branch. |
| `Str` | `syntax.k:13` | `str.k:12-15` converts an ASCII K string literal to `str(IntSeq)` | Used for docstrings and the helper’s empty separator. The symbolic entry input is already `str(CS)`. |
| `Int`, `Bool` | `syntax.k:9,11` | `core.k:193-194` cools literals to values | `Int(3)`, indices `0/1/2/3`; `Bool(true)` occurs only in helper comprehensions. |
| `Name` | `syntax.k:12` | `core.k:130-153` performs lexical/builtin lookup | Resolves local `s`, recursive global `decode_cyclic`, and builtin `len`. |
| `Call` | `syntax.k:27` | `call.k:18-32` evaluates callee/arguments; `call.k:69-85` enters closures; `functions.k:63-90` binds/returns/pops | Executes `len(s)` and the recursive call under the exact target closure. |
| `Compare`, `CmpOp` | `syntax.k:29,32` | `operators.k:12-18`; `int.k:22` implements integer `<` | Evaluates `len(s) < 3`. |
| `If` | `syntax.k:48` | strictness plus `controls.k:50-54` branches on `truthy` | Selects base versus recursive case. |
| `Return` | `syntax.k:49` | strictness plus `functions.k:78-90` sets `ret`, pops frames, restores environment/scope | Both base and recursive results follow the normal fixed return path. |
| `BinOp` | `syntax.k:14` | left-to-right `seqstrict`; `operators.k:10`; `str.k:19-23` concatenates string code sequences; `int.k:9-17` serves helper arithmetic | The target’s two `+` operations concatenate `s[2]`, `s[:2]`, and the recursive result. |
| `Subscript` | `syntax.k:22,38-39` | contexts/index dispatch `subscript.k:27-43`; index function `subscript.k:7-24` | `s[2]` becomes a one-code string through in-bounds `intSeqAt`. |
| `Slice`, `NoBound` | `syntax.k:38-39` | bound evaluation and slicing `subscript.k:45-123`; start/stop clamping `subscript.k:72-106`; `buildIS` `subscript.k:116-123` | Implements `s[:2]` and the strictly shorter `s[3:]`. |
| `Assign` | `syntax.k:41` | `controls.k:6-31` writes the active scope | Used only in `encode_cyclic`; absent from the target body. |
| `ListComp`, `CompFor` | `syntax.k:19,35-36` | macros `comprehension.k:10-25` expand to an isolated closure, list accumulator, `For`, and filters | Used only in `encode_cyclic`; fresh concrete module tests exercise it. |
| `IfExp` | `syntax.k:23` | strict condition plus `controls.k:56-60` | Used only in `encode_cyclic`’s second comprehension. |
| `Attribute` | `syntax.k:28` | `call.k:16` makes a bound method; `methods.k:24-31` defines string `join` | Used only in `encode_cyclic`’s final `"".join(groups)`. |

Fixed-semantics evaluation order is left-to-right for `BinOp` and call
arguments, the callee binding is selected through ordinary lexical lookup, and
recursive frames allocate monotonically, bind `s`, preserve the continuation,
then restore environment/scope on `#pop`. The target does not allocate heap
objects or mutate observable state.
