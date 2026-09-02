// CLOSED-FORM : COUNTER loop, additive form but the summand is PURE ARITHMETIC (no function
//               symbol): acc := A + (N*(N-1) - I*(I-1))/2.   RESULT: #Top — Z3 handles it all
//               natively (Gauss), including the floor /2.
requires "verif.k"
module ACLOSED
  imports VERIF
  claim <k> cLoop(I:Int, N:Int) => #loopDone </k>
        <acc> A:Int => A +Int ((N *Int (N -Int 1)) -Int (I *Int (I -Int 1))) /Int 2 </acc>
        <lstack> ListItem(lframe(D:K, _)) => ListItem(lframe(D, ?_:K)) ... </lstack>
        requires 0 <=Int I andBool I <=Int N
        [all-path]
endmodule
