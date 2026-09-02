requires "reference-semantics/semantics.k"

module SEMANTIC-BOUNDARY
  imports MPY

  // The supplied model recognizes SPACE but not U+00A0 as whitespace.
  claim [modeled-result]:
    <k>
      splitWS(
        iCons(97, iCons(32, iCons(98, iCons(160, iCons(99, .IntSeq))))),
        .IntSeq,
        .ValSeq)
      =>
      vCons(
        str(iCons(97, .IntSeq)),
        vCons(str(iCons(98, iCons(160, iCons(99, .IntSeq)))), .ValSeq))
    </k>

  // CPython str.split() instead produces "a", "b", "c" for this same input.
  claim [cpython-result]:
    <k>
      splitWS(
        iCons(97, iCons(32, iCons(98, iCons(160, iCons(99, .IntSeq))))),
        .IntSeq,
        .ValSeq)
      =>
      vCons(
        str(iCons(97, .IntSeq)),
        vCons(
          str(iCons(98, .IntSeq)),
          vCons(str(iCons(99, .IntSeq)), .ValSeq)))
    </k>
endmodule
