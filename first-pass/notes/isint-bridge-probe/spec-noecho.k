requires "verif-noecho.k"

module ISINT-PROBE-NOECHO-SPEC
  imports ISINT-PROBE-VERIFICATION

  claim
    <k> applyBin("+", valSeqAt(NUMS:ValSeq, 0), valSeqAt(NUMS:ValSeq, 1)) => ?_:Int ... </k>
    requires allInt(NUMS) andBool vsLen(NUMS) >=Int 2
    [all-path]
endmodule
