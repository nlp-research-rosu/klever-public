requires "verif-sum.k"

module ITER-SUM-SPEC
  imports ITER-SUM
  // loop-invariant shape: driving wrap(VS) accumulates ssum(VS, A) into <acc>.
  claim <k> #drive(wrap(VS:ValSeq)) => .K </k>
        <acc> A:Int => ?R:Int </acc>
        ensures ?R ==Int ssum(VS, A)
        [all-path]
endmodule
