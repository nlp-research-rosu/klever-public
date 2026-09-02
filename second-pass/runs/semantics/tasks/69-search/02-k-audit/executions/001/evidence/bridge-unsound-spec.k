requires "verification.k"

module BRIDGE-UNSOUND-SPEC
  imports SEARCH-VERIFICATION

  // This is deliberately false under the fixed semantics.  With input [2],
  // the real loop binds value=2, so the function returns 2.  The candidate
  // bridge accepts the arbitrary continuation, skips that binding, and proves
  // the false return value 99.
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
