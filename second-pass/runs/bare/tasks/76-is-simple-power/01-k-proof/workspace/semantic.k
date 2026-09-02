module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Ids   ::= List{String, ","}

  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" Ids ")" "," Stmts ")"
                | "If" "(" Exp "," Stmts "," Stmts ")"
                | "While" "(" Exp "," Stmts ")"
                | "Assign" "(" Exp "," Exp ")"
                | "Return" "(" Exp ")"

  syntax Exp ::= "Int" "(" Int ")"
               | "Bool" "(" Bool ")"
               | "Name" "(" String ")"
               | "BinOp" "(" String "," Exp "," Exp ")"
               | "Compare" "(" Exp "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Exp ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Value ::= Int | Bool
  syntax Result ::= "noResult" | Value

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <env> .Map </env>
      <result> noResult </result>
      <x> $X:Int </x>
      <n> $N:Int </n>
    </mpy>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Exp ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "loop" "(" Exp "," Stmts ")"
                 | "assignTo" "(" String ")"
                 | "returnValue"
                 | "binRight" "(" String "," Exp ")"
                 | "binApply" "(" String "," Value ")"
                 | "cmpRight" "(" String "," Exp ")"
                 | "cmpApply" "(" String "," Value ")"

  rule <k> Module(FuncDef("is_simple_power", Params("x", "n"), BODY))
        => exec(BODY) </k>
       <env> .Map => ("x" |-> X) ("n" |-> N) </env>
       <x> X </x>
       <n> N </n>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> If(E, THEN, ELSE) => eval(E) ~> choose(THEN, ELSE) ... </k>
  rule <k> true  ~> choose(THEN, _) => exec(THEN) ... </k>
  rule <k> false ~> choose(_, ELSE) => exec(ELSE) ... </k>

  rule <k> While(E, BODY) => eval(E) ~> loop(E, BODY) ... </k>
  rule <k> true  ~> loop(E, BODY) => exec(BODY) ~> While(E, BODY) ... </k>
  rule <k> false ~> loop(_, _) => .K ... </k>

  rule <k> Assign(Name(NAME), E) => eval(E) ~> assignTo(NAME) ... </k>
  rule <k> V:Value ~> assignTo(NAME) => .K ... </k>
       <env> RHO => RHO [ NAME <- V ] </env>

  rule <k> Return(E) => eval(E) ~> returnValue ... </k>
  rule <k> V:Value ~> returnValue ~> _REST:K => .K </k>
       <result> noResult => V </result>

  rule <k> eval(Int(I)) => I ... </k>
  rule <k> eval(Bool(B)) => B ... </k>
  rule <k> eval(Name(NAME)) => V ... </k>
       <env> ... NAME |-> V:Value ... </env>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binRight(OP, RIGHT) ... </k>
  rule <k> LEFT:Value ~> binRight(OP, RIGHT)
        => eval(RIGHT) ~> binApply(OP, LEFT) ... </k>
  rule <k> RIGHT:Int ~> binApply("*", LEFT:Int)
        => LEFT *Int RIGHT ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> cmpRight(OP, RIGHT) ... </k>
  rule <k> LEFT:Value ~> cmpRight(OP, RIGHT)
        => eval(RIGHT) ~> cmpApply(OP, LEFT) ... </k>
  rule <k> RIGHT:Int ~> cmpApply("==", LEFT:Int)
        => LEFT ==Int RIGHT ... </k>
  rule <k> RIGHT:Int ~> cmpApply("<", LEFT:Int)
        => LEFT <Int RIGHT ... </k>
endmodule
