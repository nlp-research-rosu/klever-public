requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmt ")" [symbol(module)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                  [symbol(funcDef)]
                | "Return" "(" Expr ")" [symbol(returnStmt)]

  syntax Params ::= "Params" "(" String ")" [symbol(params)]

  syntax Expr ::= "Name" "(" String ")" [symbol(name)]
                | "Int" "(" Int ")" [symbol(intExpr)]
                | "BinOp" "(" String "," Expr "," Expr ")"
                  [symbol(binOp)]
                | "BoolOp" "(" String "," Expr "," Expr ")"
                  [symbol(boolOp)]
                | "Compare" "(" Expr "," CmpOp ")"
                  [symbol(compare)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOp)]

  syntax Value ::= IntValue(Int) | BoolValue(Bool)
  syntax Result ::= "noResult" | Value
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <input> $N:Int </input>
      <result> noResult </result>
    </mpy>

  // The submitted module contains the requested entry point.  Loading the
  // module invokes that entry point with the integer in <input>.
  rule <k> Module(FuncDef("is_equal_to_sum_even", Params(X), Return(E)))
         => .K
       </k>
       <input> N </input>
       <result> noResult => eval(E, X, N) </result>

  syntax Value ::= eval(Expr, String, Int) [function]
                 | evalBin(String, Value, Value) [function]
                 | evalCompare(Value, String, Value) [function]
                 | evalBool(String, Value, Value) [function]

  rule eval(Name(X), X, N) => IntValue(N)
  rule eval(Int(I), _, _) => IntValue(I)

  rule eval(BinOp(OP, L, R), X, N)
    => evalBin(OP, eval(L, X, N), eval(R, X, N))
  rule evalBin("%", IntValue(I), IntValue(J)) => IntValue(I %Int J)
    requires J =/=Int 0

  rule eval(Compare(L, CmpOp(OP, R)), X, N)
    => evalCompare(eval(L, X, N), OP, eval(R, X, N))
  rule evalCompare(IntValue(I), ">=", IntValue(J))
    => BoolValue(I >=Int J)
  rule evalCompare(IntValue(I), "==", IntValue(J))
    => BoolValue(I ==Int J)

  rule eval(BoolOp(OP, L, R), X, N)
    => evalBool(OP, eval(L, X, N), eval(R, X, N))
  rule evalBool("and", BoolValue(B1), BoolValue(B2))
    => BoolValue(B1 andBool B2)
endmodule
