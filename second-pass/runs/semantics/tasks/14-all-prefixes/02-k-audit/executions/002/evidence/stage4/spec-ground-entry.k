requires "verification.k"

module SPEC-GROUND-ENTRY
  imports VERIFICATION

  // S = "" has zero loop iterations and returns a freshly allocated empty list.
  claim
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("all_prefixes"), (str(.IntSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "all_prefixes" |-> closureVal(
             "string", .ParamNames, allPrefixesBody(), 0),
           parent(-1))
         -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // S = "abc" returns ["a", "ab", "abc"], written without a summary symbol.
  claim
    <k>
      #loadAll(solutionModule())
      ~> Call(
           Name("all_prefixes"),
           (str(iCons(97, iCons(98, iCons(99, .IntSeq)))), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "all_prefixes" |-> closureVal(
             "string", .ParamNames, allPrefixesBody(), 0),
           parent(-1))
         -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(iCons(97, .IntSeq)),
             vCons(
               str(iCons(97, iCons(98, .IntSeq))),
               vCons(
                 str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
                 .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
