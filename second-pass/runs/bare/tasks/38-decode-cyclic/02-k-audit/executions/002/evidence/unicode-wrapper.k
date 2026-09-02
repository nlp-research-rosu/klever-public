requires "semantic.k"

module UNICODE-WRAPPER-SYNTAX
  imports MPY-SYNTAX

  syntax Py ::= "UnicodeCaseOne" | "UnicodeCaseTwo"
endmodule

module UNICODE-WRAPPER
  imports MPY
  imports UNICODE-WRAPPER-SYNTAX

  rule <k> run(UnicodeCaseOne, _) =>
           run(solutionProgram, "\u00e9\u03b1\u4e2d\U0001f642\U0001d11e")
           ... </k>

  rule <k> run(UnicodeCaseTwo, _) =>
           run(solutionProgram, "e\u0301\U0001f642\u4e2dA")
           ... </k>
endmodule
