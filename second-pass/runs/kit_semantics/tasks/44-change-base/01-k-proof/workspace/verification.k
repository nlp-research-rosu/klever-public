requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical accumulator semantics for the repeated-division loop.
  // On the verified domain N >= 0 and B >= 2, the recursive argument strictly
  // decreases whenever N > 0.
  syntax IntSeq ::= baseAcc(Int, Int, IntSeq) [function, total]

  rule baseAcc(N:Int, _B:Int, ACC:IntSeq) => ACC
    requires N <=Int 0
    [simplification]

  rule baseAcc(N:Int, B:Int, ACC:IntSeq) => ACC
    requires N >Int 0 andBool B <Int 2
    [simplification]

  rule baseAcc(N:Int, B:Int, ACC:IntSeq)
    => baseAcc(
         (N -Int pyMod(N, B)) /Int B,
         B,
         iCons(48 +Int pyMod(N, B), ACC))
    requires N >Int 0 andBool B >=Int 2
    [simplification]

  // Complete signed-integer representation used by the entry claim.
  syntax IntSeq ::= changeBaseCodes(Int, Int) [function, total]

  rule changeBaseCodes(0, _B:Int) => iCons(48, .IntSeq)
    [simplification]

  rule changeBaseCodes(N:Int, B:Int) => baseAcc(N, B, .IntSeq)
    requires N >Int 0
    [simplification]

  rule changeBaseCodes(N:Int, B:Int)
    => iCons(45, baseAcc(0 -Int N, B, .IntSeq))
    requires N <Int 0
    [simplification]
endmodule
