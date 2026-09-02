requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [body-sensitive-witness]:
    <k> run(solutionProgram,
          cons(5, cons(8, nil)),
          cons(5, cons(8, nil)), 0)
      => result(expected(cons(5, cons(8, nil)), 0)) ... </k>
endmodule
