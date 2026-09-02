requires "verification.k"

module AUDIT-CONCRETE-ENTRY-WITNESS
  imports VERIFICATION

  // Concrete substitution into the target summary for ["1", "20", "13579"].
  claim [entry-result-1-0-5]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("odd_count"),
              list(vCons(str(iCons(49, .IntSeq)),
                   vCons(str(iCons(50, iCons(48, .IntSeq))),
                   vCons(str(iCons(49, iCons(51, iCons(53, iCons(55, iCons(57, .IntSeq)))))),
                         .ValSeq)))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(sentenceVal(1),
                   vCons(sentenceVal(0),
                   vCons(sentenceVal(5), .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
