requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: 4 satisfies the entry domain, but the actual
  // submitted program and lpfSpec(4, 2) return 2, not 3.
  claim [false-result-for-four]:
    <py>
      <k> solutionModule => .K </k>
      <input> 4 </input>
      <env> .Map => ?_:Map </env>
      <result> noResult => result(3) </result>
    </py>
endmodule
