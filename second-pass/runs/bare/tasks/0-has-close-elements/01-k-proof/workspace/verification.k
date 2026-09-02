requires "semantic.k"

module VERIFICATION
  imports MPY

  // A closed K term for the exact AST emitted in solution.mpy.  Keeping this
  // in the verification layer lets claims quantify only over input values.
  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("close_to_first", Params("first", "rest", "threshold"),
        If(Compare(Call(Name("len"), Name("rest")), CmpOp("==", Int(0))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(
          Call(
            Name("abs"),
            BinOp("-", Name("first"), Subscript(Name("rest"), Int(0)))),
          CmpOp("<", Name("threshold"))),
          Return(Bool(true)),
          .Stmts)
        Return(
          Call(
            Name("close_to_first"),
            Name("first"),
            Subscript(Name("rest"), Slice(Int(1), NoBound, NoBound)),
            Name("threshold"))))
      FuncDef("has_close_elements", Params("numbers", "threshold"),
        If(Compare(Call(Name("len"), Name("numbers")), CmpOp("<", Int(2))),
          Return(Bool(false)),
          .Stmts)
        If(Call(
          Name("close_to_first"),
          Subscript(Name("numbers"), Int(0)),
          Subscript(Name("numbers"), Slice(Int(1), NoBound, NoBound)),
          Name("threshold")),
          Return(Bool(true)),
          .Stmts)
        Return(
          Call(
            Name("has_close_elements"),
            Subscript(Name("numbers"), Slice(Int(1), NoBound, NoBound)),
            Name("threshold")))))

  syntax Map ::= "solutionFunctions" [function]
               | functionsOf(Pgm) [function]
  rule solutionFunctions => functionsOf(solutionProgram)
  rule functionsOf(Module(SS)) => collect(SS)
  rule <k> verify(ARGS) => call("has_close_elements", ARGS, solutionFunctions) ... </k>

  // Independent mathematical specification: a pair exists if the head is
  // close to some tail element, or a pair exists wholly within the tail.
  syntax Bool ::= closePair(PVal, PVal, PVal) [function]
                | closeFirstRef(PVal, PVal, PVal) [function]
                | hasCloseRef(PVal, PVal) [function]
                | boolOf(PVal) [function]

  rule boolOf(VBool(B)) => B
  rule closePair(X, Y, T)
    => boolOf(compareValue("<", absValue(subValue(X, Y)), T))

  rule closeFirstRef(_, VList(.PValues), _) => false
  rule closeFirstRef(X, VList(Y, REST), T)
    => closePair(X, Y, T) orBool closeFirstRef(X, VList(REST), T)

  rule hasCloseRef(VList(.PValues), _) => false
  rule hasCloseRef(VList(_X), _) => false
  rule hasCloseRef(VList(X, Y, REST), T)
    => closeFirstRef(X, VList(Y, REST), T)
       orBool hasCloseRef(VList(Y, REST), T)
endmodule
