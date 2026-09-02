requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Guarded total projection from the dynamic Val sort to Int.  This is the
  // standard total twin of K's partial subsort cast; it is used only under
  // definedProjectInt and collapses on every statically known Int.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twin for the exact fixed rule
  // applyBin("+", I1:Int, I2:Int) => I1 +Int I2.  It lets the source's
  // value + 0 normalization refine a dynamically sorted list head.
  rule applyBin("+", V:Val, I:Int)
    => projectIntTotal(V) +Int I
    requires definedProjectInt(V)
    [simplification]

  // Exact contract domain: finite list payloads containing only non-negative
  // Python integers.
  syntax Bool ::= allNonNegative(ValSeq) [function, total]
  rule allNonNegative(.ValSeq) => true
  rule allNonNegative(vCons(V:Val, R:ValSeq))
    => definedProjectInt(V)
       andBool projectIntTotal(V) >=Int 0
       andBool allNonNegative(R)

  // shouldTake exactly mirrors the nested source condition.  A negative
  // current best is the source sentinel; otherwise only a strictly smaller
  // even value replaces it.
  syntax Bool ::= shouldTake(Int, Int) [function, total]
  rule shouldTake(B:Int, V:Int)
    => pyMod(V, 2) ==Int 0
       andBool (B <Int 0 orBool V <Int B)

  syntax Int ::= nextBest(Int, Int) [function, total]
  rule nextBest(B:Int, V:Int) => V
    requires shouldTake(B, V)
  rule nextBest(B:Int, V:Int) => B
    requires notBool shouldTake(B, V)

  syntax Int ::= nextBestIndex(Int, Int, Int, Int) [function, total]
  rule nextBestIndex(B:Int, _J:Int, V:Int, I:Int) => I
    requires shouldTake(B, V)
  rule nextBestIndex(B:Int, J:Int, V:Int, _I:Int) => J
    requires notBool shouldTake(B, V)

  syntax Int ::= scanBest(ValSeq, Int, Int) [function, total]
  rule scanBest(.ValSeq, _I:Int, B:Int) => B
  rule scanBest(vCons(V:Val, R:ValSeq), I:Int, B:Int)
    => scanBest(R, I +Int 1, nextBest(B, projectIntTotal(V)))

  syntax Int ::= scanBestIndex(ValSeq, Int, Int, Int)
    [function, total]
  rule scanBestIndex(.ValSeq, _I:Int, _B:Int, J:Int) => J
  rule scanBestIndex(
         vCons(V:Val, R:ValSeq), I:Int, B:Int, J:Int)
    => scanBestIndex(
         R,
         I +Int 1,
         nextBest(B, projectIntTotal(V)),
         nextBestIndex(B, J, projectIntTotal(V), I))

  syntax Int ::= afterIndex(ValSeq, Int) [function, total]
  rule afterIndex(.ValSeq, I:Int) => I
  rule afterIndex(vCons(_V:Val, R:ValSeq), I:Int)
    => afterIndex(R, I +Int 1)

  syntax Val ::= resultList(Int, Int) [function, total]
  rule resultList(B:Int, _J:Int) => list(.ValSeq)
    requires B <Int 0
  rule resultList(B:Int, J:Int)
    => list(vCons(B, vCons(J, .ValSeq)))
    requires B >=Int 0
endmodule
