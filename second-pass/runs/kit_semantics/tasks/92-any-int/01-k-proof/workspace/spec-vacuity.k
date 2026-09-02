requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: any_int(5, 2, 7) returns true.
  claim [false-postcondition]:
    <k> AnyIntCall(5, 2, 7) => false </k>
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
