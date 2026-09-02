requires "/tmp/audit-work/104-unique-digits-audit-002/source/verification.k"

module AUDIT-CLAIM-ENTRY
  imports VERIFICATION
  claim <k> solutionProgram ~> invoke("unique_digits", pyList(NS))
        => pyList(uniqueDigitsSpec(NS)) ... </k>
    requires positiveInts(NS)
endmodule

module AUDIT-CLAIM-DIGITS-TRUE
  imports VERIFICATION
  claim <k> allDecimalDigitsOdd(97531) => true ... </k>
endmodule

module AUDIT-CLAIM-DIGITS-FALSE
  imports VERIFICATION
  claim <k> allDecimalDigitsOdd(1422) => false ... </k>
endmodule

module AUDIT-CLAIM-EXAMPLE-ONE
  imports VERIFICATION
  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(15, cons(33, cons(1422, cons(1, .Ints))))))
        => pyList(cons(1, cons(15, cons(33, .Ints)))) ... </k>
endmodule

module AUDIT-CLAIM-EXAMPLE-TWO
  imports VERIFICATION
  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(152, cons(323, cons(1422, cons(10, .Ints))))))
        => pyList(.Ints) ... </k>
endmodule
