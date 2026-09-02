requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-WITNESS
  imports VERIFICATION

  // Satisfying instance of the universal entry claim:
  // candidate([-5, 2, -3]) + 10 = canonical([-5, 2, -3]) + 10 = 2.
  claim [universal-ground]:
    <k> run(solutionProgram,
          cons(-5, cons(2, cons(-3, nil))),
          cons(-5, cons(2, cons(-3, nil))), 10)
      => result(2) ... </k>

  // The operational rules frame rather than discard an immediate continuation.
  claim [continuation-preserved]:
    <k> run(solutionProgram,
          cons(5, cons(8, cons(7, cons(1, nil)))),
          cons(5, cons(8, cons(7, cons(1, nil)))), 0)
          ~> result(999)
      => result(12) ~> result(999) </k>
endmodule
