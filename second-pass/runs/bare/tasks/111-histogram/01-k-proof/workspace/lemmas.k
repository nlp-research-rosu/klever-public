requires "verification.k"

module VERIFIED-LOOP-LEMMAS
  imports VERIFICATION

  // These equations are the induction closures of the base/step obligations
  // proved in COUNT-LOOP-SPEC and SELECT-LOOP-SPEC. They are kept in a
  // separate compiled layer so those obligations cannot use the equations
  // they are establishing.
  rule execFor(Name("letter"), WORDS:List,
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
    => normal(countLoop(WORDS, ENV))

  rule execFor(Name("letter"), WORDS:List,
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
    => normal(selectLoop(WORDS, ENV))
endmodule
