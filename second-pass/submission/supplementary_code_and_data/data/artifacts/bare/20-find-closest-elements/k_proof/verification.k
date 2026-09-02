requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTIC

  // This is the exact constructor tree generated in solution.mpy, exposed as
  // a function so claims do not have to duplicate the program text.
  syntax Program ::= "solution" [function]
  rule solution =>
    Module(
      ImportFrom("typing", "List", "Tuple")
      FuncDef("find_closest_elements", Params("numbers"),
        Assign(Name("closest_a"), Subscript(Name("numbers"), Int(0)))
        Assign(Name("closest_b"), Subscript(Name("numbers"), Int(1)))
        If(Compare(Name("closest_b"), CmpOp("<", Name("closest_a"))),
          Assign(Name("temporary"), Name("closest_a"))
          Assign(Name("closest_a"), Name("closest_b"))
          Assign(Name("closest_b"), Name("temporary")),
          .Stmts)
        Assign(Name("best_gap"),
          BinOp("-", Name("closest_b"), Name("closest_a")))
        Assign(Name("i"), Int(0))
        While(Compare(Name("i"),
              CmpOp("<", Call(Name("len"), Name("numbers")))),
          Assign(Name("j"), BinOp("+", Name("i"), Int(1)))
          While(Compare(Name("j"),
                CmpOp("<", Call(Name("len"), Name("numbers")))),
            Assign(Name("a"), Subscript(Name("numbers"), Name("i")))
            Assign(Name("b"), Subscript(Name("numbers"), Name("j")))
            If(Compare(Name("b"), CmpOp("<", Name("a"))),
              Assign(Name("temporary"), Name("a"))
              Assign(Name("a"), Name("b"))
              Assign(Name("b"), Name("temporary")),
              .Stmts)
            Assign(Name("gap"), BinOp("-", Name("b"), Name("a")))
            If(Compare(Name("gap"), CmpOp("<", Name("best_gap"))),
              Assign(Name("best_gap"), Name("gap"))
              Assign(Name("closest_a"), Name("a"))
              Assign(Name("closest_b"), Name("b")),
              .Stmts)
            Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(TupleExpr(Name("closest_a"), Name("closest_b")))))

  // Readable constructors for proof inputs.
  syntax Value ::= nums(Rat, Rat) [function]
                 | nums(Rat, Rat, Rat, Rat) [function]
                 | nums(Rat, Rat, Rat, Rat, Rat, Rat) [function]
  rule nums(A, B) => vlist(vnum(A), vlist(vnum(B), vnil))
  rule nums(A, B, C, D) =>
    vlist(vnum(A), vlist(vnum(B), vlist(vnum(C), vlist(vnum(D), vnil))))
  rule nums(A, B, C, D, E, F) =>
    vlist(vnum(A), vlist(vnum(B), vlist(vnum(C),
      vlist(vnum(D), vlist(vnum(E), vlist(vnum(F), vnil))))))
endmodule
