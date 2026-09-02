requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-PROGRAM-IDENTITY
  imports VALID-DATE-VERIFICATION

  claim <k> solutionProgram => Module(
  FuncDef("valid_date", Params("date"),
    If(Compare(Call(Name("len"), Name("date")), CmpOp("!=", Int(10))),
      Return(Bool(false)),
      )
    If(BoolOp(
      "or",
      Compare(Subscript(Name("date"), Int(2)), CmpOp("!=", Str("-"))),
      Compare(Subscript(Name("date"), Int(5)), CmpOp("!=", Str("-")))),
      Return(Bool(false)),
      )
    Assign(
      Name("month_text"),
      Subscript(Name("date"), Slice(Int(0), Int(2), NoBound)))
    Assign(
      Name("day_text"),
      Subscript(Name("date"), Slice(Int(3), Int(5), NoBound)))
    Assign(
      Name("year_text"),
      Subscript(Name("date"), Slice(Int(6), Int(10), NoBound)))
    If(UnaryOp(
      "not",
      BoolOp(
        "and",
        Call(Attribute(Name("month_text"), "isdigit"), ),
        Call(Attribute(Name("day_text"), "isdigit"), ),
        Call(Attribute(Name("year_text"), "isdigit"), ))),
      Return(Bool(false)),
      )
    Assign(Name("month"), Call(Name("int"), Name("month_text")))
    Assign(Name("day"), Call(Name("int"), Name("day_text")))
    If(BoolOp(
      "or",
      Compare(Name("month"), CmpOp("<", Int(1))),
      Compare(Name("month"), CmpOp(">", Int(12)))),
      Return(Bool(false)),
      )
    If(Compare(Name("month"), CmpOp("==", Int(2))),
      Return(
        BoolOp(
          "and",
          Compare(Name("day"), CmpOp(">=", Int(1))),
          Compare(Name("day"), CmpOp("<=", Int(29))))),
      )
    If(BoolOp(
      "or",
      Compare(Name("month"), CmpOp("==", Int(4))),
      Compare(Name("month"), CmpOp("==", Int(6))),
      Compare(Name("month"), CmpOp("==", Int(9))),
      Compare(Name("month"), CmpOp("==", Int(11)))),
      Return(
        BoolOp(
          "and",
          Compare(Name("day"), CmpOp(">=", Int(1))),
          Compare(Name("day"), CmpOp("<=", Int(30))))),
      )
    Return(
      BoolOp(
        "and",
        Compare(Name("day"), CmpOp(">=", Int(1))),
        Compare(Name("day"), CmpOp("<=", Int(31))))))) </k>
endmodule
