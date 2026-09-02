requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false at n=3: the real last element is 8, not 9.
  claim [false-result]:
    <k> #loadAll(Module(triDefinition))
         ~> Call(Name("tri"), Int(3))
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
              vCons(9, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
