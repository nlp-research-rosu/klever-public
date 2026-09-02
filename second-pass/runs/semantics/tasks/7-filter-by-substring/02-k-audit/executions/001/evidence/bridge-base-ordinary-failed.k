requires "reference-semantics/semantics.k"

module BRIDGE-BASE
  imports MPY

  syntax StrSeq ::= ".StrSeq"
                  | ssCons(IntSeq, StrSeq)

  syntax ValSeq ::= strVals(StrSeq)
  rule strVals(.StrSeq) => .ValSeq
  rule strVals(ssCons(S:IntSeq, SS:StrSeq))
    => vCons(str(S), strVals(SS))
endmodule
