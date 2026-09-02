requires "verification.k"

module SPEC
  imports VERIFICATION

  // Empty input: return a fresh empty list and retain the input object.
  claim
    <k>
      Call(Name("sort_array"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq)
      =>
      (0 |-> list(.ValSeq))
      (1 |-> list(.ValSeq))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A singleton is necessarily in the even branch.  The result is fresh and
  // the original heap object is unchanged.
  claim
    <k>
      Call(Name("sort_array"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(F:Int, .ValSeq))
      =>
      (0 |-> list(vCons(F, .ValSeq)))
      (1 |-> list(condRev(sortVS(vCons(F, .ValSeq)), true)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires F >=Int 0

  // Every list of length at least two is head ++ middle ++ last.  Odd endpoint
  // parity selects ascending sorted order.
  claim
    <k>
      Call(Name("sort_array"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(
        vCons(F:Int, snocVS(intsVS(MIDDLE:IntSeq), L:Int)))
      =>
      (0 |-> list(vCons(F, snocVS(intsVS(MIDDLE), L))))
      (1 |-> list(
        sortVS(vCons(F, snocVS(intsVS(MIDDLE), L)))))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires F >=Int 0
      andBool L >=Int 0
      andBool nonNegativeIS(MIDDLE)
      andBool pyMod(F +Int L, 2) ==Int 1

  // Even endpoint parity selects descending (reverse of ascending) order.
  claim
    <k>
      Call(Name("sort_array"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(
        vCons(F:Int, snocVS(intsVS(MIDDLE:IntSeq), L:Int)))
      =>
      (0 |-> list(vCons(F, snocVS(intsVS(MIDDLE), L))))
      (1 |-> list(condRev(
        sortVS(vCons(F, snocVS(intsVS(MIDDLE), L))),
        true)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires F >=Int 0
      andBool L >=Int 0
      andBool nonNegativeIS(MIDDLE)
      andBool pyMod(F +Int L, 2) ==Int 0
endmodule
