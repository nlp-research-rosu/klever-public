requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Relational description of the values emitted from I through N.  F and T
  // are the factorial and triangular accumulators before step I.
  syntax Bool ::= outputOK(ValSeq, Int, Int, Int, Int)
    [function, total]
  rule outputOK(.ValSeq, I:Int, N:Int, _F:Int, _T:Int) => true
    requires I >Int N
  rule outputOK(vCons(V:Int, REST:ValSeq),
                I:Int, N:Int, F:Int, T:Int)
    => outputOK(REST, I +Int 1, N, F *Int I, T +Int I)
    requires I <=Int N andBool pyMod(I, 2) ==Int 0
      andBool V ==Int F *Int I
  rule outputOK(vCons(V:Int, REST:ValSeq),
                I:Int, N:Int, F:Int, T:Int)
    => outputOK(REST, I +Int 1, N, F *Int I, T +Int I)
    requires I <=Int N andBool notBool (pyMod(I, 2) ==Int 0)
      andBool V ==Int T +Int I

  // Associativity is the algebraic fact needed when one append has extended
  // an arbitrary already-produced prefix before the circularity is reused.
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]

  // Cancellation exposes the existential suffix used by outputOK.
  rule { valSeqConcat(P:ValSeq, A:ValSeq)
         #Equals valSeqConcat(P, B:ValSeq) }
    => { A #Equals B }
    [simplification]
  rule { P:ValSeq #Equals valSeqConcat(P, A:ValSeq) }
    => { .ValSeq #Equals A }
    [simplification]
endmodule
