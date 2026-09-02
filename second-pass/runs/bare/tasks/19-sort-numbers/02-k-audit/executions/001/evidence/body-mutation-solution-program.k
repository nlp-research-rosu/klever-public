requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY

  // A compact K spelling of the exact constructor tree in solution.mpy.
  // block(Word, Printed) is the AST for:
  //     "Printed" * numbers.count("Word")
  syntax Expr ::= block(String, String) [function]
  rule block(Word, Printed) =>
    BinOp(
      "*",
      Str(Printed),
      Call(Attribute(Name("numbers"), "count"), Str(Word)))

  syntax Expr ::= "solutionBody" [function]
  rule solutionBody =>
    Call(
      Attribute(
        BinOp("+",
          BinOp("+",
            BinOp("+",
              BinOp("+",
                BinOp("+",
                  BinOp("+",
                    BinOp("+",
                      BinOp("+",
                        BinOp("+",
                          block("zero", "bogus "),
                          block("one", "one ")),
                        block("two", "two ")),
                      block("three", "three ")),
                    block("four", "four ")),
                  block("five", "five ")),
                block("six", "six ")),
              block("seven", "seven ")),
            block("eight", "eight ")),
          block("nine", "nine ")),
        "strip"),
      .Exprs)

  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef(
        "sort_numbers",
        Params("numbers"),
        Return(solutionBody)))
endmodule
