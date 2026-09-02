requires "verification.k"

module POST-CORRECT-CONCRETE-SPEC
  imports TRI-VERIFICATION

  claim
    <k> .K => .K </k>
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
    ensures prefixIndex(
      vCons(1, vCons(3, vCons(2, vCons(8, .ValSeq)))))
      ==Int 3
endmodule

module POST-WRONG-CONCRETE-SPEC
  imports TRI-VERIFICATION

  claim
    <k> .K => .K </k>
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
    ensures prefixIndex(vCons(9, .ValSeq)) ==Int 3
endmodule

module POST-ABSTRACT-TAG-SPEC
  imports TRI-VERIFICATION

  claim
    <k> .K => .K </k>
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
    ensures prefixIndex(triPrefix(3)) ==Int 3
endmodule
