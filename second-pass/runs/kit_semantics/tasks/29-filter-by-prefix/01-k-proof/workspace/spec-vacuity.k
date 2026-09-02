requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the realizable input (["abc"], "a"): the result is not empty.
  claim [wrong-empty-result]:
    <k>
      #loadAll(filterByPrefixProgram)
      ~> Call(
           Name("filter_by_prefix"),
           list(
             vCons(
               str(strToCodes("abc")),
               .ValSeq)),
           str(strToCodes("a")))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             .Map
             => "filter_by_prefix" |->
                  closureVal(
                    ("strings", "prefix"),
                    filterFunctionBody,
                    0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
