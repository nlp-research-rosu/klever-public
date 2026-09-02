requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation. The source result is 5, but this demands 6.
  claim [false-off-by-one]:
    <k> run(solutionProgram,
          cons(5, cons(8, nil)),
          cons(5, cons(8, nil)), 0)
      => result(expected(cons(5, cons(8, nil)), 0) +Int 1) ... </k>
endmodule
