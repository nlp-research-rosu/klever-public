requires "verification.k"

module AUDIT-LOAD-SPEC
  imports TRIANGLE-VERIFICATION

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
endmodule

module AUDIT-INVALID-FIRST-SPEC
  imports TRIANGLE-VERIFICATION

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
endmodule

module AUDIT-INVALID-SECOND-SPEC
  imports TRIANGLE-VERIFICATION

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
endmodule

module AUDIT-INVALID-THIRD-SPEC
  imports TRIANGLE-VERIFICATION

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
endmodule

module AUDIT-VALID-SPEC
  imports TRIANGLE-VERIFICATION

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
