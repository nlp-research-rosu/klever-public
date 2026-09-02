requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // These two macros are the exact bodies emitted in solution.mpy.  Keeping
  // them named makes the proof claims readable while preserving the link to
  // the translated program's constructor tree.
  syntax Stmts ::= "digitBody" [macro]
                 | "countBody" [macro]

  rule digitBody =>
    If(Compare(Name("num"), CmpOp("<", UnaryOp("-", Int(9)))),
      Return(
        BinOp("+",
          BinOp("%", UnaryOp("-", Name("num")), Int(10)),
          Call(Name("digit_sum"),
            UnaryOp("-",
              BinOp("//", UnaryOp("-", Name("num")), Int(10)))))),
      If(Compare(Name("num"), CmpOp(">", Int(9))),
        Return(
          BinOp("+",
            BinOp("%", Name("num"), Int(10)),
            Call(Name("digit_sum"),
              BinOp("//", Name("num"), Int(10))))),
        Return(Name("num"))))

  rule countBody =>
    If(Compare(Name("arr"), CmpOp("==", ListExpr())),
      Return(Int(1)),
      If(Compare(
          Call(Name("digit_sum"), Subscript(Name("arr"), Int(0))),
          CmpOp(">", Int(0))),
        Return(
          BinOp("+", Int(1),
            Call(Name("count_nums"),
              Subscript(Name("arr"),
                Slice(Int(1), NoBound, NoBound))))),
        Return(
          Call(Name("count_nums"),
            Subscript(Name("arr"),
              Slice(Int(1), NoBound, NoBound))))))

  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(
      FuncDef("digit_sum", Params("num"), digitBody)
      FuncDef("count_nums", Params("arr"), countBody))

  syntax Map ::= "solutionFuns" [macro]
  rule solutionFuns =>
       ("digit_sum" |-> function("num", digitBody))
       ("count_nums" |-> function("arr", countBody))

  // Mathematical reference: decimal digits are peeled from the right.  A
  // one-digit negative number is the signed leading digit, exactly as stated
  // in prompt.py.
  syntax Int ::= "signedDigitSum" "(" Int ")"
                 [function, total, symbol(signedDigitSum)]

  rule signedDigitSum(N)
    => ((0 -Int N) %Int 10)
       +Int signedDigitSum(0 -Int ((0 -Int N) /Int 10))
    requires N <Int (0 -Int 9)

  rule signedDigitSum(N)
    => (N %Int 10) +Int signedDigitSum(N /Int 10)
    requires N >Int 9

  rule signedDigitSum(N) => N
    requires N >=Int (0 -Int 9) andBool N <=Int 9

  syntax Int ::= "countPositive" "(" VList ")"
                 [function, total, symbol(countPositive)]
  syntax Int ::= "boolToInt" "(" Bool ")"
                 [function, total, symbol(boolToInt), smt-hook((ite #1 1 0))]

  rule boolToInt(true) => 1
  rule boolToInt(false) => 0
  rule countPositive(VNil) => 0
  rule countPositive(VCons(N, REST))
    => boolToInt(signedDigitSum(N) >Int 0) +Int countPositive(REST)
endmodule
