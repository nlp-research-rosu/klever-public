requires "/tmp/audit-work/reconstruct-001/verification.k"

module AUDIT-WITNESS-SPEC
  imports VERIFICATION

  claim [entry-precondition-witness]:
    <k>
      allStrings(
        vCons(
          str(iCons(98, iCons(97, .IntSeq))),
          vCons(str(iCons(97, iCons(98, .IntSeq))), .ValSeq)))
      => true
    </k>

  claim [loop-precondition-witness]:
    <k>
      allStrings(
        vCons(
          str(iCons(98, iCons(97, .IntSeq))),
          vCons(str(iCons(97, iCons(98, .IntSeq))), .ValSeq)))
      andBool definedProjectStr(str(.IntSeq))
      andBool notBool isRefV(str(.IntSeq))
      => true
    </k>

  claim [claimed-result-witness]:
    <k>
      bestWord(
        vCons(
          str(iCons(98, iCons(97, .IntSeq))),
          vCons(str(iCons(97, iCons(98, .IntSeq))), .ValSeq)),
        str(.IntSeq),
        0 -Int 1)
      => str(iCons(97, iCons(98, .IntSeq)))
    </k>
endmodule
