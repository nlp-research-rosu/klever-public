requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant and induction lemma.  This state is reached after the
  // first target binding, so the function-local frame has exactly l, result,
  // and x.  Python's for-loop may change only the value of x.
  claim [filter-loop]:
    <k>
      #loop(
        list(intVals(INPUT)),
        Name("x"),
        positiveLoopBody)
      ~> CONT
      => CONT
    </k>
    <env> LOCAL </env>
    <scopes>
      ...
      LOCAL |-> (
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> _OLD_X),
          parent(0))
        =>
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> ?_FINAL_X),
          parent(0)))
      ...
    </scopes>
    <heap>
      ...
      ACC_LOC |-> list(
        PREFIX
        =>
        filterPositive(PREFIX, INPUT))
      ...
    </heap>

  claim [get-positive-correct]:
    <k>
      Call(
        Name("get_positive"),
        list(intVals(INPUT)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "get_positive"
               |-> closureVal(("l", .ParamNames), getPositiveBody, 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(filterPositive(.ValSeq, INPUT))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
