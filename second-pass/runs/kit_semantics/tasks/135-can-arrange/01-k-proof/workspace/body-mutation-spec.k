requires "verification.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION

  // A1 probe: replacing the implementation by `return 0` must not establish
  // the real empty-list result (-1).
  claim [mutated-body]:
    <k> Call(Name("can_arrange"), list(.ValSeq)) => -1 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "can_arrange" |->
          closureVal(
            "arr", .ParamNames,
            Return(Int(0))
            .Stmts,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
