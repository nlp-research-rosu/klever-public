requires "reference-semantics/semantics.k"

module VERIFICATION-NO-BRIDGE
  imports MPY

  syntax Int ::= decimalDigit(Int, Int) [function, total]
  rule decimalDigit(N:Int, 1) => pyMod(N, 10)
  rule decimalDigit(N:Int, P:Int)
    => pyMod((N -Int pyMod(N, P)) /Int P, 10)
    requires N >=Int 0 andBool P >Int 1

  syntax Int ::= decimalDigitSum(Int) [function, total]
  rule decimalDigitSum(N:Int)
    => decimalDigit(N, 1)
       +Int decimalDigit(N, 10)
       +Int decimalDigit(N, 100)
       +Int decimalDigit(N, 1000)
       +Int decimalDigit(N, 10000)
    requires 0 <=Int N andBool N <=Int 10000

  syntax Str ::= binaryNumeral(Int) [function, total]
  rule binaryNumeral(N:Int) => str(binCodes(N))
endmodule
