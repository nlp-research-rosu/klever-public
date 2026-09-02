requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh false result obligation. The satisfying input's real result is "is".
  claim [false-example-one]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str("This is a test"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("test") </result>
    </mpy>
endmodule
