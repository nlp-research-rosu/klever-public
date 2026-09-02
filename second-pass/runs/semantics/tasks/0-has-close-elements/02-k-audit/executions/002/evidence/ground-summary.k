requires "verification.k"

module GROUND-SUMMARY
  imports VERIFICATION-BASE

  claim <k> hasPairs(.FloatSeq, .FloatSeq, 1.0, 1) => false </k>

  claim <k> hasPairs(fCons(0.0, .FloatSeq),
                     fCons(0.0, .FloatSeq), 1.0, 1) => false </k>

  claim <k> hasPairs(fCons(A:Float, fCons(B:Float, .FloatSeq)),
                     fCons(A, fCons(B, .FloatSeq)), T:Float, 1)
         => near(A, B, T) </k>
endmodule
