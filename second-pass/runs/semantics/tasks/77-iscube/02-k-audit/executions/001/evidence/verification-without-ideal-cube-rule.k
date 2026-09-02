requires "reference-semantics/semantics.k"

module ISCube-VERIFICATION
  imports MPY

  // The reference semantics deliberately leaves symbolic floating-point
  // operations opaque.  These task-local constructors preserve the exact
  // dataflow of 1 / 3, x ** (1 / 3), and round(...) without invoking Float
  // hooks that the Haskell proof backend does not implement.
  syntax Val ::= "oneThirdV" | cubeRootV(Int)
  syntax Int ::= roundedCubeRoot(Int)
    [function, total, symbol(roundedCubeRoot), no-evaluators]

  rule applyBin("/", 1, 3) => oneThirdV [priority(40)]
  rule applyBin("**", I:Int, oneThirdV) => cubeRootV(I)
  rule applyBuiltin("round", cubeRootV(I:Int), .Vals)
    => roundedCubeRoot(I)

  // Nonlinear non-negativity is outside the arithmetic fragment discharged
  // reliably by the backend, so expose the four abs normalizations used by
  // the partition claims.
  rule absInt(N *Int N *Int N) => N *Int N *Int N
    requires N >=Int 0
    [simplification]
  rule absInt(0 -Int (N *Int N *Int N)) => N *Int N *Int N
    requires N >Int 0
    [simplification]
  rule absInt(N *Int N *Int N +Int D) => N *Int N *Int N +Int D
    requires N >=Int 0
     andBool D >Int 0
    [simplification]
  rule absInt(0 -Int (N *Int N *Int N +Int D))
    => N *Int N *Int N +Int D
    requires N >=Int 0
     andBool D >Int 0
    [simplification]

  // Ideal-real summaries for the opaque rounded cube-root operation.  The
  // second rule covers every integer strictly between N^3 and (N+1)^3 by
  // writing it N^3 + D, where 0 < D < 3*N^2 + 3*N + 1.
  rule
    (roundedCubeRoot(N *Int N *Int N +Int D) ^Int 3)
      ==Int (N *Int N *Int N +Int D)
    => false
    requires N >=Int 0
     andBool D >Int 0
     andBool D <Int (3 *Int N *Int N +Int 3 *Int N +Int 1)
    [simplification]

  // This closure is a literal K rendering of solution.mpy, factored out so
  // each proof claim starts from the same loaded module scope.
  syntax Val ::= "iscubeClosure" [function, total]
  rule iscubeClosure =>
    closureVal(
      ("a", .ParamNames),
      Assign(Name("a"), Call(Name("abs"), Name("a")))
      Return(
        Compare(
          BinOp(
            "**",
            Call(
              Name("int"),
              Call(
                Name("round"),
                BinOp("**", Name("a"),
                  BinOp("/", Int(1), Int(3))))),
            Int(3)),
          CmpOp("==", Name("a"))))
      .Stmts,
      0)
endmodule
