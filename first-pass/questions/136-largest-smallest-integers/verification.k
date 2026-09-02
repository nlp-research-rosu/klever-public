// verification.k — largest_smallest_integers on the UNIFIED semantics. One pass with FOUR
// accumulators: a/hn (largest negative + has-it flag) and b/hp (smallest positive + has-it flag),
// each seeded to 0/False so the accumulators are never None during compares (the None only appears
// in the final map). Elements are symbolic Vals under allInt, compared via projectIntTotal (the
// reference cast bridge; a/b carry isInt in the loop invariant). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module LARGEST-SMALLEST-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL   // #if _ #then _ #else _ #fi in the entry postcondition

  syntax Expr ::= Val

  // normalize the program's `hn == False` test (HN ==Bool false) to notBool HN, lining it up with
  // maxNeg/minPos's `notBool HN` branch conditions.

  // maxNeg(CS, A, HN) = running largest NEGATIVE (value A + has-it flag HN), updated on the first
  // negative or a strictly larger one. Five rules = the program's nested If on the negative side.
  syntax Val ::= maxNeg(ValSeq, Val, Bool) [function, total]
  rule maxNeg(.ValSeq, A:Val, _:Bool) => A [simplification]
  rule maxNeg(vCons(X:Val, S:ValSeq), _A:Val, HN:Bool) => maxNeg(S, X, true)
    requires projectIntTotal(X) <Int 0 andBool notBool HN [simplification]
  rule maxNeg(vCons(X:Val, S:ValSeq), A:Val, HN:Bool) => maxNeg(S, X, true)
    requires projectIntTotal(X) <Int 0 andBool HN andBool projectIntTotal(X) >Int projectIntTotal(A) [simplification]
  rule maxNeg(vCons(X:Val, S:ValSeq), A:Val, HN:Bool) => maxNeg(S, A, true)
    requires projectIntTotal(X) <Int 0 andBool HN andBool notBool (projectIntTotal(X) >Int projectIntTotal(A)) [simplification]
  rule maxNeg(vCons(X:Val, S:ValSeq), A:Val, HN:Bool) => maxNeg(S, A, HN)
    requires notBool (projectIntTotal(X) <Int 0) [simplification]

  // minPos(CS, B, HP) = running smallest POSITIVE (symmetric).
  syntax Val ::= minPos(ValSeq, Val, Bool) [function, total]
  rule minPos(.ValSeq, B:Val, _:Bool) => B [simplification]
  rule minPos(vCons(X:Val, S:ValSeq), _B:Val, HP:Bool) => minPos(S, X, true)
    requires projectIntTotal(X) >Int 0 andBool notBool HP [simplification]
  rule minPos(vCons(X:Val, S:ValSeq), B:Val, HP:Bool) => minPos(S, X, true)
    requires projectIntTotal(X) >Int 0 andBool HP andBool projectIntTotal(X) <Int projectIntTotal(B) [simplification]
  rule minPos(vCons(X:Val, S:ValSeq), B:Val, HP:Bool) => minPos(S, B, true)
    requires projectIntTotal(X) >Int 0 andBool HP andBool notBool (projectIntTotal(X) <Int projectIntTotal(B)) [simplification]
  rule minPos(vCons(X:Val, S:ValSeq), B:Val, HP:Bool) => minPos(S, B, HP)
    requires notBool (projectIntTotal(X) >Int 0) [simplification]

  // hasNeg / hasPos = does any element have that sign (the per-side flag).
  syntax Bool ::= hasNeg(ValSeq) [function, total]
  rule hasNeg(.ValSeq)                => false                                       [simplification]
  rule hasNeg(vCons(X:Val, S:ValSeq)) => (projectIntTotal(X) <Int 0) orBool hasNeg(S) [simplification]

  syntax Bool ::= hasPos(ValSeq) [function, total]
  rule hasPos(.ValSeq)                => false                                       [simplification]
  rule hasPos(vCons(X:Val, S:ValSeq)) => (projectIntTotal(X) >Int 0) orBool hasPos(S) [simplification]
endmodule
