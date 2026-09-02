requires "verification.k"

module GROUND-RESULT-SPEC
  imports VERIFICATION

  claim <k> prodSignsResult(.IntSeq) => noneV </k>

  claim <k>
          prodSignsResult(
            iCons(1, iCons(2, iCons(2, iCons(-4, .IntSeq)))))
          => -9
        </k>

  claim <k> prodSignsResult(iCons(0, iCons(1, .IntSeq))) => 0 </k>

  claim <k>
          prodSignsResult(iCons(-1, iCons(-2, iCons(-3, .IntSeq))))
          => -6
        </k>

  claim <k>
          prodSignsResult(
            iCons(10000000000000000000000000000000000000000,
              iCons(-10000000000000000000000000000000000000000,
                iCons(1, .IntSeq))))
          => -20000000000000000000000000000000000000001
        </k>
endmodule
