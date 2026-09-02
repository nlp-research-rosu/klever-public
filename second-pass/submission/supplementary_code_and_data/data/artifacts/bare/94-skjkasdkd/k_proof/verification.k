requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This macro is the exact AST emitted in solution.mpy.  Keeping it as a K
  // term lets specifications reason about the translated program itself.
  syntax Pgm ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("is_prime_from", Params("n", "divisor"),
        If(Compare(BinOp("*", Name("divisor"), Name("divisor")),
                   CmpOp(">", Name("n"))),
          Return(Bool(true)), .Stmts)
        If(Compare(BinOp("%", Name("n"), Name("divisor")),
                   CmpOp("==", Int(0))),
          Return(Bool(false)), .Stmts)
        Return(Call(Name("is_prime_from"), Name("n"),
                    BinOp("+", Name("divisor"), Int(1)))))
      FuncDef("is_prime", Params("n"),
        If(Compare(Name("n"), CmpOp("<", Int(2))),
          Return(Bool(false)), .Stmts)
        Return(Call(Name("is_prime_from"), Name("n"), Int(2))))
      FuncDef("choose_prime", Params("n", "best"),
        If(BoolOp("and",
             Call(Name("is_prime"), Name("n")),
             Compare(Name("n"), CmpOp(">", Name("best")))),
          Return(Name("n")), .Stmts)
        Return(Name("best")))
      FuncDef("largest_prime", Params("lst"),
        If(Compare(Call(Name("len"), Name("lst")), CmpOp("==", Int(0))),
          Return(Int(0)), .Stmts)
        Return(Call(Name("choose_prime"),
          Subscript(Name("lst"), Int(0)),
          Call(Name("largest_prime"),
            Subscript(Name("lst"), Slice(Int(1), NoBound, NoBound))))))
      FuncDef("digit_sum", Params("n"),
        If(Compare(Name("n"), CmpOp("<", Int(10))),
          Return(Name("n")), .Stmts)
        Return(BinOp("+", BinOp("%", Name("n"), Int(10)),
          Call(Name("digit_sum"), BinOp("//", Name("n"), Int(10))))))
      FuncDef("skjkasdkd", Params("lst"),
        Return(Call(Name("digit_sum"),
                    Call(Name("largest_prime"), Name("lst"))))))

  syntax Map ::= programDefs(Pgm) [function]
               | "solutionDefs" [macro]
  rule programDefs(Module(SS)) => collectDefs(SS)
  rule solutionDefs => programDefs(solutionProgram)

  // Independent mathematical reference functions.
  syntax Bool ::= refPrimeFrom(Int, Int) [function, total]
                | refPrime(Int) [function, total]
  rule refPrimeFrom(N, D) => true
    requires D *Int D >Int N
  rule refPrimeFrom(N, D) => false
    requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule refPrimeFrom(N, D) => refPrimeFrom(N, D +Int 1)
    requires D *Int D <=Int N andBool N %Int D =/=Int 0
  rule refPrime(N) => false requires N <Int 2
  rule refPrime(N) => refPrimeFrom(N, 2) requires N >=Int 2

  syntax Int ::= refChoose(Int, Int) [function]
               | refLargest(Vals) [function]
               | refDigitSum(Int) [function]
               | refAnswer(Vals) [function]
  rule refChoose(N, BEST) => N
    requires refPrime(N) andBool N >Int BEST
  rule refChoose(N, BEST) => BEST
    requires notBool (refPrime(N) andBool N >Int BEST)
  rule refLargest(VS) => 0
    requires valLength(VS) ==Int 0
  rule refLargest(VS) => refChoose(intHead(VS), refLargest(intTail(VS)))
    requires valLength(VS) =/=Int 0
  rule refDigitSum(N) => N requires N <Int 10
  rule refDigitSum(N) => N %Int 10 +Int refDigitSum(N /Int 10)
    requires N >=Int 10
  rule refAnswer(VS) => refDigitSum(refLargest(VS))
endmodule
