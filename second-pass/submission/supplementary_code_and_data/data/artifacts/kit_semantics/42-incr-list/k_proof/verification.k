requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The source operation `x + 1` is defined by the supplied semantics for
  // Int, Bool, and Float values.  This predicate records exactly that domain.
  syntax Bool ::= isNumericVal(Val) [function, total]
  rule isNumericVal(_:Int)   => true
  rule isNumericVal(_:Bool)  => true
  rule isNumericVal(_:Float) => true
  rule isNumericVal(_:Val)   => false [owise]

  syntax Bool ::= allNumeric(ValSeq) [function, total]
  rule allNumeric(.ValSeq)                => true
  rule allNumeric(vCons(V:Val, R:ValSeq)) => isNumericVal(V) andBool allNumeric(R)

  // Exact iterative summary of the result-list contents.  applyBin is the
  // fixed semantics' own operator dispatch; no program execution is replaced.
  syntax ValSeq ::= incrAcc(ValSeq, ValSeq) [function, total]
  rule incrAcc(ACC:ValSeq, .ValSeq) => ACC
  rule incrAcc(ACC:ValSeq, vCons(V:Val, R:ValSeq))
    => incrAcc(
         valSeqConcat(ACC, vCons(applyBin("+", V, 1), .ValSeq)),
         R)
endmodule
