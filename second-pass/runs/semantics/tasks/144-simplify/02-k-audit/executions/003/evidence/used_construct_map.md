# Used-constructor and rule map

The submitted constructor term contains:

`Module`, `FuncDef`, `Params`, `Assign`, `TupleExpr`, `Name`, `Call`,
`Attribute`, `Str`, `Return`, `Compare`, `BinOp`, `CmpOp`, and `Int`, plus
`Stmts`, `Exprs`, and `ParamNames` list productions.

All declarations come from the trusted supplied tree:

- `Module`, `Params`, `ParamNames`, and `Stmts`: `semantics/syntax.k:56-61`.
- `FuncDef`, `Assign`, and `Return`: `semantics/syntax.k:41-54`.
- `TupleExpr`, `Name`, `Call`, `Attribute`, `Str`, `Compare`, `BinOp`, and
  `Int`: `semantics/syntax.k:9-30`.
- `CmpOp` and `Exprs`: `semantics/syntax.k:32-37`.

The entry claim does not execute `Module`/`FuncDef`; `runSimplify` constructs
the same two-parameter closure body directly. The mechanical comparison is in
`program_pinning.log`. From that closure invocation, the material path is:

1. `verification.k:23-49` invokes the exact closure with `(X,N)` in order.
2. `call.k:69-74` allocates the call scope and frame; `functions.k:63-75`
   binds `x` and `n`.
3. `call.k:16`, `call.k:20-24`, `core.k:189-191`, `str.k:14`, and
   `methods.k:94-102` evaluate each left-to-right `x.split("/")` or
   `n.split("/")` call and allocate the returned list via `core.k:118-121`.
4. `tuple.k:50-57` dereferences, unpacks, and binds the two string components.
5. `core.k:131-154`, `core.k:157-181`, `call.k:20-32`, and
   `builtins.k:140-160` normally resolve and execute each `int(...)`.
6. `operators.k:12-17` dispatches multiplication, modulo, and equality to
   `int.k:14-20` and `int.k:26`.
7. `functions.k:78-90` returns the Boolean, restores the caller environment,
   and removes the call scope while retaining the two split-list heap objects.

On the candidate theorem path, step 3's recursive `splitSep` equations and
step 5's concrete decimal `int` equations cannot match the fresh
`fractionCodes`/`numCodes` constructors. Candidate rules
`verification.k:15-18` replace those two material computations.

Evaluation order is fixed by syntax strictness (`Assign` strict in its RHS,
`BinOp` `seqstrict(2,3)`, `Attribute` strict in its receiver, and `Return`
strict) plus the explicit shared argument loop. The candidate wrapper preserves
the active continuation and does not touch cells besides `<k>`.

The proof imports `MPY`, not `MPY-KRUN`; therefore none of
`semantics/concrete.k` contributes to the reachability result. The 25 supplied
opaque float/MD5/sort declarations inventoried in `rule_inventory.log` are also
unreachable from this integer/string program.
