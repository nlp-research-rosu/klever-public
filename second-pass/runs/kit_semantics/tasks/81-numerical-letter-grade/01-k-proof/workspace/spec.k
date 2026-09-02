requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k> #loop(list(VS:ValSeq), Name("grade"), GRADE-STEP) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(
          "grades"        |-> INPUT:Val
          "letter_grades" |-> ref(H:Int)
          "grade"         |-> OLDGRADE:Val,
          parent(0)
        )
        =>
        scope(
          "grades"        |-> INPUT
          "letter_grades" |-> ref(H)
          "grade"         |-> ?FINALGRADE:Val,
          parent(0)
        )
      ) ...
    </scopes>
    <heap>
      ... H |-> list(ACC:ValSeq => gradeAcc(ACC, VS)) ...
    </heap>
    requires allGradeNumbers(VS)

  claim [entry]:
    <k>
      #loadAll(GRADE-PROGRAM)
      ~> Call(
           Name("numerical_letter_grade"),
           (list(VS:ValSeq), .Exprs)
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
      .Map => 0 |-> list(gradeAcc(.ValSeq, VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
    requires allGradeNumbers(VS)
endmodule
