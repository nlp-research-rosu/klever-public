requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This is the parsed constructor tree in solution.mpy, named here so every
  // proof claim refers to the exact program rather than to a hand-written
  // summary of its behavior.
  syntax Module ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("strange_sorted", Params("ordered"),
        If(Compare(Call(Name("len"), Name("ordered")), CmpOp("==", Int(0))),
          Return(ListExpr()),
          .Stmts)
        If(Compare(Call(Name("len"), Name("ordered")), CmpOp("==", Int(1))),
          Return(Name("ordered")),
          .Stmts)
        Return(
          BinOp("+",
            ListExpr(
              Subscript(Name("ordered"), Int(0)),
              Subscript(Name("ordered"), UnaryOp("-", Int(1)))),
            Call(Name("strange_sorted"),
              Subscript(Name("ordered"),
                Slice(Int(1), UnaryOp("-", Int(1)), NoBound))))))
      FuncDef("strange_sort_list", Params("lst"),
        Return(Call(Name("strange_sorted"),
          Call(Name("sorted"), Name("lst"))))))

  // Independent contract function: alternately select the least and greatest
  // remaining elements after sorting the input.
  syntax PList ::= "weaveEnds" "(" PList ")" [function]
  rule weaveEnds(nil) => nil
  rule weaveEnds(cons(I, nil)) => cons(I, nil)
  rule weaveEnds(cons(I, cons(J, L)))
    => cons(I, cons(nth(cons(J, L), length(cons(J, L)) -Int 1),
         weaveEnds(interior(cons(I, cons(J, L))))))

  syntax PList ::= "strangeSpec" "(" PList ")" [function]
  rule strangeSpec(L) => weaveEnds(sortInts(L))
endmodule
