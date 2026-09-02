requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  // Reviewer-authored constructor-level identity check: expanding every local
  // syntax function used by sortThirdModule yields the exact submitted MPY
  // function binding and body.
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
          If(Compare(BinOp("%", Name("i"), Int(3)), CmpOp("==", Int(0))),
            Expr(
              Call(
                Attribute(Name("result"), "append"),
                Subscript(Name("thirds"), BinOp("//", Name("i"), Int(3))))),
            Expr(Call(Attribute(Name("result"), "append"), Name("value"))))
          AugAssign(Name("i"), "+", Int(1)))
        Return(Name("result"))))
    </k>
endmodule
