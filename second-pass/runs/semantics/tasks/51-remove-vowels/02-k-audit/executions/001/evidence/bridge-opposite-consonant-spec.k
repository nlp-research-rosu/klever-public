requires "bridge-audit.k"

module BRIDGE-OPPOSITE-CONSONANT-SPEC
  imports BRIDGE-AUDIT

  claim
    <k>
      strContains(iCons(98, .IntSeq), auditVowelCodes)
      =>
      true
    </k>
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
endmodule
