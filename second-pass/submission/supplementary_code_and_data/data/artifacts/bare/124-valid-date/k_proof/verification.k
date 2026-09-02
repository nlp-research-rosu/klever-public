requires "semantic.k"

module VALID-DATE-VERIFICATION
  imports MPY

  // This constant is the exact py2mpy constructor tree whose SHA-256 is
  // checked by prove.sh before proving. It is kept here so claims execute the
  // submitted program, rather than a second handwritten implementation.
  syntax Program ::= "solutionProgram" [function]
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
          .Stmts)
        Assign(Name("month"), Call(Name("int"), Name("month_text")))
        Assign(Name("day"), Call(Name("int"), Name("day_text")))
        If(BoolOp(
          "or",
          Compare(Name("month"), CmpOp("<", Int(1))),
          Compare(Name("month"), CmpOp(">", Int(12)))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Name("month"), CmpOp("==", Int(2))),
          Return(
            BoolOp(
              "and",
              Compare(Name("day"), CmpOp(">=", Int(1))),
              Compare(Name("day"), CmpOp("<=", Int(29))))),
          .Stmts)
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
          .Stmts)
        Return(
          BoolOp(
            "and",
            Compare(Name("day"), CmpOp(">=", Int(1))),
            Compare(Name("day"), CmpOp("<=", Int(31)))))))

  // An independent, declarative reading of the English contract.
  syntax Bool ::= validDateSpec(String) [function]
  rule validDateSpec(S)
    => specLength(lengthString(S) ==Int 10, S)

  syntax Bool ::= specLength(Bool, String) [function]
  rule specLength(false, _) => false
  rule specLength(true, S)
    => specSeparators(
         substrString(S, 2, 3) ==String "-"
         andBool substrString(S, 5, 6) ==String "-",
         S)

  syntax Bool ::= specSeparators(Bool, String) [function]
  rule specSeparators(false, _) => false
  rule specSeparators(true, S)
    => specDigits(
         isDigits(substrString(S, 0, 2))
         andBool isDigits(substrString(S, 3, 5))
         andBool isDigits(substrString(S, 6, 10)),
         S)

  syntax Bool ::= specDigits(Bool, String) [function]
  rule specDigits(false, _) => false
  rule specDigits(true, S)
    => validMonthDay(
         String2Int(substrString(S, 0, 2)),
         String2Int(substrString(S, 3, 5)))

  syntax Bool ::= validMonthDay(Int, Int) [function]
  rule validMonthDay(M, D)
    => M >=Int 1 andBool M <=Int 12 andBool D >=Int 1
       andBool (
         (M ==Int 2 andBool D <=Int 29)
         orBool (isThirtyDayMonth(M) andBool D <=Int 30)
         orBool (M =/=Int 2 andBool notBool isThirtyDayMonth(M)
                 andBool D <=Int 31))

  syntax Bool ::= isThirtyDayMonth(Int) [function]
  rule isThirtyDayMonth(M)
    => M ==Int 4 orBool M ==Int 6 orBool M ==Int 9 orBool M ==Int 11
endmodule

module VERIFICATION
  imports VALID-DATE-VERIFICATION
endmodule
