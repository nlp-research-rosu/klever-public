requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Exact K AST produced from solution.py by py2mpy.py.
  syntax Module ::= "solutionModule" [function, total]
  rule solutionModule =>
    // BEGIN SOLUTION MPY
    Module(
      FuncDef("solve", Params("N"),
        Assign(Name("digit_sum"), BinOp("%", Name("N"), Int(10)))
        Assign(Name("N"), BinOp("//", Name("N"), Int(10)))
        AugAssign(Name("digit_sum"), "+", BinOp("%", Name("N"), Int(10)))
        Assign(Name("N"), BinOp("//", Name("N"), Int(10)))
        AugAssign(Name("digit_sum"), "+", BinOp("%", Name("N"), Int(10)))
        Assign(Name("N"), BinOp("//", Name("N"), Int(10)))
        AugAssign(Name("digit_sum"), "+", BinOp("%", Name("N"), Int(10)))
        Assign(Name("N"), BinOp("//", Name("N"), Int(10)))
        AugAssign(Name("digit_sum"), "+", BinOp("%", Name("N"), Int(10)))
        If(Compare(Name("digit_sum"), CmpOp("<", Int(8))),
          If(Compare(Name("digit_sum"), CmpOp("==", Int(0))),
            Return(Str("0")),
            If(Compare(Name("digit_sum"), CmpOp("==", Int(1))),
              Return(Str("1")),
              If(Compare(Name("digit_sum"), CmpOp("==", Int(2))),
                Return(Str("10")),
                If(Compare(Name("digit_sum"), CmpOp("==", Int(3))),
                  Return(Str("11")),
                  If(Compare(Name("digit_sum"), CmpOp("==", Int(4))),
                    Return(Str("100")),
                    If(Compare(Name("digit_sum"), CmpOp("==", Int(5))),
                      Return(Str("101")),
                      If(Compare(Name("digit_sum"), CmpOp("==", Int(6))),
                        Return(Str("110")),
                        Return(Str("111"))))))))),
          If(Compare(Name("digit_sum"), CmpOp("<", Int(16))),
            If(Compare(Name("digit_sum"), CmpOp("==", Int(8))),
              Return(Str("1000")),
              If(Compare(Name("digit_sum"), CmpOp("==", Int(9))),
                Return(Str("1001")),
                If(Compare(Name("digit_sum"), CmpOp("==", Int(10))),
                  Return(Str("1010")),
                  If(Compare(Name("digit_sum"), CmpOp("==", Int(11))),
                    Return(Str("1011")),
                    If(Compare(Name("digit_sum"), CmpOp("==", Int(12))),
                      Return(Str("1100")),
                      If(Compare(Name("digit_sum"), CmpOp("==", Int(13))),
                        Return(Str("1101")),
                        If(Compare(Name("digit_sum"), CmpOp("==", Int(14))),
                          Return(Str("1110")),
                          Return(Str("1111"))))))))),
            If(Compare(Name("digit_sum"), CmpOp("<", Int(24))),
              If(Compare(Name("digit_sum"), CmpOp("==", Int(16))),
                Return(Str("10000")),
                If(Compare(Name("digit_sum"), CmpOp("==", Int(17))),
                  Return(Str("10001")),
                  If(Compare(Name("digit_sum"), CmpOp("==", Int(18))),
                    Return(Str("10010")),
                    If(Compare(Name("digit_sum"), CmpOp("==", Int(19))),
                      Return(Str("10011")),
                      If(Compare(Name("digit_sum"), CmpOp("==", Int(20))),
                        Return(Str("10100")),
                        If(Compare(Name("digit_sum"), CmpOp("==", Int(21))),
                          Return(Str("10101")),
                          If(Compare(Name("digit_sum"), CmpOp("==", Int(22))),
                            Return(Str("10110")),
                            Return(Str("10111"))))))))),
              If(Compare(Name("digit_sum"), CmpOp("<", Int(32))),
                If(Compare(Name("digit_sum"), CmpOp("==", Int(24))),
                  Return(Str("11000")),
                  If(Compare(Name("digit_sum"), CmpOp("==", Int(25))),
                    Return(Str("11001")),
                    If(Compare(Name("digit_sum"), CmpOp("==", Int(26))),
                      Return(Str("11010")),
                      If(Compare(Name("digit_sum"), CmpOp("==", Int(27))),
                        Return(Str("11011")),
                        If(Compare(Name("digit_sum"), CmpOp("==", Int(28))),
                          Return(Str("11100")),
                          If(Compare(Name("digit_sum"), CmpOp("==", Int(29))),
                            Return(Str("11101")),
                            If(Compare(Name("digit_sum"), CmpOp("==", Int(30))),
                              Return(Str("11110")),
                              Return(Str("11111"))))))))),
                If(Compare(Name("digit_sum"), CmpOp("==", Int(32))),
                  Return(Str("100000")),
                  If(Compare(Name("digit_sum"), CmpOp("==", Int(33))),
                    Return(Str("100001")),
                    If(Compare(Name("digit_sum"), CmpOp("==", Int(34))),
                      Return(Str("100010")),
                      If(Compare(Name("digit_sum"), CmpOp("==", Int(35))),
                        Return(Str("100011")),
                        Return(Str("100100"))))))))))))
    // END SOLUTION MPY

  // Arithmetic simplifiers justified independently by bridge-spec.k against
  // the unextended MPY semantics, for every integer tail.
  rule (((D +Int 10 *Int Q) %Int 10 +Int 10) %Int 10) => D
    requires 0 <=Int D andBool D <Int 10
    [simplification]
  rule ((D +Int 10 *Int Q -Int D) /Int 10) => Q
    requires 0 <=Int D andBool D <Int 10
    [simplification]

  // Decode an ASCII code sequence as a base-two positional numeral.
  syntax Int ::= decodeBin(IntSeq) [function, total]
  rule decodeBin(.IntSeq) => 0
  rule decodeBin(iCons(C, R)) =>
    (C -Int 48) *Int (2 ^Int isLen(R)) +Int decodeBin(R)

  syntax Bool ::= allBinDigits(IntSeq) [function, total]
  rule allBinDigits(.IntSeq) => true
  rule allBinDigits(iCons(C, R)) =>
    (C ==Int 48 orBool C ==Int 49) andBool allBinDigits(R)

  // "0", or a nonempty sequence beginning with "1" and containing only bits.
  syntax Bool ::= canonicalBin(IntSeq) [function, total]
  rule canonicalBin(iCons(48, .IntSeq)) => true
  rule canonicalBin(iCons(49, R)) => allBinDigits(R)
  rule canonicalBin(_:IntSeq) => false [owise]

  // Symbolic decimal decomposition used to parameterize exactly 0..10000.
  syntax Bool ::= digitDomain(Int, Int, Int, Int, Int) [function, total]
  rule digitDomain(D0, D1, D2, D3, D4) =>
       0 <=Int D0 andBool D0 <Int 10
    andBool 0 <=Int D1 andBool D1 <Int 10
    andBool 0 <=Int D2 andBool D2 <Int 10
    andBool 0 <=Int D3 andBool D3 <Int 10
    andBool 0 <=Int D4 andBool D4 <=Int 1
    andBool
      (D4 ==Int 0
       orBool
       (D4 ==Int 1
        andBool D0 ==Int 0
        andBool D1 ==Int 0
        andBool D2 ==Int 0
        andBool D3 ==Int 0))

endmodule
