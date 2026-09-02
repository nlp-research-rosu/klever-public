requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTIC

  // A generic one-argument function invocation layer over the translated AST.
  syntax Function ::= "closure" "(" Params "," Stmts ")"
  syntax Function ::= "findFunction" "(" String "," Stmts ")" [function]
  syntax Value ::= "invoke" "(" Function "," Value ")" [function]
                 | "outcomeValue" "(" Outcome ")" [function]
                 | "runProgram" "(" Module "," String ")" [function]

  rule findFunction(F, FuncDef(F, PARAMS, BODY) _REST:Stmts)
    => closure(PARAMS, BODY)
  rule findFunction(F, FuncDef(G, _, _) REST:Stmts)
    => findFunction(F, REST)
    requires F =/=String G

  rule invoke(closure(Params(P:String), BODY), V)
    => outcomeValue(exec(BODY, P |-> V))
  rule outcomeValue(returned(V)) => V
  rule outcomeValue(iteOutcome(B, THEN, ELSE))
    => iteValue(B, outcomeValue(THEN), outcomeValue(ELSE))
  rule runProgram(Module(STMTS), S)
    => invoke(findFunction("split_words", STMTS), VStr(S))

  // This nullary term expands to the exact constructor tree in solution.mpy.
  // Keeping it here makes every symbolic claim explicitly about the submitted
  // implementation rather than about a hand-written summary of the function.
  syntax Module ::= "solutionAST" [function]
  rule solutionAST =>
    Module(
      FuncDef("split_words", Params("txt"),
        Assign(Name("words"), Call(Attribute(Name("txt"), "split"), .Exprs))
        If(Compare(
          Call(Attribute(Str(""), "join"), Name("words")),
          CmpOp("!=", Name("txt"))),
          Return(Name("words")),
          .Stmts)
        If(Compare(Str(","), CmpOp("in", Name("txt"))),
          Return(Call(Attribute(Name("txt"), "split"), Str(","))),
          .Stmts)
        Return(
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
                            BinOp(
                              "+",
                              BinOp(
                                "+",
                                BinOp(
                                  "+",
                                  Call(Attribute(Name("txt"), "count"), Str("b")),
                                  Call(Attribute(Name("txt"), "count"), Str("d"))),
                                Call(Attribute(Name("txt"), "count"), Str("f"))),
                              Call(Attribute(Name("txt"), "count"), Str("h"))),
                            Call(Attribute(Name("txt"), "count"), Str("j"))),
                          Call(Attribute(Name("txt"), "count"), Str("l"))),
                        Call(Attribute(Name("txt"), "count"), Str("n"))),
                      Call(Attribute(Name("txt"), "count"), Str("p"))),
                    Call(Attribute(Name("txt"), "count"), Str("r"))),
                  Call(Attribute(Name("txt"), "count"), Str("t"))),
                Call(Attribute(Name("txt"), "count"), Str("v"))),
              Call(Attribute(Name("txt"), "count"), Str("x"))),
            Call(Attribute(Name("txt"), "count"), Str("z"))))))

  // The mathematical value required by the third branch of the prompt.
  syntax Int ::= "oddLetterCount" "(" String ")" [function, total]
  rule oddLetterCount(S) =>
    ((((((((((((countAllOccurrences(S, "b")
      +Int countAllOccurrences(S, "d"))
      +Int countAllOccurrences(S, "f"))
      +Int countAllOccurrences(S, "h"))
      +Int countAllOccurrences(S, "j"))
      +Int countAllOccurrences(S, "l"))
      +Int countAllOccurrences(S, "n"))
      +Int countAllOccurrences(S, "p"))
      +Int countAllOccurrences(S, "r"))
      +Int countAllOccurrences(S, "t"))
      +Int countAllOccurrences(S, "v"))
      +Int countAllOccurrences(S, "x"))
      +Int countAllOccurrences(S, "z"))

  syntax Bool ::= "containsWhitespace" "(" String ")" [function, total]
  rule containsWhitespace(S)
    => joinValues("", pySplitWhitespace(S)) =/=String S

  configuration <k> runProgram($PGM:Module, $INPUT:String) </k>
endmodule
