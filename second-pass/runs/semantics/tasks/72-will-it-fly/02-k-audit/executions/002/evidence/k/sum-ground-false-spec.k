requires "bridge-base.k"

module SUM-GROUND-FALSE-SPEC
  imports BRIDGE-BASE

  // Deliberately wrong opposite interpretation: sum([1,2]) is 3, not 4.
  claim
    <k>
      #sumAcc(list(vCons(1, vCons(2, .ValSeq))), 0)
      => 4
    </k>
endmodule
