requires "verification.k"

module SPECIALFILTER-LOOP-SPEC
  imports SPECIALFILTER-VERIFICATION-LOOP

  claim [specialfilter-loop-correct]:
    <k> #loop(list(intVals(NS:IntSeq)), Name("num"), #specialElementBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL:IntSeq))
        "count"  |-> C:Int
        "num"    |-> OLDNUM:Int
        "digits" |-> OLDDIGITS:Str,
        parent(0))
      0  |-> scope(GLOBAL:Map, parent(-1))
      -1 |-> scope(BUILTINMAP:Map, root)
      =>
      1 |-> scope(
        "nums"   |-> list(intVals(ALL))
        "count"  |-> C +Int specialCount(NS)
        "num"    |-> finalNum(OLDNUM, NS)
        "digits" |-> finalDigits(OLDDIGITS, NS),
        parent(0))
      0  |-> scope(GLOBAL, parent(-1))
      -1 |-> scope(BUILTINMAP, root)
    </scopes>
    requires notBool ("str" in_keys(GLOBAL))
      andBool "str" in_keys(BUILTINMAP)
      andBool {BUILTINMAP["str"]}:>Val ==K typeV("str")
endmodule

module SPECIALFILTER-SPEC
  imports SPECIALFILTER-VERIFICATION

  // Closure-entry smoke proof: MPY-CALL creates and later removes the local
  // frame around the exact solution.mpy body.  The universal list result is
  // established by specialfilter-loop-correct above.
  claim [specialfilter-empty-call-correct]:
    <k>
      #applyK(
        toCall(closureVal(
          ("nums", .ParamNames),
          #specialFunctionBody,
          0)),
        (list(intVals(.IntSeq)), .Vals))
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
