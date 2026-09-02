requires "semantic.k"

module VERIFICATION
  imports MPY

  // This nullary function is the exact constructor term in solution.mpy.
  syntax Program ::= "solutionProgram" "(" ")" [function]
  rule solutionProgram() =>
    Module(
      FuncDef("insert_sorted", Params("x", "xs"),
        If(Compare(Name("xs"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(Name("x"))),
          If(Compare(Name("x"), CmpOp("<=", Subscript(Name("xs"), Int(0)))),
            Return(BinOp("+", ListExpr(Name("x")), Name("xs"))),
            Return(
              BinOp(
                "+",
                ListExpr(Subscript(Name("xs"), Int(0))),
                Call(
                  Name("insert_sorted"),
                  Name("x"),
                  Subscript(Name("xs"), Slice(Int(1), NoBound, NoBound))))))))
      FuncDef("sort_values", Params("xs"),
        If(Compare(Name("xs"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          Return(
            Call(
              Name("insert_sorted"),
              Subscript(Name("xs"), Int(0)),
              Call(
                Name("sort_values"),
                Subscript(Name("xs"), Slice(Int(1), NoBound, NoBound)))))))
      FuncDef("even_values", Params("l"),
        If(Compare(Name("l"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          Return(
            BinOp(
              "+",
              ListExpr(Subscript(Name("l"), Int(0))),
              Call(
                Name("even_values"),
                Subscript(Name("l"), Slice(Int(2), NoBound, NoBound)))))))
      FuncDef("rebuild", Params("l", "evens"),
        If(Compare(Name("l"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          If(Compare(
            Subscript(Name("l"), Slice(Int(1), NoBound, NoBound)),
            CmpOp("==", ListExpr(.Exprs))),
            Return(ListExpr(Subscript(Name("evens"), Int(0)))),
            Return(
              BinOp(
                "+",
                ListExpr(
                  Subscript(Name("evens"), Int(0)),
                  Subscript(Name("l"), Int(1))),
                Call(
                  Name("rebuild"),
                  Subscript(Name("l"), Slice(Int(2), NoBound, NoBound)),
                  Subscript(Name("evens"), Slice(Int(1), NoBound, NoBound))))))))
      FuncDef("sort_even", Params("l"),
        Return(Name("l"))))

  // Mathematical reference functions over runtime lists.
  syntax List ::= "evenPositions" "(" List ")" [function]
                | "oddPositions" "(" List ")" [function]
                | "insertReference" "(" PyVal "," List ")" [function]
                | "sortReference" "(" List ")" [function]
                | "rebuildReference" "(" List "," List ")" [function]
                | "sortEvenReference" "(" List ")" [function]

  rule evenPositions(L) => .List
    requires size(L) ==Int 0
  rule evenPositions(L)
    => ListItem(headInt(L)) evenPositions(dropList(L, 2))
    requires notBool size(L) ==Int 0

  rule oddPositions(L) => evenPositions(dropList(L, 1))

  rule insertReference(pyInt(X), L) => ListItem(X)
    requires size(L) ==Int 0
  rule insertReference(pyInt(X), L) => ListItem(X) L
    requires notBool size(L) ==Int 0
     andBool X <=Int headInt(L)
  rule insertReference(pyInt(X), L)
    => ListItem(headInt(L))
       insertReference(pyInt(X), dropList(L, 1))
    requires notBool size(L) ==Int 0
     andBool notBool X <=Int headInt(L)

  rule sortReference(L) => .List
    requires size(L) ==Int 0
  rule sortReference(L)
    => insertReference(pyInt(headInt(L)), sortReference(dropList(L, 1)))
    requires notBool size(L) ==Int 0

  rule rebuildReference(L, _EVENS) => .List
    requires size(L) ==Int 0
  rule rebuildReference(L, EVENS) => ListItem(headInt(EVENS))
    requires notBool size(L) ==Int 0
     andBool size(dropList(L, 1)) ==Int 0
  rule rebuildReference(L, EVENS)
    => ListItem(headInt(EVENS)) ListItem(headInt(dropList(L, 1)))
       rebuildReference(dropList(L, 2), dropList(EVENS, 1))
    requires notBool size(L) ==Int 0
     andBool notBool size(dropList(L, 1)) ==Int 0

  rule sortEvenReference(L)
    => rebuildReference(L, sortReference(evenPositions(L)))
endmodule
