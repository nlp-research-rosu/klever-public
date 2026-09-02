requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  syntax KItem ::= "#runDecimalToBinaryMutated" "(" Int ")"

  rule doSlice(
         str(iCons(_FIRST:Int, iCons(_SECOND:Int, REST:IntSeq))),
         someB(2),
         noB,
         noB)
    => str(REST)
    [priority(40)]

  // Material body mutation: final literal is "dx", not submitted "db".
  rule #runDecimalToBinaryMutated(N:Int)
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
               Str("dx")))
           .Stmts,
           0),
         N)
endmodule
