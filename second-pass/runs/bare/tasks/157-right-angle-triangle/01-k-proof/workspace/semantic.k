module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The source constructors emitted by py2mpy.py for this program.
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "BoolOp" "(" String "," Exprs ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Exprs ::= List{Expr, ","}

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Program ::= "Module" "(" Stmts ")"

  syntax Ints ::= List{Int, ","}
  syntax Arguments ::= "Args" "(" Ints ")"
  syntax Input ::= Program
                 | "run" "(" Program "," String "," Arguments ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports DOMAINS
  imports MAP

  syntax Value ::= "iVal" "(" Int ")" | "bVal" "(" Bool ")"
  syntax Result ::= "noResult" | "result" "(" Bool ")"

  syntax KItem ::= "bind" "(" Strings "," Ints ")"
                 | "eval" "(" Expr ")"
                 | "binRight" "(" String "," Expr ")"
                 | "binApply" "(" String "," Int ")"
                 | "cmpRight" "(" String "," Expr ")"
                 | "cmpApply" "(" String "," Int ")"
                 | "boolTail" "(" String "," Exprs ")"
                 | "boolMerge" "(" String "," Bool "," Exprs ")"
                 | "publish"

  configuration
    <mpy>
      <k> $PGM:Input </k>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // A HumanEval file is a module containing one target definition. Reusing F
  // in both positions enforces that the requested entry point is that target.
  rule <k>
         run(Module(FuncDef(F, Params(PS), Return(E))), F, Args(IS))
         => bind(PS, IS) ~> eval(E) ~> publish
       </k>

  rule <k> bind(.Strings, .Ints) => .K ... </k>
  rule <k> bind((P, PS), (I, IS)) => bind(PS, IS) ... </k>
       <env> R => R [ P <- I ] </env>

  rule <k> eval(Int(I)) => iVal(I) ... </k>
  rule <k> eval(Name(X)) => iVal(I) ... </k>
       <env> ... X |-> I:Int ... </env>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binRight(OP, R) ... </k>
  rule <k> iVal(I) ~> binRight(OP, R) => eval(R) ~> binApply(OP, I) ... </k>
  rule <k> iVal(J) ~> binApply("+", I) => iVal(I +Int J) ... </k>
  rule <k> iVal(J) ~> binApply("*", I) => iVal(I *Int J) ... </k>

  rule <k> eval(Compare(L, CmpOp(OP, R)))
           => eval(L) ~> cmpRight(OP, R) ...
       </k>
  rule <k> iVal(I) ~> cmpRight(OP, R) => eval(R) ~> cmpApply(OP, I) ... </k>
  rule <k> iVal(J) ~> cmpApply(">", I) => bVal(I >Int J) ... </k>
  rule <k> iVal(J) ~> cmpApply("==", I) => bVal(I ==Int J) ... </k>

  // All operands in the translated program are booleans. Evaluating the full
  // list is observationally equivalent to Python short-circuiting here because
  // the expression language is pure.
  rule <k> eval(BoolOp(OP, E, ES)) => eval(E) ~> boolTail(OP, ES) ... </k>
  rule <k> bVal(B) ~> boolTail(_OP, .Exprs) => bVal(B) ... </k>
  rule <k> bVal(B) ~> boolTail(OP, E, ES)
           => eval(E) ~> boolMerge(OP, B, ES) ...
       </k>
  rule <k> bVal(C) ~> boolMerge("and", B, ES)
           => bVal(B andBool C) ~> boolTail("and", ES) ...
       </k>
  rule <k> bVal(C) ~> boolMerge("or", B, ES)
           => bVal(B orBool C) ~> boolTail("or", ES) ...
       </k>

  rule <k> bVal(B) ~> publish => .K </k>
       <env> _ => .Map </env>
       <result> noResult => result(B) </result>
endmodule
