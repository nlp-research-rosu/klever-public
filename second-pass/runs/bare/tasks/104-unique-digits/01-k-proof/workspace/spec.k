requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal end-to-end contract for every list in the prompt's domain.
  // solutionProgram expands to the complete AST in solution.mpy.
  claim <k> solutionProgram ~> invoke("unique_digits", pyList(NS))
        => pyList(uniqueDigitsSpec(NS)) ... </k>
    requires positiveInts(NS)

  // Concrete digit checks cover both branches of the decimal predicate.
  claim <k> allDecimalDigitsOdd(97531) => true ... </k>
  claim <k> allDecimalDigitsOdd(1422) => false ... </k>

  // The two examples supplied by the original prompt.
  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(15, cons(33, cons(1422, cons(1, .Ints))))))
        => pyList(cons(1, cons(15, cons(33, .Ints)))) ... </k>

  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(152, cons(323, cons(1422, cons(10, .Ints))))))
        => pyList(.Ints) ... </k>
endmodule
