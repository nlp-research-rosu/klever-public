requires "verification.k"

module MAX-ELEMENT-GROUND-WITNESS
  imports MAX-ELEMENT-VERIFICATION

  // Satisfies the universal entry precondition with FIRST=2 and
  // REST=iCons(-1,iCons(9,iCons(9,iCons(0,.IntSeq)))).
  claim [ground-witness]:
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(2,
                       intVals(iCons(0 -Int 1,
                               iCons(9,
                               iCons(9,
                               iCons(0, .IntSeq))))))),
                  .Exprs))
      => 9 </k>
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
