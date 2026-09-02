requires "verification.k"

module CHOOSE-NUM-SPEC
  imports CHOOSE-NUM-VERIFICATION

  // For positive integers, pyMod(Y, 2) is either 0 or 1.  These four claims
  // are therefore exhaustive.  They also state why the result is maximal:
  // an even upper endpoint is itself the answer; an odd upper endpoint has
  // Y - 1 as its greatest even predecessor.

  claim [all-positive-inputs]:
    <k> #chooseNum(X:Int, Y:Int) => largestEvenInRange(X, Y) </k>
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
    requires X >Int 0 andBool Y >Int 0

  claim [even-upper-in-range]:
    <k> #chooseNum(X:Int, Y:Int) => Y </k>
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
    requires X >Int 0 andBool Y >Int 0
     andBool pyMod(Y, 2) ==Int 0
     andBool X <=Int Y

  claim [even-upper-before-range]:
    <k> #chooseNum(X:Int, Y:Int) => -1 </k>
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
    requires X >Int 0 andBool Y >Int 0
     andBool pyMod(Y, 2) ==Int 0
     andBool X >Int Y

  claim [odd-upper-predecessor-in-range]:
    <k> #chooseNum(X:Int, Y:Int) => Y -Int 1 </k>
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
    requires X >Int 0 andBool Y >Int 0
     andBool pyMod(Y, 2) ==Int 1
     andBool X <Int Y

  claim [odd-upper-no-even-in-range]:
    <k> #chooseNum(X:Int, Y:Int) => -1 </k>
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
    requires X >Int 0 andBool Y >Int 0
     andBool pyMod(Y, 2) ==Int 1
     andBool X >=Int Y
endmodule
