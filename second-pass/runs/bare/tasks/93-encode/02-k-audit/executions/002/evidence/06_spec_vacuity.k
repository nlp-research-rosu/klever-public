requires "verification.k"
requires "concrete.k"

module CONCRETE-SPEC-VACUITY-AUDIT
  imports CONCRETE
  imports VERIFICATION

  // Fresh false result mutation: Python returns "TGST" for the satisfying
  // input "test", so the final "S" below must remain unmet.
  claim [false-example-test]:
    <k> encodeProgram() ~> invoke("encode", pyStr("test")) => .K </k>
    <env> .Map => ?RHO </env>
    <functions> .Map => ?FS </functions>
    <result> noResult => returned(pyStr("TGSS")) </result>
endmodule
