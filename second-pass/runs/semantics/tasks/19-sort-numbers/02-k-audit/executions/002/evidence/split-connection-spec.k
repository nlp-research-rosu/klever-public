requires "verification-bridge-free.k"

module SPLIT-CONNECTION-SPEC
  imports SORT-NUMBERS-BRIDGE-FREE

  claim [split-connection]:
    <k> splitWS(encodedWords(WORDS:NumWords), .IntSeq, .ValSeq)
        => wordsVS(WORDS) </k>
endmodule
