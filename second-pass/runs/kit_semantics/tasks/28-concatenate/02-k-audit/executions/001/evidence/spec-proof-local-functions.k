requires "verification.k"

module SPEC-PROOF-LOCAL-FUNCTIONS
  imports VERIFICATION

  claim [string-codes-string]:
    <k> stringCodes(str(iCons(97, .IntSeq))) => iCons(97, .IntSeq) ... </k>

  claim [string-codes-non-string]:
    <k> stringCodes(7) => .IntSeq ... </k>

  claim [recognizer-empty]:
    <k> isStringSeq(.ValSeq) => true ... </k>

  claim [recognizer-strings]:
    <k>
      isStringSeq(vCons(str(.IntSeq), vCons(str(iCons(97, .IntSeq)), .ValSeq)))
      => true
      ...
    </k>

  claim [recognizer-rejects-non-string]:
    <k> isStringSeq(vCons(7, .ValSeq)) => false ... </k>

  claim [concat-ground]:
    <k>
      concatFrom(
        iCons(120, .IntSeq),
        vCons(str(iCons(97, .IntSeq)), vCons(str(iCons(98, .IntSeq)), .ValSeq))
      )
      => iCons(120, iCons(97, iCons(98, .IntSeq)))
      ...
    </k>

  claim [last-empty]:
    <k> lastFrom(str(iCons(120, .IntSeq)), .ValSeq) => str(iCons(120, .IntSeq)) ... </k>

  claim [last-nonempty]:
    <k>
      lastFrom(
        str(iCons(120, .IntSeq)),
        vCons(str(iCons(97, .IntSeq)), vCons(str(iCons(98, .IntSeq)), .ValSeq))
      )
      => str(iCons(98, .IntSeq))
      ...
    </k>

  claim [simplification-overlap]:
    <k>
      applyBin("+", str(iCons(120, .IntSeq)), str(iCons(97, .IntSeq)))
      => str(iCons(120, iCons(97, .IntSeq)))
      ...
    </k>
endmodule
