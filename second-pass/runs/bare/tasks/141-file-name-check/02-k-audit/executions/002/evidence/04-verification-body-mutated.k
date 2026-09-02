requires "semantic.k"

module VERIFICATION-BODY-MUTATED
  imports SEMANTIC

  syntax Program ::= "solutionProgram" [function, total, symbol]
  syntax Int ::= digitCount(String) [function, total, symbol]
  syntax Bool ::= startsWithAsciiLetter(String) [function, total, symbol]
                | hasAcceptedSuffix(String) [function, total, symbol]
                | validFileName(String) [function, total, symbol]
  syntax PyVal ::= contractResult(String) [function, total, symbol]

  rule digitCount(S) =>
       occurrences(S, "0")
    +Int occurrences(S, "1")
    +Int occurrences(S, "2")
    +Int occurrences(S, "3")
    +Int occurrences(S, "4")
    +Int occurrences(S, "5")
    +Int occurrences(S, "6")
    +Int occurrences(S, "7")
    +Int occurrences(S, "8")
    +Int occurrences(S, "9")

  rule startsWithAsciiLetter(S) =>
       ("a" <=String substrString(S, 0, 1)
         andBool substrString(S, 0, 1) <=String "z")
    orBool
       ("A" <=String substrString(S, 0, 1)
         andBool substrString(S, 0, 1) <=String "Z")

  rule hasAcceptedSuffix(S) =>
       endsWith(S, ".txt")
    orBool endsWith(S, ".exe")
    orBool endsWith(S, ".dll")

  // This is the prompt's contract, stated independently of the AST evaluator.
  // Exactly one dot plus an accepted final suffix makes the text after that
  // unique dot exactly txt/exe/dll. A nonempty name makes character 0 defined.
  rule validFileName(S) =>
       occurrences(S, ".") ==Int 1
    andBool digitCount(S) <=Int 3
    andBool lengthString(S) >Int 0
    andBool startsWithAsciiLetter(S)
    andBool hasAcceptedSuffix(S)

  // The same contract as a total result-valued decision tree. Each rejection
  // node is the negation of one conjunct of validFileName, in prompt order.
  rule contractResult(S) =>
    IteVal(occurrences(S, ".") =/=Int 1,
      VStr("No"),
      IteVal(digitCount(S) >Int 3,
        VStr("No"),
        IteVal(lengthString(S) ==Int 0,
          VStr("No"),
          IteVal(notBool startsWithAsciiLetter(S),
            VStr("No"),
            IteVal(hasAcceptedSuffix(S), VStr("Yes"), VStr("No"))))))

  // A checked-in AST constant connects the proof to solution.mpy. prove.sh
  // regenerates solution.mpy and checks its recorded digest before kprove.
  rule solutionProgram =>
    Module(
      FuncDef("file_name_check", Params("file_name"),
        Assign(
          Name("digits"),
          BinOp(
            "+",
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Call(
                              Attribute(Name("file_name"), "count"),
                              Str("0")),
                            Call(
                              Attribute(Name("file_name"), "count"),
                              Str("1"))),
                          Call(
                            Attribute(Name("file_name"), "count"),
                            Str("2"))),
                        Call(
                          Attribute(Name("file_name"), "count"),
                          Str("3"))),
                      Call(Attribute(Name("file_name"), "count"), Str("4"))),
                    Call(Attribute(Name("file_name"), "count"), Str("5"))),
                  Call(Attribute(Name("file_name"), "count"), Str("6"))),
                Call(Attribute(Name("file_name"), "count"), Str("7"))),
              Call(Attribute(Name("file_name"), "count"), Str("8"))),
            Call(Attribute(Name("file_name"), "count"), Str("9"))))
        If(Compare(
          Call(Attribute(Name("file_name"), "count"), Str(".")),
          CmpOp("!=", Int(1))),
          Return(Str("No")),
          .Stmts)
        If(Compare(Name("digits"), CmpOp(">", Int(3))),
          Return(Str("No")),
          .Stmts)
        If(Compare(Call(Name("len"), Name("file_name")), CmpOp("==", Int(0))),
          Return(Str("No")),
          .Stmts)
        Assign(Name("first"), Subscript(Name("file_name"), Int(0)))
        If(UnaryOp(
          "not",
          BoolOp(
            "or",
            BoolOp(
              "and",
              Compare(Str("a"), CmpOp("<=", Name("first"))),
              Compare(Name("first"), CmpOp("<=", Str("z")))),
            BoolOp(
              "and",
              Compare(Str("A"), CmpOp("<=", Name("first"))),
              Compare(Name("first"), CmpOp("<=", Str("Z")))))),
          Return(Str("No")),
          .Stmts)
        If(BoolOp(
          "or",
          Call(Attribute(Name("file_name"), "endswith"), Str(".txt")),
          Call(Attribute(Name("file_name"), "endswith"), Str(".exe")),
          Call(Attribute(Name("file_name"), "endswith"), Str(".dll"))),
          Return(Str("No")),
          .Stmts)
        Return(Str("No"))))
endmodule
