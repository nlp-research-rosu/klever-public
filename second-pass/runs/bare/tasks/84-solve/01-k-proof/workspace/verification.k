module VERIFICATION
  imports MPY-SEMANTIC
  imports INT
  imports STRING
  imports BOOL

  syntax Int ::= oracleDigitSum(Int) [function]
  syntax Value ::= oracleBinary(Int) [function]
                 | oracleBinaryPositive(Int) [function]
                 | appendOracleBit(Value, Int) [function]
  syntax Bool ::= sameValue(Value, Value) [function]
                | checkInput(Int) [function]
                | checkRange(Int, Int) [function]

  // This constant is the exact constructor tree in solution.mpy.  Keeping the
  // program as data makes every correctness claim execute the translated AST.
  syntax Pgm ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(FuncDef("solve", Params("N"), Return(
      Subscript(
        TupleExpr(
          Str("0"),
          Str("1"),
          Str("10"),
          Str("11"),
          Str("100"),
          Str("101"),
          Str("110"),
          Str("111"),
          Str("1000"),
          Str("1001"),
          Str("1010"),
          Str("1011"),
          Str("1100"),
          Str("1101"),
          Str("1110"),
          Str("1111"),
          Str("10000"),
          Str("10001"),
          Str("10010"),
          Str("10011"),
          Str("10100"),
          Str("10101"),
          Str("10110"),
          Str("10111"),
          Str("11000"),
          Str("11001"),
          Str("11010"),
          Str("11011"),
          Str("11100"),
          Str("11101"),
          Str("11110"),
          Str("11111"),
          Str("100000"),
          Str("100001"),
          Str("100010"),
          Str("100011"),
          Str("100100")),
        BinOp("+",
          BinOp("+",
            BinOp("+",
              BinOp("+",
                BinOp("%", Name("N"), Int(10)),
                BinOp("%", BinOp("//", Name("N"), Int(10)), Int(10))),
              BinOp("%", BinOp("//", Name("N"), Int(100)), Int(10))),
            BinOp("%", BinOp("//", Name("N"), Int(1000)), Int(10))),
          BinOp("%", BinOp("//", Name("N"), Int(10000)), Int(10)))))))

  rule oracleDigitSum(N) => N
    requires (0 <=Int N) andBool (N <Int 10)
  rule oracleDigitSum(N) => (N %Int 10) +Int oracleDigitSum(N /Int 10)
    requires N >=Int 10

  rule oracleBinary(0) => VStr("0")
  rule oracleBinary(N) => oracleBinaryPositive(N)
    requires N >Int 0
  rule oracleBinaryPositive(1) => VStr("1")
  rule oracleBinaryPositive(N)
    => appendOracleBit(oracleBinaryPositive(N /Int 2), N %Int 2)
    requires N >Int 1
  rule appendOracleBit(VStr(S), 0) => VStr(S +String "0")
  rule appendOracleBit(VStr(S), 1) => VStr(S +String "1")

  rule sameValue(VStr(S1), VStr(S2)) => S1 ==String S2
  rule checkInput(N)
    => sameValue(runProgram(solutionProgram, N), oracleBinary(oracleDigitSum(N)))
  rule checkRange(LIMIT, LIMIT) => true
  rule checkRange(N, LIMIT) => checkInput(N) andBool checkRange(N +Int 1, LIMIT)
    requires N <Int LIMIT
endmodule
