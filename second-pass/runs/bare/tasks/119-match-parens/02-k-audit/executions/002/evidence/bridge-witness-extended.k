requires "verification.k"

module BRIDGE-WITNESS-EXTENDED
  imports MPY-VERIFICATION

  syntax Pgm ::= "missingBindingProbe" | "missingMatchBindingProbe"

  rule <k> missingBindingProbe =>
        invoke(
          closure("is_balanced", Params("s", "depth"),
            If(Compare(Name("depth"), CmpOp("<", Int(0))),
              Return(Bool(false)),
              .Stmts)
            If(Compare(Name("s"), CmpOp("==", Str(""))),
              Return(Compare(Name("depth"), CmpOp("==", Int(0)))),
              .Stmts)
            If(Compare(Subscript(Name("s"), Int(0)), CmpOp("==", Str("("))),
              Return(
                Call(
                  Name("is_balanced"),
                  Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
                  BinOp("+", Name("depth"), Int(1)))),
              .Stmts)
            Return(
              Call(
                Name("is_balanced"),
                Subscript(Name("s"), Slice(Int(1), NoBound, NoBound)),
                BinOp("-", Name("depth"), Int(1))))),
          strVal(parens(lp rp .PString)), intVal(0), .Values) ... </k>

  rule <k> missingMatchBindingProbe =>
        invoke(
          closure("match_parens", Params("lst"),
            If(Call(Name("is_balanced"),
              BinOp("+", Subscript(Name("lst"), Int(0)),
                         Subscript(Name("lst"), Int(1))),
              Int(0)),
              Return(Str("Yes")),
              .Stmts)
            If(Call(Name("is_balanced"),
              BinOp("+", Subscript(Name("lst"), Int(1)),
                         Subscript(Name("lst"), Int(0))),
              Int(0)),
              Return(Str("Yes")),
              .Stmts)
            Return(Str("No"))),
          listVal(
            strVal(parens(.PString)),
            strVal(parens(.PString)),
            .Values),
          .Values) ... </k>
endmodule
