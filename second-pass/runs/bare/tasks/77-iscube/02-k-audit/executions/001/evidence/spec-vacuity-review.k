requires "verification.k"

module AUDIT-VACUITY-SPEC
  imports VERIFICATION

  // False for the satisfying original witness N=1: iscube(1) returns true.
  claim [false-result-on-one]:
    <k>
      iscubeProgram ~> invoke(IntVal(1)) => .K
    </k>
    <funs> .Map => ?_ </funs>
    <env> .Map => ?_ </env>
    <result> .K => BoolVal(false) ~> .K </result>
endmodule
