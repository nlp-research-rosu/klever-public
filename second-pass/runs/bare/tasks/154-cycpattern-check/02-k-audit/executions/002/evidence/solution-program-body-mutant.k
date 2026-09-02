requires "semantic.k"

module SOLUTION-PROGRAM-BODY-MUTANT
  imports MPY-SYNTAX
  syntax Program ::= mutatedSolutionProgram() [macro]
  rule mutatedSolutionProgram() =>
    Module(
      FuncDef("cycpattern_check", Params("a", "b"),
        Assign(Name("i"), Int(0))
        While(Compare(Name("i"), CmpOp("<", Call(Name("len"), Name("b")))),
          If(Compare(
            BinOp(
              "+",
              Subscript(Name("b"), Slice(Name("i"), NoBound, NoBound)),
              Subscript(Name("b"), Slice(NoBound, Name("i"), NoBound))),
            CmpOp("in", Name("a"))),
            Return(Bool(false)),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Bool(false))))
endmodule
