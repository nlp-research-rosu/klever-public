requires "verification.k"

module SEARCH-WITNESS-EXTENSION
  imports SEARCH-VERIFICATION

  syntax IntValSeq ::= "oneSeq" [macro]
                       | "twoSeq" [macro]
                       | "twoTwoSeq" [macro]
                       | "exampleSeq" [macro]

  rule oneSeq => vCons(1, .ValSeq)
  rule twoSeq => vCons(2, .ValSeq)
  rule twoTwoSeq => vCons(2, vCons(2, .ValSeq))
  rule exampleSeq
    => vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq))))))
endmodule
