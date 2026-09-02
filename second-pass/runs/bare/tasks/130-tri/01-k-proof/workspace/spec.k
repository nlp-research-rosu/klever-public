requires "verification.k"

module TRI-SPEC
  imports TRI-VERIFICATION

  // Inductive interpreter theorem.  Recursive Python calls re-enter this
  // judgment at N - 1, so the claim is also the proof's induction hypothesis.
  claim <k> evalCall(solutionProgram, "tri", N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0

  // End-to-end correctness from the semantics' configured entry point.
  claim <k> run(solutionProgram, N)
          => returned(LVal(triPrefix(N))) ... </k>
    requires N >=Int 0

  // Base values and both branches of the stated recurrence.
  claim <k> triValue(0) => 1 ... </k>
  claim <k> triValue(1) => 3 ... </k>
  claim <k> triValue(N) => 1 +Int (N /Int 2) ... </k>
    requires N >=Int 2 andBool N %Int 2 ==Int 0
  claim <k> triValue(N)
          => triValue(N -Int 1) +Int triValue(N -Int 2) +Int triValue(N +Int 1)
        ... </k>
    requires N >=Int 3 andBool N %Int 2 =/=Int 0
endmodule
