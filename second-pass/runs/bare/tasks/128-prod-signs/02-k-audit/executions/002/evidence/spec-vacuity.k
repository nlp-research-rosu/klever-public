requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation.  The real result for this satisfying input is
  // -9; this mutation requires -8 while preserving the executed program term.
  claim [false-example-result]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(1, 2, 2, -4) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map =>
      "arr" |-> listVal(1, 2, 2, -4)
      "total" |-> 9
      "sign" |-> -1
      "x" |-> -4
    </env>
    <result> noResult => result(-8) </result>
endmodule
