requires "verification.k"

module SPEC-AUDIT
  imports MPY-VERIFICATION

  // End-to-end execution for each constructor in the input alphabet.
  claim [audit-entry-whole]:
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

  // The complete example from prompt.py, proved through the translated AST.
  claim [audit-entry-example]:
    <mpy>
      <k>
        theProgram ~>
        invoke("parse_music",
               pyStr("o o| .| o| o| .| .| .| .| o o"))
        => .K
      </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(
            ListItem(pyInt(4))
            ListItem(pyInt(2))
            ListItem(pyInt(1))
            ListItem(pyInt(2))
            ListItem(pyInt(2))
            ListItem(pyInt(1))
            ListItem(pyInt(1))
            ListItem(pyInt(1))
            ListItem(pyInt(1))
            ListItem(pyInt(4))
            ListItem(pyInt(4)))
          "music_string" |->
            pyStr("o o| .| o| o| .| .| .| .| o o")
          "note" |-> pyStr("o")
      </env>
      <result>
        noResult => pyList(
          ListItem(pyInt(4))
          ListItem(pyInt(2))
          ListItem(pyInt(1))
          ListItem(pyInt(2))
          ListItem(pyInt(2))
          ListItem(pyInt(1))
          ListItem(pyInt(1))
          ListItem(pyInt(1))
          ListItem(pyInt(1))
          ListItem(pyInt(4))
          ListItem(pyInt(4)))
      </result>
    </mpy>

  claim [audit-entry-half]:
    <mpy>
      <k> theProgram ~> invoke("parse_music", pyStr("o|")) => .K </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(ListItem(pyInt(2)))
          "music_string" |-> pyStr("o|")
          "note" |-> pyStr("o|")
      </env>
      <result>
        noResult => pyList(ListItem(pyInt(2)))
      </result>
    </mpy>

  claim [audit-entry-quarter]:
    <mpy>
      <k> theProgram ~> invoke("parse_music", pyStr(".|")) => .K </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(ListItem(pyInt(1)))
          "music_string" |-> pyStr(".|")
          "note" |-> pyStr(".|")
      </env>
      <result>
        noResult => pyList(ListItem(pyInt(1)))
      </result>
    </mpy>

  // Inductive loop step for a whole note. PREFIX and REST are universally
  // quantified, so the claim covers any iteration in any finite input.
  claim [audit-loop-whole]:
    <mpy>
      <k>
        loop("note", ListItem(pyStr("o")) REST:List, parserBranch)
        => loop("note", REST, parserBranch)
      </k>
      <functions> .Map </functions>
      <env>
        "beats" |-> pyList(PREFIX:List)
        => "beats" |-> pyList(PREFIX ListItem(pyInt(4)))
           "note" |-> pyStr("o")
      </env>
      <result> noResult </result>
    </mpy>

  // Inductive loop step for a half note.
  claim [audit-loop-half]:
    <mpy>
      <k>
        loop("note", ListItem(pyStr("o|")) REST:List, parserBranch)
        => loop("note", REST, parserBranch)
      </k>
      <functions> .Map </functions>
      <env>
        "beats" |-> pyList(PREFIX:List)
        => "beats" |-> pyList(PREFIX ListItem(pyInt(2)))
           "note" |-> pyStr("o|")
      </env>
      <result> noResult </result>
    </mpy>

  // Inductive loop step for a quarter note.
  claim [audit-loop-quarter]:
    <mpy>
      <k>
        loop("note", ListItem(pyStr(".|")) REST:List, parserBranch)
        => loop("note", REST, parserBranch)
      </k>
      <functions> .Map </functions>
      <env>
        "beats" |-> pyList(PREFIX:List)
        => "beats" |-> pyList(PREFIX ListItem(pyInt(1)))
           "note" |-> pyStr(".|")
      </env>
      <result> noResult </result>
    </mpy>

  // Base case: after the finite token list is exhausted, return the exact
  // accumulated prefix without changing it.
  claim [audit-loop-base]:
    <mpy>
      <k>
        loop("note", .List, parserBranch) ~> Return(Name("beats"))
        => .K
      </k>
      <functions> .Map </functions>
      <env> "beats" |-> pyList(PREFIX:List) </env>
      <result> noResult => pyList(PREFIX) </result>
    </mpy>

  // Source-to-invariant bridge for a whole-note prefix and arbitrary suffix.
  claim [audit-bridge-whole]:
    <mpy>
      <k>
        theProgram ~>
        invoke("parse_music", pyStr("o" +String " " +String T:String))
        => loop("note", ListItem(pyStr("o")) splitWords(T), parserBranch) ~>
           Return(Name("beats"))
      </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(.List)
          "music_string" |-> pyStr("o" +String " " +String T)
      </env>
      <result> noResult </result>
    </mpy>

  // Source-to-invariant bridge for a half-note prefix.
  claim [audit-bridge-half]:
    <mpy>
      <k>
        theProgram ~>
        invoke("parse_music", pyStr("o|" +String " " +String T:String))
        => loop("note", ListItem(pyStr("o|")) splitWords(T), parserBranch) ~>
           Return(Name("beats"))
      </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(.List)
          "music_string" |-> pyStr("o|" +String " " +String T)
      </env>
      <result> noResult </result>
    </mpy>

  // Source-to-invariant bridge for a quarter-note prefix.
  claim [audit-bridge-quarter]:
    <mpy>
      <k>
        theProgram ~>
        invoke("parse_music", pyStr(".|" +String " " +String T:String))
        => loop("note", ListItem(pyStr(".|")) splitWords(T), parserBranch) ~>
           Return(Name("beats"))
      </k>
      <functions>
        .Map => "parse_music" |->
          function("music_string", parserFunctionBody)
      </functions>
      <env>
        .Map =>
          "beats" |-> pyList(.List)
          "music_string" |-> pyStr(".|" +String " " +String T)
      </env>
      <result> noResult </result>
    </mpy>
endmodule
