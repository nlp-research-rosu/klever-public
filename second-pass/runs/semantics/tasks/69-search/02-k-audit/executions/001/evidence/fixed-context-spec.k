requires "fixed-context-verification.k"

module FIXED-CONTEXT-SPEC
  imports FIXED-CONTEXT-VERIFICATION

  // Fixed supplied semantics over the real ValSeq constructors: [2] iterates,
  // binds value=2, and the admitted continuation therefore returns 2.
  claim
    <k> Call(Name("probe"), list(vCons(2, .ValSeq)), .Exprs)
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "probe" |-> closureVal(
               "lst" , .ParamNames,
               Assign(Name("result"), UnaryOp("-", Int(1)))
               Assign(Name("value"), Int(99))
               For(Name("value"), Name("lst"), #fixedOuterBody)
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
