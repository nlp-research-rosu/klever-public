requires "verification.k"

module SPEC
  imports VERIFICATION

  // The eight claims cover every combination of the numeric value classes
  // represented by MPY for side lengths: Int and Float.

  claim [right-angle-iii]:
    <k> Call(Name("right_angle_triangle"), A:Int, B:Int, C:Int)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-iif]:
    <k> Call(Name("right_angle_triangle"), A:Int, B:Int, C:Float)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-ifi]:
    <k> Call(Name("right_angle_triangle"), A:Int, B:Float, C:Int)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-iff]:
    <k> Call(Name("right_angle_triangle"), A:Int, B:Float, C:Float)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-fii]:
    <k> Call(Name("right_angle_triangle"), A:Float, B:Int, C:Int)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-fif]:
    <k> Call(Name("right_angle_triangle"), A:Float, B:Int, C:Float)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-ffi]:
    <k> Call(Name("right_angle_triangle"), A:Float, B:Float, C:Int)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)

  claim [right-angle-fff]:
    <k> Call(Name("right_angle_triangle"), A:Float, B:Float, C:Float)
         => ?RESULT:Bool </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "right_angle_triangle" |-> rightAngleTriangleClosure(),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RESULT ==Bool ratExpected(A, B, C)
endmodule
