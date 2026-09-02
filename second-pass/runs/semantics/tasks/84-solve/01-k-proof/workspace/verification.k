requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The digit in decimal place P (P = 1, 10, 100, ...).  Python's
  // non-negative // and % are expressed with the supplied pyMod operation.
  syntax Int ::= decimalDigit(Int, Int) [function, total]
  rule decimalDigit(N:Int, 1) => pyMod(N, 10)
  rule decimalDigit(N:Int, P:Int)
    => pyMod((N -Int pyMod(N, P)) /Int P, 10)
    requires N >=Int 0 andBool P >Int 1

  // N is bounded by 10000, so these are all and only its possible places.
  syntax Int ::= decimalDigitSum(Int) [function, total]
  rule decimalDigitSum(N:Int)
    => decimalDigit(N, 1)
       +Int decimalDigit(N, 10)
       +Int decimalDigit(N, 100)
       +Int decimalDigit(N, 1000)
       +Int decimalDigit(N, 10000)
    requires 0 <=Int N andBool N <=Int 10000

  // A binary numeral has no Python "0b" prefix.
  syntax Str ::= binaryNumeral(Int) [function, total]
  rule binaryNumeral(N:Int) => str(binCodes(N))

  // Symbolic slicing in the reference semantics deliberately leaves buildIS
  // opaque when its tail is opaque.  This exact prefix lemma is the defining
  // slice identity needed for bin(N)[2:]; it does not summarize solve.
  rule <k>
         Subscript(
           str(iCons(48, iCons(98, REST:IntSeq))),
           Slice(Int(2), NoBound, NoBound))
         => str(REST)
         ...
       </k>
       [priority(40)]
endmodule
