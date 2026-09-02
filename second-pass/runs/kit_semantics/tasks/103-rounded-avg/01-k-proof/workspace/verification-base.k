requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  syntax Int ::= roundedInt(Int, Int) [function, total]
  rule roundedInt(N, M)
    => (N +Int M -Int pyMod(N +Int M, 2)) /Int 2
       +Int pyMod(N +Int M, 2)
            *Int pyMod(
              (N +Int M -Int pyMod(N +Int M, 2)) /Int 2,
              2)

  syntax Int ::= bitWeight(IntSeq) [function, total]
               | bitValue(IntSeq)  [function, total]
  rule bitWeight(.IntSeq) => 1
  rule bitWeight(iCons(_:Int, R:IntSeq)) => 2 *Int bitWeight(R)
  rule bitValue(.IntSeq) => 0
  rule bitValue(iCons(C:Int, R:IntSeq))
    => (C -Int 48) *Int bitWeight(R) +Int bitValue(R)

  syntax Bool ::= allBits(IntSeq)   [function, total]
                | startsOne(IntSeq) [function, total]
  rule allBits(.IntSeq) => true
  rule allBits(iCons(C:Int, R:IntSeq))
    => (C ==Int 48 orBool C ==Int 49) andBool allBits(R)
  rule startsOne(iCons(49, _:IntSeq)) => true
  rule startsOne(_:IntSeq) => false [owise]

  syntax IntSeq ::= loopDigits(Int, IntSeq)
    [function, total, symbol(loopDigits), no-evaluators]
  rule loopDigits(V, A) => A
    requires V <=Int 1
    [concrete]
  rule loopDigits(V, A)
    => loopDigits(
         (V -Int pyMod(V, 2)) /Int 2,
         iCons(48 +Int pyMod(V, 2), A))
    requires V >Int 1
    [concrete]
  rule loopDigits(V, A) => A
    requires V ==Int 1
    [simplification]
  rule loopDigits(Q, iCons(C, A))
    => loopDigits(2 *Int Q +Int (C -Int 48), A)
    requires Q >=Int 1
      andBool C >=Int 48
      andBool C <=Int 49
    [symbolic(Q), simplification(40)]

  rule 2 *Int ((V -Int pyMod(V, 2)) /Int 2) +Int pyMod(V, 2) => V
    requires V >=Int 0
    [simplification]
  rule 2 *Int ((V -Int ((V %Int 2 +Int 2) %Int 2)) /Int 2)
       +Int ((V %Int 2 +Int 2) %Int 2)
    => V
    requires V >=Int 0
    [simplification]
endmodule
