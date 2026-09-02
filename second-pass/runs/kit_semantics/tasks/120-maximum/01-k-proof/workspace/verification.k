requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A definitional name for the value produced by the source expression
  // sorted(arr)[len(arr) - k:].  This does not rewrite source execution.
  syntax Val ::= maximumResult(ValSeq, Int) [function, total]
  rule maximumResult(VS, K)
    => doSlice(
         list(sortVS(VS)),
         someB(vsLen(VS) -Int K),
         noB,
         noB)
endmodule
