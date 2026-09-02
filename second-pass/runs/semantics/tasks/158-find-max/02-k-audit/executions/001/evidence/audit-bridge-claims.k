requires "audit-bridge-free.k"

module AUDIT-BRIDGE-CLAIMS
  imports AUDIT-BRIDGE-FREE

  claim [empty-iterator-connection]:
    <k> #iterNext(list(wordVals(.WordSeq))) ~> KONT:K
      => #iterDone ~> KONT
    </k>

  claim [nonempty-iterator-connection]:
    <k> #iterNext(list(wordVals(
          wCons(WORD:IntSeq, REST:WordSeq)))) ~> KONT:K
      => #iterYield(str(WORD), list(wordVals(REST))) ~> KONT
    </k>
endmodule
