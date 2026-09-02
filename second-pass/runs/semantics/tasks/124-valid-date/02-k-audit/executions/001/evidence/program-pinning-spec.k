requires "verification.k"

module PROGRAM-PINNING-SPEC
  imports VALID-DATE-VERIFICATION

  // RHS is the freshly regenerated solution.mpy term, included verbatim.
  claim validDateModule
    =>
    Module(
      FuncDef("valid_date", Params("date"),
        If(Compare(Call(Name("len"), Name("date")), CmpOp("!=", Int(10))),
          Return(Bool(false)),
          .Stmts)
        If(BoolOp(
          "or",
          Compare(
            Call(Name("ord"), Subscript(Name("date"), Int(2))),
            CmpOp("!=", Int(45))),
          Compare(
            Call(Name("ord"), Subscript(Name("date"), Int(5))),
            CmpOp("!=", Int(45)))),
          Return(Bool(false)),
          .Stmts)
        Assign(
          Name("m0"),
          Call(Name("ord"), Subscript(Name("date"), Int(0))))
        Assign(
          Name("m1"),
          Call(Name("ord"), Subscript(Name("date"), Int(1))))
        Assign(
          Name("d0"),
          Call(Name("ord"), Subscript(Name("date"), Int(3))))
        Assign(
          Name("d1"),
          Call(Name("ord"), Subscript(Name("date"), Int(4))))
        Assign(
          Name("y0"),
          Call(Name("ord"), Subscript(Name("date"), Int(6))))
        Assign(
          Name("y1"),
          Call(Name("ord"), Subscript(Name("date"), Int(7))))
        Assign(
          Name("y2"),
          Call(Name("ord"), Subscript(Name("date"), Int(8))))
        Assign(
          Name("y3"),
          Call(Name("ord"), Subscript(Name("date"), Int(9))))
        If(BoolOp(
          "or",
          Compare(Name("m0"), CmpOp("<", Int(48))),
          Compare(Name("m0"), CmpOp(">", Int(57))),
          Compare(Name("m1"), CmpOp("<", Int(48))),
          Compare(Name("m1"), CmpOp(">", Int(57))),
          Compare(Name("d0"), CmpOp("<", Int(48))),
          Compare(Name("d0"), CmpOp(">", Int(57))),
          Compare(Name("d1"), CmpOp("<", Int(48))),
          Compare(Name("d1"), CmpOp(">", Int(57))),
          Compare(Name("y0"), CmpOp("<", Int(48))),
          Compare(Name("y0"), CmpOp(">", Int(57))),
          Compare(Name("y1"), CmpOp("<", Int(48))),
          Compare(Name("y1"), CmpOp(">", Int(57))),
          Compare(Name("y2"), CmpOp("<", Int(48))),
          Compare(Name("y2"), CmpOp(">", Int(57))),
          Compare(Name("y3"), CmpOp("<", Int(48))),
          Compare(Name("y3"), CmpOp(">", Int(57)))),
          Return(Bool(false)),
          .Stmts)
        Assign(
          Name("month"),
          BinOp(
            "-",
            BinOp(
              "+",
              BinOp("*", BinOp("-", Name("m0"), Int(48)), Int(10)),
              Name("m1")),
            Int(48)))
        Assign(
          Name("day"),
          BinOp(
            "-",
            BinOp(
              "+",
              BinOp("*", BinOp("-", Name("d0"), Int(48)), Int(10)),
              Name("d1")),
            Int(48)))
        If(BoolOp(
          "or",
          Compare(Name("month"), CmpOp("<", Int(1))),
          Compare(Name("month"), CmpOp(">", Int(12)))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("day"), CmpOp("<", Int(1))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("month"), CmpOp("==", Int(2))),
          Return(Compare(Name("day"), CmpOp("<=", Int(29)))),
          .Stmts)
        If(BoolOp(
          "or",
          Compare(Name("month"), CmpOp("==", Int(4))),
          Compare(Name("month"), CmpOp("==", Int(6))),
          Compare(Name("month"), CmpOp("==", Int(9))),
          Compare(Name("month"), CmpOp("==", Int(11)))),
          Return(Compare(Name("day"), CmpOp("<=", Int(30)))),
          .Stmts)
        Return(Compare(Name("day"), CmpOp("<=", Int(31))))))
endmodule
