requires "verification.k"

module MODEL-BOUNDARY
  imports VERIFICATION-BASE

  // The symbolic MPY list-membership model uses structural K equality, so
  // Bool(true) and Int(1) remain distinct here.  MPY-KRUN's concrete-only
  // numOrKEq rule instead matches CPython and collapses them.
  claim [symbolic-bool-int-distinct]:
    <k>
      dedupFromVS(
        vCons(true, vCons(1, .ValSeq)),
        .ValSeq)
      => vCons(true, vCons(1, .ValSeq))
    </k>
endmodule
