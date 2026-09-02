requires "verification.k"

module MUTATED-LOOP-LEMMAS
  imports VERIFICATION

  // Deliberately false summary: discard every count-loop iteration.
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
    => normal(ENV)

  rule execFor(Name("letter"), WORDS:List,
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
    => normal(selectLoop(WORDS, ENV))
endmodule

module MUTATED-MAIN-SPEC
  imports MUTATED-LOOP-LEMMAS

  claim [wrong-bridge-must-not-prove]:
    <k>
      execute(histogramProgram(), "a b b a")
      => pyDict(
           pyString("a") |-> pyInt(2)
           pyString("b") |-> pyInt(2),
           ListItem(pyString("a"))
           ListItem(pyString("b")))
    </k>
endmodule
