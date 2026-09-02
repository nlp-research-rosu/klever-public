requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports VERIFICATION

  claim <k> arrangeResult(.ValSeq) => -1 </k>
    [label(summary-empty)]

  claim <k> arrangeResult(vCons(7, .ValSeq)) => -1 </k>
    [label(summary-singleton)]

  claim <k> arrangeResult(
          vCons(1, vCons(2, vCons(4, vCons(3, vCons(5, .ValSeq))))))
        => 3
        </k>
    [label(summary-documented-drop)]

  claim <k> arrangeResult(vCons(1, vCons(2, vCons(3, .ValSeq)))) => -1 </k>
    [label(summary-documented-increasing)]

  claim <k> arrangeResult(
          vCons(5, vCons(4, vCons(3, vCons(2, vCons(1, .ValSeq))))))
        => 4
        </k>
    [label(summary-descending)]
endmodule
