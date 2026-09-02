requires "reference-semantics/semantics.k"

module LEMMA-SPEC
  imports MPY

  claim [gt3-under-le3]:
    <k> (N:Int >Int 3) => false </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <=Int 3
endmodule
