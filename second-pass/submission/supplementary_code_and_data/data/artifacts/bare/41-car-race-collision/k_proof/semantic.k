module SEMANTIC-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmt ")"                  [symbol(Module)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                                                               [symbol(FuncDef)]
                | "Return" "(" Expr ")"                     [symbol(Return)]

  syntax Params ::= "Params" "(" String ")"                [symbol(Params)]

  syntax Expr ::= "Int" "(" Int ")"                        [symbol(Int)]
                | "Name" "(" String ")"                    [symbol(Name)]
                | "BinOp" "(" String "," Expr "," Expr ")"
                                                               [symbol(BinOp)]
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports INT
  imports MAP

  syntax KItem ::= "run" "(" String "," Int ")"           [symbol(run)]
                 | "definition" "(" String "," Stmt ")"   [symbol(definition)]
                 | "execute" "(" Stmt ")"                  [symbol(execute)]
                 | "evaluate" "(" Expr ")"                 [symbol(evaluate)]
                 | "multiplyRight" "(" Expr ")"            [symbol(multiplyRight)]
                 | "multiplyBy" "(" Int ")"                [symbol(multiplyBy)]
                 | "finishReturn"                             [symbol(finishReturn)]

  configuration
    <state>
      <k> $PGM:Pgm ~> run("car_race_collision", $N:Int) </k>
      <functions> .Map </functions>
      <environment> .Map </environment>
      <result> 0 </result>
    </state>

  rule <k> Module(FuncDef(F, Params(P), BODY)) => .K ... </k>
       <functions> .Map => F |-> definition(P, BODY) </functions>

  rule <k> run(F, I) => execute(BODY) ... </k>
       <functions>... F |-> definition(P, BODY) ...</functions>
       <environment> _ => P |-> I </environment>

  rule <k> execute(Return(E)) => evaluate(E) ~> finishReturn ... </k>

  rule <k> evaluate(Int(I)) => I ... </k>

  rule <k> evaluate(Name(X)) => I ... </k>
       <environment>... X |-> I ...</environment>

  rule <k> evaluate(BinOp("*", L, R))
        => evaluate(L) ~> multiplyRight(R) ... </k>

  rule <k> I:Int ~> multiplyRight(R)
        => evaluate(R) ~> multiplyBy(I) ... </k>

  rule <k> J:Int ~> multiplyBy(I) => I *Int J ... </k>

  rule <k> I:Int ~> finishReturn => .K ... </k>
       <result> _ => I </result>
endmodule
