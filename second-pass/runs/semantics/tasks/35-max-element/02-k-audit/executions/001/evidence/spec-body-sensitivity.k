requires "verification-body-mutated.k"

module SPEC-BODY-SENSITIVITY
  imports MAX-ELEMENT-VERIFICATION-BODY-MUTATED

  // The original maximum obligation is false for the mutated body: it returns
  // 2 for this satisfying input instead of 9.
  claim [body-sensitive-ground]:
    <k> #loadAll(mutatedMaxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(2,
                       mutatedIntVals(iCons(0 -Int 1,
                                      iCons(9,
                                      iCons(0, .IntSeq)))))),
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
