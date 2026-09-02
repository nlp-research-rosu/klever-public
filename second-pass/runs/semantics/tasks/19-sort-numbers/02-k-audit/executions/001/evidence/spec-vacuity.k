requires "verification.k"

module AUDITOR-SPEC-VACUITY
  imports SORT-NUMBERS-VERIFICATION

  // Deliberately false: it claims every result contains one additional zero.
  // Satisfying witness WORDS=.NumWords has actual output "" but mutated output
  // "zero" under the supplied sortKeyVS contract.
  claim [sort-numbers-extra-zero]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("sort_numbers"), str(encodedWords(WORDS:NumWords)))
        => numericOutput(nw(zeroW, WORDS)) </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1)))
             (-1 |-> builtinsScope) => ?_:Map </scopes>
    <scopeLoc> 1 => ?_:Int </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List => ?_:List </stack>
    <ret> noRet => ?_:RetState </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
