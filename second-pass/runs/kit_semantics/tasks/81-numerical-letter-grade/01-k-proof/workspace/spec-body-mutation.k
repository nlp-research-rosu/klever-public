requires "mutation.k"

module SPEC-BODY-MUTATION
  imports MUTATION

  // This is the real loop machinery with a materially wrong body but the
  // original result summary. A sound, body-sensitive theory must reject it.
  claim [wrong-loop-body]:
    <k> #loop(list(VS:ValSeq), Name("grade"), MUTANT-STEP) => .K ... </k>
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
endmodule
