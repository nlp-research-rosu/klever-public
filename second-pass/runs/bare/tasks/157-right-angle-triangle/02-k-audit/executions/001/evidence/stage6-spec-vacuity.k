requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: (3,4,5) returns true, so false is impossible.
  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(3, 4, 5))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(false) </result>
endmodule
