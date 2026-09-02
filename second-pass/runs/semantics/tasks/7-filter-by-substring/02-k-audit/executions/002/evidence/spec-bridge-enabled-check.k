requires "verification.k"

module FILTER-BRIDGE-ENABLED-CHECK
  imports FILTER-VERIFICATION

  claim
    <k> #iterNext(list(strVals(.StrSeq))) ~> CONT:K
      => #iterDone ~> CONT
    </k>

  claim
    <k> #iterNext(list(strVals(ssCons(S:IntSeq, SS:StrSeq)))) ~> CONT:K
      => #iterYield(str(S), list(strVals(SS))) ~> CONT
    </k>

  claim
    <k> Compare(str(P:IntSeq), CmpOp("in", str(S:IntSeq))) ~> CONT:K
      => strContains(P, S) ~> CONT
    </k>
endmodule
