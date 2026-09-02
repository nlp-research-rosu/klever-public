requires "verification.k"

module GROUND-RESULT-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  claim [empty]:
    <k> checkDictCaseResult(.ValSeq, false, true, true) => false </k>

  claim [one-ascii-lower]:
    <k> checkDictCaseResult(
          vCons(str(iCons(97, .IntSeq)), .ValSeq),
          false, true, true)
      => true
    </k>

  claim [one-ascii-upper]:
    <k> checkDictCaseResult(
          vCons(str(iCons(65, .IntSeq)), .ValSeq),
          false, true, true)
      => true
    </k>

  claim [mixed-ascii]:
    <k> checkDictCaseResult(
          vCons(str(iCons(97, .IntSeq)),
            vCons(str(iCons(65, .IntSeq)), .ValSeq)),
          false, true, true)
      => false
    </k>

  claim [non-string]:
    <k> checkDictCaseResult(vCons(8, .ValSeq), false, true, true)
      => false
    </k>

  // U+00E9 LATIN SMALL LETTER E WITH ACUTE. Python says "é".islower() is
  // true; the supplied semantics' ASCII-only isLowerC says false.
  claim [unicode-lower-formal]:
    <k> checkDictCaseResult(
          vCons(str(iCons(233, .IntSeq)), .ValSeq),
          false, true, true)
      => false
    </k>

  // The prompt requires checking every key; this is false. The trusted
  // canonical's early break incorrectly returns true after the first two keys.
  claim [canonical-early-break-witness-formal]:
    <k> checkDictCaseResult(
          vCons(str(iCons(97, .IntSeq)),
            vCons(str(iCons(98, iCons(50, .IntSeq))),
              vCons(str(iCons(65, .IntSeq)), .ValSeq))),
          false, true, true)
      => false
    </k>
endmodule
