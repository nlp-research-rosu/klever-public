requires "verification.k"

module FILTER-BY-PREFIX-SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: ["a"] filtered by "a" is ["a"], not [].
  claim
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          filterByPrefixDef))
      ~> Call(
           Name("filter_by_prefix"),
           stringList(sCons(iCons(97, .IntSeq), .StrList)),
           str(iCons(97, .IntSeq)))
      ~> #checkFilter(.ValSeq)
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
