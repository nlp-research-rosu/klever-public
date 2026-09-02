requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The translated solution, exposed as a closed module term for both the
  // concrete harness and the reachability claims.
  syntax Stmts ::= "solutionBody" [function]
  rule solutionBody =>
        If(Compare(Name("n"), CmpOp("<", Int(10))),
          Return(
            TupleExpr(
              BinOp("//", Name("n"), Int(2)),
              BinOp("//", BinOp("+", Name("n"), Int(1)), Int(2)))),
          .Stmts)
        If(Compare(Name("n"), CmpOp("<", Int(100))),
          Assign(Name("two_digit"), BinOp("//", Name("n"), Int(11)))
          Return(
            TupleExpr(
              BinOp("+", Int(4),
                BinOp("//", Name("two_digit"), Int(2))),
              BinOp("+", Int(5),
                BinOp("//",
                  BinOp("+", Name("two_digit"), Int(1)),
                  Int(2))))),
          .Stmts)
        If(Compare(Name("n"), CmpOp("==", Int(1000))),
          Return(TupleExpr(Int(48), Int(60))),
          .Stmts)
        Assign(Name("hundreds"),
          BinOp("//", Name("n"), Int(100)))
        Assign(Name("current_block"),
          BinOp("+",
            BinOp("//",
              BinOp("-",
                BinOp("%", Name("n"), Int(100)),
                Name("hundreds")),
              Int(10)),
            Int(1)))
        Assign(Name("even"),
          BinOp("+", Int(8),
            BinOp("*", Int(10),
              BinOp("//",
                BinOp("-", Name("hundreds"), Int(1)),
                Int(2)))))
        Assign(Name("odd"),
          BinOp("+", Int(10),
            BinOp("*", Int(10),
              BinOp("//", Name("hundreds"), Int(2)))))
        If(
          Compare(
            BinOp("%", Name("hundreds"), Int(2)),
            CmpOp("==", Int(0))),
          AugAssign(Name("even"), "+", Name("current_block")),
          AugAssign(Name("odd"), "+", Name("current_block")))
        Return(TupleExpr(Name("even"), Name("odd")))

  syntax Module ::= "solutionModule" [function]
  rule solutionModule =>
    Module(
      FuncDef(
        "even_odd_palindrome",
        Params("n"),
        solutionBody))

  // Start from the standard initial configuration, install the definition,
  // and call the required entry point on N.
  syntax KItem ::= "#runEvenOdd" "(" Int ")"
  rule #runEvenOdd(N:Int) =>
    #loadAll(solutionModule)
    ~> Call(Name("even_odd_palindrome"), N)

  // Mathematical specification.  For three-digit inputs H is the leading
  // digit and C is the number of H?H palindromes not exceeding N.
  syntax Int ::= leadingDigit(Int) [function, total]
  rule leadingDigit(N:Int) => N /Int 100

  syntax Int ::= currentBlock(Int) [function, total]
  rule currentBlock(N:Int) =>
    (N %Int 100 -Int leadingDigit(N) +Int 10) /Int 10

  syntax Int ::= evenPalindromes(Int) [function]
  rule evenPalindromes(N:Int) => N /Int 2
    requires 1 <=Int N andBool N <Int 10
  rule evenPalindromes(N:Int) => 4 +Int (N /Int 11) /Int 2
    requires 10 <=Int N andBool N <Int 100
  rule evenPalindromes(N:Int) =>
      8
      +Int 10 *Int ((leadingDigit(N) -Int 1) /Int 2)
      +Int (#if leadingDigit(N) %Int 2 ==Int 0
            #then currentBlock(N) #else 0 #fi)
    requires 100 <=Int N andBool N <Int 1000
  rule evenPalindromes(1000) => 48

  syntax Int ::= oddPalindromes(Int) [function]
  rule oddPalindromes(N:Int) => (N +Int 1) /Int 2
    requires 1 <=Int N andBool N <Int 10
  rule oddPalindromes(N:Int) =>
      5 +Int ((N /Int 11) +Int 1) /Int 2
    requires 10 <=Int N andBool N <Int 100
  rule oddPalindromes(N:Int) =>
      10
      +Int 10 *Int (leadingDigit(N) /Int 2)
      +Int (#if leadingDigit(N) %Int 2 ==Int 1
            #then currentBlock(N) #else 0 #fi)
    requires 100 <=Int N andBool N <Int 1000
  rule oddPalindromes(1000) => 60

endmodule
