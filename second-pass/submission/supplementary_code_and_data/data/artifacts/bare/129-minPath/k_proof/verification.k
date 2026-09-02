requires "semantic.k"

module MINPATH-VERIFICATION
  imports MPY

  // Compact value constructors used only to state readable claims.  They
  // expand to the same vList/ListItem representation consumed by MPY.
  syntax Val ::= "grid2" "(" Int "," Int "," Int "," Int ")" [function]
               | "grid3" "(" Int "," Int "," Int "," Int "," Int ","
                            Int "," Int "," Int "," Int ")" [function]
               | "path1" "(" Int ")" [function]
               | "path3" "(" Int ")" [function]
               | "path5" "(" Int ")" [function]
               | "path6" "(" Int ")" [function]

  rule grid2(A, B, C, D) =>
    vList(ListItem(vList(ListItem(vInt(A)) ListItem(vInt(B))))
          ListItem(vList(ListItem(vInt(C)) ListItem(vInt(D)))))

  rule grid3(A, B, C, D, E, F, G, H, I) =>
    vList(ListItem(vList(ListItem(vInt(A)) ListItem(vInt(B)) ListItem(vInt(C))))
          ListItem(vList(ListItem(vInt(D)) ListItem(vInt(E)) ListItem(vInt(F))))
          ListItem(vList(ListItem(vInt(G)) ListItem(vInt(H)) ListItem(vInt(I)))))

  rule path1(_M) => vList(ListItem(vInt(1)))
  rule path3(M) =>
    vList(ListItem(vInt(1)) ListItem(vInt(M)) ListItem(vInt(1)))
  rule path5(M) =>
    vList(ListItem(vInt(1)) ListItem(vInt(M)) ListItem(vInt(1))
          ListItem(vInt(M)) ListItem(vInt(1)))
  rule path6(M) =>
    vList(ListItem(vInt(1)) ListItem(vInt(M)) ListItem(vInt(1))
          ListItem(vInt(M)) ListItem(vInt(1)) ListItem(vInt(M)))

  syntax Bool ::= "validTail" "(" Int "," Int "," Int ")" [function]
  rule validTail(A, B, C) =>
    A >=Int 2 andBool A <=Int 4 andBool
    B >=Int 2 andBool B <=Int 4 andBool
    C >=Int 2 andBool C <=Int 4 andBool
    A =/=Int B andBool A =/=Int C andBool B =/=Int C

  // This constant expands to the exact constructor term emitted in
  // solution.mpy. Keeping
  // it as a Program term lets specifications share the program without adding
  // any proof-only execution rule.
  syntax Program ::= "solutionProgram"
  rule solutionProgram =>
    Module(
      FuncDef("minPath", Params("grid", "k"),
        Assign(Name("n"), Call(Name("len"), Name("grid")))
        Assign(Name("x"), Int(0))
        Assign(Name("y"), Int(0))
        Assign(Name("i"), Int(0))
        While(Compare(Name("i"), CmpOp("<", Name("n"))),
          Assign(Name("j"), Int(0))
          While(Compare(Name("j"), CmpOp("<", Name("n"))),
            If(Compare(
              Subscript(Subscript(Name("grid"), Name("i")), Name("j")),
              CmpOp("==", Int(1))),
              Assign(Name("x"), Name("i"))
              Assign(Name("y"), Name("j")),
              .Stmts)
            Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Assign(Name("best"),
          BinOp("+", BinOp("*", Name("n"), Name("n")), Int(1)))
        If(Compare(Name("x"), CmpOp(">", Int(0))),
          If(Compare(
            Subscript(
              Subscript(Name("grid"), BinOp("-", Name("x"), Int(1))),
              Name("y")),
            CmpOp("<", Name("best"))),
            Assign(Name("best"),
              Subscript(
                Subscript(Name("grid"), BinOp("-", Name("x"), Int(1))),
                Name("y"))),
            .Stmts),
          .Stmts)
        If(Compare(BinOp("+", Name("x"), Int(1)), CmpOp("<", Name("n"))),
          If(Compare(
            Subscript(
              Subscript(Name("grid"), BinOp("+", Name("x"), Int(1))),
              Name("y")),
            CmpOp("<", Name("best"))),
            Assign(Name("best"),
              Subscript(
                Subscript(Name("grid"), BinOp("+", Name("x"), Int(1))),
                Name("y"))),
            .Stmts),
          .Stmts)
        If(Compare(Name("y"), CmpOp(">", Int(0))),
          If(Compare(
            Subscript(
              Subscript(Name("grid"), Name("x")),
              BinOp("-", Name("y"), Int(1))),
            CmpOp("<", Name("best"))),
            Assign(Name("best"),
              Subscript(
                Subscript(Name("grid"), Name("x")),
                BinOp("-", Name("y"), Int(1)))),
            .Stmts),
          .Stmts)
        If(Compare(BinOp("+", Name("y"), Int(1)), CmpOp("<", Name("n"))),
          If(Compare(
            Subscript(
              Subscript(Name("grid"), Name("x")),
              BinOp("+", Name("y"), Int(1))),
            CmpOp("<", Name("best"))),
            Assign(Name("best"),
              Subscript(
                Subscript(Name("grid"), Name("x")),
                BinOp("+", Name("y"), Int(1)))),
            .Stmts),
          .Stmts)
        Assign(Name("answer"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        While(Compare(Name("i"), CmpOp("<", Name("k"))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Expr(Call(Attribute(Name("answer"), "append"), Int(1))),
            Expr(Call(Attribute(Name("answer"), "append"), Name("best"))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("answer"))))
endmodule
