requires "verif-suml.k"

module ITER-SUML-SPEC
  imports ITER-SUML
  // loop-invariant shape: driving wrap(VS) accumulates ssum(VS, A) into <acc>.
  claim <k> #drive(wrap(VS:ValSeq)) => .K </k>
        <acc> A:Int => ?R:Int </acc>
        ensures ?R ==Int ssum(VS, A)
        [all-path]
endmodule
