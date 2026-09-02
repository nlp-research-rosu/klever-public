requires "04_verification_body_mutant.k"

module AUDIT-BODY-MUTANT-SPEC
  imports AUDIT-BODY-MUTANT

  claim [third-branch-witness]:
    <k> AnyIntCall(13, 4, 9) => true </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
