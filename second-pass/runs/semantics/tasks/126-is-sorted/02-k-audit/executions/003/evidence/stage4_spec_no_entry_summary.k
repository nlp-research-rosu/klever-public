requires "verification-no-entry-summary.k"

module IS-SORTED-LOOP-SPEC
  imports IS-SORTED-VERIFICATION

  claim [loop-scan-correct]:
    <k>
      #loop(list(intsToVals(IS:IntSeq)),
            Name("number"),
            isSortedLoopBody)
      ~> Return(Name("result"))
      ~> #endcall
      =>
      scanResult(scanAll(OK:Bool, PREV:Int, COUNT:Int, IS)) ~> CONT:K
    </k>
    <env> FRAME:Int => CALLER:Int </env>
    <scopes>
      FRAME |-> scope(
        ("$plain" |-> true)
        ("result" |-> OK)
        ("previous" |-> PREV)
        ("repeats" |-> COUNT)
        ("number" |-> _NUMBER:Int)
        LOCALS:Map,
        PARENT:Parent)
      BASE:Map
      =>
      BASE
    </scopes>
    <scopeLoc> CURRENT:Int => SAVED:Int </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, SAVED))
      STACK:List
      =>
      STACK
    </stack>
    <ret> noRet => noRet </ret>
    requires FRAME ==Int SAVED
     andBool notBool FRAME in_keys(BASE)
     andBool notBool "result" in_keys(LOCALS)
     andBool notBool "previous" in_keys(LOCALS)
     andBool notBool "repeats" in_keys(LOCALS)
     andBool notBool "number" in_keys(LOCALS)
     andBool notBool "$plain" in_keys(LOCALS)
     andBool notBool "$cells" in_keys(LOCALS)
     andBool notBool "$cells" in_keys(
       ("result" |-> OK)
       ("previous" |-> PREV)
       ("repeats" |-> COUNT)
       LOCALS)
endmodule

module IS-SORTED-SPEC
  imports IS-SORTED-WITH-LOOP-LEMMA

  claim [is-sorted-correct]:
    <k>
      #applyK(toCall(isSortedClosure),
              (list(intsToVals(INPUT:IntSeq)), .Vals))
      =>
      scanResult(scanAll(true, 0, 0, INPUT))
    </k>
    <env> 0 => 0 </env>
    <scopes>
      0 |-> scope("is_sorted" |-> isSortedClosure, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope("is_sorted" |-> isSortedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
endmodule
