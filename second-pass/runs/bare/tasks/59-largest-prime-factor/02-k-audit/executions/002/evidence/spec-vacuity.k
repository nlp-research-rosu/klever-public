requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation.  The immutable program returns 29 for this
  // satisfiable initial state; this claim deliberately requires 30.
  claim [false-result-13195]:
    <py>
      <k> solutionModule => .K </k>
      <input> 13195 </input>
      <env> .Map => ?_:Map </env>
      <result> noResult => result(30) </result>
    </py>
endmodule
