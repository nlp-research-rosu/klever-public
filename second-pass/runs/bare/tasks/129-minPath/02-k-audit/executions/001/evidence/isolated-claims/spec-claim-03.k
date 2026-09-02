requires "../verification.k"

module MINPATH-SPEC-03
  imports MINPATH-VERIFICATION

  claim
    <k> solutionProgram ~> start(grid3(5, 9, 3, 4, 1, 6, 7, 8, 2), 6)
      => .K </k>
    <result> none => some(path6(4)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>

  // Symbolic 2x2 coverage.  The range, disequality, and ordering constraints
  // make A/B/C a permutation of 2,3,4.  For every location of 1, the two
  // claims cover both possible orders of its two neighbors.
endmodule
