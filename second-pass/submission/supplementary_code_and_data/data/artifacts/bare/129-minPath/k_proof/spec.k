requires "verification.k"

module MINPATH-SPEC
  imports MINPATH-VERIFICATION

  // The two examples from prompt.py.
  claim
    <k> solutionProgram ~> start(grid3(1, 2, 3, 4, 5, 6, 7, 8, 9), 3)
      => .K </k>
    <result> none => some(path3(2)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>

  claim
    <k> solutionProgram ~> start(grid3(5, 9, 3, 4, 1, 6, 7, 8, 2), 1)
      => .K </k>
    <result> none => some(path1(1)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>

  // The same interior placement with a longer path observes the selected
  // minimum (4) and the complete alternating construction.
  claim
    <k> solutionProgram ~> start(grid3(5, 9, 3, 4, 1, 6, 7, 8, 2), 6)
      => .K </k>
    <result> none => some(path6(4)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>

  // Symbolic 2x2 coverage.  The range, disequality, and ordering constraints
  // make A/B/C a permutation of 2,3,4.  For every location of 1, the two
  // claims cover both possible orders of its two neighbors.
  claim
    <k> solutionProgram ~> start(grid2(1, A, B, C), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B

  claim
    <k> solutionProgram ~> start(grid2(1, A, B, C), 5) => .K </k>
    <result> none => some(path5(B)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool B <Int A

  claim
    <k> solutionProgram ~> start(grid2(A, 1, C, B), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B

  claim
    <k> solutionProgram ~> start(grid2(A, 1, C, B), 5) => .K </k>
    <result> none => some(path5(B)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool B <Int A

  claim
    <k> solutionProgram ~> start(grid2(A, C, 1, B), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B

  claim
    <k> solutionProgram ~> start(grid2(A, C, 1, B), 5) => .K </k>
    <result> none => some(path5(B)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool B <Int A

  claim
    <k> solutionProgram ~> start(grid2(C, A, B, 1), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B

  claim
    <k> solutionProgram ~> start(grid2(C, A, B, 1), 5) => .K </k>
    <result> none => some(path5(B)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool B <Int A
endmodule
