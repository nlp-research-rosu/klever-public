requires "domain.k"

module CONNECTION-SPEC
  imports STRING-SEQUENCE-DOMAIN

  claim [string-iterator-normalization]:
    <k>
      #iterNext(list(vCons(V:Val, REST:ValSeq))) ~> CONT:K
      =>
      #iterYield(
        str(stringCodes(V)),
        list(REST))
      ~> CONT
    </k>
    requires isStringVal(V)
endmodule
