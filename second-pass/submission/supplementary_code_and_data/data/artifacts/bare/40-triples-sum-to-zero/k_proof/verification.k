requires "semantic.k"

module VERIFICATION
  imports MPY

  // These three constants quote the exact source tree.  They let helper
  // claims name execution states without weakening the program pattern.
  syntax Stmts ::= "pairBody" [function]
                 | "tripleBody" [function]
  syntax Program ::= "solutionProgram" [function]
  syntax Map ::= "solutionFunctions" [function]

  rule pairBody =>
    If(UnaryOp("not", Name("rest")),
      Return(Bool(false)) .Stmts,
      .Stmts)
    If(Compare(
      BinOp(
        "-",
        BinOp("-", Int(0), Name("first")),
        Subscript(Name("rest"), Int(0))),
      CmpOp(
        "in",
        Subscript(Name("rest"), Slice(Int(1), NoBound, NoBound))),
      .CmpOps),
      Return(Bool(true)) .Stmts,
      .Stmts)
    Return(
      Call(
        Name("_has_pair_sum"),
        Name("first"),
        Subscript(Name("rest"), Slice(Int(1), NoBound, NoBound)),
        .Exprs))
    .Stmts

  rule tripleBody =>
    If(UnaryOp("not", Name("l")),
      Return(Bool(false)) .Stmts,
      .Stmts)
    If(Call(
      Name("_has_pair_sum"),
      Subscript(Name("l"), Int(0)),
      Subscript(Name("l"), Slice(Int(1), NoBound, NoBound)),
      .Exprs),
      Return(Bool(true)) .Stmts,
      .Stmts)
    Return(
      Call(
        Name("triples_sum_to_zero"),
        Subscript(Name("l"), Slice(Int(1), NoBound, NoBound)),
        .Exprs))
    .Stmts

  rule solutionProgram =>
    Module(
      FuncDef(
        "_has_pair_sum", Params("first", "rest", .Ids), pairBody)
      FuncDef(
        "triples_sum_to_zero", Params("l", .Ids), tripleBody)
      .Stmts)

  rule solutionFunctions =>
    ("_has_pair_sum" |->
      function(Params("first", "rest", .Ids), pairBody))
    ("triples_sum_to_zero" |->
      function(Params("l", .Ids), tripleBody))

  // Independent mathematical specification: choose a first position, then a
  // later second position, then test for the required value at a later third
  // position.  Thus the three positions are necessarily distinct.
  syntax Bool ::= hasPairWith(Int, Ints) [function, total]
                | hasZeroTriple(Ints) [function, total]

  rule hasPairWith(_, .Ints) => false
  rule hasPairWith(I, J ; IS)
    => memberInt(0 -Int I -Int J, IS) orBool hasPairWith(I, IS)

  rule hasZeroTriple(.Ints) => false
  rule hasZeroTriple(I ; IS)
    => hasPairWith(I, IS) orBool hasZeroTriple(IS)
endmodule
