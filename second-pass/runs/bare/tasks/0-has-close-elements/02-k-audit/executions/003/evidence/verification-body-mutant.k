requires "/tmp/audit-work/candidate-src/semantic.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Pgm ::= "mutatedSolutionProgram" [function]
  rule mutatedSolutionProgram =>
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
          Return(Bool(true)),
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

  syntax Map ::= "mutatedSolutionFunctions" [function]
  rule mutatedSolutionFunctions => collectFunctions(mutatedSolutionProgram)

  syntax Map ::= collectFunctions(Pgm) [function]
  rule collectFunctions(Module(SS)) => collect(SS)

  syntax KItem ::= "verifyMutant" "(" PValues ")"
  rule <k> verifyMutant(ARGS)
        => call("has_close_elements", ARGS, mutatedSolutionFunctions) ... </k>
endmodule
