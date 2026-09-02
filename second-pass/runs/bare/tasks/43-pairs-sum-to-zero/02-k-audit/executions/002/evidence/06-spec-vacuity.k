requires "candidate/verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Universal functional-correctness claim.  L is arbitrary: the proof
  // splits on emptiness and membership, and its recursive branch closes by
  // circularity on rest(L).
  claim
    <k>
      run(
        Module(
          FuncDef("pairs_sum_to_zero", Params("l"),
            If(UnaryOp("not", Name("l")),
              Return(Bool(false)) .Stmts,
              .Stmts)
            If(Compare(
              UnaryOp("-", Subscript(Name("l"), Int(0))),
              CmpOp("in", Subscript(Name("l"),
                Slice(Int(1), NoBound, NoBound)))),
              Return(Bool(true)) .Stmts,
              .Stmts)
            Return(Call(Name("pairs_sum_to_zero"),
              Subscript(Name("l"), Slice(Int(1), NoBound, NoBound))))
            .Stmts)
          .Stmts),
        L:ISeq)
      => pyBool(notBool hasZeroPair(L))
    </k>
    <program>
      Module(
        FuncDef("pairs_sum_to_zero", Params("l"),
          If(UnaryOp("not", Name("l")),
            Return(Bool(false)) .Stmts,
            .Stmts)
          If(Compare(
            UnaryOp("-", Subscript(Name("l"), Int(0))),
            CmpOp("in", Subscript(Name("l"),
              Slice(Int(1), NoBound, NoBound)))),
            Return(Bool(true)) .Stmts,
            .Stmts)
          Return(Call(Name("pairs_sum_to_zero"),
            Subscript(Name("l"), Slice(Int(1), NoBound, NoBound))))
          .Stmts)
        .Stmts)
    </program>
    <env> .Map </env>
endmodule
