requires "verification.k"

module ROUNDED-AVG-SPEC-VACUITY
  imports ROUNDED-AVG-VERIFICATION

  // Deliberately false mutation of the integral-mean branch:
  // for N=1, M=3 the real result is bin(2), not bin(3).
  claim
    <k> roundedAvgCall(N:Int, M:Int)
      => str(iCons(48, iCons(98, binCodes(((N +Int M) /Int 2) +Int 1))))
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
    requires N >Int 0 andBool M >Int 0 andBool N <=Int M
      andBool pyMod(N +Int M, 2) ==Int 0
endmodule
