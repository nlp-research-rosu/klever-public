requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false result obligation. On [1] and [1], both the accumulator and
  // returned sorted list contain 1, so demanding empty lists is false.
  claim [false-empty-result]:
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
      0 |-> list(.ValSeq)
      1 |-> list(sortVS(.ValSeq))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
