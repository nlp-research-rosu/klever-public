requires "verification.k"

module INTENT-BRIDGE-PROBE
  imports VERIFICATION

  claim <k>
          joinCodes(
            iCons(32, .IntSeq),
            sortKeyVS(
              splitWS(strToCodes("three one five"), .IntSeq, .ValSeq),
              boundMethodV(numberOrder, "index")))
          => strToCodes("one three five")
        </k>
endmodule
