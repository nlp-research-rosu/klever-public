requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Deliberately false: append zero to every claimed result.  For the
  // satisfying empty input, the real result is [] but this demands [0].
  claim [get-positive-wrong]:
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
      0 |-> list(
        valSeqConcat(
          filterPositive(.ValSeq, INPUT),
          vCons(0, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

