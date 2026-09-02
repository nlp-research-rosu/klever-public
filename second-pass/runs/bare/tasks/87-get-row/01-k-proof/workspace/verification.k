requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // These macros are the exact constructor tree emitted in solution.mpy.
  syntax Program ::= "solutionProgram" [macro]
  syntax Stmts ::= "getRowBody" [macro]

  rule solutionProgram =>
    Module(FuncDef("get_row", Params("lst", "x", .Strings), getRowBody))

  rule getRowBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("row"), Int(0))
    For(Name("values"), Name("lst"),
      Assign(Name("col"),
        BinOp("-", Call(Name("len"), Name("values"), .Exprs), Int(1)))
      While(Compare(Name("col"), CmpOp(">=", Int(0)), .CmpOps),
        If(Compare(Subscript(Name("values"), Name("col")),
                   CmpOp("==", Name("x")), .CmpOps),
          Assign(Name("result"),
            BinOp("+", Name("result"),
              ListExpr(TupleExpr(Name("row"), Name("col"), .Exprs), .Exprs))),
          .Stmts)
        Assign(Name("col"), BinOp("-", Name("col"), Int(1))))
      Assign(Name("row"), BinOp("+", Name("row"), Int(1))))
    Return(Name("result"))

  // A mathematical input domain: finite matrices whose elements are integers.
  syntax IntList ::= "inil" | "icons" "(" Int "," IntList ")"
  syntax Matrix ::= "mnil" | "mcons" "(" IntList "," Matrix ")"

  syntax VList ::= "encodeInts" "(" IntList ")" [function]
  rule encodeInts(inil) => vnil
  rule encodeInts(icons(I, IS)) => vcons(pyInt(I), encodeInts(IS))

  syntax VList ::= "encodeMatrix" "(" Matrix ")" [function]
  rule encodeMatrix(mnil) => vnil
  rule encodeMatrix(mcons(IS, MS)) =>
    vcons(pyList(encodeInts(IS)), encodeMatrix(MS))

  // Independent extensional contract. rowCoords returns matching columns in
  // descending order; matrixCoords concatenates rows in ascending order.
  syntax VList ::= "rowCoords" "(" IntList "," Int "," Int "," Int ")" [function, total]
  rule rowCoords(inil, _, _, _) => vnil
  rule rowCoords(icons(I, IS), X, R, C) =>
    coordStep(I ==Int X, IS, X, R, C)

  syntax VList ::= "coordStep" "(" Bool "," IntList "," Int "," Int "," Int ")" [function, total]
  rule coordStep(true, IS, X, R, C) =>
    vconcat(rowCoords(IS, X, R, C +Int 1),
            vcons(pyTuple(vcons(pyInt(R), vcons(pyInt(C), vnil))), vnil))
  rule coordStep(false, IS, X, R, C) => rowCoords(IS, X, R, C +Int 1)

  syntax VList ::= "matrixCoords" "(" Matrix "," Int "," Int ")" [function]
  rule matrixCoords(mnil, _, _) => vnil
  rule matrixCoords(mcons(IS, MS), X, R) =>
    vconcat(rowCoords(IS, X, R, 0), matrixCoords(MS, X, R +Int 1))

  syntax Matrix ::= "promptMatrix" [macro]
  syntax Matrix ::= "thirdMatrix" [macro]
  syntax Value ::= "promptInput" [macro]
  syntax Value ::= "thirdInput" [macro]

  rule promptMatrix =>
    mcons(icons(1, icons(2, icons(3, icons(4, icons(5, icons(6, inil)))))),
    mcons(icons(1, icons(2, icons(3, icons(4, icons(1, icons(6, inil)))))),
    mcons(icons(1, icons(2, icons(3, icons(4, icons(5, icons(1, inil)))))),
    mnil)))

  rule promptInput => pyList(encodeMatrix(promptMatrix))

  rule thirdMatrix =>
    mcons(inil, mcons(icons(1, inil),
      mcons(icons(1, icons(2, icons(3, inil))), mnil)))

  rule thirdInput => pyList(encodeMatrix(thirdMatrix))

  // Expected coordinates for the symbolic matrix [[A, B], [C]].  The flags
  // are ordered by source elements, while coordinates are emitted B, A, C.
  syntax VList ::= "addCoord" "(" Bool "," Value "," VList ")" [function, total]
  rule addCoord(true, V, VS) => vcons(V, VS)
  rule addCoord(false, _, VS) => VS

  syntax VList ::= "expectedFlags" "(" Bool "," Bool "," Bool ")" [function, total]
  rule expectedFlags(AH, BH, CH) =>
    addCoord(BH, pyTuple(vcons(pyInt(0), vcons(pyInt(1), vnil))),
      addCoord(AH, pyTuple(vcons(pyInt(0), vcons(pyInt(0), vnil))),
        addCoord(CH, pyTuple(vcons(pyInt(1), vcons(pyInt(0), vnil))), vnil)))
endmodule
