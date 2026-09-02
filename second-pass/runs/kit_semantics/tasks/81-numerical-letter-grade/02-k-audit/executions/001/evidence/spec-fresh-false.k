requires "verification.k"

module SPEC-FRESH-FALSE
  imports VERIFICATION

  // Fresh audit mutation. Empty input satisfies the numeric precondition, but
  // the real program returns [], while this postcondition requires ["A+"].
  claim [wrong-empty-result]:
    <k>
      #loadAll(GRADE-PROGRAM)
      ~> Call(
           Name("numerical_letter_grade"),
           (list(.ValSeq), .Exprs)
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
      0 |-> list(
        vCons(str(strToCodes("A+")), .ValSeq)
      )
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
