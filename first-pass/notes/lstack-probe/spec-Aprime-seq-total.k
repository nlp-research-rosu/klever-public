// A'  : SEQUENCE loop, TOTAL summary seqSum.   RESULT: #Top  (PROVES)
requires "verif.k"
module APRIME
  imports VERIF
  claim <k> sLoop(S:IntSeq) => #loopDone </k>
        <acc> A:Int => A +Int seqSum(S) </acc>
        <lstack> ListItem(lframe(D:K, _)) => ListItem(lframe(D, ?_:K)) ... </lstack>
        [all-path]
endmodule
