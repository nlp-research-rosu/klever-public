requires "verification.k"

module PROGRAM-PINNING
  imports VERIFICATION-BASE

  // RHS is the trusted-translator output in submitted solution.mpy, written
  // without the proof-only body abbreviations.
  claim <k> solutionModule()
         => Module(
              ImportFrom("typing", "List")
              FuncDef("is_close_to_any",
                Params("number", "numbers", "threshold", "start"),
                Assign(Name("found"), Bool(false))
                Assign(Name("index"), Int(0))
                Assign(Name("other"), Name("number"))
                For(Name("other"), Name("numbers"),
                  If(Compare(Name("index"),
                             CmpOp(">=", Name("start"))),
                    If(Compare(
                      Call(Name("abs"),
                           BinOp("-", Name("number"), Name("other"))),
                      CmpOp("<", Name("threshold"))),
                      Assign(Name("found"), Bool(true))
                      Break,
                      .Stmts),
                    .Stmts)
                  AugAssign(Name("index"), "+", Int(1)))
                Assign(Name("index"), Int(0))
                Assign(Name("other"), Name("number"))
                Return(Name("found")))
              FuncDef("has_close_elements",
                Params("numbers", "threshold"),
                Assign(Name("found"), Bool(false))
                Assign(Name("start"), Int(1))
                Assign(Name("number"), Name("threshold"))
                For(Name("number"), Name("numbers"),
                  If(Call(Name("is_close_to_any"),
                          Name("number"), Name("numbers"),
                          Name("threshold"), Name("start")),
                    Assign(Name("found"), Bool(true))
                    Break,
                    .Stmts)
                  AugAssign(Name("start"), "+", Int(1)))
                Assign(Name("start"), Int(1))
                Assign(Name("number"), Name("threshold"))
                Return(Name("found")))) </k>
endmodule
