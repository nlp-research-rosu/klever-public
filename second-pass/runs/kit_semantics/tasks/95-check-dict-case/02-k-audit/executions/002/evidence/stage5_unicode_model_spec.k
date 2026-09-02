requires "verification.k"

module AUDIT-UNICODE-MODEL-SPEC
  imports VERIFICATION

  // Concrete fixed-model witness: code point U+00E9 is not in the supplied
  // semantics' ASCII-only lower-case range, although CPython "é".islower()
  // is true.
  claim [method-gap]:
    <k>
      applyMethod(str(iCons(233, .IntSeq)), "islower", .Vals)
      =>
      false
    </k>

  claim [summary-gap]:
    <k>
      checkCaseSummary(
        true, true, false,
        vCons(str(iCons(233, .IntSeq)), .ValSeq))
      =>
      false
    </k>
endmodule
