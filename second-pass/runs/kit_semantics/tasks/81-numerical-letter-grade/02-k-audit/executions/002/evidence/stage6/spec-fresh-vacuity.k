requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-FRESH-VACUITY
  imports VERIFICATION

  // Companion witness: the realizable empty input returns ref(0) to [].
  claim [correct-empty]:
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>

  // Fresh false result mutation: same state, but demands noneV instead of ref(0).
  claim [false-empty-return]:
    <k>
      #loadAll(GRADE-PROGRAM)
      ~> Call(
           Name("numerical_letter_grade"),
           (list(.ValSeq), .Exprs)
         )
      => noneV
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
