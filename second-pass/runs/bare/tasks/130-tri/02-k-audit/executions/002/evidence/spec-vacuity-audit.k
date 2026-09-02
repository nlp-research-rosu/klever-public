requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports TRI-VERIFICATION

  // Fresh false result mutation. Input N = 3 satisfies the entry domain, but
  // the real submitted body and generated semantics return [1, 3, 2, 8].
  claim [wrong-last-element]:
    <k> run(solutionProgram, 3)
        => returned(LVal(cons(1, cons(3, cons(2, cons(9, nil)))))) ... </k>
endmodule

