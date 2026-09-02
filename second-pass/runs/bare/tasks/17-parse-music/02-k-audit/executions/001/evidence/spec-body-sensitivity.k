requires "verification-body-mutated.k"

module SPEC-BODY-SENSITIVITY
  imports MPY-VERIFICATION-BODY-MUTATED

  claim [whole-still-four]:
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
        noResult => pyList(ListItem(pyInt(4)))
      </result>
    </mpy>
endmodule
