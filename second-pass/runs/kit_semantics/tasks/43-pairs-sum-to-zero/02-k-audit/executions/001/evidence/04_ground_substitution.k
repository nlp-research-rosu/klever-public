requires "verification.k"

module GROUND-SUBSTITUTION
  imports VERIFICATION

  claim [empty-domain]:
    <k> allInts(.ValSeq) => true ... </k>

  claim [empty-result]:
    <k> anyInverse(.ValSeq, .ValSeq) => false ... </k>

  claim [nonzero-pair-domain]:
    <k> allInts(vCons(1, vCons(-1, .ValSeq))) => true ... </k>

  claim [nonzero-pair-result]:
    <k>
      anyInverse(
        vCons(1, vCons(-1, .ValSeq)),
        vCons(1, vCons(-1, .ValSeq)))
      => true
      ...
    </k>

  claim [single-zero-result]:
    <k>
      anyInverse(vCons(0, .ValSeq), vCons(0, .ValSeq))
      => false
      ...
    </k>

  claim [two-zero-result]:
    <k>
      anyInverse(
        vCons(0, vCons(0, .ValSeq)),
        vCons(0, vCons(0, .ValSeq)))
      => true
      ...
    </k>
endmodule
