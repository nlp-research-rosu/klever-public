requires "verification.k"

module FILTER-BY-PREFIX-GROUND-CORRECT
  imports VERIFICATION

  // Witness: strings=["a", "b"], prefix="a", expected result=["a"].
  claim
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          filterByPrefixDef))
      ~> Call(
           Name("filter_by_prefix"),
           stringList(
             sCons(iCons(97, .IntSeq),
               sCons(iCons(98, .IntSeq), .StrList))),
           str(iCons(97, .IntSeq)))
      ~> #checkFilter(
           vCons(str(iCons(97, .IntSeq)), .ValSeq))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => ?FINALSC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(str(iCons(97, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
