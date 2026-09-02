requires "verification-nobridge.k"

module SPLIT-CONNECTION-SPEC
  imports SORT-NUMBERS-VERIFICATION

  // Bridge-free value theorem: fixed splitWS on the candidate's encoded,
  // well-formed word strings produces exactly the declared word sequence.
  claim [split-encoded-words]:
    <k> splitWS(encodedWords(WORDS:NumWords), .IntSeq, .ValSeq)
        => wordsVS(WORDS) </k>
endmodule
