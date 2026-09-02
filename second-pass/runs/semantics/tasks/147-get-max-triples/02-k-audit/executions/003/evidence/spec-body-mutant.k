requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [changed-body-must-not-prove]:
    <k>
      Call(Name("get_max_triples"), (Int(N:Int), .Exprs))
      => tripleCountMutant(N)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |-> closureVal(
          ("n", .ParamNames), getMaxTriplesBodyMutant, 0),
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
    requires N >Int 0
endmodule
