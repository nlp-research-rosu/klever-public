requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-GROUND-WITNESSES
  imports VERIFICATION

  // The empty sequence satisfies the entry/loop numeric-domain predicate.
  claim [empty-precondition]:
    <k> allGradeNumbers(.ValSeq) => true </k>

  // Concrete substitution of the documented satisfying input into gradeAcc.
  claim [example-summary]:
    <k>
      gradeAcc(
        .ValSeq,
        vCons(4.0,
          vCons(3,
            vCons(1.7,
              vCons(2,
                vCons(3.5, .ValSeq)))))
      )
      =>
      vCons(str(strToCodes("A+")),
        vCons(str(strToCodes("B")),
          vCons(str(strToCodes("C-")),
            vCons(str(strToCodes("C")),
              vCons(str(strToCodes("A-")), .ValSeq)))))
    </k>

  // A fully realizable ground instance of the actual entry configuration.
  claim [empty-entry]:
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
      .Map => 0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
