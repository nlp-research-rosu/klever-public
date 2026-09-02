requires "/tmp/audit-work/104-unique-digits/candidate/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: [1] satisfies positiveInts but must return [1], not [].
  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(1, .Ints)))
        => pyList(.Ints) ... </k>
    requires positiveInts(cons(1, .Ints))
endmodule
