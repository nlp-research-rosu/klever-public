requires "05_verification_body_mutated.k"

module AUDIT-BODY-MUTATION-SPEC
  imports AUDIT-BODY-MUTATED

  claim [unchanged-postcondition]:
    <k>
      Call(Name("get_max_triples"), (Int(N:Int), .Exprs))
      => auditTripleCount(N)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |-> closureVal(
          ("n", .ParamNames), auditMutatedBody, 0),
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
