requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim [ground-one-one]:
    <k>
      #loadAll(Module(
        FuncDef("common", Params("l1", "l2"), commonBody())
      ))
      ~> Call(
           Name("common"),
           list(vCons(1, .ValSeq)),
           list(vCons(1, .ValSeq)))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope(
        "common" |-> closureVal(
          ("l1", "l2", .ParamNames),
          commonBody(),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(sortVS(vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
