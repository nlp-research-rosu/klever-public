requires "semantic.k"

module VERIFICATION
  imports MPY

  // The exact constructor term generated from solution.py.  Keeping it as a
  // named constant makes the claims readable without adding behavior to it.
  syntax Pgm ::= "solutionProgram" [function, total]
  syntax Stmts ::= "solutionFunctions" [function, total]
  rule solutionProgram => Module(solutionFunctions)
  rule solutionFunctions =>
      FuncDef("insert_char", Params("char", "word", "before"),
        If(Compare(Name("word"), CmpOp("==", Str(""))),
          Return(BinOp("+", Name("before"), Name("char"))),
          .Stmts)
        If(Compare(Name("char"), CmpOp("<=", Subscript(Name("word"), Int(0)))),
          Return(
            BinOp(
              "+",
              BinOp("+", Name("before"), Name("char")),
              Name("word"))),
          .Stmts)
        Return(
          Call(
            Name("insert_char"),
            Name("char"),
            Subscript(Name("word"), Slice(Int(1), NoBound, NoBound)),
            BinOp("+", Name("before"), Subscript(Name("word"), Int(0))))))
      FuncDef("process_words", Params("text", "word", "result"),
        If(Compare(Name("text"), CmpOp("==", Str(""))),
          Return(BinOp("+", Name("result"), Name("word"))),
          .Stmts)
        If(Compare(Subscript(Name("text"), Int(0)), CmpOp("==", Str(" "))),
          Return(
            Call(
              Name("process_words"),
              Subscript(Name("text"), Slice(Int(1), NoBound, NoBound)),
              Str(""),
              BinOp("+", BinOp("+", Name("result"), Name("word")), Str(" ")))),
          .Stmts)
        Return(
          Call(
            Name("process_words"),
            Subscript(Name("text"), Slice(Int(1), NoBound, NoBound)),
            Call(
              Name("insert_char"),
              Subscript(Name("text"), Int(0)),
              Name("word"),
              Str("")),
            Name("result"))))
      FuncDef("anti_shuffle", Params("s"),
        Return(Str("")))

  // Mathematical reference: insert a character into an already sorted word.
  // BEFORE is the prefix already known to be smaller than the character.
  syntax String ::= refInsert ( String , String , String ) [function]

  rule refInsert(C, WORD, BEFORE) => BEFORE +String C
    requires WORD ==String ""
  rule refInsert(C, WORD, BEFORE) =>
    BEFORE +String C +String WORD
    requires notBool (WORD ==String "")
     andBool C <=String substrString(WORD, 0, 1)
  rule refInsert(C, WORD, BEFORE) =>
    refInsert(C,
      substrString(WORD, 1, lengthString(WORD)),
      BEFORE +String substrString(WORD, 0, 1))
    requires notBool (WORD ==String "")
     andBool notBool (C <=String substrString(WORD, 0, 1))

  // Mathematical reference: scan left-to-right, sorting one word at a time.
  // RESULT contains all complete words and their original separating spaces.
  syntax String ::= refProcess ( String , String , String ) [function]
  syntax String ::= antiShuffleSpec ( String ) [function, total]

  rule refProcess(TEXT, WORD, RESULT) => RESULT +String WORD
    requires TEXT ==String ""
  rule refProcess(TEXT, WORD, RESULT) =>
    refProcess(
      substrString(TEXT, 1, lengthString(TEXT)),
      "",
      RESULT +String WORD +String " ")
    requires notBool (TEXT ==String "")
     andBool substrString(TEXT, 0, 1) ==String " "
  rule refProcess(TEXT, WORD, RESULT) =>
    refProcess(
      substrString(TEXT, 1, lengthString(TEXT)),
      refInsert(substrString(TEXT, 0, 1), WORD, ""),
      RESULT)
    requires notBool (TEXT ==String "")
     andBool notBool (substrString(TEXT, 0, 1) ==String " ")

  rule antiShuffleSpec(S) => refProcess(S, "", "")
endmodule
