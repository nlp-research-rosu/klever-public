requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation: the satisfiable input (1,5) really reaches
  // binVal(3), so changing only the result obligation to binVal(4) must fail.
  claim [false-result-1-5]:
    <py>
      <k> boot(roundedAvgProgram, 1, 5) => .K </k>
      <env> .Map => ("n" |-> intVal(1)) ("m" |-> intVal(5)) </env>
      <result> noResult => result(binVal(4)) </result>
    </py>
endmodule
