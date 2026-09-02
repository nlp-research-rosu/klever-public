requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // Concrete syntax emitted by py2mpy.py for the program subset used here.
  syntax Program ::= "Module" "(" Function ")" [symbol(Module)]
  syntax Function ::= "FuncDef" "(" String "," "Params" "(" String ")" "," Statement ")" [symbol(FuncDef)]
  syntax Statement ::= "Return" "(" Expr ")" [symbol(Return)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(IntLiteral)]
                | "Name" "(" String ")" [symbol(Name)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING

  syntax KItem ::= "invoke" "(" String "," Int ")" [symbol(invoke)]
                 | "noResult" [symbol(noResult)]

  syntax Int ::= "evalExpr" "(" Expr "," String "," Int ")" [function]

  // Expression semantics.  The last two arguments model the single local
  // parameter binding needed by this translated function.
  rule evalExpr(Int(I), _P, _V) => I
  rule evalExpr(Name(P), P, V) => V
  rule evalExpr(BinOp("+", L, R), P, V)
    => evalExpr(L, P, V) +Int evalExpr(R, P, V)
  rule evalExpr(BinOp("*", L, R), P, V)
    => evalExpr(L, P, V) *Int evalExpr(R, P, V)
  rule evalExpr(BinOp("//", L, R), P, V)
    => evalExpr(L, P, V) /Int evalExpr(R, P, V)

  configuration
    <mpy>
      <k> $PGM:Program ~> invoke($FUNCTION:String, $ARG:Int) </k>
      <result> noResult </result>
    </mpy>

  rule <k> Module(FuncDef(F, Params(P), Return(E))) ~> invoke(F, V) => .K </k>
       <result> noResult => evalExpr(E, P, V) </result>
endmodule
