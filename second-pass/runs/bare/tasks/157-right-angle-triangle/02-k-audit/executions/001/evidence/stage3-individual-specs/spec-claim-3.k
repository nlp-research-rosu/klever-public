requires "verification.k"

module SPEC-CLAIM-3
  imports VERIFICATION

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(1, 2, 3))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(false) </result>
endmodule
