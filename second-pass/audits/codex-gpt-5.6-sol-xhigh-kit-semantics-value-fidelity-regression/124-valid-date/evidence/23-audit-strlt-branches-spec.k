requires "audit-verification-no-lemma.k"

module AUDIT-STRLT-BRANCHES-SPEC
  imports VERIFICATION

  claim [one-code-strlt-less]:
    <k> strLt(iCons(A:Int, .IntSeq), iCons(B:Int, .IntSeq)) => true </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A <Int B

  claim [one-code-strlt-greater]:
    <k> strLt(iCons(A:Int, .IntSeq), iCons(B:Int, .IntSeq)) => false </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >Int B

  claim [one-code-strlt-equal]:
    <k> strLt(iCons(A:Int, .IntSeq), iCons(B:Int, .IntSeq)) => false </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A ==Int B
endmodule
