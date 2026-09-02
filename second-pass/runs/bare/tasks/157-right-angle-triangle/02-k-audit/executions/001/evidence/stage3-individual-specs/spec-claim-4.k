requires "verification.k"

module SPEC-CLAIM-4
  imports VERIFICATION

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(5, 3, 4))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(true) </result>
endmodule
