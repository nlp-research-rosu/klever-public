requires "verification.k"

module GROUND-WITNESS
  imports MAX-ELEMENT-VERIFICATION

  claim
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(1,
                       intVals(iCons(2, iCons(3, .IntSeq))))),
                  .Exprs))
      => 3 </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope)
          => ?FINALSCOPES:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
