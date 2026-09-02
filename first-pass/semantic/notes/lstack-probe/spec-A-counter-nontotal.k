// A   : COUNTER loop, NON-TOTAL summary sumTo, ADDITIVE form (acc := A + sumTo(I,N)).
//       RESULT: FAILS — on the associativity  (A +Int I) +Int Y  ==  A +Int (I +Int Y)
//       (everything else is identical to A')
requires "verif.k"
module ACLAIM
  imports VERIF
  claim <k> cLoop(I:Int, N:Int) => #loopDone </k>
        <acc> A:Int => A +Int sumTo(I, N) </acc>
        <lstack> ListItem(lframe(D:K, _)) => ListItem(lframe(D, ?_:K)) ... </lstack>
        requires 0 <=Int I andBool I <=Int N
        [all-path]
endmodule
