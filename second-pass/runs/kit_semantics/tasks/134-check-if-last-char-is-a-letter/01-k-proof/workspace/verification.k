requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Definitional summary of the prompt's predicate over the semantics' string
  // representation.  It does not rewrite or bypass any program computation.
  syntax Bool ::= standaloneLastLetter(IntSeq) [function, total]

  rule standaloneLastLetter(IS:IntSeq) => false
    requires isLen(IS) ==Int 0

  rule standaloneLastLetter(IS:IntSeq) => false
    requires isLen(IS) >Int 0
      andBool notBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))

  rule standaloneLastLetter(IS:IntSeq) => true
    requires isLen(IS) ==Int 1
      andBool isAlphaC(intSeqAt(IS, 0))

  rule standaloneLastLetter(IS:IntSeq)
    => intSeqAt(IS, isLen(IS) -Int 2) ==Int 32
    requires isLen(IS) >Int 1
      andBool isAlphaC(intSeqAt(IS, isLen(IS) -Int 1))

  // Derived constructor-disjointness lemma needed by the backend to simplify
  // the non-emptiness conjunct in str.isalpha() on a one-character string.
  rule iCons(_C:Int, _REST:IntSeq) ==K .IntSeq
    => false
    [simplification]

  // Equality of singleton code sequences is equality of their sole codes.
  rule iCons(C:Int, .IntSeq) ==K iCons(D:Int, .IntSeq)
    => C ==Int D
    [simplification]
endmodule
