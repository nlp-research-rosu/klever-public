requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Index ::= Expr | Slice

  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "ListExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  // Runtime values.  The explicit Ints datatype makes list induction and
  // symbolic execution independent of K's builtin, heterogenous List sort.
  syntax Ints ::= ".Ints"
                | Int "::" Ints [symbol(intsCons)]
  syntax Val ::= "intV" "(" Int ")"
               | "boolV" "(" Bool ")"
               | "listV" "(" Ints ")"

  syntax Vals ::= ".Vals"
                | Val ";" Vals [symbol(valsCons)]

  syntax Def ::= "def" "(" Params "," Stmts ")"
               | lookupDef(String, Stmts) [function]

  syntax Outcome ::= "normal"
                   | "returned" "(" Val ")"

  syntax KItem ::= "#run" "(" Pgm "," Val ")" [function]
  syntax Val ::= evalCall(String, Vals, Stmts) [function]
               | invoke(Def, Vals, Stmts) [function]
               | outcomeValue(Outcome) [function]
               | evalExpr(Expr, Map, Stmts) [function]
               | evalUnary(String, Val) [function]
               | evalBin(String, Val, Val) [function]
               | evalCompare(String, Val, Val) [function]
               | evalBoolBin(String, Val, Val) [function]
               | evalBitCount(Val) [function]
               | lookupEnv(String, Map) [function]
               | evalLen(Val) [function]
               | evalIndex(Val, Val) [function]
               | evalTail(Val) [function]
  syntax Outcome ::= evalStmts(Stmts, Map, Stmts) [function]
                   | evalAfterIf(Val, Stmts, Stmts, Stmts, Map, Stmts) [function]
                   | continueWith(Outcome, Stmts, Map, Stmts) [function]
  syntax Vals ::= evalArgs(Exprs, Map, Stmts) [function]
  syntax Ints ::= evalListItems(Exprs, Map, Stmts) [function]
                | appendInts(Ints, Ints) [function]
  syntax Int ::= intOf(Val) [function]
               | lengthInts(Ints) [function]
               | bitCount(Int) [function]

  configuration <k> #run($PGM:Pgm, $ARGS:Val) </k>

  rule #run(Module(DEFS), INPUT) => evalCall("sort_array", INPUT ; .Vals, DEFS)

  rule lookupDef(NAME, FuncDef(NAME, PS, BODY) REST) => def(PS, BODY)
  rule lookupDef(NAME, FuncDef(OTHER, PS, BODY) REST)
    => lookupDef(NAME, REST)
    requires NAME =/=String OTHER

  rule evalCall(NAME, ARGS, DEFS)
    => invoke(lookupDef(NAME, DEFS), ARGS, DEFS)

  rule invoke(def(Params(X:String), BODY), V ; .Vals, DEFS)
    => outcomeValue(evalStmts(BODY, X |-> V, DEFS))
  rule invoke(def(Params(X:String, Y:String), BODY), V1 ; V2 ; .Vals, DEFS)
    => outcomeValue(evalStmts(BODY, (X |-> V1) (Y |-> V2), DEFS))

  rule outcomeValue(returned(V)) => V

  rule evalStmts(.Stmts, RHO, DEFS) => normal
  rule evalStmts(Return(E) REST, RHO, DEFS)
    => returned(evalExpr(E, RHO, DEFS))
  rule evalStmts(If(COND, THEN, ELSE) REST, RHO, DEFS)
    => evalAfterIf(evalExpr(COND, RHO, DEFS), THEN, ELSE, REST, RHO, DEFS)

  rule evalAfterIf(boolV(B), THEN, ELSE, REST, RHO, DEFS)
    => continueWith(evalStmts(THEN, RHO, DEFS), REST, RHO, DEFS)
    requires B
  rule evalAfterIf(boolV(B), THEN, ELSE, REST, RHO, DEFS)
    => continueWith(evalStmts(ELSE, RHO, DEFS), REST, RHO, DEFS)
    requires notBool B
  rule continueWith(returned(V), REST, RHO, DEFS) => returned(V)
  rule continueWith(normal, REST, RHO, DEFS) => evalStmts(REST, RHO, DEFS)

  rule evalExpr(Int(I), RHO, DEFS) => intV(I)
  rule evalExpr(Bool(B), RHO, DEFS) => boolV(B)
  rule evalExpr(Name(X), RHO, DEFS) => lookupEnv(X, RHO)
  rule lookupEnv(X, (X |-> V) RHO) => V
  rule evalExpr(UnaryOp(OP, E), RHO, DEFS)
    => evalUnary(OP, evalExpr(E, RHO, DEFS))
  rule evalExpr(BinOp(OP, L, R), RHO, DEFS)
    => evalBin(OP, evalExpr(L, RHO, DEFS), evalExpr(R, RHO, DEFS))
  rule evalExpr(BoolOp(OP, L:Expr, R:Expr), RHO, DEFS)
    => evalBoolBin(OP, evalExpr(L, RHO, DEFS), evalExpr(R, RHO, DEFS))
  rule evalExpr(Compare(L, CmpOp(OP, R)), RHO, DEFS)
    => evalCompare(OP, evalExpr(L, RHO, DEFS), evalExpr(R, RHO, DEFS))
  rule evalExpr(Call(Name("len"), E), RHO, DEFS)
    => evalLen(evalExpr(E, RHO, DEFS))
  rule evalExpr(Call(Attribute(E, "bit_count"), .Exprs), RHO, DEFS)
    => evalBitCount(evalExpr(E, RHO, DEFS))
  rule evalExpr(Call(Name(F), ES), RHO, DEFS)
    => evalCall(F, evalArgs(ES, RHO, DEFS), DEFS)
    requires F =/=String "len"
  rule evalExpr(ListExpr(ES), RHO, DEFS)
    => listV(evalListItems(ES, RHO, DEFS))
  rule evalExpr(Subscript(E, I:Expr), RHO, DEFS)
    => evalIndex(evalExpr(E, RHO, DEFS), evalExpr(I, RHO, DEFS))
  rule evalExpr(Subscript(E, Slice(Int(1), NoBound, NoBound)), RHO, DEFS)
    => evalTail(evalExpr(E, RHO, DEFS))

  rule evalArgs(.Exprs, RHO, DEFS) => .Vals
  rule evalArgs(E, ES, RHO, DEFS)
    => evalExpr(E, RHO, DEFS) ; evalArgs(ES, RHO, DEFS)

  rule evalListItems(.Exprs, RHO, DEFS) => .Ints
  rule evalListItems(E, ES, RHO, DEFS)
    => intOf(evalExpr(E, RHO, DEFS)) :: evalListItems(ES, RHO, DEFS)

  rule intOf(intV(I)) => I

  rule evalUnary("-", intV(I)) => intV(0 -Int I)

  rule evalBin("+", intV(I), intV(J)) => intV(I +Int J)
  rule evalBin("+", listV(IS), listV(JS)) => listV(appendInts(IS, JS))
  rule evalBin("%", intV(I), intV(J)) => intV(I %Int J)
    requires J =/=Int 0
  rule evalBin("//", intV(I), intV(J)) => intV(I /Int J)
    requires J =/=Int 0

  rule evalCompare("==", intV(I), intV(J)) => boolV(I ==Int J)
  rule evalCompare("==", listV(.Ints), listV(.Ints)) => boolV(true)
  rule evalCompare("==", listV(I :: IS), listV(.Ints)) => boolV(false)
  rule evalCompare("==", listV(.Ints), listV(J :: JS)) => boolV(false)
  rule evalCompare("<", intV(I), intV(J)) => boolV(I <Int J)
  rule evalCompare("<=", intV(I), intV(J)) => boolV(I <=Int J)

  rule evalBoolBin("and", boolV(B1), boolV(B2)) => boolV(B1 andBool B2)
  rule evalBoolBin("or", boolV(B1), boolV(B2)) => boolV(B1 orBool B2)

  rule evalBitCount(intV(I)) => intV(bitCount(I))
  rule bitCount(N) => bitCount(0 -Int N) requires N <Int 0
  rule bitCount(0) => 0
  rule bitCount(N) => (N %Int 2) +Int bitCount(N /Int 2)
    requires N >Int 0

  rule evalLen(listV(IS)) => intV(lengthInts(IS))
  rule lengthInts(.Ints) => 0
  rule lengthInts(I :: IS) => 1 +Int lengthInts(IS)

  rule evalIndex(listV(I :: IS), intV(0)) => intV(I)
  rule evalTail(listV(I :: IS)) => listV(IS)

  rule appendInts(.Ints, JS) => JS
  rule appendInts(I :: IS, JS) => I :: appendInts(IS, JS)
endmodule
