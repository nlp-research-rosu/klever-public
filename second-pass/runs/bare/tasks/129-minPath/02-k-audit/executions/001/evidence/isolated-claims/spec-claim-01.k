requires "../verification.k"

module MINPATH-SPEC-01
  imports MINPATH-VERIFICATION

  claim
    <k> solutionProgram ~> start(grid3(1, 2, 3, 4, 5, 6, 7, 8, 9), 3)
      => .K </k>
    <result> none => some(path3(2)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
endmodule
