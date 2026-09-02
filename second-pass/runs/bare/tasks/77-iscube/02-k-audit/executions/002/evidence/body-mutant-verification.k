requires "verification.k"

module BODY-MUTANT-VERIFICATION
  imports VERIFICATION

  syntax Pgm ::= "iscubeProgramMutated"
  rule iscubeProgramMutated =>
    Module(
      FuncDef("iscube", Params("a"),
        If(Compare(Name("a"), CmpOp("<", Int(0))),
          Assign(Name("a"), UnaryOp("-", Name("a"))),
          .Stmts)
        Assign(Name("n"), Int(0))
        While(Compare(
          BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
          CmpOp("<", Name("a"))),
          Assign(Name("n"), BinOp("+", Name("n"), Int(2))))
        Return(Compare(
          BinOp("*", BinOp("*", Name("n"), Name("n")), Name("n")),
          CmpOp("==", Name("a"))))))
endmodule
