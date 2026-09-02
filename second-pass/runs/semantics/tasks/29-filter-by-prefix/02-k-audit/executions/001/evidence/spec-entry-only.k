requires "verification.k"

module FILTER-BY-PREFIX-ENTRY-ONLY-SPEC
  imports VERIFICATION

  claim
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          filterByPrefixDef))
      ~> Call(
           Name("filter_by_prefix"),
           stringList(INPUT:StrList),
           str(PREFIX:IntSeq))
      ~> #checkFilter(
           prefixFilter(PREFIX, INPUT))
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
      => 0 |-> list(prefixFilter(PREFIX, INPUT))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
