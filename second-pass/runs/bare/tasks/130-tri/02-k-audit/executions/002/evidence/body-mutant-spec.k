requires "verification-body-mutant.k"

module BODY-MUTANT-SPEC
  imports TRI-VERIFICATION-BODY-MUTANT

  // Deliberately false: the mutated program returns [1, 4] for N = 1.
  claim [body-sensitive]:
    <k> run(mutatedSolutionProgram, 1)
        => returned(LVal(cons(1, cons(3, nil)))) ... </k>
endmodule

