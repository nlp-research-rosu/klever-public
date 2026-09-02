requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The constructors below are the portion of py2mpy.py's output language
  // needed by solution.py.  Lists use the same concrete punctuation emitted
  // by the fixed transliterator.
  syntax Module ::= "Module" "(" Stmts ")"
                  | "solutionProgram" [function]
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" ParamList ")"
  syntax ParamList ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "ListExpr" "(" ExprList ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "IfExp" "(" Expr "," Expr "," Expr ")"
                | "Subscript" "(" Expr "," Index ")"
                | "Call" "(" Expr "," ExprList ")"
  syntax ExprList ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Index ::= Expr
                 | Slice
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr
                 | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  // Runtime values are deliberately distinct from source expressions.  This
  // prevents the semantics from silently treating untranslated syntax as an
  // already-computed Python value.
  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "listVal" "(" Vals ")"
               | Row
               | "gridVal" "(" Rows ")"
               | "noneVal"
  syntax Vals ::= List{Val, ","}
  // Contract-typed list values used by the universal proof.  They rule out
  // impossible Python inputs (non-integer cells or non-row grid elements)
  // at the grammar level while listVal remains available for ordinary runs.
  syntax Ints ::= List{Int, ","}
  syntax Row ::= "rowVal" "(" Ints ")"
  syntax Rows ::= List{Row, ","}

  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax Exprs ::= "exprs" "(" ExprList ")"
  syntax Values ::= "values" "(" Vals ")"
  syntax ArgVals ::= "noArgs"
                   | "arg" "(" Val "," ArgVals ")"

  // A translated module is the program supplied to krun.  ARGS is a
  // comma-separated Vals term, for example:
  //   -cARGS='listVal(listVal(intVal(1))), intVal(2)'
  configuration
    <max-fill>
      <k> $PGM:Module </k>
      <args> $ARGS:Vals </args>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noneVal </result>
    </max-fill>

  syntax Map ::= collectFunctions(Stmts) [function]
  rule collectFunctions(.Stmts) => .Map
  rule collectFunctions(FuncDef(F, P, BODY) REST)
    => (F |-> function(P, BODY)) collectFunctions(REST)

  syntax ArgVals ::= fromVals(Vals) [function]
  rule fromVals(.Vals) => noArgs
  rule fromVals(V, VS) => arg(V, fromVals(VS))

  syntax ArgVals ::= appendArg(ArgVals, Val) [function]
  rule appendArg(noArgs, V) => arg(V, noArgs)
  rule appendArg(arg(H, T), V) => arg(H, appendArg(T, V))

  syntax Vals ::= argValsToVals(ArgVals) [function]
  rule argValsToVals(noArgs) => .Vals
  rule argValsToVals(arg(V, REST)) => V, argValsToVals(REST)

  syntax Map ::= bindParams(Params, ArgVals) [function]
  rule bindParams(Params(.ParamList), noArgs) => .Map
  rule bindParams(Params(P, PS), arg(V, VS))
    => (P |-> V) bindParams(Params(PS), VS)

  syntax Val ::= arithmetic(String, Val, Val) [function]
  rule arithmetic("+", intVal(I), intVal(J)) => intVal(I +Int J)
  rule arithmetic("-", intVal(I), intVal(J)) => intVal(I -Int J)
  rule arithmetic("//", intVal(I), intVal(J)) => intVal(I /Int J)
    requires J =/=Int 0

  syntax Val ::= getItem(Val, Val) [function]
  rule getItem(listVal(V, VS), intVal(0)) => V
  rule getItem(listVal(V, VS), intVal(I))
    => getItem(listVal(VS), intVal(I -Int 1))
    requires I >Int 0
  rule getItem(rowVal(I, IS), intVal(0)) => intVal(I)
  rule getItem(rowVal(I, IS), intVal(N))
    => getItem(rowVal(IS), intVal(N -Int 1))
    requires N >Int 0
  rule getItem(gridVal(R, RS), intVal(0)) => R
  rule getItem(gridVal(R, RS), intVal(N))
    => getItem(gridVal(RS), intVal(N -Int 1))
    requires N >Int 0

  syntax Val ::= dropItems(Int, Val) [function]
  rule dropItems(0, listVal(VS)) => listVal(VS)
  rule dropItems(I, listVal(V, VS)) => dropItems(I -Int 1, listVal(VS))
    requires I >Int 0
  rule dropItems(0, rowVal(IS)) => rowVal(IS)
  rule dropItems(N, rowVal(I, IS)) => dropItems(N -Int 1, rowVal(IS))
    requires N >Int 0
  rule dropItems(0, gridVal(RS)) => gridVal(RS)
  rule dropItems(N, gridVal(R, RS)) => dropItems(N -Int 1, gridVal(RS))
    requires N >Int 0

  // Control frames for a left-to-right, small-step expression evaluator.
  // Calls save and restore the caller environment explicitly.  Besides
  // matching Python's evaluation order, this shape exposes recursive calls to
  // kprove so the claims in spec.k can be used as circularities.
  syntax KItem ::= invoke(String, ArgVals)
                 | restoreEnv(Map)
                 | binRight(String, Expr)
                 | binApply(String, Val)
                 | chooseBranch(Expr, Expr)
                 | "compareEmpty"
                 | subscriptIndex(Expr)
                 | subscriptApply(Val)
                 | sliceFrom(Int)
                 | evalCallArgs(String, Exprs, ArgVals)
                 | collectCallArg(String, Exprs, ArgVals)
                 | evalListItems(Exprs, ArgVals)
                 | collectListItem(Exprs, ArgVals)

  rule
    <k> Module(SS) => invoke("max_fill", fromVals(VS)) </k>
    <args> VS </args>
    <functions> .Map => collectFunctions(SS) </functions>

  rule
    <k> invoke(F, VS) => BODY ~> restoreEnv(OLD) ... </k>
    <functions> (F |-> function(P, BODY)) FS </functions>
    <env> OLD => bindParams(P, VS) </env>

  rule <k> Return(E) .Stmts => E ... </k>
  rule
    <k> V:Val ~> restoreEnv(OLD) => V ... </k>
    <env> _ => OLD </env>

  rule <k> Int(I) => intVal(I) ... </k>
  rule <k> Name(X) => V ... </k> <env> (X |-> V) ENV </env>

  rule <k> BinOp(OP, L, R) => L ~> binRight(OP, R) ... </k>
  rule <k> V:Val ~> binRight(OP, R) => R ~> binApply(OP, V) ... </k>
  rule <k> W:Val ~> binApply(OP, V) => arithmetic(OP, V, W) ... </k>

  rule <k> IfExp(COND, YES, NO) => COND ~> chooseBranch(YES, NO) ... </k>
  rule <k> boolVal(true) ~> chooseBranch(YES, NO) => YES ... </k>
  rule <k> boolVal(false) ~> chooseBranch(YES, NO) => NO ... </k>

  // Only equality with [] is exercised by solution.mpy.  Keeping it as two
  // constructor rules makes the empty/nonempty cases explicit to the prover.
  rule <k> Compare(E, CmpOp("==", ListExpr(.ExprList)))
            => E ~> compareEmpty ... </k>
  rule <k> listVal(.Vals) ~> compareEmpty => boolVal(true) ... </k>
  rule <k> listVal(V, VS) ~> compareEmpty => boolVal(false) ... </k>
  rule <k> rowVal(.Ints) ~> compareEmpty => boolVal(true) ... </k>
  rule <k> rowVal(I, IS) ~> compareEmpty => boolVal(false) ... </k>
  rule <k> gridVal(.Rows) ~> compareEmpty => boolVal(true) ... </k>
  rule <k> gridVal(R, RS) ~> compareEmpty => boolVal(false) ... </k>

  rule <k> Subscript(BASE, IDX:Expr)
            => BASE ~> subscriptIndex(IDX) ... </k>
  rule <k> V:Val ~> subscriptIndex(IDX)
            => IDX ~> subscriptApply(V) ... </k>
  rule <k> I:Val ~> subscriptApply(V) => getItem(V, I) ... </k>
  rule <k> Subscript(BASE, Slice(Int(START), NoBound, NoBound))
            => BASE ~> sliceFrom(START) ... </k>
  rule <k> V:Val ~> sliceFrom(START) => dropItems(START, V) ... </k>

  rule <k> Call(Name(F), ES)
            => evalCallArgs(F, exprs(ES), noArgs) ... </k>
  rule <k> evalCallArgs(F, exprs(.ExprList), VS) => invoke(F, VS) ... </k>
  rule <k> evalCallArgs(F, exprs(E, ES), VS)
            => E ~> collectCallArg(F, exprs(ES), VS) ... </k>
  rule <k> V:Val ~> collectCallArg(F, ES, VS)
            => evalCallArgs(F, ES, appendArg(VS, V)) ... </k>

  rule <k> ListExpr(ES)
            => evalListItems(exprs(ES), noArgs) ... </k>
  rule <k> evalListItems(exprs(.ExprList), VS)
            => listVal(argValsToVals(VS)) ... </k>
  rule <k> evalListItems(exprs(E, ES), VS)
            => E ~> collectListItem(exprs(ES), VS) ... </k>
  rule <k> V:Val ~> collectListItem(ES, VS)
            => evalListItems(ES, appendArg(VS, V)) ... </k>

  rule
    <k> V:Val => .K </k>
    <result> noneVal => V </result>
endmodule
