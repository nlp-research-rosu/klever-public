requires "verification.k"

module SPEC-CLAIM-1
  imports VERIFICATION

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(A, B, C))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(rightTriangle(A, B, C)) </result>
endmodule
