requires "verification-body-mutated.k"

module BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTATED

  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "Hello world" </input>
        <result> 0 </result>
endmodule
