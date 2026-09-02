requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" FuncDef ")"
  syntax FuncDef ::= "FuncDef" "(" String "," Params "," Stmt ")"
  syntax Params ::= "Params" "(" String ")"

  syntax Stmt ::= "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "TupleExpr" "(" NeExprs ")"
  syntax NeExprs ::= Expr
                   | Expr "," NeExprs
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports STRING

  syntax Value ::= VInt(Int)
                 | VStr(String)
                 | VTuple(VList)
  syntax VList ::= "VNil"
                 | VCons(Value, VList)

  syntax Value ::= evalExpr(Expr, String, Int) [function]
                 | nthValue(VList, Int) [function]
                 | evalNthExpr(NeExprs, Int, String, Int) [function]
  syntax VList ::= evalExprs(NeExprs, String, Int) [function]
  syntax Int ::= getInt(Value) [function]

  rule evalExpr(Name(X), X, N) => VInt(N)
  rule evalExpr(Int(I), _, _) => VInt(I)
  rule evalExpr(Str(S), _, _) => VStr(S)

  rule evalExpr(BinOp("+", E1, E2), X, N)
    => VInt(getInt(evalExpr(E1, X, N)) +Int getInt(evalExpr(E2, X, N)))
  rule evalExpr(BinOp("//", E1, E2), X, N)
    => VInt(getInt(evalExpr(E1, X, N)) /Int getInt(evalExpr(E2, X, N)))
  rule evalExpr(BinOp("%", E1, E2), X, N)
    => VInt(getInt(evalExpr(E1, X, N)) %Int getInt(evalExpr(E2, X, N)))

  rule evalExpr(TupleExpr(ES), X, N) => VTuple(evalExprs(ES, X, N))
  rule evalExpr(Subscript(TupleExpr(ES), E2), X, N)
    => evalNthExpr(ES, getInt(evalExpr(E2, X, N)), X, N)

  syntax VList ::= tupleItems(Value) [function]
  rule tupleItems(VTuple(VS)) => VS
  rule getInt(VInt(I)) => I

  rule evalExprs(E:Expr, X, N) => VCons(evalExpr(E, X, N), VNil)
  rule evalExprs((E:Expr, ES:NeExprs), X, N)
    => VCons(evalExpr(E, X, N), evalExprs(ES, X, N))

  rule evalNthExpr(E:Expr, 0, X, N) => evalExpr(E, X, N)
  rule evalNthExpr((E:Expr, _), 0, X, N) => evalExpr(E, X, N)
  rule evalNthExpr((_:Expr, ES:NeExprs), I, X, N)
    => evalNthExpr(ES, I -Int 1, X, N)
    requires I >Int 0

  rule nthValue(VCons(V, _), 0) => V
  rule nthValue(VCons(_, VS), I) => nthValue(VS, I -Int 1)
    requires I >Int 0

  syntax Value ::= runProgram(Pgm, Int) [function]
  rule runProgram(
         Module(FuncDef("solve", Params(X), Return(E))),
         N)
    => evalExpr(E, X, N)

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <input> $N:Int </input>
      <result> .K </result>
    </mpy>

  rule <k> P:Pgm => .K </k>
       <input> N </input>
       <result> .K => runProgram(P, N) </result>
endmodule

module SEMANTIC
  imports MPY-SEMANTIC
  imports VERIFICATION
endmodule
