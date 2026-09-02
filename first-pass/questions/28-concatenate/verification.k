requires "../../reference/src/lemmas.k"

module CONCATENATE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // the code-seq of a str Val (the Str cast twin, mirrors projectIntTotal)

  // str `+` on symbolic str Vals concatenates the code-seqs
  rule applyBin("+", V:Val, W:Val) => str(seqConcat(codesProj(V), codesProj(W)))
    requires isStr(V) andBool isStr(W) [simplification]

  // provenance marker
  syntax StrList ::= strListOf(ValSeq)

  // the concatenation of the string list's codes, in order
  syntax IntSeq ::= concatVS(StrList) [function, total]
  rule concatVS(strListOf(.ValSeq)) => .IntSeq [simplification]
  rule concatVS(strListOf(vCons(V:Val, R:ValSeq)))
    => seqConcat(codesProj(V), concatVS(strListOf(R)))
    requires isStr(V)
    [simplification]
endmodule
