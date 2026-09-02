// CONTROL: the SAME loop-break over seq(IntSeq) — a GENUINE Int head, no cast at all. Branches directly.
requires "verif.k"
module CONTROL-SEQ-SPEC
  imports VERIF
  claim <k> iloop(seq(IS:IntSeq)) => .K </k> <acc> A:Int => prefixSumI(IS, A) </acc> [all-path]
endmodule
