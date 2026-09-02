// #Top — the working idiom, on the harder BREAK shape: head-exposed claim (I:Int, IS:Ints).
// The head is Int by sort, so applyCmp reduces to I <Int 0 with no cast; the claim re-applies
// co-inductively to the injected tail (claim application DOES narrow).
requires "verif-overload.k"
module HEADEXPOSED-BRANCH-SPEC
  imports VERIF-OVERLOAD
  claim <k> loopU(listU((I:Int, IS:Ints))) => .K </k>
        <acc> A:Int => prefixSumU((I, IS), A) </acc> [all-path]
endmodule
