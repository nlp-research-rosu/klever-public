// #Top — 3-way differential, leg 1 (BASELINE): bare VS:ValSeq length claim on the plain
// definition. This is exactly today's production idiom: constructor narrowing, no remainder.
requires "verif-plain.k"
module LEN-PLAIN-SPEC
  imports VERIF-PLAIN
  claim <k> cloop(list(VS:ValSeq)) => .K </k> <acc> A:Int => lenAcc(VS, A) </acc> [all-path]
endmodule
