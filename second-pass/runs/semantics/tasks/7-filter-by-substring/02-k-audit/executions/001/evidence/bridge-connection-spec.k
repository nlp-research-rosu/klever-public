requires "bridge-base.k"

module BRIDGE-CONNECTION-SPEC
  imports BRIDGE-BASE

  claim [iter-empty]:
    <k> #iterNext(list(strVals(.StrSeq))) ~> CONT:K
      => #iterDone ~> CONT
    </k>

  claim [iter-cons]:
    <k> #iterNext(list(strVals(ssCons(S:IntSeq, SS:StrSeq)))) ~> CONT:K
      => #iterYield(str(S), list(strVals(SS))) ~> CONT
    </k>

  claim [contains-true]:
    <k> Compare(str(P:IntSeq), CmpOp("in", str(S:IntSeq))) ~> CONT:K
      => true ~> CONT
    </k>
    requires strContains(P, S) ==Bool true

  claim [contains-false]:
    <k> Compare(str(P:IntSeq), CmpOp("in", str(S:IntSeq))) ~> CONT:K
      => false ~> CONT
    </k>
    requires strContains(P, S) ==Bool false
endmodule
