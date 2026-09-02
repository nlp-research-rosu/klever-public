requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the submitted program returns true at the satisfying
  // concrete input N = 8, but this mutation demands false.
  claim [false-example-8]:
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> 8 </input>
    <result> noResult => BoolValue(false) </result>
endmodule
