requires "verification.k"

module X-OR-Y-BODY-MUT-VERIFICATION
  imports X-OR-Y-VERIFICATION

  // Material mutation: a found divisor returns x instead of y.
  syntax Stmts ::= "xOrYLoopBodyMutated" [macro]
  rule xOrYLoopBodyMutated
    => If(
         Compare(BinOp("%", Name("n"), Name("divisor")),
                 CmpOp("==", Int(0))),
         Return(Name("x")),
         .Stmts)
endmodule
