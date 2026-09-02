requires "verification.k"

module TRIANGLE-SPEC
  imports TRIANGLE-VERIFICATION

  // Loading the translated module binds the required entry point to precisely
  // the closure whose behavior is proved below.
  claim
    <k> #loadAll(triangleAreaModule) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> triangleAreaClosure,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>

  // The four claims partition all integer triples according to the program's
  // left-to-right short-circuit validity test.

  claim
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => -1
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
    requires A +Int B <=Int C

  claim
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => -1
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
    requires A +Int B >Int C
     andBool A +Int C <=Int B

  claim
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => -1
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
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C <=Int A

  claim
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => expectedArea(A, B, C)
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
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C >Int A
endmodule
