requires "/tmp/audit-work/130-tri-audit/verification.k"

module BRIDGE-WITNESS-SPEC
  imports TRI-VERIFICATION

  // Intended-domain witness n=0. Under the supplied semantics the returned
  // heap payload is vCons(1, .ValSeq), not the proof-local triPrefix term.
  claim
    <k> Call(closureVal(("n", .ParamNames), TriFunctionBody, 0),
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
