requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact translated body of solution.py, named only to keep claims readable.
  syntax Stmts ::= "evenOddBody" [function, total]
  rule evenOddBody
    => Expr(Str("Return the counts of even and odd decimal digits in num."))
       Assign(Name("num"), Call(Name("abs"), Name("num")))
       Assign(Name("even"), Int(0))
       Assign(Name("odd"), Int(0))
       If(Compare(Name("num"), CmpOp("==", Int(0))),
          Return(TupleExpr(Int(1), Int(0))) .Stmts,
          .Stmts)
       While(Compare(Name("num"), CmpOp(">", Int(0))),
         Assign(Name("even"),
                BinOp("-",
                  BinOp("+", Name("even"), Int(1)),
                  BinOp("%", Name("num"), Int(2))))
         Assign(Name("odd"),
                BinOp("+", Name("odd"), BinOp("%", Name("num"), Int(2))))
         Assign(Name("num"), BinOp("//", Name("num"), Int(10)))
         .Stmts)
       Return(TupleExpr(Name("even"), Name("odd")))
       .Stmts

  syntax Val ::= "evenOddClosure" [function, total]
  rule evenOddClosure => closureVal("num", evenOddBody, 0)

  // Mathematical counts for a strictly-positive decimal representation.
  // The zero terminator contributes no digit; the public summaries below give
  // the integer 0 its single even digit.
  syntax Int ::= evenPos(Int) [function, total, no-evaluators]
               | oddPos(Int)  [function, total, no-evaluators]
               | decEven(Int) [function, total]
               | decOdd(Int)  [function, total]

  rule evenPos(0) => 0
  rule oddPos(0)  => 0
  rule evenPos(N) => 0 requires N ==Int 0 [simplification]
  rule oddPos(N)  => 0 requires N ==Int 0 [simplification]

  // The negative branch is outside loop use but totalizes the symbols.
  rule evenPos(N) => evenPos(0 -Int N) requires N <Int 0
  rule oddPos(N)  => oddPos(0 -Int N)  requires N <Int 0

  rule decEven(0) => 1
  rule decEven(N) => evenPos(N)        requires N >Int 0
  rule decEven(N) => evenPos(0 -Int N) requires N <Int 0

  rule decOdd(0) => 0
  rule decOdd(N) => oddPos(N)        requires N >Int 0
  rule decOdd(N) => oddPos(0 -Int N) requires N <Int 0

  // Public zero case after the program's abs call.
  rule { 1 #Equals decEven(N) } => #Top
    requires absInt(N) ==Int 0
    [simplification]
  rule { 0 #Equals decOdd(N) } => #Top
    requires absInt(N) ==Int 0
    [simplification]
  rule { evenPos(absInt(N)) #Equals decEven(N) } => #Top
    requires absInt(N) >Int 0
    [simplification]
  rule { decEven(N) #Equals evenPos(absInt(N)) } => #Top
    requires absInt(N) >Int 0
    [simplification]
  rule { oddPos(absInt(N)) #Equals decOdd(N) } => #Top
    requires absInt(N) >Int 0
    [simplification]
  rule { decOdd(N) #Equals oddPos(absInt(N)) } => #Top
    requires absInt(N) >Int 0
    [simplification]

  // One-step decimal recurrence in the exact matching-logic equality shapes
  // produced after the loop circularity applies.
  rule { E +Int evenPos(N)
         #Equals (E +Int 1 -Int ((N %Int 2 +Int 2) %Int 2))
                    +Int evenPos((N -Int ((N %Int 10 +Int 10) %Int 10))
                                    /Int 10) } => #Top
    requires N >Int 0
    [simplification]
  rule { (E +Int 1 -Int ((N %Int 2 +Int 2) %Int 2))
           +Int evenPos((N -Int ((N %Int 10 +Int 10) %Int 10))
                           /Int 10)
         #Equals E +Int evenPos(N) } => #Top
    requires N >Int 0
    [simplification]
  rule { O +Int oddPos(N)
         #Equals (O +Int ((N %Int 2 +Int 2) %Int 2))
                    +Int oddPos((N -Int ((N %Int 10 +Int 10) %Int 10))
                                   /Int 10) } => #Top
    requires N >Int 0
    [simplification]
  rule { (O +Int ((N %Int 2 +Int 2) %Int 2))
           +Int oddPos((N -Int ((N %Int 10 +Int 10) %Int 10))
                          /Int 10)
         #Equals O +Int oddPos(N) } => #Top
    requires N >Int 0
    [simplification]
endmodule
