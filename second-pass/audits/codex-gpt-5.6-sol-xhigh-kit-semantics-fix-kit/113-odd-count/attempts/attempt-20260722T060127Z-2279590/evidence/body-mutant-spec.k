requires "body-mutant-verification.k"

module AUDIT-BODY-MUTANT-SPEC
  imports AUDIT-BODY-MUTATION-VERIFICATION

  // The mutant increments by zero. The correct sentenceVal(1) for ["1"] must
  // therefore be unreachable if the proof is sensitive to the real body.
  claim [changed-body-must-not-prove]:
    <k>
      #loadAll(auditBodyMutantProgram)
      ~> Call(Name("odd_count"),
              list(vCons(str(iCons(49, .IntSeq)), .ValSeq)))
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
      .Map => 0 |-> list(vCons(sentenceVal(1), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
