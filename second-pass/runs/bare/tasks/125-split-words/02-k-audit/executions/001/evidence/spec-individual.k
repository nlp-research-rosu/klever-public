requires "verification.k"

module AUDIT-SPEC-UNIVERSAL
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, S:String)
          => iteValue(
               containsWhitespace(S),
               VList(pySplitWhitespace(S)),
               iteValue(
                 findString(S, ",", 0) >=Int 0,
                 VList(pySplitOn(S, ",")),
                 VInt(oddLetterCount(S)))) ... </k>
endmodule

module AUDIT-SPEC-EXAMPLE-SPACE
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "Hello world!")
          => VList(ListItem(VStr("Hello")) ListItem(VStr("world!"))) ... </k>
endmodule

module AUDIT-SPEC-EXAMPLE-COMMA
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "Hello,world!")
          => VList(ListItem(VStr("Hello")) ListItem(VStr("world!"))) ... </k>
endmodule

module AUDIT-SPEC-EXAMPLE-COUNT
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "abcdef") => VInt(3) ... </k>
endmodule

module AUDIT-SPEC-EMPTY
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "") => VInt(0) ... </k>
endmodule

module AUDIT-SPEC-WHITESPACE-PRECEDENCE
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "a,b c")
          => VList(ListItem(VStr("a,b")) ListItem(VStr("c"))) ... </k>
endmodule

module AUDIT-SPEC-UNICODE-WHITESPACE
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "left\u2003right")
          => VList(ListItem(VStr("left")) ListItem(VStr("right"))) ... </k>
endmodule

module AUDIT-SPEC-EMPTY-COMMA-FIELDS
  imports MPY-VERIFICATION
  claim <k> runProgram(solutionAST, "a,,b,")
          => VList(
               ListItem(VStr("a"))
               ListItem(VStr(""))
               ListItem(VStr("b"))
               ListItem(VStr(""))) ... </k>
endmodule
