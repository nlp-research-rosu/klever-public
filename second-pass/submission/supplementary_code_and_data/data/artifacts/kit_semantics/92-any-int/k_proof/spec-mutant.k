requires "verification-mutant.k"

module SPEC-MUTANT
  imports VERIFICATION-MUTANT

  // (3, 1, 2) is true only through the deliberately removed third disjunct.
  claim [body-sensitive-witness]:
    <k> AnyIntCallMutant(3, 1, 2) => true </k>
    <env> 0 </env>
    <scopes> 0 |-> anyIntMutantModuleScope
              -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
