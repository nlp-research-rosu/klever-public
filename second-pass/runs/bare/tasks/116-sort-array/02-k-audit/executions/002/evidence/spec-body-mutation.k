requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  // Reviewer mutation: the executed sort_array body now returns [99] on [].
  // The original empty-result obligation must therefore become false.
  claim [empty-body-mutation]:
    <k> #run(solutionProgram, listV(.Ints))
      => listV(.Ints) </k>
endmodule
