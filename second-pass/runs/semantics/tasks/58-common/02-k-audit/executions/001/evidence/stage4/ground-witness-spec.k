requires "verification.k"

module GROUND-WITNESS-SPEC
  imports VERIFICATION

  claim [ground-witness]:
    <k>
      #loadAll(Module(commonDefinition))
      ~> Call(
           Name("common"),
           list(vCons(2, vCons(2, vCons(1, vCons(1, .ValSeq))))),
           list(vCons(1, vCons(2, vCons(2, .ValSeq))))
         )
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
      0 |-> list(vCons(2, vCons(1, .ValSeq)))
      1 |-> list(vCons(1, vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
