requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // An exact name for the translator output in solution.mpy.  This equation
  // only constructs the source AST; MPY still performs loading, lookup,
  // argument evaluation, frame management, the body, and return control.
  syntax Module ::= "validDateProgram" [function, total]
  rule validDateProgram
    => Module(
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
             Name("month_tens"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(0))),
               Int(48)))
           Assign(
             Name("month_ones"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(1))),
               Int(48)))
           Assign(
             Name("day_tens"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(3))),
               Int(48)))
           Assign(
             Name("day_ones"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(4))),
               Int(48)))
           Assign(
             Name("year_thousands"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(6))),
               Int(48)))
           Assign(
             Name("year_hundreds"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(7))),
               Int(48)))
           Assign(
             Name("year_tens"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(8))),
               Int(48)))
           Assign(
             Name("year_ones"),
             BinOp(
               "-",
               Call(Name("ord"), Subscript(Name("date"), Int(9))),
               Int(48)))
           If(BoolOp(
             "or",
             Compare(Name("month_tens"), CmpOp("<", Int(0))),
             Compare(Name("month_tens"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("month_ones"), CmpOp("<", Int(0))),
             Compare(Name("month_ones"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("day_tens"), CmpOp("<", Int(0))),
             Compare(Name("day_tens"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("day_ones"), CmpOp("<", Int(0))),
             Compare(Name("day_ones"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("year_thousands"), CmpOp("<", Int(0))),
             Compare(Name("year_thousands"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("year_hundreds"), CmpOp("<", Int(0))),
             Compare(Name("year_hundreds"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("year_tens"), CmpOp("<", Int(0))),
             Compare(Name("year_tens"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           If(BoolOp(
             "or",
             Compare(Name("year_ones"), CmpOp("<", Int(0))),
             Compare(Name("year_ones"), CmpOp(">", Int(9)))),
             Return(Bool(false)),
             .Stmts)
           Assign(
             Name("month"),
             BinOp(
               "+",
               BinOp("*", Name("month_tens"), Int(10)),
               Name("month_ones")))
           Assign(
             Name("day"),
             BinOp(
               "+",
               BinOp("*", Name("day_tens"), Int(10)),
               Name("day_ones")))
           If(Compare(Name("month"), CmpOp("==", Int(2))),
             Return(
               BoolOp(
                 "and",
                 Compare(Name("day"), CmpOp(">=", Int(1))),
                 Compare(Name("day"), CmpOp("<=", Int(28))))),
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
           If(BoolOp(
             "or",
             Compare(Name("month"), CmpOp("==", Int(1))),
             Compare(Name("month"), CmpOp("==", Int(3))),
             Compare(Name("month"), CmpOp("==", Int(5))),
             Compare(Name("month"), CmpOp("==", Int(7))),
             Compare(Name("month"), CmpOp("==", Int(8))),
             Compare(Name("month"), CmpOp("==", Int(10))),
             Compare(Name("month"), CmpOp("==", Int(12)))),
             Return(
               BoolOp(
                 "and",
                 Compare(Name("day"), CmpOp(">=", Int(1))),
                 Compare(Name("day"), CmpOp("<=", Int(31))))),
             .Stmts)
           Return(Bool(false))))

  // Proof-local mathematical summaries.  None of these rules rewrites an
  // MPY program term or bypasses fixed-semantics execution.
  syntax Bool ::= asciiDigit(Int) [function, total]
  rule asciiDigit(C) => 48 <=Int C andBool C <=Int 57

  syntax Bool ::= validMonthDay(Int, Int) [function, total]
  rule validMonthDay(M, D)
    => (M ==Int 2
        andBool 1 <=Int D andBool D <=Int 29)
       orBool
       ((M ==Int 4 orBool M ==Int 6 orBool M ==Int 9 orBool M ==Int 11)
        andBool 1 <=Int D andBool D <=Int 30)
       orBool
       ((M ==Int 1 orBool M ==Int 3 orBool M ==Int 5
         orBool M ==Int 7 orBool M ==Int 8 orBool M ==Int 10
         orBool M ==Int 12)
        andBool 1 <=Int D andBool D <=Int 31)

  syntax Bool ::= validDateResult(IntSeq) [function, total]
  rule validDateResult(CS) => false
    requires isLen(CS) =/=Int 10

  rule validDateResult(CS)
    => intSeqAt(CS, 2) ==Int 45
       andBool intSeqAt(CS, 5) ==Int 45
       andBool asciiDigit(intSeqAt(CS, 0))
       andBool asciiDigit(intSeqAt(CS, 1))
       andBool asciiDigit(intSeqAt(CS, 3))
       andBool asciiDigit(intSeqAt(CS, 4))
       andBool asciiDigit(intSeqAt(CS, 6))
       andBool asciiDigit(intSeqAt(CS, 7))
       andBool asciiDigit(intSeqAt(CS, 8))
       andBool asciiDigit(intSeqAt(CS, 9))
       andBool validMonthDay(
         (intSeqAt(CS, 0) -Int 48) *Int 10
           +Int (intSeqAt(CS, 1) -Int 48),
         (intSeqAt(CS, 3) -Int 48) *Int 10
           +Int (intSeqAt(CS, 4) -Int 48))
    requires isLen(CS) ==Int 10
endmodule
