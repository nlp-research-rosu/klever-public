requires "verification.k"

module AUDITOR-GROUND-SPEC
  imports VERIFICATION

  claim [ground-empty]:
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("anti_shuffle"), str(.IntSeq), .Exprs)
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // "ba a" -> "ab a"; witnesses insertion-before, append, and separator paths.
  claim [ground-ba-space-a]:
    <k>
      #loadAll(solutionModule())
      ~> Call(
           Name("anti_shuffle"),
           str(iCons(98, iCons(97, iCons(32, iCons(97, .IntSeq))))),
           .Exprs)
      =>
      str(iCons(97, iCons(98, iCons(32, iCons(97, .IntSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // "aa" -> "aa"; witnesses the comparison-equality path.
  claim [ground-duplicate]:
    <k>
      #loadAll(solutionModule())
      ~> Call(
           Name("anti_shuffle"),
           str(iCons(97, iCons(97, .IntSeq))),
           .Exprs)
      =>
      str(iCons(97, iCons(97, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
