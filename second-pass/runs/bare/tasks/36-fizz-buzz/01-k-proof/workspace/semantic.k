requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" String ")" "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "BoolOp" "(" String "," Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  configuration
    <fizz>
      <k> $PGM:Program </k>
      <input> $N:Int </input>
      <env> .Map </env>
      <result> 0 </result>
    </fizz>

  syntax KItem ::= assignTo(String)
                 | binLeft(String, Expr)
                 | binRight(String, Int)
                 | compareLeft(String, Expr)
                 | compareRight(String, Int)
                 | orElse(Expr)
                 | ifThenElse(Stmts, Stmts)
                 | whileBody(Expr, Stmts)
                 | "returnValue"

  // Loading the translated module invokes its required entry point with the
  // integer supplied in <input>.  Function-body execution below is ordinary
  // small-step execution over the translated AST.
  rule <k> Module(FuncDef("fizz_buzz", Params("n"), BODY)) => BODY </k>
       <input> N </input>
       <env> .Map => "n" |-> N "count" |-> 0 "i" |-> 0 "x" |-> 0 </env>

  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> Name(X) => Int(I) ... </k>
       <env> ... X |-> I ... </env>

  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ... </k>
  rule <k> Int(I) ~> assignTo(X) => .K ... </k>
       <env> ... X |-> (_ => I) ... </env>

  rule <k> BinOp(OP, L, R) => L ~> binLeft(OP, R) ... </k>
  rule <k> Int(A) ~> binLeft(OP, R) => R ~> binRight(OP, A) ... </k>
  rule <k> Int(B) ~> binRight("+", A) => Int(A +Int B) ... </k>
  rule <k> Int(B) ~> binRight("%", A) => Int(A %Int B) ... </k>
    requires B =/=Int 0
  rule <k> Int(B) ~> binRight("//", A) => Int(A /Int B) ... </k>
    requires B =/=Int 0

  rule <k> Compare(L, CmpOp(OP, R)) => L ~> compareLeft(OP, R) ... </k>
  rule <k> Int(A) ~> compareLeft(OP, R) => R ~> compareRight(OP, A) ... </k>
  rule <k> Int(B) ~> compareRight("<", A) => Bool(A <Int B) ... </k>
  rule <k> Int(B) ~> compareRight(">", A) => Bool(A >Int B) ... </k>
  rule <k> Int(B) ~> compareRight("==", A) => Bool(A ==Int B) ... </k>

  rule <k> BoolOp("or", L, R) => L ~> orElse(R) ... </k>
  rule <k> Bool(true) ~> orElse(_) => Bool(true) ... </k>
  rule <k> Bool(false) ~> orElse(R) => R ... </k>

  rule <k> If(E, THEN, ELSE) => E ~> ifThenElse(THEN, ELSE) ... </k>
  rule <k> Bool(true) ~> ifThenElse(THEN, _) => THEN ... </k>
  rule <k> Bool(false) ~> ifThenElse(_, ELSE) => ELSE ... </k>

  rule <k> While(E, BODY) => E ~> whileBody(E, BODY) ... </k>
  rule <k> Bool(true) ~> whileBody(E, BODY) => BODY ~> While(E, BODY) ... </k>
  rule <k> Bool(false) ~> whileBody(_, _) => .K ... </k>

  rule <k> Return(E) => E ~> returnValue ... </k>
  rule <k> Int(I) ~> returnValue ~> _REST:K => .K </k>
       <result> _ => I </result>
endmodule
