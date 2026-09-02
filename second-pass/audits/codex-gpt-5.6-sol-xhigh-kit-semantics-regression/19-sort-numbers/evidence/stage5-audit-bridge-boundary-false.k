requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-BOUNDARY-FALSE
  imports MPY

  // Demonstrably false: comma is not whitespace, so the baseline splitWS
  // returns one token "one,two", not two tokens.
  claim [comma-is-space]:
    <k> splitWS(
          joinCodes(
            iCons(44, .IntSeq),
            vCons(str(strToCodes("one")),
              vCons(str(strToCodes("two")), .ValSeq))),
          .IntSeq,
          .ValSeq)
      => vCons(str(strToCodes("one")),
           vCons(str(strToCodes("two")), .ValSeq)) </k>
endmodule
