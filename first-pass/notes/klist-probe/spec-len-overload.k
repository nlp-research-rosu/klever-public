// FAIL — 3-way differential, leg 3 (OVERLOAD): same bare VS:ValSeq claim on the overloaded
// definition. The tags demote vCons/.ValSeq to `anywhere`, so exhaustiveness is lost: stuck on
// the semantically-empty remainder (not nil, not any cons) the prover cannot discharge.
requires "verif-overload.k"
module LEN-OVERLOAD-SPEC
  imports VERIF-OVERLOAD
  claim <k> cloop(list(VS:ValSeq)) => .K </k> <acc> A:Int => lenAcc(VS, A) </acc> [all-path]
endmodule
