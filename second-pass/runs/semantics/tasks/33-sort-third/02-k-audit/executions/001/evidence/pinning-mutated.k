requires "verification.k"

module PINNING-MUTATED
  imports VERIFICATION

  // Reviewer mutation: only the branch divisor is changed from 3 to 2.
  // The real-program pinning equality must reject this AST.
  claim
    <k>
      sortThirdModule
      =>
      Module(
        FuncDef("sort_third", Params("l"),
          Expr(Str("Sort the elements whose indices are divisible by three."))
          Assign(
            Name("thirds"),
            Call(
              Name("sorted"),
              Subscript(Name("l"), Slice(NoBound, NoBound, Int(3)))))
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("i"), Int(0))
          Assign(Name("value"), NoneVal)
          For(Name("value"), Name("l"),
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("thirds"), BinOp("//", Name("i"), Int(3))))),
              Expr(Call(Attribute(Name("result"), "append"), Name("value"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result"))))
    </k>
endmodule
