requires "verification.k"

module SPEC
  imports VERIFICATION

  // The generated solution.mpy term appears literally in each claim.  The
  // two claims partition precisely the prompt's positive-integer domain.
  claim [positive-n-one]:
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
      <result> noResult => result(qualifyingCount(1)) </result>
    </mpy>

  claim [positive-n-gt-one]:
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
        ~> entry("starts_one_ends", N)
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
      <env> .Map => "n" |-> N </env>
      <control> normal </control>
      <result> noResult => result(qualifyingCount(N)) </result>
    </mpy>
    requires N >Int 1
endmodule
