requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION

  claim [ground-distinct]:
    <k> #loadAll(solutionProgram)
         ~> Call(Name("next_smallest"),
                 (list(vCons(3, vCons(1, vCons(2, .ValSeq)))), .Exprs))
        => 2 </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "next_smallest" |->
                    closureVal(("lst", .ParamNames), nextSmallestBody, 0),
                  parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-no-second]:
    <k> #loadAll(solutionProgram)
         ~> Call(Name("next_smallest"),
                 (list(vCons(1, vCons(1, .ValSeq))), .Exprs))
        => noneV </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "next_smallest" |->
                    closureVal(("lst", .ParamNames), nextSmallestBody, 0),
                  parent(-1)))
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
