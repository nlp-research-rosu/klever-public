requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION

  // Satisfying substitution H = rat(1,1),
  // T = rat(2,1), rat(3,1), rat(4,1), .Nums.
  claim [documented-example]:
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
        noResult => result(rat(1024,1024))
      </result>
    </mad>

  // A second satisfying substitution crossing both branches of absNum.
  claim [mixed-sign-example]:
    <mad>
      <k>
        init(solutionProgram,
          nums(rat(-2,1),rat(0,1),rat(2,1)))
        => .K
      </k>
      <env>
        emptyEnv
        => bind("mean", rat(0,3),
             bind("numbers",
               nums(rat(-2,1),rat(0,1),rat(2,1)),
               emptyEnv))
      </env>
      <result>
        noResult => result(rat(108,81))
      </result>
    </mad>

endmodule
