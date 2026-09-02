requires "verification.k"

module MINPATH-SPEC-VACUITY
  imports MINPATH-VERIFICATION

  // Fresh false mutation of claim 1:
  // actual [1,2,1], deliberately required [1,3,1].
  claim
    <k> solutionProgram ~> start(grid3(1, 2, 3, 4, 5, 6, 7, 8, 9), 3)
      => .K </k>
    <result> none => some(path3(3)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
endmodule
