requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // False for this satisfiable initial state: actual submitted result is 1.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "The sky is blue. The sun is shining. I love this weather" </input>
        <result> 0 => 2 </result>
endmodule
