requires "../../tmp/audit-work/93-encode/concrete.k"
requires "../../tmp/audit-work/93-encode/verification.k"

module AUDIT-SPEC-VACUITY
  imports CONCRETE
  imports VERIFICATION

  // Fresh false result mutation of CONCRETE-SPEC.example-test.
  // The submitted and trusted Python functions both return "TGST" for "test";
  // this mutation instead requires "TGSA".
  claim [false-example-test-result]:
    <k> encodeProgram() ~> invoke("encode", pyStr("test")) => .K </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult => returned(pyStr("TGSA")) </result>
endmodule
