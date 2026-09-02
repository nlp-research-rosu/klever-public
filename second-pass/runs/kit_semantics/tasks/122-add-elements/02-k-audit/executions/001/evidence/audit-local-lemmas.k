requires "verification-base.k"

module AUDIT-LOCAL-LEMMAS
  imports VERIFICATION-BASE

  claim [projection-positive]:
    <k> projectIntTotal(99) => 99 </k>
  claim [projection-negative]:
    <k> projectIntTotal(-100) => -100 </k>
  claim [integer-domain]:
    <k>
      allInts(vCons(99, vCons(-100, vCons(7, .ValSeq)))) => true
    </k>
  claim [prefix-boundary]:
    <k>
      qualifyingPrefix(
        vCons(99, vCons(-100, vCons(7, .ValSeq))),
        2
      )
      =>
      99
    </k>
  claim [documented-result]:
    <k>
      qualifyingPrefix(
        vCons(111,
          vCons(21,
            vCons(3,
              vCons(4000,
                vCons(5,
                  vCons(6,
                    vCons(7,
                      vCons(8,
                        vCons(9, .ValSeq))))))))),
        4
      )
      =>
      24
    </k>
endmodule
