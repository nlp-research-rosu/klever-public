requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Haskell kprove has no FLOAT.int2float hook.  MPY intentionally treats
  // intToF as an opaque proof-domain primitive, but its [concrete] twin is
  // nevertheless selected by the backend for mixed symbolic arithmetic.
  // Reify that existing trust boundary as a constructor in proof definitions.
  // The input remains visible, so claims are parametric in the conversion.
  syntax Float ::= proofIntToF(Int)
    [function, total, symbol(proofIntToF), no-evaluators]
  rule intToF(I:Int) => proofIntToF(I) [simplification]

  // Exact quotation of solution.mpy.  This is data consumed by the fixed
  // #loadAll/definition/call semantics; it does not summarize execution.
  syntax Module ::= triangleProgram() [function, total]
  rule triangleProgram() =>
    Module(
      Import("math")
      FuncDef("triangle_area", Params("a", "b", "c"),
        If(BoolOp(
          "or",
          Compare(BinOp("+", Name("a"), Name("b")), CmpOp("<=", Name("c"))),
          Compare(BinOp("+", Name("a"), Name("c")), CmpOp("<=", Name("b"))),
          Compare(BinOp("+", Name("b"), Name("c")), CmpOp("<=", Name("a")))),
          Return(UnaryOp("-", Int(1))),
          .Stmts)
        Assign(
          Name("semi_perimeter"),
          BinOp(
            "/",
            BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
            Int(2)))
        Assign(
          Name("area"),
          Call(
            Attribute(Name("math"), "sqrt"),
            BinOp(
              "*",
              BinOp(
                "*",
                BinOp(
                  "*",
                  Name("semi_perimeter"),
                  BinOp("-", Name("semi_perimeter"), Name("a"))),
                BinOp("-", Name("semi_perimeter"), Name("b"))),
              BinOp("-", Name("semi_perimeter"), Name("c")))))
        Return(Call(Name("round"), Name("area"), Int(2)))))

  // Contract-level summaries.  Each equation merely names the value of the
  // validity predicate or Heron expression using fixed MPY operators.
  syntax Bool ::= invalidTriangle(Val, Val, Val) [function, total]
  rule invalidTriangle(A, B, C) =>
       applyCmp("<=", applyBin("+", A, B), C)
    orBool applyCmp("<=", applyBin("+", A, C), B)
    orBool applyCmp("<=", applyBin("+", B, C), A)

  syntax Val ::= semiPerimeter(Val, Val, Val) [function, total]
  rule semiPerimeter(A, B, C) =>
    applyBin("/", applyBin("+", applyBin("+", A, B), C), 2)

  syntax Val ::= heronProduct(Val, Val, Val) [function, total]
  rule heronProduct(A, B, C) =>
    applyBin(
      "*",
      applyBin(
        "*",
        applyBin(
          "*",
          semiPerimeter(A, B, C),
          applyBin("-", semiPerimeter(A, B, C), A)),
        applyBin("-", semiPerimeter(A, B, C), B)),
      applyBin("-", semiPerimeter(A, B, C), C))

  syntax Val ::= triangleAreaSpec(Val, Val, Val) [function, total]
  rule triangleAreaSpec(A, B, C) =>
    #if invalidTriangle(A, B, C)
    #then -1
    #else applyBuiltin(
            "round",
            sqrtF({heronProduct(A, B, C)}:>Float),
            (2, .Vals))
    #fi
endmodule
