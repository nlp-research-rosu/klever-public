requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  // The right-hand side is the trusted-translator output in
  // regenerated-solution.mpy, represented with explicit empty-list tails.
  claim
    <mpy>
      <k> solutionProgram =>
        Module(
      FuncDef("_has_pair_sum", Params("first", "rest", .Ids),
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
        .Stmts)
      FuncDef("triples_sum_to_zero", Params("l", .Ids),
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
        .Stmts)
        .Stmts) </k>
      <funs> _FUNS </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>
endmodule
