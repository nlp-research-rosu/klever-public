// SAME claim as spec-branch, but over verif-partial (projectIntTotal is a bare [function]):
// the comparison projectIntTotal(V)<0 is not SMT-representable, so the branch can't decide.
requires "verif-partial.k"
module BRANCH-PARTIAL-SPEC
  imports VERIF
  claim <k> loop(list(VS:ValSeq)) => .K </k> <acc> A:Int => prefixSumAcc(VS, A) </acc> requires allInt(VS) [all-path]
endmodule
