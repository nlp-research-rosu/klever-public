requires "/audit-output/evidence/stage5/body-mutant-verification.k"

module SPEC-ENTRY-BODY-MUTATION
  imports BODY-MUTANT-VERIFICATION

  // False for the mutated body: [4.0] now returns ["Z"], not ["A+"].
  claim [mutated-entry]:
    <k>
      #loadAll(MUTANT-PROGRAM)
      ~> Call(
           Name("numerical_letter_grade"),
           (list(vCons(4.0, .ValSeq)), .Exprs)
         )
      => ref(0)
    </k>
    <env> 0 => 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(str(strToCodes("A+")), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
