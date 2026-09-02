requires "/tmp/audit-work/104-unique-digits/candidate/verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [entry]:
    <k> solutionProgram ~> invoke("unique_digits", pyList(NS))
      => pyList(uniqueDigitsSpec(NS)) ... </k>
    requires positiveInts(NS)

  claim [odd-true]:
    <k> allDecimalDigitsOdd(97531) => true ... </k>

  claim [odd-false]:
    <k> allDecimalDigitsOdd(1422) => false ... </k>

  claim [example-one]:
    <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(15, cons(33, cons(1422, cons(1, .Ints))))))
      => pyList(cons(1, cons(15, cons(33, .Ints)))) ... </k>

  claim [example-two]:
    <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(152, cons(323, cons(1422, cons(10, .Ints))))))
      => pyList(.Ints) ... </k>
endmodule
