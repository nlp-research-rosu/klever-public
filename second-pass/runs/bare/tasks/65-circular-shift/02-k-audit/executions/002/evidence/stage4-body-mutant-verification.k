requires "semantic.k"

module AUDIT-BODY-MUTANT-VERIFICATION
  imports MPY

  // Material mutation of the executed program term: concatenate prefix before
  // suffix, so (12, 1) returns "12" instead of the submitted body's "21".
  syntax Program ::= "solutionProgramBodyMutant" [macro]
  rule solutionProgramBodyMutant =>
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
              Slice(NoBound,
                    BinOp("-", Call(Name("len"), Name("s")), Name("shift")),
                    NoBound)),
            Subscript(Name("s"),
              Slice(BinOp("-", Call(Name("len"), Name("s")), Name("shift")),
                    NoBound, NoBound))))))
endmodule
