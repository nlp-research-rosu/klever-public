requires "verification.k"

module REVIEWER-FALSE-RESULT
  imports VERIFICATION

  // Fresh auditor mutation. For the satisfiable input N = 5, the real result
  // is [2, 3], while this obligation requires [2, 4].
  claim [wrong-five-result]:
    <k>
      FuncDef("count_up_to", Params("n"), countBody)
      ~> Call(Name("count_up_to"), (N:Int, .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => "count_up_to" |->
                    closureVal(("n", .ParamNames), countBody, 0),
                    parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(2, vCons(4, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N ==Int 5 andBool N >=Int 0
endmodule
