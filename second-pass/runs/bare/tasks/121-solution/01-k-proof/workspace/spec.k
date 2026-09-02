requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [example-one]:
    <k> run(solutionProgram,
          cons(5, cons(8, cons(7, cons(1, nil)))),
          cons(5, cons(8, cons(7, cons(1, nil)))), 0)
      => result(12) ... </k>

  claim [example-two]:
    <k> run(solutionProgram,
          cons(3, cons(3, cons(3, cons(3, cons(3, nil))))),
          cons(3, cons(3, cons(3, cons(3, cons(3, nil))))), 0)
      => result(9) ... </k>

  claim [example-three]:
    <k> run(solutionProgram,
          cons(30, cons(13, cons(24, cons(321, nil)))),
          cons(30, cons(13, cons(24, cons(321, nil)))), 0)
      => result(0) ... </k>

  claim [all-integer-lists]:
    <k> run(solutionProgram, INPUT, _ORIGINAL, ACC)
      => result(expected(INPUT, ACC)) ... </k>
endmodule
