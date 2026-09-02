requires "verification.k"

module AUDIT-LOCAL-EQUATIONS
  imports VERIFICATION

  claim [string-predicate-positive]:
    <k> isStringVal(str(.IntSeq)) => true </k>

  claim [string-predicate-negative]:
    <k> isStringVal(0) => false </k>

  claim [domain-empty]:
    <k> allDigitStrings(.ValSeq) => true </k>

  claim [domain-digits]:
    <k>
      allDigitStrings(
        vCons(
          str(iCons(48, iCons(57, .IntSeq))),
          vCons(str(.IntSeq), .ValSeq)))
      =>
      true
    </k>

  claim [domain-alpha-rejected]:
    <k>
      allDigitStrings(
        vCons(str(iCons(97, .IntSeq)), .ValSeq))
      =>
      false
    </k>

  claim [domain-nonstring-rejected]:
    <k>
      allDigitStrings(vCons(1, .ValSeq))
      =>
      false
    </k>

  claim [projection]:
    <k>
      stringCodes(str(iCons(49, .IntSeq)))
      =>
      iCons(49, .IntSeq)
    </k>

  claim [five-odd-digits]:
    <k>
      oddDigitCount(
        iCons(49, iCons(51, iCons(53, iCons(55, iCons(57, .IntSeq))))))
      =>
      5
    </k>

  claim [one-line]:
    <k>
      oddLine(iCons(49, .IntSeq))
      =>
      str(strToCodes(
        "the number of odd elements 1n the str1ng 1 of the 1nput."))
    </k>

  claim [one-list]:
    <k>
      oddLinesAcc(
        .ValSeq,
        vCons(str(iCons(49, .IntSeq)), .ValSeq))
      =>
      vCons(
        str(strToCodes(
          "the number of odd elements 1n the str1ng 1 of the 1nput.")),
        .ValSeq)
    </k>

  claim [guarded-count]:
    <k>
      applyMethod(
        str(iCons(49, iCons(49, .IntSeq))),
        "count",
        str(iCons(49, .IntSeq)),
        .Vals)
      =>
      2
    </k>
endmodule
