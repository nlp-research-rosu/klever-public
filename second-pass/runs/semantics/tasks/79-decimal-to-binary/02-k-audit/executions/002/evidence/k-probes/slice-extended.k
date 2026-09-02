requires "verification.k"

module SLICE-EXTENDED
  imports VERIFICATION

  syntax KItem ::= "#bang"
  rule <k> str(IS:IntSeq) ~> #bang => str(seqConcat(IS, iCons(33, .IntSeq))) ... </k>
endmodule
