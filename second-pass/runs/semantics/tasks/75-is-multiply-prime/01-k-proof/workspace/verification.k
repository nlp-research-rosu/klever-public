requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The Module term below is the exact program generated in solution.mpy.
  // #forgetEntryPoint removes only the module binding installed by #loadAll,
  // restoring the initial proof state between exhaustive checkpoints.
  syntax KItem ::= #runIsMultiplyPrime(Int)
                 | "#forgetEntryPoint"
                 | #expect(Bool)

  // A concrete result can pass its checkpoint only when it is the expected
  // Boolean. A wrong result leaves the proof configuration stuck.
  rule <k> B:Bool ~> #expect(B) => .K ... </k>

  rule <k> #runIsMultiplyPrime(A:Int)
        => #loadAll(
             Module(
               FuncDef(
                 "is_multiply_prime",
                 Params("a"),
                 Expr(
                   Str(
                     "Return whether a has exactly three prime factors, with multiplicity."))
                 Assign(Name("factor_count"), Int(0))
                 Assign(Name("factor"), Int(2))
                 While(
                   Compare(
                     BinOp("*", Name("factor"), Name("factor")),
                     CmpOp("<=", Name("a"))),
                   If(
                     Compare(
                       BinOp("%", Name("a"), Name("factor")),
                       CmpOp("==", Int(0))),
                     AugAssign(Name("factor_count"), "+", Int(1))
                     AugAssign(Name("a"), "//", Name("factor")),
                     AugAssign(Name("factor"), "+", Int(1))))
                 If(
                   Compare(Name("a"), CmpOp(">", Int(1))),
                   AugAssign(Name("factor_count"), "+", Int(1)),
                   .Stmts)
                 Return(
                   Compare(
                     Name("factor_count"),
                     CmpOp("==", Int(3)))))))
           ~> Call(Name("is_multiply_prime"), Int(A))
           ~> #forgetEntryPoint ... </k>

  rule <k> B:Bool ~> #forgetEntryPoint => B ... </k>
       <scopes>
         ... 0 |-> scope(
           M:Map => M [ "is_multiply_prime" <- undef ],
           parent(-1))
         ...
       </scopes>
    requires "is_multiply_prime" in_keys(M)
endmodule
