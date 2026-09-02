requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact closure corresponding to the sole FuncDef in solution.mpy.
  syntax Val ::= "validDateClosure" [function, total]
  rule validDateClosure
    => closureVal(
         ("date", .ParamNames),
         If(Compare(Call(Name("len"), Name("date")),
                    CmpOp("!=", Int(10))),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(Compare(Subscript(Name("date"), Int(2)),
                    CmpOp("!=", Str("-"))),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(Compare(Subscript(Name("date"), Int(5)),
                    CmpOp("!=", Str("-"))),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(0)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(0)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(1)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(1)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(3)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(3)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(4)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(4)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(6)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(6)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(7)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(7)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(8)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(8)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Subscript(Name("date"), Int(9)),
                            CmpOp("<", Str("0"))),
                    Compare(Subscript(Name("date"), Int(9)),
                            CmpOp(">", Str("9"))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         Assign(Name("month_text"),
                Subscript(Name("date"), Slice(NoBound, Int(2), NoBound)))
         Assign(Name("day_text"),
                Subscript(Name("date"), Slice(Int(3), Int(5), NoBound)))
         Assign(Name("month"), Call(Name("int"), (Name("month_text"), .Exprs)))
         Assign(Name("day"), Call(Name("int"), (Name("day_text"), .Exprs)))
         If(BoolOp("or",
                   (Compare(Name("month"), CmpOp("<", Int(1))),
                    Compare(Name("month"), CmpOp(">", Int(12))),
                    .Exprs)),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(Compare(Name("day"), CmpOp("<", Int(1))),
            Return(Bool(false)) .Stmts,
            .Stmts)
         If(Compare(Name("month"), CmpOp("==", Int(2))),
            Return(Compare(Name("day"), CmpOp("<=", Int(29)))) .Stmts,
            .Stmts)
         If(BoolOp("or",
                   (Compare(Name("month"), CmpOp("==", Int(4))),
                    Compare(Name("month"), CmpOp("==", Int(6))),
                    Compare(Name("month"), CmpOp("==", Int(9))),
                    Compare(Name("month"), CmpOp("==", Int(11))),
                    .Exprs)),
            Return(Compare(Name("day"), CmpOp("<=", Int(30)))) .Stmts,
            .Stmts)
         Return(Compare(Name("day"), CmpOp("<=", Int(31)))) .Stmts,
         0)

  // Decimal values of the fixed-width month and day fields.
  syntax Int ::= twoDigit(Int, Int) [function, total]
  rule twoDigit(A, B) => (A -Int 48) *Int 10 +Int (B -Int 48)

  // The contract's month-dependent inclusive day limit. Outside the valid
  // month range the value is immaterial because validDate10 also rejects it.
  syntax Int ::= daysInMonth(Int) [function, total]
  rule daysInMonth(M)
    => #if M ==Int 2
       #then 29
       #else #if M ==Int 4 orBool M ==Int 6 orBool
                 M ==Int 9 orBool M ==Int 11
             #then 30
             #else 31
             #fi
       #fi

  // Mathematical validity predicate for an exact ten-code ASCII string.
  syntax Bool ::= validDate10(
                    Int, Int, Int, Int, Int,
                    Int, Int, Int, Int, Int) [function, total]
  rule validDate10(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9)
    => isDigitC(C0) andBool isDigitC(C1)
       andBool C2 ==Int 45
       andBool isDigitC(C3) andBool isDigitC(C4)
       andBool C5 ==Int 45
       andBool isDigitC(C6) andBool isDigitC(C7)
       andBool isDigitC(C8) andBool isDigitC(C9)
       andBool twoDigit(C0, C1) >=Int 1
       andBool twoDigit(C0, C1) <=Int 12
       andBool twoDigit(C3, C4) >=Int 1
       andBool twoDigit(C3, C4) <=Int daysInMonth(twoDigit(C0, C1))
endmodule
