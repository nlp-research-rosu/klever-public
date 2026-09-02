requires "verification-nobridge.k"

module SPLIT-GROUND-SPEC
  imports SORT-NUMBERS-VERIFICATION

  claim [empty]:
    <k> splitWS(encodedWords(.NumWords), .IntSeq, .ValSeq)
        => wordsVS(.NumWords) </k>

  claim [zero]:
    <k> splitWS(encodedWords(nw(zeroW, .NumWords)), .IntSeq, .ValSeq)
        => wordsVS(nw(zeroW, .NumWords)) </k>

  claim [nine]:
    <k> splitWS(encodedWords(nw(nineW, .NumWords)), .IntSeq, .ValSeq)
        => wordsVS(nw(nineW, .NumWords)) </k>

  claim [three-one-five]:
    <k> splitWS(
          encodedWords(nw(threeW, nw(oneW, nw(fiveW, .NumWords)))),
          .IntSeq,
          .ValSeq)
        => wordsVS(nw(threeW, nw(oneW, nw(fiveW, .NumWords)))) </k>

  claim [duplicates]:
    <k> splitWS(
          encodedWords(nw(nineW, nw(zeroW, nw(nineW, .NumWords)))),
          .IntSeq,
          .ValSeq)
        => wordsVS(nw(nineW, nw(zeroW, nw(nineW, .NumWords)))) </k>

  // Fixed-semantics dispatch must preserve an admitted continuation exactly.
  claim [continuation]:
    <k> #applyK(
          toCall(boundMethodV(
            str(encodedWords(nw(threeW, nw(oneW, nw(fiveW, .NumWords))))),
            "split")),
          .Vals)
        ~> Int(7)
        => #alloc(list(wordsVS(
             nw(threeW, nw(oneW, nw(fiveW, .NumWords))))))
        ~> Int(7) </k>
endmodule
