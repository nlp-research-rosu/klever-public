requires "../verification.k"

module MINPATH-SPEC-04
  imports MINPATH-VERIFICATION

  claim
    <k> solutionProgram ~> start(grid2(1, A, B, C), 5) => .K </k>
    <result> none => some(path5(A)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
    requires validTail(A, B, C) andBool A <Int B
endmodule
