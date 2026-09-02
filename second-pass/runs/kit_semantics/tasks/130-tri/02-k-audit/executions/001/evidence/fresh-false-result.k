requires "verification.k"

module AUDIT-FRESH-FALSE-RESULT
  imports VERIFICATION

  // N=5 is a satisfiable source-contract input. The actual last value is 15.
  // This fresh mutation requires 16, changing a result-constraining obligation.
  claim [n5-last-element-off-by-one]:
    <k> #loadAll(Module(triDefinition))
         ~> Call(Name("tri"), Int(5))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(1,
          vCons(3,
            vCons(2,
              vCons(8,
                vCons(3,
                  vCons(16, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
