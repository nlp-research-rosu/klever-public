requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the empty input returns [], not ["E"].
  claim [false-empty-result]:
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
        vCons(str(strToCodes("E")), .ValSeq)
      )
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
