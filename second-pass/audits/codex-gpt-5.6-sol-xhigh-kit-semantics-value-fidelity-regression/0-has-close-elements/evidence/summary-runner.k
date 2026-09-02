requires "verification.k"

module SUMMARY-RUNNER
  imports VERIFICATION

  syntax Stmt ::= "SummaryChecks"

  rule <k> SummaryChecks => .K ... </k>
    requires outerAcc(false, 0, .FloatSeq, .FloatSeq, 0.5)
             ==Bool false
     andBool outerAcc(
               false, 0,
               fCons(4.0, .FloatSeq),
               fCons(4.0, .FloatSeq),
               1.0
             )
             ==Bool false
     andBool outerAcc(
               false, 0,
               fCons(0.0, fCons(1.0, .FloatSeq)),
               fCons(0.0, fCons(1.0, .FloatSeq)),
               1.0
             )
             ==Bool false
     andBool outerAcc(
               false, 0,
               fCons(0.0, fCons(1.0, .FloatSeq)),
               fCons(0.0, fCons(1.0, .FloatSeq)),
               1.1
             )
             ==Bool true
     andBool outerAcc(
               false, 0,
               fCons(2.0, fCons(2.0, .FloatSeq)),
               fCons(2.0, fCons(2.0, .FloatSeq)),
               0.0001
             )
             ==Bool true
     andBool outerAcc(
               false, 0,
               fCons(0.0, fCons(0.0, .FloatSeq)),
               fCons(0.0, fCons(0.0, .FloatSeq)),
               0.0 -Float 1.0
             )
             ==Bool false
endmodule
