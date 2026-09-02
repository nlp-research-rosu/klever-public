requires "verification-body-mutated.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTATED

  claim
    <k>
      #isEqualToSumEven(N:Int)
      => (N >=Int 8 andBool pyMod(N, 2) ==Int 0)
    </k>
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
endmodule
