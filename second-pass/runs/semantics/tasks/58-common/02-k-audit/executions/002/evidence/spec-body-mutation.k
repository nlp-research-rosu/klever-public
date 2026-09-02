requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [member-fold]:
    <k>
      #memberAcc(V:Val, list(VS:ValSeq)) ~> CONT:K
    =>
      memberVS(V, VS) ~> CONT
    </k>

  claim [common-loop]:
    <k>
      #loop(list(FIRST:ValSeq), Name("item"), commonLoopBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |->
        scope(
          ("l1" |-> list(_ORIGINAL:ValSeq))
          ("l2" |-> list(SECOND:ValSeq))
          ("result" |-> ref(H:Int))
          ("item" |-> (OLD:Val => lastAfter(FIRST, OLD)))
          .Map,
          parent(0)
        )
      ...
    </scopes>
    <heap>
      ... H |-> list(ACC:ValSeq => commonAcc(FIRST, SECOND, ACC)) ...
    </heap>
endmodule
