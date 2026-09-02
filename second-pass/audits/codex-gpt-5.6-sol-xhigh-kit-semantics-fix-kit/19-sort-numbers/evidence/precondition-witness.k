requires "verification.k"

module PRECONDITION-WITNESS
  imports VERIFICATION

  claim <k>
          validNumeralTokens(
            splitWS(strToCodes("three one five"), .IntSeq, .ValSeq))
          => true
        </k>
endmodule
