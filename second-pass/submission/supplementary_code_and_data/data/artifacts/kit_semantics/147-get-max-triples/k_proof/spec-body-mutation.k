requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [changed-body]:
    <k>
      Call(Name("get_max_triples"), Int(N))
      => expectedTriples(N)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "get_max_triples" |->
          closureVal("n", Return(Int(0)), 0),
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
    requires N ==Int 4
endmodule
