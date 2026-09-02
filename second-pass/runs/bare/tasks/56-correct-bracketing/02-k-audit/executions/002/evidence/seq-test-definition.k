requires "semantic.k"

module SEQ-TEST-SYNTAX
  imports MPY-SYNTAX
  syntax Pgm ::= "SeqEmpty"
               | "SeqPair"
               | "SeqClose"
endmodule

module SEQ-TEST
  imports MPY
  imports SEQ-TEST-SYNTAX

  // Replace only the default top-level harness invocation, so the exact
  // correctProgram body executes with a concrete proof-surrogate value.
  rule <k>
    SeqEmpty ~> invoke("correct_bracketing", SVal(_))
    => correctProgram()
       ~> invoke("correct_bracketing", SeqVal(noBrackets()))
    ...
  </k>
  rule <k>
    SeqPair ~> invoke("correct_bracketing", SVal(_))
    => correctProgram()
       ~> invoke(
            "correct_bracketing",
            SeqVal(openBracket(closeBracket(noBrackets()))))
    ...
  </k>
  rule <k>
    SeqClose ~> invoke("correct_bracketing", SVal(_))
    => correctProgram()
       ~> invoke("correct_bracketing", SeqVal(closeBracket(noBrackets())))
    ...
  </k>
endmodule
