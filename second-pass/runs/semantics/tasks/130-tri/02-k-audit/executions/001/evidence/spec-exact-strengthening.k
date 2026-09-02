requires "verification.k"

module TRI-EXACT-STRENGTHENING-SPEC
  imports TRI-VERIFICATION

  // True intended strengthening: preserve the entire abstract mathematical
  // prefix, not only prefixIndex(?RESULT) == N.
  claim
    <k> Call(closureVal(("n", .ParamNames), TriFunctionBody, 0),
             Int(N:Int), .Exprs)
      =>
         ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(triPrefix(N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule
