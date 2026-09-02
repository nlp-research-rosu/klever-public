requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [filter-loop-body-mutation]:
    <k>
      #loop(
        list(intVals(INPUT)),
        Name("x"),
        mutatedPositiveLoopBody)
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

  claim [get-positive-body-mutation]:
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
               |-> closureVal(("l", .ParamNames), mutatedGetPositiveBody, 0),
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
