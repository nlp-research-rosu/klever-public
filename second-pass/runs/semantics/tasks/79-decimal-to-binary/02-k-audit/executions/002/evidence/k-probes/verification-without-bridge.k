requires "reference-semantics/semantics.k"

module VERIFICATION-WITHOUT-BRIDGE
  imports MPY

  syntax KItem ::= "#runDecimalToBinaryFixed" "(" Int ")"

  rule #runDecimalToBinaryFixed(N:Int)
    => Call(
         closureVal(
           "decimal",
           Return(
             BinOp(
               "+",
               BinOp(
                 "+",
                 Str("db"),
                 Subscript(
                   Call(Name("bin"), Name("decimal")),
                   Slice(Int(2), NoBound, NoBound))),
               Str("db")))
           .Stmts,
           0),
         N)
endmodule
