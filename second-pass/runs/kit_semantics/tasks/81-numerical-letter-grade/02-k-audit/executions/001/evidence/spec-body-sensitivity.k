requires "verification-body-mutant.k"

module SPEC-BODY-SENSITIVITY
  imports AUDIT-BODY-MUTANT

  // The actual k-cell executes AUDIT-MUTANT-STEP while the destination retains
  // the original gradeAcc summary. A body-insensitive proof would accept this.
  claim [mutated-loop-body]:
    <k>
      #loop(list(VS:ValSeq), Name("grade"), AUDIT-MUTANT-STEP)
      => .K
      ...
    </k>
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
