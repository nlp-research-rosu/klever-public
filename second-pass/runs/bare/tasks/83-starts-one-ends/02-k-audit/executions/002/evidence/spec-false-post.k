requires "verification.k"

module SPEC-FALSE-POST
  imports VERIFICATION

  // Fresh reviewer mutation: the real n=1 program returns 1, but this
  // result-constraining postcondition deliberately requires 2.
  claim [false-post-n-one]:
    <mpy>
      <k>
        Module(
          FuncDef("starts_one_ends", Params("n"),
            Expr(
              Str(
                "\n    Given a positive integer n, return the count of the numbers of n-digit\n    positive integers that start or end with 1.\n    "))
            If(Compare(Name("n"), CmpOp("==", Int(1))),
              Return(Int(1)),
              Return(
                BinOp(
                  "*",
                  Int(18),
                  BinOp("**", Int(10), BinOp("-", Name("n"), Int(2))))))))
        ~> entry("starts_one_ends", 1)
      => .K
      </k>
      <function>
        noFunction
      => function("starts_one_ends", "n",
           Expr(
             Str(
               "\n    Given a positive integer n, return the count of the numbers of n-digit\n    positive integers that start or end with 1.\n    "))
           If(Compare(Name("n"), CmpOp("==", Int(1))),
             Return(Int(1)),
             Return(
               BinOp(
                 "*",
                 Int(18),
                 BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))))))
      </function>
      <env> .Map => "n" |-> 1 </env>
      <control> normal </control>
      <result>
        noResult
      => result(qualifyingCount(1) +Int 1)
      </result>
    </mpy>
endmodule
