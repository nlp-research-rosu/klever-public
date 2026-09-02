requires "verification.k"

module BODY-SENSITIVITY
  imports VERIFICATION

  // Witness for the singleton precondition represented by the first entry
  // claim. The post-state result is deliberately a concrete integer.
  claim [witness-n-one]:
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
                  Int(19),
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
                 Int(19),
                 BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))))))
      </function>
      <env> .Map => "n" |-> 1 </env>
      <control> normal </control>
      <result> noResult => result(1) </result>
    </mpy>

  // N=2 satisfies N > 1, the second entry precondition. Again the returned
  // value is grounded rather than sharing a symbolic helper with execution.
  claim [witness-n-two]:
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
                  Int(19),
                  BinOp("**", Int(10), BinOp("-", Name("n"), Int(2))))))))
        ~> entry("starts_one_ends", 2)
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
                 Int(19),
                 BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))))))
      </function>
      <env> .Map => "n" |-> 2 </env>
      <control> normal </control>
      <result> noResult => result(18) </result>
    </mpy>
endmodule
