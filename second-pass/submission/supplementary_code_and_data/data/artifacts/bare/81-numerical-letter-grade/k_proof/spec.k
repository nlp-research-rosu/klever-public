requires "verification.k"

module SPEC
  imports VERIFICATION

  // The loop handles the empty list and returns a fresh empty result.
  claim [empty-input]:
    <k> solutionProgram => .K </k>
    <input> .Vals </input>
    <env>
      .Map
      => ("grades" |-> list(.Vals)) ("result" |-> list(.Vals))
    </env>
    <result> noResult => list(.Vals) </result>

  // For every exact rational GPA (positive denominator), the translated
  // Python decision tree agrees with the independently stated grading table.
  // Symbolic execution splits this claim across every table interval.
  claim [all-single-grades]:
    <k> solutionProgram => .K </k>
    <input> num(P, Q) :: .Vals </input>
    <env>
      .Map
      =>
        "grade" |-> num(P, Q)
        "grades" |-> list(num(P, Q) :: .Vals)
        "result" |-> list(expectedGrade(P, Q) :: .Vals)
    </env>
    <result> noResult => list(expectedGrade(P, Q) :: .Vals) </result>
    requires Q >Int 0

  // Inductive loop invariant, first iteration: for any accumulated output
  // and any unprocessed tail, one iteration appends exactly the reference
  // grade and leaves the tail as the next loop state.
  claim [loop-step-new-variable]:
    <k>
      loop("grade", gradingBody, num(P, Q) :: REST)
      => loop("grade", gradingBody, REST)
    </k>
    <env>
      ("grades" |-> list(ALL)) ("result" |-> list(OUT))
      =>
      ("grade" |-> num(P, Q))
      ("grades" |-> list(ALL))
      ("result" |-> list(append(OUT, expectedGrade(P, Q))))
    </env>
    requires Q >Int 0

  // The same invariant for all later iterations, where the loop variable is
  // updated rather than inserted. Together with the empty-loop equation this
  // is the structural induction step for lists of arbitrary finite length.
  claim [loop-step-existing-variable]:
    <k>
      loop("grade", gradingBody, num(P, Q) :: REST)
      => loop("grade", gradingBody, REST)
    </k>
    <env>
      ("grade" |-> _OLD)
      ("grades" |-> list(ALL))
      ("result" |-> list(OUT))
      =>
      ("grade" |-> num(P, Q))
      ("grades" |-> list(ALL))
      ("result" |-> list(append(OUT, expectedGrade(P, Q))))
    </env>
    requires Q >Int 0

  claim [loop-empty]:
    <k> loop("grade", gradingBody, .Vals) => .K </k>

  // The prompt's full example additionally checks traversal, mutation order,
  // strict-boundary behavior, and preservation of output list order.
  claim [prompt-example]:
    <k> solutionProgram => .K </k>
    <input>
      num(4, 1) :: num(3, 1) :: num(17, 10) :: num(2, 1) :: num(35, 10) :: .Vals
    </input>
    <env>
      .Map
      =>
        "grade" |-> num(35, 10)
        "grades" |-> list(
          num(4, 1) :: num(3, 1) :: num(17, 10) :: num(2, 1) :: num(35, 10) :: .Vals)
        "result" |-> list(
          str("A+") :: str("B") :: str("C-") :: str("C") :: str("A-") :: .Vals)
    </env>
    <result>
      noResult
      => list(str("A+") :: str("B") :: str("C-") :: str("C") :: str("A-") :: .Vals)
    </result>
endmodule
