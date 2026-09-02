requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real empty-list result is zero, not one.
  claim [false-empty-result]:
    <k> solutionProgram ~> invoke("count_nums", ListV(VNil))
      => IntV(1) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
endmodule
