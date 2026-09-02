requires "verification.k"

module CONNECTION-GROUND-SPEC
  imports VERIFICATION

  claim [count-ground-three-items]:
    <k>
      execFor(Name("letter"),
        ListItem(pyString("a"))
        ListItem(pyString("b"))
        ListItem(pyString("a")),
        If(Compare(Name("letter"), CmpOp("in", Name("counts"))),
          Assign(Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
          Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp(">", Name("maximum"))),
          Assign(Name("maximum"), Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        initialEnv(
          ListItem(pyString("a"))
          ListItem(pyString("b"))
          ListItem(pyString("a"))))
      => normal(countLoop(
          ListItem(pyString("a"))
          ListItem(pyString("b"))
          ListItem(pyString("a")),
          initialEnv(
            ListItem(pyString("a"))
            ListItem(pyString("b"))
            ListItem(pyString("a")))))
    </k>

  claim [select-ground-winner-and-loser]:
    <k>
      execFor(Name("letter"),
        ListItem(pyString("a"))
        ListItem(pyString("b")),
        If(Compare(Subscript(Name("counts"), Name("letter")),
                   CmpOp("==", Name("maximum"))),
          Assign(Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
          .Stmts),
        beforeSelect(
          ListItem(pyString("a"))
          ListItem(pyString("b"))
          ListItem(pyString("a"))))
      => normal(selectLoop(
          ListItem(pyString("a"))
          ListItem(pyString("b")),
          beforeSelect(
            ListItem(pyString("a"))
            ListItem(pyString("b"))
            ListItem(pyString("a")))))
    </k>
endmodule
