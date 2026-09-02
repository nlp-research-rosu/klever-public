requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Reviewer sensitivity mutation: change the executed then-branch from
  // Return(Int(1)) to Return(Int(2)), while retaining the true original
  // postcondition.  The mutation appears in both the initial Module term and
  // the expected registered function value.
  claim [changed-body-n-one]:
    <mpy>
      <k>
        Module(
          FuncDef("starts_one_ends", Params("n"),
            Expr(
              Str(
                "\n    Given a positive integer n, return the count of the numbers of n-digit\n    positive integers that start or end with 1.\n    "))
            If(Compare(Name("n"), CmpOp("==", Int(1))),
              Return(Int(2)),
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
             Return(Int(2)),
             Return(
               BinOp(
                 "*",
                 Int(18),
                 BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))))))
      </function>
      <env> .Map => "n" |-> 1 </env>
      <control> normal </control>
      <result> noResult => result(qualifyingCount(1)) </result>
    </mpy>
endmodule
