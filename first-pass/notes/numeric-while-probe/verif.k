requires "../../src/lemmas.k"
module NWPROBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  syntax Expr ::= Val
  // digit-sum accumulator matching the reference's // and % (pyMod-based) for n>0.
  syntax Int ::= digitAcc(Int, Int) [function, total]
  rule digitAcc(N:Int, R:Int) => R requires N <=Int 0 [simplification]
  rule digitAcc(N:Int, R:Int) => digitAcc((N -Int pyMod(N, 10)) /Int 10, R +Int pyMod(N, 10))
       requires N >Int 0 [simplification]
endmodule
