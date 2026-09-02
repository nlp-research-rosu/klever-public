requires "verification.k"

module EXTENSION-GROUND
  imports VERIFICATION

  claim [int-recognition]:
    <k> isIntVal(7) => true </k>

  claim [non-int-recognition]:
    <k> isIntVal(true) => false </k>

  claim [project-int]:
    <k> projectIntTotal(7) => 7 </k>

  claim [dispatch-equality]:
    <k> applyCmp("==", 2, 2) => true </k>

  claim [dispatch-greater-equal]:
    <k> applyCmp(">=", 3, 2) => true </k>

  claim [dispatch-greater]:
    <k> applyCmp(">", 3, 2) => true </k>

  claim [dispatch-addition]:
    <k> applyBin("+", 2, 3) => 5 </k>

  claim [positive-precondition-witness]:
    <k> allPositive(vCons(1, .ValSeq)) => true </k>

  claim [frequency-witness]:
    <k>
      frequencyOf(2, vCons(2, vCons(1, vCons(2, .ValSeq)))) => 2
    </k>

  claim [update-below-threshold]:
    <k> updateAnswer(-1, 2, 1) => -1 </k>

  claim [update-qualifying]:
    <k> updateAnswer(-1, 2, 2) => 2 </k>

  claim [update-not-larger]:
    <k> updateAnswer(3, 2, 2) => 3 </k>

  claim [summary-documented-example]:
    <k>
      searchSummary(
        vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq)))))),
        vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq)))))),
        -1)
      => 2
    </k>
endmodule
