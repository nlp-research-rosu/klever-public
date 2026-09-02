requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [member-fold]:
    <k>
      #memberAcc(V:Val, list(VS:ValSeq)) ~> CONT:K
    =>
      memberVS(V, VS) ~> CONT
    </k>

  // Inductive loop invariant.  The result heap object is transformed exactly
  // by commonAcc; all unrelated scope and heap entries remain unchanged.
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

  // Whole-function correctness from the pristine semantic configuration.
  // sorted is the reference semantics' trusted ascending-sort primitive;
  // commonSpec is the unique intersection defined above.
  claim [common-function]:
    <k>
      #loadAll(Module(commonDefinition))
      ~> Call(Name("common"), list(FIRST:ValSeq), list(SECOND:ValSeq))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |->
        scope(
          "common" |->
            closureVal(
              ("l1", "l2"),
              commonBody,
              0
            ),
          parent(-1)
        )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(commonSpec(FIRST, SECOND))
      1 |-> list(sortVS(commonSpec(FIRST, SECOND)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
