requires "/tmp/audit-work/130-tri-audit/verification.k"
requires "/tmp/audit-work/130-tri-audit/spec.k"

module TRI-VACUITY-SPEC
  imports TRI-LOOP-SPEC

  // False result mutation: demand a prefix index one larger than the input.
  // Satisfying witness N=0 returns [1], whose candidate summary rule gives
  // prefixIndex(vCons(1, .ValSeq)) = 0, not 1.
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
