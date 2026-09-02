requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional correctness for every nonempty finite rational
  // input list.  H and T are arbitrary, so this is not bounded testing.
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
        => result(mathMAD(H, T))
      </result>
    </mad>

endmodule
