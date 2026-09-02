requires "reference-semantics/semantics.k"

module SLICE-FIXED
  imports MPY

  syntax KItem ::= "#bang"
  rule <k> str(IS:IntSeq) ~> #bang => str(seqConcat(IS, iCons(33, .IntSeq))) ... </k>
endmodule
