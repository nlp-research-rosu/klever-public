requires "verification.k"

module SPEC-CLAIM-2
  imports VERIFICATION

  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(3, 4, 5))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(true) </result>
endmodule
