requires "verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  claim [empty-domain-witness]:
    <k> allStrVS(.ValSeq) => true </k>

  claim [documented-domain-witness]:
    <k>
      allStrVS(
        vCons(str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
        vCons(str(iCons(98, iCons(97, iCons(99, iCons(100, .IntSeq))))),
        vCons(str(iCons(99, iCons(100, iCons(101, .IntSeq)))),
        vCons(str(iCons(97, iCons(114, iCons(114, iCons(97, iCons(121, .IntSeq)))))),
        .ValSeq)))))
      =>
      true
    </k>

  claim [empty-result-witness]:
    <k>
      filterAcc(.ValSeq, iCons(97, .IntSeq), .ValSeq)
      =>
      .ValSeq
    </k>

  claim [documented-result-witness]:
    <k>
      filterAcc(
        .ValSeq,
        iCons(97, .IntSeq),
        vCons(str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
        vCons(str(iCons(98, iCons(97, iCons(99, iCons(100, .IntSeq))))),
        vCons(str(iCons(99, iCons(100, iCons(101, .IntSeq)))),
        vCons(str(iCons(97, iCons(114, iCons(114, iCons(97, iCons(121, .IntSeq)))))),
        .ValSeq)))))
      =>
      vCons(str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
      vCons(str(iCons(98, iCons(97, iCons(99, iCons(100, .IntSeq))))),
      vCons(str(iCons(97, iCons(114, iCons(114, iCons(97, iCons(121, .IntSeq)))))),
      .ValSeq)))
    </k>
endmodule
