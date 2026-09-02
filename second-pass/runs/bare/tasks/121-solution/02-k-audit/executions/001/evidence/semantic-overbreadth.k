requires "/tmp/audit-work/candidate-src/verification.k"

module SEMANTIC-OVERBREADTH
  imports VERIFICATION

  // K's modInt is Euclidean: this closes as intVal(1).
  // CPython evaluates 1 % -2 to -1. The submitted solution always divides by
  // positive 2, so this witnesses an off-program over-broad rule, not a false
  // result for any submitted-program list input.
  claim [negative-divisor]:
    <k> eval(BinOp("%", Int(1), Int(-2)), emptyEnv)
      => intVal(1) </k>
endmodule
