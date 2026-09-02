requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False result mutation: the real body does not return true for every Int;
  // N = 4 is a satisfying initial state and a concrete counterexample.
  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> N:Int </input>
    <result> noResult => BoolValue(true) </result>
endmodule
