requires "verification.k"

module SPEC
  imports VERIFICATION

  // A positive Pythagorean equality may place the hypotenuse in any position.
  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => true </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C >Int 0
      andBool A *Int A +Int B *Int B ==Int C *Int C

  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => true </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C >Int 0
      andBool A *Int A +Int C *Int C ==Int B *Int B

  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => true </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C >Int 0
      andBool B *Int B +Int C *Int C ==Int A *Int A

  // Non-positive lengths cannot be triangle sides.  The claims mirror the
  // implementation's short-circuit order, yielding three disjoint cases.
  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => false </k>
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
    requires A <=Int 0

  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => false </k>
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
    requires A >Int 0 andBool B <=Int 0

  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => false </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C <=Int 0

  // For positive lengths, if none of the three Pythagorean equalities holds,
  // the implementation returns False.  Together the seven claims partition
  // all integer inputs and state the complete contract.
  claim
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => false </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C >Int 0
      andBool A *Int A +Int B *Int B =/=Int C *Int C
      andBool A *Int A +Int C *Int C =/=Int B *Int B
      andBool B *Int B +Int C *Int C =/=Int A *Int A
endmodule
