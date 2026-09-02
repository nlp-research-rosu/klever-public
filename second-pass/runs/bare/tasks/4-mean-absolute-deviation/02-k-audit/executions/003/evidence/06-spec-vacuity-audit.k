requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the documented satisfying input [1,2,3,4] returns 1.
  claim
    <mad>
      <k>
        init(solutionProgram, nums(H, T))
        => .K
      </k>
      <env>
        emptyEnv
        => bind("mean", divNum(sumNums(H, T), countNums(H, T)),
             bind("numbers", nums(H, T), emptyEnv))
      </env>
      <result>
        noResult
        => result(rat(0, 1))
      </result>
    </mad>

endmodule
