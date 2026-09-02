requires "reference-semantics/semantics.k"

module VALID-DATE-VERIFICATION
  imports MPY

  // The translated body from solution.mpy, named so the symbolic claims can
  // install exactly the implementation being verified in the module scope.
  syntax Stmts ::= "validDateBody" [function, total]
  rule validDateBody =>
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
    Return(Compare(Name("day"), CmpOp("<=", Int(31))))

  syntax Val ::= "validDateClosure" [function, total]
  rule validDateClosure => closureVal("date", validDateBody, 0)

  syntax Module ::= "validDateModule" [function, total]
  rule validDateModule =>
    Module(FuncDef("valid_date", Params("date"), validDateBody))

  // Independent executable form of the natural-language contract.
  syntax Bool ::= digitCode(Int) [function, total]
  rule digitCode(C:Int) => 48 <=Int C andBool C <=Int 57

  syntax Int ::= dateNumber(Int, Int) [function, total]
  rule dateNumber(T:Int, O:Int) => ((T -Int 48) *Int 10) +Int O -Int 48

  syntax Int ::= dateLimit(Int) [function, total]
  rule dateLimit(M:Int) =>
    #if M ==Int 2
    #then 29
    #else
      #if M ==Int 4 orBool M ==Int 6 orBool M ==Int 9 orBool M ==Int 11
      #then 30
      #else 31
      #fi
    #fi

  syntax Bool ::= validDate10(
    Int, Int, Int, Int, Int, Int, Int, Int, Int, Int
  ) [function, total]
  rule validDate10(
    M0:Int, M1:Int, SEP1:Int, D0:Int, D1:Int, SEP2:Int,
    Y0:Int, Y1:Int, Y2:Int, Y3:Int
  ) =>
    SEP1 ==Int 45
    andBool SEP2 ==Int 45
    andBool digitCode(M0)
    andBool digitCode(M1)
    andBool digitCode(D0)
    andBool digitCode(D1)
    andBool digitCode(Y0)
    andBool digitCode(Y1)
    andBool digitCode(Y2)
    andBool digitCode(Y3)
    andBool 1 <=Int dateNumber(M0, M1)
    andBool dateNumber(M0, M1) <=Int 12
    andBool 1 <=Int dateNumber(D0, D1)
    andBool dateNumber(D0, D1) <=Int dateLimit(dateNumber(M0, M1))
endmodule
