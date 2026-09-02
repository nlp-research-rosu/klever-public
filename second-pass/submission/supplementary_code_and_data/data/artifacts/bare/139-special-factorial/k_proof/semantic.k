requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= List{Stmt, ""} [symbol(Stmts)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")"                         [symbol(Return)]
                | "If" "(" Expr "," Stmts "," Stmts ")"      [symbol(If)]
                | "Assign" "(" Expr "," Expr ")"               [symbol(Assign)]

  syntax Params ::= "Params" "(" String ")" [symbol(Params)]

  syntax Expr ::= "Int" "(" Int ")"                            [symbol(IntExpr)]
                | "Name" "(" String ")"                        [symbol(Name)]
                | "BinOp" "(" String "," Expr "," Expr ")"   [symbol(BinOp)]
                | "Compare" "(" Expr "," CmpOp ")"            [symbol(Compare)]
                | "Call" "(" Expr "," Expr ")"                [symbol(Call)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax Function ::= "function" "(" String "," Stmts ")" [symbol(function)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports MPY-VERIFICATION
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Result ::= "noResult" | "result" "(" Int ")" [symbol(result)]
  syntax Frame ::= "frame" "(" String "," Map "," K ")" [symbol(frame)]
  syntax CallStack ::= ".CallStack"
                     | "push" "(" Frame "," CallStack ")" [symbol(push)]

  syntax KItem ::= "init" "(" Pgm "," Int ")"              [symbol(init)]
                 | "load" "(" Stmts ")"                    [symbol(load)]
                 | "start" "(" Int ")"                     [symbol(start)]
                 | "eval" "(" Expr ")"                     [symbol(eval)]
                 | "exec" "(" Stmts ")"                    [symbol(exec)]
                 | "execStmt" "(" Stmt ")"                 [symbol(execStmt)]
                 | "binLeft" "(" String "," Expr ")"       [symbol(binLeft)]
                 | "binRight" "(" String "," Int ")"       [symbol(binRight)]
                 | "cmpLeft" "(" String "," Expr ")"       [symbol(cmpLeft)]
                 | "cmpRight" "(" String "," Int ")"       [symbol(cmpRight)]
                 | "branch" "(" Stmts "," Stmts ")"        [symbol(branch)]
                 | "enter" "(" String ")"                  [symbol(enter)]
                 | "assign" "(" String ")"                 [symbol(assign)]
                 | "continueInt" "(" Int "," K ")"         [symbol(continueInt)]
                 | "continueBool" "(" Bool "," K ")"       [symbol(continueBool)]
                 | "returned" "(" String "," Int "," K ")" [symbol(returned)]
                 | "returning"                               [symbol(returning)]
                 | "finish"                                  [symbol(finish)]

  configuration
    <mpy>
      <k> init($PGM:Pgm, $N:Int) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <stack> .CallStack </stack>
      <result> noResult </result>
    </mpy>

  rule <k> init(Module(SS), N) => load(SS) ~> start(N) ... </k>

  rule <k> load(.Stmts) => . ... </k>
  rule <k> load(FuncDef(F, Params(P), BODY) REST)
        => load(REST) ... </k>
       <functions> FUNS => FUNS [ F <- function(P, BODY) ] </functions>

  rule <k> start(N)
        => eval(Call(Name("special_factorial"), Int(N))) ~> finish ... </k>

  rule <k> exec(.Stmts) => . ... </k>
  rule <k> exec(S REST) => execStmt(S) ~> exec(REST) ... </k>

  rule <k> execStmt(If(E, THEN, ELSE)) => eval(E) ~> branch(THEN, ELSE) ... </k>
  rule <k> continueBool(B, branch(THEN, _ELSE) ~> KONT)
        => exec(THEN) ~> KONT </k>
    requires B
  rule <k> continueBool(B, branch(_THEN, ELSE) ~> KONT)
        => exec(ELSE) ~> KONT </k>
    requires notBool B

  rule <k> execStmt(Return(E)) => eval(E) ~> returning ... </k>
  rule <k> execStmt(Assign(Name(X), E)) => eval(E) ~> assign(X) ... </k>
  rule <k> continueInt(V, assign(X) ~> KONT) => KONT </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> eval(Int(I)) ~> KONT:K => continueInt(I, KONT) </k>
  rule <k> eval(Name(X)) ~> KONT:K => continueInt(I, KONT) </k>
       <env>... X |-> I:Int ...</env>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binLeft(OP, RIGHT) ... </k>
  rule <k> continueInt(I, binLeft(OP, RIGHT) ~> KONT)
        => eval(RIGHT) ~> binRight(OP, I) ~> KONT </k>
  rule <k> continueInt(J, binRight("*", I) ~> KONT)
        => continueInt(I *Int J, KONT) </k>
  rule <k> continueInt(J, binRight("-", I) ~> KONT)
        => continueInt(I -Int J, KONT) </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> cmpLeft(OP, RIGHT) ... </k>
  rule <k> continueInt(I, cmpLeft("<=", RIGHT) ~> KONT)
        => eval(RIGHT) ~> cmpRight("<=", I) ~> KONT </k>
  rule <k> continueInt(J, cmpRight("<=", I) ~> KONT)
        => continueBool(I <=Int J, KONT) </k>

  rule <k> eval(Call(Name(F), ARG)) => eval(ARG) ~> enter(F) ... </k>
  rule <k> continueInt(V, enter(F) ~> KONT) => exec(BODY) </k>
       <functions>... F |-> function(P, BODY) ...</functions>
       <env> ENV => P |-> V </env>
       <stack> STACK => push(frame(F, ENV, KONT), STACK) </stack>

  rule <k> continueInt(V, returning ~> _REST:K) => returned(F, V, KONT) </k>
       <env> _ => ENV </env>
       <stack> push(frame(F, ENV, KONT), STACK) => STACK </stack>

  rule <k> returned(_F, V, KONT) => continueInt(V, KONT) </k>

  rule <k> continueInt(V, finish) => .K </k>
       <result> noResult => result(V) </result>
endmodule
