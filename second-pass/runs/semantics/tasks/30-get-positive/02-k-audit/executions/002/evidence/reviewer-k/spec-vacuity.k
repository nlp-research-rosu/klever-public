requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Keep the genuine loop lemma so the entry mutation reaches its final
  // result obligation rather than failing because an auxiliary claim is absent.
  claim [filter-loop-vacuity-support]:
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

  // Deliberately false result: append an extra 1 to every returned list.
  // Satisfying witness INPUT=.IntSeq: the real output is [], not [1].
  claim [get-positive-false-extra-one]:
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
          vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
