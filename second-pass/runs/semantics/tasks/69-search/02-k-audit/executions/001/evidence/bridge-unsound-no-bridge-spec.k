requires "verification-no-bridge.k"

module BRIDGE-UNSOUND-NO-BRIDGE-SPEC
  imports SEARCH-VERIFICATION

  // Same false claim as bridge-unsound-spec.k, but compiled without the
  // candidate operational bridge.
  claim
    <k> Call(Name("probe"), list((vCons(2, .ValSeq)):IntValSeq), .Exprs)
      => 99
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "probe" |-> closureVal(
               "lst" , .ParamNames,
               Assign(Name("result"), UnaryOp("-", Int(1)))
               Assign(Name("value"), Int(99))
               For(Name("value"), Name("lst"), #outerBody)
               Return(Name("value")) .Stmts,
               0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
