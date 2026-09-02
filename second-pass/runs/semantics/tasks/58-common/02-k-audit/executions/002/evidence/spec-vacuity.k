requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Auditor mutation: falsely require every returned common list to be empty.
  // Satisfiable counterexample: FIRST=[1], SECOND=[1], whose actual result is [1].
  claim [common-function-false-empty]:
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
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
