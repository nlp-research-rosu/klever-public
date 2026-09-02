requires "verification.k"

module SPEC
  imports VERIFICATION

  // The implementation computes the contract characterization for every Int.
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
    <result> noResult => BoolValue(sumFourPositiveEvens(N)) </result>

  // Necessity: any sum of four positive evens is accepted.
  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> A:Int +Int B:Int +Int C:Int +Int D:Int </input>
    <result> noResult => BoolValue(true) </result>
  requires A >Int 0 andBool A %Int 2 ==Int 0
       andBool B >Int 0 andBool B %Int 2 ==Int 0
       andBool C >Int 0 andBool C %Int 2 ==Int 0
       andBool D >Int 0 andBool D %Int 2 ==Int 0

  // Sufficiency: these explicit witnesses establish the "exactly 4" part.
  claim
    <k> checkCanonicalWitnesses(N) => .K </k>
    <input> N:Int </input>
    <result> noResult => BoolValue(true) </result>
  requires sumFourPositiveEvens(N)

  // Prompt examples, retained as independently executable proof targets.
  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> 4 </input>
    <result> noResult => BoolValue(false) </result>

  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> 6 </input>
    <result> noResult => BoolValue(false) </result>

  claim
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(
              BoolOp("and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(BinOp("%", Name("n"), Int(2)),
                        CmpOp("==", Int(0))))))) => .K
      </k>
    <input> 8 </input>
    <result> noResult => BoolValue(true) </result>
endmodule
