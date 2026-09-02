requires "semantic.k"

module VERIFICATION-VACUITY
  imports MPY

  syntax Pgm ::= "solutionProgram" [function]

  rule solutionProgram =>
    Module(
      FuncDef("even_odd_palindrome", Params("n"),
        If(Compare(Name("n"), CmpOp("<", Int(10))),
          Assign(Name("even"), BinOp("//", Name("n"), Int(2)))
          Assign(Name("odd"), BinOp("-", Name("n"), Name("even")))
          Return(TupleExpr(Name("even"), Name("odd"))),
          .Stmts)
        Assign(Name("even"), Int(4))
        Assign(Name("odd"), Int(5))
        Assign(Name("pairs"), BinOp("//", Name("n"), Int(11)))
        If(Compare(Name("pairs"), CmpOp(">", Int(9))),
          Assign(Name("pairs"), Int(9)),
          .Stmts)
        Assign(
          Name("even"),
          BinOp("+", Name("even"), BinOp("//", Name("pairs"), Int(2))))
        Assign(
          Name("odd"),
          BinOp(
            "-",
            BinOp("+", Name("odd"), Name("pairs")),
            BinOp("//", Name("pairs"), Int(2))))
        If(Compare(Name("n"), CmpOp(">=", Int(101))),
          Assign(Name("lead"), BinOp("//", Name("n"), Int(100)))
          If(Compare(Name("lead"), CmpOp(">", Int(9))),
            Assign(Name("lead"), Int(9))
            Assign(Name("extra"), Int(10)),
            Assign(
              Name("middle"),
              BinOp("%", BinOp("//", Name("n"), Int(10)), Int(10)))
            Assign(
              Name("candidate"),
              BinOp(
                "+",
                BinOp("*", Name("lead"), Int(101)),
                BinOp("*", Name("middle"), Int(10))))
            Assign(Name("extra"), Name("middle"))
            If(Compare(Name("candidate"), CmpOp("<=", Name("n"))),
              Assign(Name("extra"), BinOp("+", Name("extra"), Int(1))),
              .Stmts))
          Assign(Name("previous"), BinOp("-", Name("lead"), Int(1)))
          Assign(Name("even_leads"), BinOp("//", Name("previous"), Int(2)))
          Assign(
            Name("odd_leads"),
            BinOp("-", Name("previous"), Name("even_leads")))
          Assign(
            Name("even"),
            BinOp(
              "+",
              Name("even"),
              BinOp("*", Name("even_leads"), Int(10))))
          Assign(
            Name("odd"),
            BinOp("+", Name("odd"), BinOp("*", Name("odd_leads"), Int(10))))
          If(Compare(BinOp("%", Name("lead"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("even"), BinOp("+", Name("even"), Name("extra"))),
            Assign(Name("odd"), BinOp("+", Name("odd"), Name("extra")))),
          .Stmts)
        Return(TupleExpr(Name("even"), Name("odd")))))

  // Independent reference model: reverse the decimal digits, then classify
  // each palindrome by parity.  These equations cover exactly 1..1000.
  syntax Int ::= "reverseDigits" "(" Int ")" [function]
               | "evenPalindrome" "(" Int ")" [function]
               | "oddPalindrome" "(" Int ")" [function]

  rule reverseDigits(N) => N
    requires 0 <=Int N andBool N <Int 10
  rule reverseDigits(N) => (N %Int 10) *Int 10 +Int (N /Int 10)
    requires 10 <=Int N andBool N <Int 100
  rule reverseDigits(N) => (N %Int 10) *Int 100
                           +Int ((N /Int 10) %Int 10) *Int 10
                           +Int (N /Int 100)
    requires 100 <=Int N andBool N <Int 1000
  rule reverseDigits(1000) => 1

  rule evenPalindrome(N) => 1
    requires reverseDigits(N) ==Int N andBool (N %Int 2 ==Int 0)
  rule evenPalindrome(N) => 0
    requires notBool (reverseDigits(N) ==Int N andBool (N %Int 2 ==Int 0))
  rule oddPalindrome(N) => 1
    requires reverseDigits(N) ==Int N andBool (N %Int 2 ==Int 1)
  rule oddPalindrome(N) => 0
    requires notBool (reverseDigits(N) ==Int N andBool (N %Int 2 ==Int 1))

  syntax KItem ::= "verifyRange" "(" Pgm "," Int "," Int "," Int "," Int ")" [symbol]
                 | "expect" "(" Int "," Int ")" [symbol]
                 | "verified" [symbol]

  rule <k> verifyRange(P, N, MAX, EVENS, ODDS)
        => run(P, N)
        // Auditor mutation: demand one extra even palindrome at every checked
        // input.  At the first satisfying input, n = 1, the real result is
        // (0,1), while this mutated obligation demands (1,1).
        ~> expect(EVENS +Int evenPalindrome(N) +Int 1,
                  ODDS +Int oddPalindrome(N))
        ~> verifyRange(P, N +Int 1, MAX,
                       EVENS +Int evenPalindrome(N),
                       ODDS +Int oddPalindrome(N)) ... </k>
    requires N <=Int MAX

  rule verifyRange(_, N, MAX, _, _) => verified
    requires N >Int MAX

  rule <k> VTuple(VInt(E), VInt(O)) ~> expect(E, O) => . ... </k>
       <env> _ => .Map </env>
endmodule
