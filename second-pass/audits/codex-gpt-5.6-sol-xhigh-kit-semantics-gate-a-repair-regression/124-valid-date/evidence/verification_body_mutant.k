requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This nullary function is only a checked textual container for the exact
  // py2mpy translation of solution.py.  Its equation exposes the AST; all
  // function lookup, argument evaluation, body execution, return control, and
  // state cleanup are performed by the supplied MPY rules.
  syntax Module ::= "solutionProgram" [function, total]
// BEGIN_SOLUTION_MPY
rule solutionProgram =>
Module(
  FuncDef("valid_date", Params("date"),
    If(Compare(Call(Name("len"), Name("date")), CmpOp("!=", Int(10))),
      Return(Bool(false)),
      .Stmts)
    If(BoolOp(
      "or",
      Compare(Subscript(Name("date"), Int(2)), CmpOp("!=", Str("-"))),
      Compare(Subscript(Name("date"), Int(5)), CmpOp("!=", Str("-")))),
      Return(Bool(false)),
      .Stmts)
    Assign(
      Name("c0"),
      Call(Name("ord"), Subscript(Name("date"), Int(0))))
    Assign(
      Name("c1"),
      Call(Name("ord"), Subscript(Name("date"), Int(1))))
    Assign(
      Name("c3"),
      Call(Name("ord"), Subscript(Name("date"), Int(3))))
    Assign(
      Name("c4"),
      Call(Name("ord"), Subscript(Name("date"), Int(4))))
    Assign(
      Name("c6"),
      Call(Name("ord"), Subscript(Name("date"), Int(6))))
    Assign(
      Name("c7"),
      Call(Name("ord"), Subscript(Name("date"), Int(7))))
    Assign(
      Name("c8"),
      Call(Name("ord"), Subscript(Name("date"), Int(8))))
    Assign(
      Name("c9"),
      Call(Name("ord"), Subscript(Name("date"), Int(9))))
    If(BoolOp(
      "or",
      Compare(Name("c0"), CmpOp("<", Int(48))),
      Compare(Name("c0"), CmpOp(">", Int(57))),
      Compare(Name("c1"), CmpOp("<", Int(48))),
      Compare(Name("c1"), CmpOp(">", Int(57))),
      Compare(Name("c3"), CmpOp("<", Int(48))),
      Compare(Name("c3"), CmpOp(">", Int(57))),
      Compare(Name("c4"), CmpOp("<", Int(48))),
      Compare(Name("c4"), CmpOp(">", Int(57))),
      Compare(Name("c6"), CmpOp("<", Int(48))),
      Compare(Name("c6"), CmpOp(">", Int(57))),
      Compare(Name("c7"), CmpOp("<", Int(48))),
      Compare(Name("c7"), CmpOp(">", Int(57))),
      Compare(Name("c8"), CmpOp("<", Int(48))),
      Compare(Name("c8"), CmpOp(">", Int(57))),
      Compare(Name("c9"), CmpOp("<", Int(48))),
      Compare(Name("c9"), CmpOp(">", Int(57)))),
      Return(Bool(false)),
      .Stmts)
    Assign(
      Name("month"),
      BinOp(
        "-",
        BinOp(
          "+",
          BinOp("*", BinOp("-", Name("c0"), Int(48)), Int(10)),
          Name("c1")),
        Int(48)))
    Assign(
      Name("day"),
      BinOp(
        "-",
        BinOp(
          "+",
          BinOp("*", BinOp("-", Name("c3"), Int(48)), Int(10)),
          Name("c4")),
        Int(48)))
    If(BoolOp(
      "or",
      Compare(Name("month"), CmpOp("<", Int(1))),
      Compare(Name("month"), CmpOp(">", Int(12))),
      Compare(Name("day"), CmpOp("<", Int(1)))),
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
    Return(Bool(false))))
// END_SOLUTION_MPY

  // Mathematical contract for an input already known to contain ten codes.
  // The source's two-digit int conversions are the Horner expressions below.
  syntax IntSeq ::= dateCodes(
      Int, Int, Int, Int, Int, Int, Int, Int, Int, Int
    ) [function, total]
  rule dateCodes(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9)
    => iCons(C0, iCons(C1, iCons(C2, iCons(C3, iCons(C4,
       iCons(C5, iCons(C6, iCons(C7, iCons(C8, iCons(C9, .IntSeq))))))))))

  syntax Bool ::= validDate10(
      Int, Int, Int, Int, Int, Int, Int, Int, Int, Int
    ) [function, total]
  rule validDate10(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9)
    => isDigitC(C0) andBool isDigitC(C1)
       andBool C2 ==Int 45
       andBool isDigitC(C3) andBool isDigitC(C4)
       andBool C5 ==Int 45
       andBool isDigitC(C6) andBool isDigitC(C7)
       andBool isDigitC(C8) andBool isDigitC(C9)
       andBool monthDayOK(
         ((C0 -Int 48) *Int 10) +Int (C1 -Int 48),
         ((C3 -Int 48) *Int 10) +Int (C4 -Int 48)
       )

  syntax Bool ::= monthDayOK(Int, Int) [function, total]
  rule monthDayOK(M, D)
    => M >=Int 1 andBool M <=Int 12 andBool D >=Int 1
       andBool (
         (M ==Int 2 andBool D <=Int 29)
         orBool (
           (M ==Int 4 orBool M ==Int 6 orBool M ==Int 9 orBool M ==Int 11)
           andBool D <=Int 30
         )
         orBool (
           notBool (
             M ==Int 2 orBool M ==Int 4 orBool M ==Int 6
             orBool M ==Int 9 orBool M ==Int 11
           )
           andBool D <=Int 31
         )
       )

endmodule
