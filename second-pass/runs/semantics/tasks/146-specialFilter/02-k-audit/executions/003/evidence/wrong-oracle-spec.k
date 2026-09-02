requires "wrong-oracle-verification.k"

module SPECIALFILTER-WRONG-ORACLE-SPEC
  imports SPECIALFILTER-WRONG-ORACLE

  // False for CPython, the trusted canonical function, and fixed concrete
  // semantics: specialFilter([11]) is 1, not 0.
  claim
    <k>
      #applyK(
        toCall(closureVal(
          ("nums", .ParamNames),
          #specialFunctionBody,
          0)),
        (list(intVals(iCons(11, .IntSeq))), .Vals))
      =>
      0
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
