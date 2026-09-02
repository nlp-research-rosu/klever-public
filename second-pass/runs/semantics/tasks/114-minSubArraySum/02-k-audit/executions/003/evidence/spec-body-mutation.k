requires "verification-body-mutation.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Inductive loop theorem.  This is proved without the summary rule from the
  // VERIFICATION module.
  claim <k>
          #loop(
            list(intVals(iCons(I:Int, R:IntSeq))),
            Name("value"),
            kadaneBody)
          => .K
          ...
        </k>
        <env> L:Int </env>
        <scopes>
          ...
          L |-> scope(
            (("nums" |-> INPUT:Val)
             ("smallest" |-> B:Int)
             ("current" |-> C:Int)
             ("value" |-> _OLD:Val))
              =>
            (("nums" |-> INPUT)
             ("smallest" |->
                kadaneSmallest(iCons(I, R), C, B))
             ("current" |->
                kadaneCurrent(iCons(I, R), C))
             ("value" |-> lastFrom(R, I))),
            parent(0))
          ...
        </scopes>
endmodule

module LOAD-SPEC
  imports VERIFICATION-BASE

  // Loading the exact generated definition installs the exact closure used by
  // the function-correctness claim below.
  claim
    <k>
      #loadAll(Module(minSubArraySumDef .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               .Map
                 => "minSubArraySum" |-> minSubArraySumClosure,
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module FUNCTION-SPEC
  imports VERIFICATION

  // Full symbolic execution of the loaded generated closure on an arbitrary
  // non-empty list of mathematical integers.
  claim
    <k>
      #applyK(
        toCall(minSubArraySumClosure),
        (list(intVals(iCons(H:Int, T:IntSeq))), .Vals))
      => minSubArraySumSpec(iCons(H, T))
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
    <exit-code> 0 </exit-code>
endmodule
