requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports MAX-ELEMENT-VERIFICATION-BODY-MUTATED

  claim
    <k> #loadAll(maxElementProgramMutated)
         ~> Call(Name("max_element"),
                 (list(vCons(1, vCons(2, vCons(3, .ValSeq)))), .Exprs))
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
