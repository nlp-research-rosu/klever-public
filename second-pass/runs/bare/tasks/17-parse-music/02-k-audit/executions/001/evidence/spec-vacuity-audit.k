requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // False mutation of the result-bearing obligation in the true "o" claim:
  // the executed program returns [4], not [5].
  claim [whole-note-wrong-result]:
    <mpy>
      <k> theProgram ~> invoke("parse_music", pyStr("o")) => .K </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(ListItem(pyInt(4)))
          "music_string" |-> pyStr("o")
          "note" |-> pyStr("o")
      </env>
      <result>
        noResult => pyList(ListItem(pyInt(5)))
      </result>
    </mpy>
endmodule
