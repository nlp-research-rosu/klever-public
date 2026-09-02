requires "verification-body-mutant.k"

module ROUNDED-AVG-SPEC-BODY-MUTANT
  imports ROUNDED-AVG-VERIFICATION-BODY-MUTANT

  // Contract branch: an inverted inclusive interval returns -1.
  claim
    <k> roundedAvgCall(N:Int, M:Int) => -1 </k>
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
    requires N >Int 0 andBool M >Int 0 andBool N >Int M

  // Valid interval, integral mean: no rounding adjustment is needed.
  claim
    <k> roundedAvgCall(N:Int, M:Int)
      => str(iCons(48, iCons(98, binCodes((N +Int M) /Int 2))))
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

  // Exact x.5 mean whose lower neighbor is even: half-even rounds down.
  claim
    <k> roundedAvgCall(N:Int, M:Int)
      => str(iCons(48, iCons(98, binCodes((N +Int M -Int 1) /Int 2))))
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
      andBool pyMod(N +Int M, 2) ==Int 1
      andBool pyMod((N +Int M -Int 1) /Int 2, 2) ==Int 0

  // Exact x.5 mean whose lower neighbor is odd: half-even rounds up.
  claim
    <k> roundedAvgCall(N:Int, M:Int)
      => str(iCons(48, iCons(98,
           binCodes(((N +Int M -Int 1) /Int 2) +Int 1))))
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
      andBool pyMod(N +Int M, 2) ==Int 1
      andBool pyMod((N +Int M -Int 1) /Int 2, 2) ==Int 1
endmodule
