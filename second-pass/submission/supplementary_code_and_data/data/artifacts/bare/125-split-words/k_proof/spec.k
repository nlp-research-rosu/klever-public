requires "verification.k"

module SPLIT-WORDS-SPEC
  imports MPY-VERIFICATION

  // One total symbolic claim states the contract for every String. The nested
  // conditional encodes the three exhaustive branches and their precedence.
  claim <k> runProgram(solutionAST, S:String)
          => iteValue(
               containsWhitespace(S),
               VList(pySplitWhitespace(S)),
               iteValue(
                 findString(S, ",", 0) >=Int 0,
                 VList(pySplitOn(S, ",")),
                 VInt(oddLetterCount(S)))) ... </k>

  // Original prompt examples.
  claim <k> runProgram(solutionAST, "Hello world!")
          => VList(ListItem(VStr("Hello")) ListItem(VStr("world!"))) ... </k>

  claim <k> runProgram(solutionAST, "Hello,world!")
          => VList(ListItem(VStr("Hello")) ListItem(VStr("world!"))) ... </k>

  claim <k> runProgram(solutionAST, "abcdef") => VInt(3) ... </k>

  // Edge cases: empty input, whitespace precedence, and preserved empty comma
  // fields.
  claim <k> runProgram(solutionAST, "") => VInt(0) ... </k>

  claim <k> runProgram(solutionAST, "a,b c")
          => VList(ListItem(VStr("a,b")) ListItem(VStr("c"))) ... </k>

  claim <k> runProgram(solutionAST, "left\u2003right")
          => VList(ListItem(VStr("left")) ListItem(VStr("right"))) ... </k>

  claim <k> runProgram(solutionAST, "a,,b,")
          => VList(
               ListItem(VStr("a"))
               ListItem(VStr(""))
               ListItem(VStr("b"))
               ListItem(VStr(""))) ... </k>
endmodule
