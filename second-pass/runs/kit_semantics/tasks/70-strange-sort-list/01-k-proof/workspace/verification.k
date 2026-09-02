requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // True exactly when every element of the modeled Python list is an integer.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq)                => true
  rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)

  // Append the alternating leftmost/rightmost elements from S[L..R] to A.
  // The three guards partition all integer bounds, and recursive calls shrink
  // R - L by two.
  syntax ValSeq ::= strangeAcc(ValSeq, ValSeq, Int, Int) [function, total]
  rule strangeAcc(A:ValSeq, _:ValSeq, L:Int, R:Int) => A
    requires L >Int R
  rule strangeAcc(A:ValSeq, S:ValSeq, L:Int, R:Int)
    => valSeqConcat(A, vCons(valSeqAt(S, L), .ValSeq))
    requires L ==Int R
  rule strangeAcc(A:ValSeq, S:ValSeq, L:Int, R:Int)
    => strangeAcc(
         valSeqConcat(
           valSeqConcat(A, vCons(valSeqAt(S, L), .ValSeq)),
           vCons(valSeqAt(S, R), .ValSeq)),
         S, L +Int 1, R -Int 1)
    requires L <Int R

  // Removing a known-present integer key from a disjoint Map fragment leaves
  // exactly that fragment. This only canonicalizes the Map update emitted by
  // the fixed #pop rule.
  rule (M:Map K:Int |-> _V:Scope) [K <- undef] => M
    requires notBool K in_keys(M)
    [simplification]
endmodule
