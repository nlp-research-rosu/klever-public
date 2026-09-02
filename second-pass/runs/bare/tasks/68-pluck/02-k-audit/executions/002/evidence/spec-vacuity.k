requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-result mutation.  This is the original entry shape
  // specialized to a one-element abstract array, but it falsely requires the
  // program to return [] for every element.  The satisfying interpretation
  // arrayAt(68, 0) = 2 corresponds to Python input [2], whose result is [2, 0].
  claim
    <py>
      <k> solutionProgram ~> start => .K </k>
      <args> VArray(ID, 0, 1) </args>
      <env> .Map => .Map </env>
      <funs> .Map => solutionFunctions </funs>
      <stack> .List => .List </stack>
      <result> VNone => VList(.Ints) </result>
    </py>
endmodule
