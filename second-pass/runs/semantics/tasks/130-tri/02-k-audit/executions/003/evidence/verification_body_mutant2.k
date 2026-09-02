requires "reference-semantics/semantics.k"

module TRI-VERIFICATION
  imports MPY

  // Mathematical value at an index.  The two step rules are the contract:
  // even indices have the stated closed value, while odd indices use the
  // preceding two values and the (even) following value.
  syntax Int ::= triAt(Int)
    [function, total, symbol(triAt), no-evaluators]

  rule triAt(0) => 1 [simplification]
  rule triAt(1) => 3 [simplification]

  rule 1 +Int ((I:Int -Int pyMod(I, 2)) /Int 2)
    => triAt(I)
    requires I >=Int 2 andBool pyMod(I, 2) ==Int 0
    [simplification]

  // The integer backend canonicalizes the preceding expression to this form
  // once the even-path constraint discharges the remainder.
  rule (I:Int /Int 2) +Int 1
    => triAt(I)
    requires I >=Int 2 andBool pyMod(I, 2) ==Int 0
    [simplification]

  rule ((triAt(I -Int 1) +Int triAt(I -Int 2)) +Int 1)
       +Int (((I +Int 1) -Int pyMod(I +Int 1, 2)) /Int 2)
    => triAt(I)
    requires I >=Int 3 andBool pyMod(I, 2) ==Int 1
    [simplification]

  // Canonical Haskell-backend form of the odd recurrence after pyMod unfolds.
  rule ((triAt(I:Int +Int -1) +Int triAt(I +Int -2)) +Int 1)
       +Int (((I +Int 1)
              -Int ((((I +Int 1) %Int 2) +Int 2) %Int 2)) /Int 2)
    => triAt(I)
    requires I >=Int 3
     andBool (((I %Int 2) +Int 2) %Int 2) ==Int 1
    [simplification]

  // An abstract prefix is characterized inductively by the two concrete
  // bases and by appending the next contract value.
  syntax ValSeq ::= triPrefix(Int)
  syntax Int ::= prefixIndex(ValSeq)
    [function, total, symbol(prefixIndex), no-evaluators]

  rule vCons(1, .ValSeq) => triPrefix(0)
  rule vCons(1, vCons(3, .ValSeq)) => triPrefix(1)
  rule prefixIndex(vCons(1, .ValSeq)) => 0 [simplification]
  rule prefixIndex(vCons(1, vCons(3, .ValSeq))) => 1 [simplification]
  rule prefixIndex(triPrefix(J:Int)) => J [simplification]
  rule prefixIndex(
         valSeqConcat(VS:ValSeq, vCons(triAt(I:Int), .ValSeq)))
    => I
    requires I >=Int 2
     andBool prefixIndex(VS) ==Int I +Int -1
    [simplification]
  rule valSeqConcat(triPrefix(I:Int +Int -1), vCons(triAt(I), .ValSeq))
    => triPrefix(I)
    requires I >=Int 2
    [simplification]

  // Exact constructor fragments generated from solution.py.  Keeping them
  // named makes the reachability claims readable without changing semantics.
  syntax Expr ::= "TriLoopCond" [macro]
  rule TriLoopCond
    => Compare(Name("i"), CmpOp("<=", Name("n")))

  syntax Stmts ::= "TriLoopBody" [macro]
  rule TriLoopBody
    => If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
         Assign(Name("value"),
           BinOp("+", Int(2), BinOp("//", Name("i"), Int(2))))
         .Stmts,
         Assign(Name("value"),
           BinOp("+",
             BinOp("+", BinOp("+", Name("b"), Name("a")), Int(1)),
             BinOp("//", BinOp("+", Name("i"), Int(1)), Int(2))))
         .Stmts)
       Expr(Call(Attribute(Name("result"), "append"),
                 Name("value"), .Exprs))
       Assign(Name("a"), Name("b"))
       Assign(Name("b"), Name("value"))
       AugAssign(Name("i"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "TriFunctionBody" [macro]
  rule TriFunctionBody
    => If(Compare(Name("n"), CmpOp("==", Int(0))),
         Return(ListExpr(Int(1), .Exprs)) .Stmts,
         .Stmts)
       Assign(Name("result"), ListExpr(Int(1), Int(3), .Exprs))
       Assign(Name("a"), Int(1))
       Assign(Name("b"), Int(3))
       Assign(Name("value"), Int(3))
       Assign(Name("i"), Int(2))
       While(TriLoopCond, TriLoopBody)
       Return(Name("result"))
       .Stmts
endmodule
