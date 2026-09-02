requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [int-int]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Int, B:Int)
      => expectedCompare(A, B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [int-float]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Int, B:Float)
      => expectedCompare(A, B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [float-int]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Float, B:Int)
      => expectedCompare(A, B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [float-float]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Float, B:Float)
      => expectedCompare(A, B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [int-str]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Int, str(B:IntSeq))
      => expectedCompare(A, str(B)) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [str-int]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), str(A:IntSeq), B:Int)
      => expectedCompare(str(A), B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [float-str]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), A:Float, str(B:IntSeq))
      => expectedCompare(A, str(B)) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [str-float]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), str(A:IntSeq), B:Float)
      => expectedCompare(str(A), B) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [str-str]:
    <k> #loadAll(solutionModule()) ~>
        Call(Name("compare_one"), str(A:IntSeq), str(B:IntSeq))
      => expectedCompare(str(A), str(B)) </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
