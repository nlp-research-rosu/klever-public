requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the satisfying input (3,4,5) returns true.
  claim <k>
          run(solutionProgram,
              "right_angle_triangle", Args(3, 4, 5))
          => .K
        </k>
        <env> .Map </env>
        <result> noResult => result(false) </result>
endmodule
