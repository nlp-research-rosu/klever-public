requires "../verification.k"

module MINPATH-SPEC-10
  imports MINPATH-VERIFICATION

  claim
    <k> solutionProgram ~> start(grid2(C, A, B, 1), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B
endmodule
