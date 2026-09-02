requires "semantic.k"

module VERIFICATION
  imports MPY

  // This is the exact tree emitted in solution.mpy, with ARG supplied
  // as the call argument.  It keeps specifications readable without adding a
  // semantic shortcut for specialFilter.
  syntax Program ::= SFTest ( Expr )
  syntax KItem ::= "clearFunctions"
  rule <k> SFTest(ARG) => Run(
    Module(
      FuncDef("specialFilter", Params("nums"),
        Assign(Name("count"), Int(0))
        For(Name("num"), Name("nums"),
          If(Compare(Name("num"), CmpOp(">", Int(10))),
            Assign(Name("first"), Name("num"))
            While(Compare(Name("first"), CmpOp(">=", Int(10))),
              Assign(Name("first"), BinOp("//", Name("first"), Int(10))))
            If(Compare(BinOp("%", Name("first"), Int(2)), CmpOp("==", Int(1))),
              If(Compare(BinOp("%", Name("num"), Int(2)), CmpOp("==", Int(1))),
                AugAssign(Name("count"), "+", Int(1)),
                .Stmts),
              .Stmts),
            .Stmts))
        Return(Name("count")))),
    Call(Name("specialFilter"), ARG)) ~> clearFunctions ... </k>

  rule <k> V:Value ~> clearFunctions => V ... </k>
       <functions> _ => .Map </functions>
endmodule
