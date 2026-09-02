requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  syntax KItem ::= "#runDecimalToBinary" "(" Int ")"

  // Symbolic summary of the reference slice equations for a known two-code
  // prefix and an arbitrary tail.  Concrete execution uses the unextended
  // MPY-KRUN module; this proof-only rule prevents buildIS from getting stuck
  // solely because it cannot case-split an abstract IntSeq tail.
  rule doSlice(
         str(iCons(_FIRST:Int, iCons(_SECOND:Int, REST:IntSeq))),
         someB(2),
         noB,
         noB)
    => str(REST)
    [priority(40)]

  rule #runDecimalToBinary(N:Int)
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
