requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the documented satisfying input has MAD 1, not 0.
  // This changes the result-bearing destination while preserving actual
  // program execution and a realizable initial state.
  claim [false-documented-result]:
    <mad>
      <k>
        init(solutionProgram,
          nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1)))
        => .K
      </k>
      <env>
        emptyEnv
        => bind("mean", rat(10,4),
             bind("numbers",
               nums(rat(1,1),rat(2,1),rat(3,1),rat(4,1)),
               emptyEnv))
      </env>
      <result>
        noResult => result(rat(0,1))
      </result>
    </mad>

endmodule
