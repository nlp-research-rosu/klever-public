requires "verification.k"

module AUDIT-VACUITY
  imports MPY-VERIFICATION

  // Deliberately false: the length-2 word "aa" is selected, so the real
  // result is "aa", not the empty string.
  claim [false-aa-result]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str("aa"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("") </result>
    </mpy>
endmodule
