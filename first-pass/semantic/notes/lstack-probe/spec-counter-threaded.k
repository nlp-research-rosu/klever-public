// THREADED : COUNTER loop, same NON-TOTAL summary but accumulator-passing (acc := sumToAcc(I,N,A)).
//            RESULT: #Top — threading makes the inductive term equal the unfold syntactically,
//            so no associativity is needed and Z3 is never asked to bridge it.
requires "verif.k"
module ATHR
  imports VERIF
  claim <k> cLoop(I:Int, N:Int) => #loopDone </k>
        <acc> A:Int => sumToAcc(I, N, A) </acc>
        <lstack> ListItem(lframe(D:K, _)) => ListItem(lframe(D, ?_:K)) ... </lstack>
        requires 0 <=Int I andBool I <=Int N
        [all-path]
endmodule
