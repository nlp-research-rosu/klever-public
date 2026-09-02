module MPY-VERIFICATION
  imports MPY-SEMANTICS

  // The exact AST generated in solution.mpy.  Keeping it as a named function
  // makes the quantified claims readable while still proving the translated
  // program, rather than a hand-written shortcut command.
  syntax Program ::= "#solutionProgram" [function]
  rule #solutionProgram =>
    Module(
      FuncDef("by_length", Params("arr"),
        Return(
          BinOp("+",
            BinOp("+",
              BinOp("+",
                BinOp("+",
                  BinOp("+",
                    BinOp("+",
                      BinOp("+",
                        BinOp("+",
                          BinOp("*", ListExpr(Str("Nine")),
                            Call(Attribute(Name("arr"), "count"), Int(9))),
                          BinOp("*", ListExpr(Str("Eight")),
                            Call(Attribute(Name("arr"), "count"), Int(8)))),
                        BinOp("*", ListExpr(Str("Seven")),
                          Call(Attribute(Name("arr"), "count"), Int(7)))),
                      BinOp("*", ListExpr(Str("Six")),
                        Call(Attribute(Name("arr"), "count"), Int(6)))),
                    BinOp("*", ListExpr(Str("Five")),
                      Call(Attribute(Name("arr"), "count"), Int(5)))),
                  BinOp("*", ListExpr(Str("Four")),
                    Call(Attribute(Name("arr"), "count"), Int(4)))),
                BinOp("*", ListExpr(Str("Three")),
                  Call(Attribute(Name("arr"), "count"), Int(3)))),
              BinOp("*", ListExpr(Str("Two")),
                Call(Attribute(Name("arr"), "count"), Int(2)))),
            BinOp("*", ListExpr(Str("One")),
              Call(Attribute(Name("arr"), "count"), Int(1)))))))

  // A contract-level characterization of the prompt: for each valid digit,
  // descending from 9 to 1, emit its name once per occurrence in the input.
  // Values outside 1..9 never contribute a block.
  syntax Value ::= "#byLength" "(" PyVals ")" [function]
  rule #byLength(XS) =>
    #add(
      #add(
        #add(
          #add(
            #add(
              #add(
                #add(
                  #add(
                    #multiply(pyList("Nine" :: .PyVals), #count(pyList(XS), 9)),
                    #multiply(pyList("Eight" :: .PyVals), #count(pyList(XS), 8))),
                  #multiply(pyList("Seven" :: .PyVals), #count(pyList(XS), 7))),
                #multiply(pyList("Six" :: .PyVals), #count(pyList(XS), 6))),
              #multiply(pyList("Five" :: .PyVals), #count(pyList(XS), 5))),
            #multiply(pyList("Four" :: .PyVals), #count(pyList(XS), 4))),
          #multiply(pyList("Three" :: .PyVals), #count(pyList(XS), 3))),
        #multiply(pyList("Two" :: .PyVals), #count(pyList(XS), 2))),
      #multiply(pyList("One" :: .PyVals), #count(pyList(XS), 1)))
endmodule
