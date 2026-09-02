requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: this ground call returns the separately allocated
  // sorted list at ref(1), not the accumulator list at ref(0).
  claim [false-result]:
    <k>
      #loadAll(Module(
        FuncDef("common", Params("l1", "l2"), commonBody())
      ))
      ~> Call(
           Name("common"),
           list(vCons(1, .ValSeq)),
           list(vCons(1, .ValSeq)))
    =>
      ref(0)
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
