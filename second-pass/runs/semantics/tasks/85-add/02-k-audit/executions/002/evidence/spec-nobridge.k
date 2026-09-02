requires "/audit-output/evidence/verification-nobridge.k"

module SPEC-NOBRIDGE
  imports VERIFICATION-NOBRIDGE

  claim [loop-invariant-bound]:
    <k>
      #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
      =>
      .K
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(
        ("lst" |-> LST:Val)
        ("total" |-> ACC)
        ("odd_index" |-> ODD)
        ("value" |-> OLDVALUE:Int),
        PARENT:Parent))
      RESTSCOPES:Map
      =>
      (L |-> scope(
        ("total" |-> addAccSpec(INPUT, ODD, ACC))
        ?FINALBINDINGS:Map,
        PARENT))
      RESTSCOPES
    </scopes>
    requires notBool (L in_keys(RESTSCOPES))

  claim [add-correct]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("add"), (list(intVals(INPUT:IntSeq)), .Exprs))
      =>
      addAccSpec(INPUT, false, 0)
    </k>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <env> 0 </env>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
