requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Canonical program term used by spec.k.  prove.sh macro-expands this term
  // and solution.mpy and compares their canonical KAST, binding the proof to
  // the freshly translated implementation rather than to a stale copy.
  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("prime_length", Params("string"), CellVars("n"), FreeVars(.Strings),
        Assign(Name("n"), Call(Name("len"), Name("string")))
        Return(
          BoolOp(
            "and",
            Compare(Name("n"), CmpOp(">=", Int(2))),
            Call(
              Name("all"),
              GenExp(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("!=", Int(0))),
                CompFor(
                  Name("i"),
                  Call(Name("range"), Int(2), Name("n")),
                  Bool(true))))))))

  // Mathematical contract used by the reachability specification.  For
  // N >= 2, N is prime exactly when no integer in [2, N) divides it.
  syntax Bool ::= isPrime(Int) [function, total]
  rule isPrime(N) => (N >=Int 2 andBool noDivisors(N, 2, N))
endmodule
