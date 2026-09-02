requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh audit mutation: the real program returns 0 for this satisfiable
  // ground input, so demanding 1 must leave an unmet result obligation.
  claim <k> start => done </k>
        <program> solutionModule </program>
        <input> "Hello world" </input>
        <result> 0 => 1 </result>
endmodule
