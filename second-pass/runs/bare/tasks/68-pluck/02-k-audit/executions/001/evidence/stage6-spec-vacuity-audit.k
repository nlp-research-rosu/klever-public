requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh result mutation: [2] satisfies LENGTH >= 0 but the real result is
  // [2, 0], so universally requiring [] is deliberately false.
  claim
    <py>
      <k> solutionProgram ~> start => .K </k>
      <args> VArray(ID, 0, LENGTH) </args>
      <env> .Map => .Map </env>
      <funs> .Map => solutionFunctions </funs>
      <stack> .List => .List </stack>
      <result> VNone => VList(.Ints) </result>
    </py>
    requires LENGTH >=Int 0
endmodule
