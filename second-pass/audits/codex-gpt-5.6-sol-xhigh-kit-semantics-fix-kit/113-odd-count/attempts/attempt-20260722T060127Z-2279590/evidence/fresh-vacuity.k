requires "verification.k"

module AUDIT-FRESH-VACUITY
  imports VERIFICATION

  // Input ["2"] satisfies digitStrings. Its real odd count is 0, so requiring
  // sentenceVal(1) deliberately falsifies the result-constraining obligation.
  claim [false-even-digit-result]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(Name("odd_count"),
              list(vCons(str(iCons(50, .IntSeq)), .ValSeq)))
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
