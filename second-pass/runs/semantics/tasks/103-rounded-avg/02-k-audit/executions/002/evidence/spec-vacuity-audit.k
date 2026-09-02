requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports ROUNDED-AVG-VERIFICATION

  // Deliberately false off-by-one mutation of the integral-mean result.
  // Satisfying witness N=1, M=5: the program returns bin(3) = "0b11",
  // while this destination requires bin(4) = "0b100".
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
