requires "../verification.k"

module MINPATH-SPEC-02
  imports MINPATH-VERIFICATION

  claim
    <k> solutionProgram ~> start(grid3(5, 9, 3, 4, 1, 6, 7, 8, 2), 1)
      => .K </k>
    <result> none => some(path1(1)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>

  // The same interior placement with a longer path observes the selected
  // minimum (4) and the complete alternating construction.
endmodule
