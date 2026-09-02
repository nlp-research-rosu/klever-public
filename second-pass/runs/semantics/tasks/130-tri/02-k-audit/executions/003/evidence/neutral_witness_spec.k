requires "/audit-output/evidence/neutral_verification.k"

module NEUTRAL-WITNESS-SPEC
  imports TRI-NEUTRAL-VERIFICATION

  claim
    <k> Call(closureVal(("n", .ParamNames), NeutralTriFunctionBody, 0),
             Int(0), .Exprs)
      =>
         ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(triPrefix(0)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
