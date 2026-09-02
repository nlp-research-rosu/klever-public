requires "connection-verification.k"

module ADD-ELEMENTS-CONNECTION-SPEC
  imports ADD-ELEMENTS-CONNECTION-VERIFICATION

  claim [sl-adjust-connection]:
    <k>
      slAdjust(
        vsLen(PREFIX:ValSeq) +Int 1,
        vsLen(valSeqConcat(PREFIX, SUFFIX:ValSeq)) +Int 1,
        1
      )
      =>
      vsLen(PREFIX) +Int 1
      ...
    </k>

  claim [build-vs-connection]:
    <k>
      buildVS(
        vCons(HEAD:Val, valSeqConcat(PREFIX:ValSeq, SUFFIX:ValSeq)),
        0,
        vsLen(PREFIX) +Int 1,
        1
      )
      =>
      vCons(HEAD, PREFIX)
      ...
    </k>
endmodule
