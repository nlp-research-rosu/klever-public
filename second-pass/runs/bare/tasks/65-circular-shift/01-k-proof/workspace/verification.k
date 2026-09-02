requires "semantic.k"

module VERIFICATION
  imports MPY

  // A named copy of the exact constructor tree emitted in solution.mpy.
  // Keeping it here makes proof claims readable while krun independently parses
  // and executes the generated solution.mpy file.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("circular_shift", Params("x", "shift"),
        Assign(Name("s"), Call(Name("str"), Name("x")))
        If(
          Compare(Name("shift"), CmpOp(">", Call(Name("len"), Name("s")))),
          Return(Subscript(Name("s"),
            Slice(NoBound, NoBound, UnaryOp("-", Int(1))))),
          .Stmts)
        Return(
          BinOp("+",
            Subscript(Name("s"),
              Slice(BinOp("-", Call(Name("len"), Name("s")), Name("shift")),
                    NoBound, NoBound)),
            Subscript(Name("s"),
              Slice(NoBound,
                    BinOp("-", Call(Name("len"), Name("s")), Name("shift")),
                    NoBound))))))

  syntax Val ::= runSolution(Val, Val) [function]
  rule runSolution(X, SHIFT)
    => runProgram(solutionProgram, "circular_shift", (X, SHIFT))

  // Independent mathematical rendering of the two clauses in the contract.
  syntax String ::= normalCircularShift(String, Int) [function]
  rule normalCircularShift(S, SHIFT)
    => substrString(S, lengthString(S) -Int SHIFT, lengthString(S))
       +String substrString(S, 0, lengthString(S) -Int SHIFT)
endmodule
