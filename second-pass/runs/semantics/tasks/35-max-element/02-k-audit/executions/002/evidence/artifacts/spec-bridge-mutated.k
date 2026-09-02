requires "verification-bridge-mutated.k"

module SPEC-BRIDGE-MUTATED
  imports MAX-ELEMENT-VERIFICATION-BRIDGE-MUTATED

  claim
    <k> #loadAll(maxElementProgramBridgeMutated)
         ~> Call(Name("max_element"),
                 (list(vCons(1,
                       intValsBridgeMutated(iCons(2, .IntSeq)))),
                  .Exprs))
      => 2 </k>
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
