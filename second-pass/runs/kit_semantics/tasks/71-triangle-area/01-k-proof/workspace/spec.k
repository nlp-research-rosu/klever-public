requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [triangle-area-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-float-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Float, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-int-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-int-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Int, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-float-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Float, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-float-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Float, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-float-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Float, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-bool-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Bool, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-bool-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Bool, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-int-bool-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Int, B:Bool, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-int-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Int, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-int-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Int, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-int-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Int, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-float-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Float, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-float-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Float, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-bool-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Bool, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-bool-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Bool, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-float-bool-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Float, B:Bool, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-int-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Int, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-int-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Int, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-int-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Int, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-float-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Float, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-float-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Float, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-float-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Float, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-bool-int]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Bool, C:Int, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-bool-float]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Bool, C:Float, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [triangle-area-bool-bool-bool]:
    <k>
      #loadAll(triangleProgram())
        ~> Call(Name("triangle_area"), (A:Bool, B:Bool, C:Bool, .Exprs))
      => triangleAreaSpec(A, B, C)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
