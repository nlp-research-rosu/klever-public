requires "verification-body-mut.k"

module ANY-INT-SPEC-BODY-MUT
  imports ANY-INT-VERIFICATION-BODY-MUT

  claim
    <k> #anyIntMut(X:Int, Y:Int, Z:Int)
      => sumConditionMut(X, Y, Z)
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
