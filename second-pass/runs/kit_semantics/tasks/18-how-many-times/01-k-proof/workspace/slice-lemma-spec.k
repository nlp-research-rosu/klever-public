requires "reference-semantics/semantics.k"

module SLICE-LEMMA-SPEC
  imports MPY

  // Bridge-free validation of the derived simplification lemma used by the
  // target proof.  Every nonempty IntSeq has this constructor form.
  claim [slice-tail]:
    <k>
      buildIS(
        iCons(C:Int, CS:IntSeq),
        clampHi(1, isLen(iCons(C, CS)), 1),
        isLen(iCons(C, CS)),
        1)
      => CS
    </k>
endmodule
