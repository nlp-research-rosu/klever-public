requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
                   | "Run" "(" Program "," Expr "," Expr ")"

  // The translator prints statement sequences by juxtaposition.
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
  syntax Params ::= "Params" "(" Strings ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "IfExp" "(" Expr "," Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  configuration <k> $PGM:Program </k>

  syntax Val ::= "VInt" "(" Int ")" | "VBool" "(" Bool ")"
  syntax Env ::= "emptyEnv"
               | "bind" "(" Env "," String "," Val ")"

  syntax Val ::= "lookup" "(" Env "," String ")" [function]
  rule lookup(bind(_ENV, NAME, VALUE), NAME) => VALUE
  rule lookup(bind(ENV, BOUND, _VALUE), NAME) => lookup(ENV, NAME)
    requires BOUND =/=String NAME

  syntax Val ::= "negate" "(" Val ")" [function]
  rule negate(VInt(I)) => VInt(0 -Int I)

  syntax Val ::= "subtract" "(" Val "," Val ")" [function]
  rule subtract(VInt(I), VInt(J)) => VInt(I -Int J)

  syntax Val ::= "modulo" "(" Val "," Val ")" [function]
  rule modulo(VInt(I), VInt(J)) => VInt(I %Int J)

  syntax Val ::= "compare" "(" String "," Val "," Val ")" [function]
  rule compare(">",  VInt(I), VInt(J)) => VBool(I >Int J)
  rule compare("==", VInt(I), VInt(J)) => VBool(I ==Int J)

  syntax Bool ::= "truth" "(" Val ")" [function]
  rule truth(VBool(B)) => B

  syntax Val ::= "eval" "(" Expr "," Env ")" [function]
  rule eval(Int(I), _ENV) => VInt(I)
  rule eval(Bool(B), _ENV) => VBool(B)
  rule eval(Name(NAME), ENV) => lookup(ENV, NAME)
  rule eval(UnaryOp("-", E), ENV) => negate(eval(E, ENV))
  rule eval(BinOp("-", E1, E2), ENV)
    => subtract(eval(E1, ENV), eval(E2, ENV))
  rule eval(BinOp("%", E1, E2), ENV)
    => modulo(eval(E1, ENV), eval(E2, ENV))
  rule eval(Compare(E1, CmpOp(OP, E2)), ENV)
    => compare(OP, eval(E1, ENV), eval(E2, ENV))
  rule eval(IfExp(COND, THEN, _ELSE), ENV) => eval(THEN, ENV)
    requires truth(eval(COND, ENV))
  rule eval(IfExp(COND, _THEN, ELSE), ENV) => eval(ELSE, ENV)
    requires notBool truth(eval(COND, ENV))

  // This condition's programs contain one two-argument function whose body is
  // a return expression. Run supplies its two arguments and evaluates that
  // translated body in an environment named by the translated parameters.
  rule <k>
         Run(Module(FuncDef(_FNAME, Params(P1, P2), Return(E))), Int(X), Int(Y))
      => eval(E, bind(bind(emptyEnv, P1, VInt(X)), P2, VInt(Y)))
         ...
       </k>
endmodule
