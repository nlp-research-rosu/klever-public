requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The suffix of the final result produced by loop iterations I .. N-1.
  // SV is sorted(buildVS(VS, 0, N, 3)).
  syntax ValSeq ::= mergeThirdFrom(ValSeq, ValSeq, Int, Int)
                    [function, total]

  rule mergeThirdFrom(_VS, _SV, I, N) => .ValSeq
    requires I >=Int N

  rule mergeThirdFrom(VS, SV, I, N)
    => vCons(valSeqAt(SV, I /Int 3),
             mergeThirdFrom(VS, SV, I +Int 1, N))
    requires I <Int N andBool pyMod(I, 3) ==Int 0

  rule mergeThirdFrom(VS, SV, I, N)
    => vCons(valSeqAt(VS, I),
             mergeThirdFrom(VS, SV, I +Int 1, N))
    requires I <Int N andBool pyMod(I, 3) =/=Int 0

  syntax ValSeq ::= sortThirdResult(ValSeq)
                    [function, total, no-evaluators]

  // A folding orientation for the exact complete-result definition avoids
  // unbounded eager unfolding when VS is symbolic.
  rule mergeThirdFrom(
         VS,
         sortVS(buildVS(VS, 0, vsLen(VS), 3)),
         0,
         vsLen(VS))
    => sortThirdResult(VS)
    [simplification]

  rule sortThirdResult(VS) => .ValSeq
    requires vsLen(VS) <=Int 0
    [simplification]

  // Derived from the two exhaustive equations for valSeqConcat in MPY-LIST.
  rule valSeqConcat(valSeqConcat(A, B), C)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

  // Right identity, also derived by structural induction from MPY-LIST.
  rule valSeqConcat(A, .ValSeq) => A [simplification]
endmodule
