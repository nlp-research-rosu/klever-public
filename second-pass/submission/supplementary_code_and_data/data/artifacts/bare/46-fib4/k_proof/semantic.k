requires "verification.k"

module SEMANTIC-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= Module(Stmts)
                   | "solutionProgram"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt  ::= FuncDef(String, Params, Stmts)
                 | Return(Exp)
                 | Assign(Exp, Exp)
                 | If(Exp, Stmts, Stmts)
                 | While(Exp, Stmts)

  syntax Params ::= Params(String)

  syntax Exp ::= Int(Int)
               | Name(String)
               | BinOp(String, Exp, Exp)
               | Compare(Exp, CmpOp)
  syntax CmpOp ::= CmpOp(String, Exp)
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports VERIFICATION
  imports MAP
  imports BOOL

  syntax Result ::= "noResult" | "result" "(" Int ")"
  syntax KItem ::= "exec" "(" Stmts ")"

  configuration
    <fib4>
      <k> $PGM:Program </k>
      <arg> $ARG:Int </arg>
      <env> .Map </env>
      <result> noResult </result>
    </fib4>

  // Exact constructor tree emitted by py2mpy.py for solution.py.  The proof
  // claims use this name; concrete krun commands consume solution.mpy itself.
  rule solutionProgram =>
    Module(
      FuncDef("fib4", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(0))),
          Return(Int(0)), .Stmts)
        If(Compare(Name("n"), CmpOp("==", Int(1))),
          Return(Int(0)), .Stmts)
        If(Compare(Name("n"), CmpOp("==", Int(2))),
          Return(Int(2)), .Stmts)
        If(Compare(Name("n"), CmpOp("==", Int(3))),
          Return(Int(0)), .Stmts)
        Assign(Name("a"), Int(0))
        Assign(Name("b"), Int(0))
        Assign(Name("c"), Int(2))
        Assign(Name("d"), Int(0))
        Assign(Name("e"), Int(0))
        Assign(Name("i"), Int(4))
        While(Compare(Name("i"), CmpOp("<=", Name("n"))),
          Assign(Name("e"),
            BinOp("+", BinOp("+", BinOp("+", Name("a"), Name("b")),
                                      Name("c")), Name("d")))
          Assign(Name("a"), Name("b"))
          Assign(Name("b"), Name("c"))
          Assign(Name("c"), Name("d"))
          Assign(Name("d"), Name("e"))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("d"))))

  // The module contains one entry point.  Loading it binds its sole argument
  // and schedules the function body.
  rule <k> Module(FuncDef(_, Params(X), BODY)) => exec(BODY) ... </k>
       <arg> N </arg>
       <env> .Map => X |-> N </env>

  rule <k> exec(.Stmts) => .K ... </k>

  rule <k> exec(Assign(Name(X), E) REST) => exec(REST) ... </k>
       <env> M => M [ X <- evalInt(E, M) ] </env>

  rule <k> exec(If(Compare(Name(X), CmpOp("==", Int(J))), THEN, _) REST)
        => exec(THEN) ~> exec(REST) ... </k>
       <env> (X |-> I) _ </env>
    requires I ==Int J
  rule <k> exec(If(Compare(Name(X), CmpOp("==", Int(J))), _, ELSE) REST)
        => exec(ELSE) ~> exec(REST) ... </k>
       <env> (X |-> I) _ </env>
    requires I =/=Int J

  rule <k> exec(While(Compare(Name(X), CmpOp("<=", Name(Y))), BODY) REST)
        => exec(BODY)
        ~> exec(While(Compare(Name(X), CmpOp("<=", Name(Y))), BODY) REST) ... </k>
       <env> (X |-> I) (Y |-> J) _ </env>
    requires I <=Int J
  rule <k> exec(While(Compare(Name(X), CmpOp("<=", Name(Y))), _) REST)
        => exec(REST) ... </k>
       <env> (X |-> I) (Y |-> J) _ </env>
    requires I >Int J

  rule <k> exec(Return(E) _REST) ~> _:K => .K </k>
       <env> M </env>
       <result> noResult => result(evalInt(E, M)) </result>

  syntax Int ::= "evalInt" "(" Exp "," Map ")" [function, total]
  rule evalInt(Int(I), _) => I
  rule evalInt(Name(X), (X |-> I) _M) => I
  rule evalInt(BinOp("+", L, R), M) => evalInt(L, M) +Int evalInt(R, M)

  syntax Bool ::= "evalBool" "(" Exp "," Map ")" [function, total]
  rule evalBool(Compare(L, CmpOp("==", R)), M)
    => evalInt(L, M) ==Int evalInt(R, M)
  rule evalBool(Compare(L, CmpOp("<=", R)), M)
    => evalInt(L, M) <=Int evalInt(R, M)
endmodule
