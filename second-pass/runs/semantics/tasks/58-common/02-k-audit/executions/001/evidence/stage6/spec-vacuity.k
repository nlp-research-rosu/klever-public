requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Fresh false mutation: the real execution returns the newly allocated
  // sorted-list object at heap location 1, not the accumulator object at 0.
  claim [wrong-return-ref]:
    <k>
      #loadAll(Module(commonDefinition))
      ~> Call(Name("common"), list(FIRST:ValSeq), list(SECOND:ValSeq))
    =>
      ref(0)
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
