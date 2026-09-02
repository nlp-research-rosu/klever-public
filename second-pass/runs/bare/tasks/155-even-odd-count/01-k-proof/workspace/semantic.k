module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "TupleExpr" "(" Exprs ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP
  imports K-EQUAL

  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "pairVal" "(" Val "," Val ")"
               | "noResult"

  syntax Val ::= eval(Expr, Map) [function]
               | envGet(Map, String) [function]
               | negVal(Val) [function]
               | addVal(Val, Val) [function]
               | modVal(Val, Val) [function]
               | divVal(Val, Val) [function]
               | ltVal(Val, Val) [function]
               | gtVal(Val, Val) [function]
               | eqVal(Val, Val) [function]
  syntax KItem ::= exec(Stmts)
                 | loop(Expr, Stmts)

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <env> .Map </env>
      <input> $NUM:Int </input>
      <result> noResult </result>
    </mpy>

  rule envGet((X |-> V:Val) _REST, X) => V

  rule eval(Int(I), _) => intVal(I)
  rule eval(Name(X), ENV) => envGet(ENV, X)
  rule eval(UnaryOp("-", E), ENV) => negVal(eval(E, ENV))
  rule eval(BinOp("+", E1, E2), ENV) => addVal(eval(E1, ENV), eval(E2, ENV))
  rule eval(BinOp("%", E1, E2), ENV) => modVal(eval(E1, ENV), eval(E2, ENV))
  rule eval(BinOp("//", E1, E2), ENV) => divVal(eval(E1, ENV), eval(E2, ENV))
  rule eval(Compare(E, CmpOp("<", E2)), ENV) => ltVal(eval(E, ENV), eval(E2, ENV))
  rule eval(Compare(E, CmpOp(">", E2)), ENV) => gtVal(eval(E, ENV), eval(E2, ENV))
  rule eval(Compare(E, CmpOp("==", E2)), ENV) => eqVal(eval(E, ENV), eval(E2, ENV))
  rule eval(TupleExpr(E1, E2), ENV) => pairVal(eval(E1, ENV), eval(E2, ENV))

  rule negVal(intVal(I)) => intVal(0 -Int I)
  rule addVal(intVal(I1), intVal(I2)) => intVal(I1 +Int I2)
  rule modVal(intVal(I1), intVal(I2)) => intVal(I1 %Int I2)
  rule divVal(intVal(I1), intVal(I2)) => intVal(I1 /Int I2)
  rule ltVal(intVal(I1), intVal(I2)) => boolVal(I1 <Int I2)
  rule gtVal(intVal(I1), intVal(I2)) => boolVal(I1 >Int I2)
  rule eqVal(intVal(I1), intVal(I2)) => boolVal(I1 ==Int I2)

  rule <k> Module(FuncDef("even_odd_count", Params("num"), BODY)) => exec(BODY) ... </k>
       <env> .Map => ("num" |-> intVal(N)
                      "even" |-> intVal(0)
                      "odd" |-> intVal(0)) </env>
       <input> N </input>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec((S:Stmt REST:Stmts)) => S ~> exec(REST) ... </k>

  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>

  rule <k> AugAssign(Name(X), "+", E) => .K ... </k>
       <env> ENV => ENV [ X <- addVal(envGet(ENV, X), eval(E, ENV)) ] </env>

  rule <k> If(E, THEN, _) => exec(THEN) ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K boolVal(true)
  rule <k> If(E, _, ELSE) => exec(ELSE) ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K boolVal(false)

  rule <k> While(E, BODY) => loop(E, BODY) ... </k>
  rule <k> loop(E, BODY) => exec(BODY) ~> loop(E, BODY) ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K boolVal(true)
  rule <k> loop(E, _) => .K ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K boolVal(false)

  rule <k> Return(E) ~> _REST => .K </k>
       <env> ENV </env>
       <result> noResult => eval(E, ENV) </result>
endmodule
