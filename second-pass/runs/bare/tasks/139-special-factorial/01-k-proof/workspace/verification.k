module MPY-VERIFICATION
  imports INT
  imports MAP
  imports MPY-SYNTAX

  syntax Int ::= "factorialSpec" "(" Int ")" [function, total, symbol(factorialSpec)]
               | "specialFactorialSpec" "(" Int ")"
                   [function, total, symbol(specialFactorialSpec)]

  rule factorialSpec(N) => 1
    requires N <=Int 1
  rule factorialSpec(N) => N *Int factorialSpec(N -Int 1)
    requires N >Int 1

  rule specialFactorialSpec(N) => 1
    requires N <=Int 1
  rule specialFactorialSpec(N)
    => factorialSpec(N) *Int specialFactorialSpec(N -Int 1)
    requires N >Int 1

  syntax Map ::= "solutionFunctions" [macro]
  rule solutionFunctions
    => ("factorial" |-> function("n",
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Int(1)),
            .Stmts)
          Assign(Name("old_n"), Name("n"))
          Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
          Return(BinOp("*", Name("old_n"),
            Call(Name("factorial"), Name("n")))))
       ("special_factorial" |-> function("n",
          If(Compare(Name("n"), CmpOp("<=", Int(1))),
            Return(Int(1)),
            .Stmts)
          Assign(Name("factorial_n"),
            Call(Name("factorial"), Name("n")))
          Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
          Return(BinOp("*", Name("factorial_n"),
            Call(Name("special_factorial"), Name("n")))))))

  syntax Pgm ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef("factorial", Params("n"),
           If(Compare(Name("n"), CmpOp("<=", Int(1))),
             Return(Int(1)),
             .Stmts)
           Assign(Name("old_n"), Name("n"))
           Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
           Return(BinOp("*", Name("old_n"),
             Call(Name("factorial"), Name("n")))))
         FuncDef("special_factorial", Params("n"),
           If(Compare(Name("n"), CmpOp("<=", Int(1))),
             Return(Int(1)),
             .Stmts)
           Assign(Name("factorial_n"),
             Call(Name("factorial"), Name("n")))
           Assign(Name("n"), BinOp("-", Name("n"), Int(1)))
           Return(BinOp("*", Name("factorial_n"),
             Call(Name("special_factorial"), Name("n"))))))
endmodule
