module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmt ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String "," String ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports MAP

  syntax PyVal ::= "pyInt" "(" Int ")"
  syntax Function ::= "function" "(" String "," String "," Stmt ")"

  syntax KItem ::= "load" "(" Pgm ")"
                 | "invoke" "(" String "," PyVal "," PyVal ")"
                 | "bind" "(" String "," PyVal ")"
                 | "eval" "(" Expr ")"
                 | "plusLeft" "(" Expr ")"
                 | "plusRight" "(" PyVal ")"
                 | "finishReturn"

  configuration
    <mpy>
      <k> load($PGM:Pgm) ~> invoke("add", pyInt($ARG1:Int), pyInt($ARG2:Int)) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> 0 </result>
    </mpy>

  rule <k> load(Module(S)) => S ... </k>

  rule <k> FuncDef(F, Params(X, Y), BODY) => .K ... </k>
       <functions> .Map => F |-> function(X, Y, BODY) </functions>

  rule <k> invoke(F, VX, VY)
         => bind(X, VX) ~> bind(Y, VY) ~> BODY ... </k>
       <functions> F |-> function(X, Y, BODY) </functions>

  rule <k> bind(X, V) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> Return(E) => eval(E) ~> finishReturn ... </k>

  rule <k> eval(Int(I)) => pyInt(I) ... </k>

  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> eval(BinOp("+", LEFT, RIGHT))
         => eval(LEFT) ~> plusLeft(RIGHT) ... </k>

  rule <k> pyInt(I) ~> plusLeft(RIGHT)
         => eval(RIGHT) ~> plusRight(pyInt(I)) ... </k>

  rule <k> pyInt(J) ~> plusRight(pyInt(I))
         => pyInt(I +Int J) ... </k>

  rule <k> pyInt(I) ~> finishReturn => .K ... </k>
       <result> _ => I </result>
endmodule
