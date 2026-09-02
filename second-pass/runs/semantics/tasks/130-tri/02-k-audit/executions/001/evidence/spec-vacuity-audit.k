requires "spec.k"

module TRI-VACUITY-AUDIT-SPEC
  imports TRI-LOOP-SPEC

  // Fresh false mutation: the actual prefix index is N, not N+1.
  // N=0 is a concrete satisfying witness: tri(0) returns [1], whose
  // candidate-defined prefixIndex is 0.
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
    <heap> .Map => 0 |-> list(?RESULT:ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    ensures prefixIndex(?RESULT) <=Int N +Int 1
     andBool prefixIndex(?RESULT) >=Int N +Int 1
endmodule
