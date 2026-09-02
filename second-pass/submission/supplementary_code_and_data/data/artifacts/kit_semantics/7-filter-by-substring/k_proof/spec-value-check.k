requires "verification.k"

module SPEC-VALUE-CHECK
  imports VERIFICATION

  claim [codes-a]:
    <k>
      strCodes(str(iCons(97, .IntSeq)))
      =>
      iCons(97, .IntSeq)
    </k>

  claim [contains-yes]:
    <k>
      applyCmp(
        "in",
        str(iCons(97, .IntSeq)),
        str(iCons(97, .IntSeq)))
      =>
      true
    </k>

  claim [contains-no]:
    <k>
      applyCmp(
        "in",
        str(iCons(97, .IntSeq)),
        str(iCons(98, .IntSeq)))
      =>
      false
    </k>
endmodule
