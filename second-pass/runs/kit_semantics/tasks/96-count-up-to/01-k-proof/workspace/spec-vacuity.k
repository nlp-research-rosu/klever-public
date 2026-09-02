requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness N = 0: the real result is
  // empty, while this mutation requires a leading zero.
  claim [false-result]:
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
    <heap> .Map => 0 |-> list(vCons(0, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N ==Int 0
endmodule
