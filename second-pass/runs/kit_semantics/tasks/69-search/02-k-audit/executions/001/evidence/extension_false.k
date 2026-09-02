requires "verification.k"

module EXTENSION-FALSE
  imports VERIFICATION

  claim [wrong-project]:
    <k> projectIntTotal(1) => 2 </k>

  claim [wrong-addition]:
    <k> applyBin("+", 1, 2) => 4 </k>

  claim [wrong-summary]:
    <k>
      searchSummary(
        vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq)))))),
        vCons(4, vCons(1, vCons(2, vCons(2, vCons(3, vCons(1, .ValSeq)))))),
        -1)
      => 3
    </k>
endmodule
