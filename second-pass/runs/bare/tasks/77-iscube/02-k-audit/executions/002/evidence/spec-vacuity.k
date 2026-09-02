requires "verification.k"

module SPEC-VACUITY
  imports GAP-VERIFICATION

  // Input 2 satisfies N=1, D=1 in the positive-noncube partition.
  // The real result is false, so requiring true is a meaningful contradiction.
  claim [false-result-for-two]:
    <k>
      iscubeProgram ~> invoke(IntVal(2)) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(true) ~> .K </result>
endmodule
