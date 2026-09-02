requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Starting candidate enumeration at 3 omits the prime 2.  The unchanged
  // postcondition for the concrete witness 5 must therefore be rejected.
  claim [skip-two]:
    <k>
      FuncDef("count_up_to", Params("n"), countBodyStart3)
      ~> Call(Name("count_up_to"), (Int(5), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => "count_up_to" |->
                    closureVal(("n", .ParamNames), countBodyStart3, 0),
                    parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(primesBelow(5)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
