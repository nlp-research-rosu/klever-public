requires "verification.k"

module VALIDATION
  imports VERIFICATION

  // Exact source closure used only by negative validation probes.
  syntax Val ::= "originalCountNumsClosure" [function, total]
  rule originalCountNumsClosure
    => closureVal(
         "arr" , .ParamNames,
         Assign(Name("count"), Int(0))
         For(
           Name("num"),
           Name("arr"),
           If(Compare(Name("num"), CmpOp("<", Int(0))),
             Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
             Assign(Name("n"), Name("num")) .Stmts)
           Assign(Name("digit_sum"), Int(0))
           Assign(Name("first_digit"), Int(0))
           Assign(Name("char"), Str("0"))
           Assign(Name("digit"), Int(0))
           For(
             Name("char"),
             Call(Name("str"), Name("n")),
             Assign(Name("digit"), Call(Name("int"), Name("char")))
             If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
               Assign(Name("first_digit"), Name("digit")) .Stmts,
               .Stmts)
             AugAssign(Name("digit_sum"), "+", Name("digit"))
             .Stmts)
           If(Compare(Name("num"), CmpOp("<", Int(0))),
             AugAssign(
               Name("digit_sum"),
               "-",
               BinOp("*", Int(2), Name("first_digit")))
             .Stmts,
             .Stmts)
           If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
             AugAssign(Name("count"), "+", Int(1)) .Stmts,
             .Stmts)
           .Stmts)
         Return(Name("count"))
         .Stmts,
         0)

  // Material mutation: initialize count to one instead of zero.
  syntax Val ::= "mutatedCountNumsClosure" [function, total]
  rule mutatedCountNumsClosure
    => closureVal(
         "arr" , .ParamNames,
         Assign(Name("count"), Int(1))
         For(
           Name("num"),
           Name("arr"),
           If(Compare(Name("num"), CmpOp("<", Int(0))),
             Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
             Assign(Name("n"), Name("num")) .Stmts)
           Assign(Name("digit_sum"), Int(0))
           Assign(Name("first_digit"), Int(0))
           Assign(Name("char"), Str("0"))
           Assign(Name("digit"), Int(0))
           For(
             Name("char"),
             Call(Name("str"), Name("n")),
             Assign(Name("digit"), Call(Name("int"), Name("char")))
             If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
               Assign(Name("first_digit"), Name("digit")) .Stmts,
               .Stmts)
             AugAssign(Name("digit_sum"), "+", Name("digit"))
             .Stmts)
           If(Compare(Name("num"), CmpOp("<", Int(0))),
             AugAssign(
               Name("digit_sum"),
               "-",
               BinOp("*", Int(2), Name("first_digit")))
             .Stmts,
             .Stmts)
           If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
             AugAssign(Name("count"), "+", Int(1)) .Stmts,
             .Stmts)
           .Stmts)
         Return(Name("count"))
         .Stmts,
         0)
endmodule
