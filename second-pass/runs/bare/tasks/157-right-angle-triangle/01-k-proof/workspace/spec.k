requires "verification.k"

module SPEC
  imports VERIFICATION

  // Complete functional-correctness statement over the Int domain.
  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(A, B, C))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(rightTriangle(A, B, C)) </result>

  // Executable witnesses for the prompt examples and side-order symmetry.
  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(3, 4, 5))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(true) </result>

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(1, 2, 3))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(false) </result>

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(5, 3, 4))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(true) </result>
endmodule
