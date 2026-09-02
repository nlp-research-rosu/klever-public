requires "verification.k"

module SPECIALFILTER-SPEC-VACUITY
  imports SPECIALFILTER-VERIFICATION

  // False mutation: the empty input is required to return 1 instead of 0.
  // Its precondition is the same satisfiable precondition as the positive
  // closure-entry claim.
  claim [specialfilter-empty-call-false-result]:
    <k>
      #applyK(
        toCall(closureVal(
          ("nums", .ParamNames),
          #specialFunctionBody,
          0)),
        (list(intVals(.IntSeq)), .Vals))
      =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
endmodule
