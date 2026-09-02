requires "/tmp/audit-work/fresh/verification.k"

module AUDIT-CONCRETE-SUBSTITUTIONS
  imports EVEN-ODD-VERIFICATION-SUMMARY

  claim
    <k> Call(Name("even_odd_count"), Int(-12)) => tuple(vCons(1, vCons(1, .ValSeq))) </k>
    <env> 0 </env>
    <scopes> 0 |-> #evenOddModuleScope -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(Name("even_odd_count"), Int(0)) => tuple(vCons(1, vCons(0, .ValSeq))) </k>
    <env> 0 </env>
    <scopes> 0 |-> #evenOddModuleScope -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(Name("even_odd_count"), Int(123)) => tuple(vCons(1, vCons(2, .ValSeq))) </k>
    <env> 0 </env>
    <scopes> 0 |-> #evenOddModuleScope -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
