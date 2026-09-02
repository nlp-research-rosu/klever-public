requires "verification.k"

module SPEC-MODULO-FALSE
  imports VERIFICATION

  // This closes in the candidate theory but is false of Python:
  // Python evaluates -3 % 2 to 1, not -1.
  claim [python-signed-modulo-counterexample]:
    <k> Module(
          FuncDef("is_equal_to_sum_even", Params("n"),
            Return(BinOp("%", Name("n"), Int(2))))) => .K
    </k>
    <input> -3 </input>
    <result> noResult => IntValue(-1) </result>
endmodule
