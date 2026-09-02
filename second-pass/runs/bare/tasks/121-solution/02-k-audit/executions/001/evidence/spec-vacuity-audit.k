requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation of example one: the realizable source state returns
  // 12 in both Python implementations and the fixed K semantics, not 13.
  claim [false-example-one-result]:
    <k> run(solutionProgram,
          cons(5, cons(8, cons(7, cons(1, nil)))),
          cons(5, cons(8, cons(7, cons(1, nil)))), 0)
      => result(13) ... </k>
endmodule
