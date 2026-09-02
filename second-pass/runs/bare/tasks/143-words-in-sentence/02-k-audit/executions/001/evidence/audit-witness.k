requires "verification.k"

module AUDIT-WITNESS
  imports MPY-VERIFICATION

  // Satisfies the entry claim's empty-store/no-requires precondition.
  claim [concrete-entry-witness]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str("aa bbbb ccc"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("aa ccc") </result>
    </mpy>

  // Ground instance satisfying the loop claim's disjoint-key precondition.
  claim [empty-loop-witness]:
    <mpy>
      <k> loop("word", WNil, solutionLoopBody) => .K </k>
      <functions> .Map </functions>
      <env> "result" |-> Str("") "word" |-> Str("old") </env>
      <result> NoneVal </result>
    </mpy>
endmodule
