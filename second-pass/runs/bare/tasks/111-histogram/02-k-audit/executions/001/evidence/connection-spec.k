requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION

  claim [count-loop-universal-connection]:
    <k>
      execFor(Name("letter"), WORDS:List,
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
    </k>

  claim [select-loop-universal-connection]:
    <k>
      execFor(Name("letter"), WORDS:List,
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        ENV:Map)
      => normal(selectLoop(WORDS, ENV))
    </k>
endmodule
