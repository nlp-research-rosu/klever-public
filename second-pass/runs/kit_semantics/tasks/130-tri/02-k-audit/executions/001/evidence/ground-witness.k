requires "verification.k"

module AUDIT-GROUND-WITNESS
  imports VERIFICATION

  // N = 0 satisfies the entry precondition N >= 0.
  claim [result-n0]:
    <k> triResult(0)
      => vCons(1, .ValSeq)
    </k>

  // N = 3 exercises the base, even, and odd program branches.
  claim [result-n3]:
    <k> triResult(3)
      => vCons(1,
           vCons(3,
             vCons(2,
               vCons(8, .ValSeq))))
    </k>

  claim [result-n4]:
    <k> triResult(4)
      => vCons(1,
           vCons(3,
             vCons(2,
               vCons(8,
                 vCons(3, .ValSeq)))))
    </k>

  claim [result-n10]:
    <k> triResult(10)
      => vCons(1,
           vCons(3,
             vCons(2,
               vCons(8,
                 vCons(3,
                   vCons(15,
                     vCons(4,
                       vCons(24,
                         vCons(5,
                           vCons(35,
                             vCons(6, .ValSeq)))))))))))
    </k>
endmodule
