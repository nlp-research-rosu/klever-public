requires "semantic.k"

module VERIFICATION
  imports MPY

  // Mathematical specification by inclusion-exclusion.  For N > 1, fixing
  // the first digit leaves 10 * 10^(N-2) choices; fixing the last leaves
  // 9 * 10^(N-2), since the first digit cannot be zero; fixing both leaves
  // 10^(N-2).  The union is starts + ends - overlap.
  syntax Int ::= decimalMiddles(Int) [function]
               | startsWithOne(Int) [function]
               | endsWithOne(Int) [function]
               | startsAndEndsWithOne(Int) [function]
               | qualifyingCount(Int) [function]

  rule decimalMiddles(K) => 10 ^Int K requires K >=Int 0
  rule startsWithOne(N) => 10 *Int decimalMiddles(N -Int 2)
    requires N >Int 1
  rule endsWithOne(N) => 9 *Int decimalMiddles(N -Int 2)
    requires N >Int 1
  rule startsAndEndsWithOne(N) => decimalMiddles(N -Int 2)
    requires N >Int 1

  rule qualifyingCount(1) => 1
  rule qualifyingCount(N)
    => startsWithOne(N) +Int endsWithOne(N) -Int startsAndEndsWithOne(N)
    requires N >Int 1
endmodule
