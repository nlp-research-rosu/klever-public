requires "/tmp/audit-work/104-unique-digits-audit-002/source/verification.k"

module AUDIT-BRIDGE-CONTEXT
  imports VERIFICATION

  // The operational bridge accepts and preserves an arbitrary suffix.
  claim <k> solutionProgram
            ~> invoke("unique_digits", pyList(cons(15, cons(2, .Ints))))
            ~> pyBool(false)
        => pyList(cons(15, .Ints)) ~> pyBool(false) ... </k>
endmodule
