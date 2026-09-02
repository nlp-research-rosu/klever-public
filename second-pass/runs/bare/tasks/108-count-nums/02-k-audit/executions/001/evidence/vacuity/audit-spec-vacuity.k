requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: [11] satisfies the positive-head entry case, but the
  // program and countPositive both return 1, not 0.
  claim
    <k> solutionProgram ~> invoke(
          "count_nums", ListV(VCons(11, VNil)))
      => IntV(0) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
endmodule
