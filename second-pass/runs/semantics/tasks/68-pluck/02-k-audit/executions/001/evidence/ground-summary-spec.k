requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports PLUCK-VERIFICATION

  claim <k> pluckResult(.ValSeq)
          => .ValSeq
        </k>

  claim <k> pluckResult(vCons(4, vCons(2, vCons(3, .ValSeq))))
          => vCons(2, vCons(1, .ValSeq))
        </k>

  claim <k> pluckResult(vCons(5, vCons(0, vCons(3, vCons(0, vCons(4, vCons(2, .ValSeq)))))))
          => vCons(0, vCons(1, .ValSeq))
        </k>

  claim <k> pluckResult(vCons(7, vCons(5, vCons(9, .ValSeq))))
          => .ValSeq
        </k>

  claim <k> pluckResult(vCons(6, vCons(2, vCons(9, vCons(2, .ValSeq)))))
          => vCons(2, vCons(1, .ValSeq))
        </k>

  claim <k> pluckResult(vCons(9, vCons(7, vCons(0, .ValSeq))))
          => vCons(0, vCons(2, .ValSeq))
        </k>
endmodule
