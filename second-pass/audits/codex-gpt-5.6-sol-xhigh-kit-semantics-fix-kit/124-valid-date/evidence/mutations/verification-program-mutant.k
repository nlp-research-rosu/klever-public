requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Exact translated body of solution.py, named so the specification can pin
  // the module binding to the program under verification.
  syntax Module ::= "validDateProgram" [function, total]
  syntax Stmts ::= "validDateBody" [function, total]
  syntax Val ::= "validDateClosure" [function, total]

  rule validDateProgram
    => Module(FuncDef("valid_date", Params("date"), Return(Bool(false))))

  rule validDateClosure
    => closureVal(("date", .ParamNames), validDateBody, 0)

  rule validDateBody
    => If(Compare(Call(Name("len"), Name("date")), CmpOp("!=", Int(10))),
         Return(Bool(false)),
         .Stmts)
       If(BoolOp(
            "or",
            (Compare(Subscript(Name("date"), Int(2)), CmpOp("!=", Str("-"))),
             Compare(Subscript(Name("date"), Int(5)), CmpOp("!=", Str("-"))),
             .Exprs)),
         Return(Bool(false)),
         .Stmts)
       Assign(
         Name("month_tens"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(0))), Int(48)))
       Assign(
         Name("month_ones"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(1))), Int(48)))
       Assign(
         Name("day_tens"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(3))), Int(48)))
       Assign(
         Name("day_ones"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(4))), Int(48)))
       Assign(
         Name("year_thousands"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(6))), Int(48)))
       Assign(
         Name("year_hundreds"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(7))), Int(48)))
       Assign(
         Name("year_tens"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(8))), Int(48)))
       Assign(
         Name("year_ones"),
         BinOp("-", Call(Name("ord"), Subscript(Name("date"), Int(9))), Int(48)))
       If(BoolOp(
            "or",
            (Compare(Name("month_tens"), CmpOp("<", Int(0))),
             Compare(Name("month_tens"), CmpOp(">", Int(9))),
             Compare(Name("month_ones"), CmpOp("<", Int(0))),
             Compare(Name("month_ones"), CmpOp(">", Int(9))),
             Compare(Name("day_tens"), CmpOp("<", Int(0))),
             Compare(Name("day_tens"), CmpOp(">", Int(9))),
             Compare(Name("day_ones"), CmpOp("<", Int(0))),
             Compare(Name("day_ones"), CmpOp(">", Int(9))),
             Compare(Name("year_thousands"), CmpOp("<", Int(0))),
             Compare(Name("year_thousands"), CmpOp(">", Int(9))),
             Compare(Name("year_hundreds"), CmpOp("<", Int(0))),
             Compare(Name("year_hundreds"), CmpOp(">", Int(9))),
             Compare(Name("year_tens"), CmpOp("<", Int(0))),
             Compare(Name("year_tens"), CmpOp(">", Int(9))),
             Compare(Name("year_ones"), CmpOp("<", Int(0))),
             Compare(Name("year_ones"), CmpOp(">", Int(9))),
             .Exprs)),
         Return(Bool(false)),
         .Stmts)
       Assign(
         Name("month"),
         BinOp("+", BinOp("*", Name("month_tens"), Int(10)), Name("month_ones")))
       Assign(
         Name("day"),
         BinOp("+", BinOp("*", Name("day_tens"), Int(10)), Name("day_ones")))
       If(BoolOp(
            "or",
            (Compare(Name("month"), CmpOp("<", Int(1))),
             Compare(Name("month"), CmpOp(">", Int(12))),
             Compare(Name("day"), CmpOp("<", Int(1))),
             .Exprs)),
         Return(Bool(false)),
         .Stmts)
       If(Compare(Name("month"), CmpOp("==", Int(2))),
         Return(Compare(Name("day"), CmpOp("<=", Int(29)))),
         .Stmts)
       If(BoolOp(
            "or",
            (Compare(Name("month"), CmpOp("==", Int(4))),
             Compare(Name("month"), CmpOp("==", Int(6))),
             Compare(Name("month"), CmpOp("==", Int(9))),
             Compare(Name("month"), CmpOp("==", Int(11))),
             .Exprs)),
         Return(Compare(Name("day"), CmpOp("<=", Int(30)))),
         .Stmts)
       Return(Compare(Name("day"), CmpOp("<=", Int(31))))

  // Mathematical decoding used only in the postcondition. These functions do
  // not intercept or replace any program operation.
  syntax Int ::= dateDigit(Int) [function, total]
               | dateTwoDigits(Int, Int) [function, total]
  syntax Bool ::= badDateDigit(Int) [function, total]
                | validDate10(Int, Int, Int, Int, Int,
                              Int, Int, Int, Int, Int) [function, total]

  rule dateDigit(C) => C -Int 48
  rule dateTwoDigits(A, B) => dateDigit(A) *Int 10 +Int dateDigit(B)
  rule badDateDigit(C) => dateDigit(C) <Int 0 orBool dateDigit(C) >Int 9

  rule validDate10(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9)
    => #if C2 =/=Int 45 orBool C5 =/=Int 45
       #then false
       #else #if badDateDigit(C0) orBool badDateDigit(C1)
                  orBool badDateDigit(C3) orBool badDateDigit(C4)
                  orBool badDateDigit(C6) orBool badDateDigit(C7)
                  orBool badDateDigit(C8) orBool badDateDigit(C9)
             #then false
             #else #if dateTwoDigits(C0, C1) <Int 1
                        orBool dateTwoDigits(C0, C1) >Int 12
                        orBool dateTwoDigits(C3, C4) <Int 1
                   #then false
                   #else #if dateTwoDigits(C0, C1) ==Int 2
                         #then dateTwoDigits(C3, C4) <=Int 29
                         #else #if dateTwoDigits(C0, C1) ==Int 4
                                    orBool dateTwoDigits(C0, C1) ==Int 6
                                    orBool dateTwoDigits(C0, C1) ==Int 9
                                    orBool dateTwoDigits(C0, C1) ==Int 11
                               #then dateTwoDigits(C3, C4) <=Int 30
                               #else dateTwoDigits(C3, C4) <=Int 31
                               #fi
                         #fi
                   #fi
             #fi
       #fi
endmodule
