requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // A fully ground entry state satisfying get-positive-correct's precondition.
  // Python input: [-2, 0, 3, 5]; expected result: [3, 5].
  claim [get-positive-ground]:
    <k>
      Call(
        Name("get_positive"),
        list(intVals(iCons(-2, iCons(0, iCons(3, iCons(5, .IntSeq)))))))
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
      0 |-> list(vCons(3, vCons(5, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A fully ground loop-head state satisfying filter-loop's precondition.
  // It starts with accumulator [7] and remaining input [-2, 3], yielding [7, 3].
  claim [filter-loop-ground]:
    <k>
      #loop(
        list(intVals(iCons(-2, iCons(3, .IntSeq)))),
        Name("x"),
        positiveLoopBody)
      ~> .K
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      1 |-> (
        scope(
          ("l" |-> ref(9))
          ("result" |-> ref(0))
          ("x" |-> 42),
          parent(0))
        =>
        scope(
          ("l" |-> ref(9))
          ("result" |-> ref(0))
          ("x" |-> 3),
          parent(0)))
    </scopes>
    <heap>
      0 |-> list(vCons(7, .ValSeq))
      =>
      0 |-> list(vCons(7, vCons(3, .ValSeq)))
    </heap>
endmodule
