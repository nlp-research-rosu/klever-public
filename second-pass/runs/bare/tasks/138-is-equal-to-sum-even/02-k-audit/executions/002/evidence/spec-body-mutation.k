requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The executed body now uses threshold 10, but the original threshold-8
  // result obligation is retained. N = 8 is a concrete counterexample.
  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(10))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> N:Int </input>
    <result> noResult => BoolValue(sumFourPositiveEvens(N)) </result>
endmodule
