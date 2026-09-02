requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh auditor mutation. The initial state is realized by n=1,m=5.
  // The real K execution returns binVal(3), so binVal(4) is deliberately false.
  claim [false-result-1-5]:
    <py>
      <k> boot(roundedAvgProgram, 1, 5) => .K </k>
      <env> .Map => ("n" |-> intVal(1)) ("m" |-> intVal(5)) </env>
      <result> noResult => result(binVal(4)) </result>
    </py>
endmodule
