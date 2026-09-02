// CONTROL : SEQUENCE loop, but NON-TOTAL summary seqSumNT (same rules as seqSum, minus [total]).
//           RESULT: FAILS — so the SEQ loop breaks too once the summary is non-total.
//           => it is the summary's [total]-ness, NOT counter-vs-seq, NOT the <lstack>.
requires "verif.k"
module ACTRL
  imports VERIF
  claim <k> sLoop(S:IntSeq) => #loopDone </k>
        <acc> A:Int => A +Int seqSumNT(S) </acc>
        <lstack> ListItem(lframe(D:K, _)) => ListItem(lframe(D, ?_:K)) ... </lstack>
        [all-path]
endmodule
