requires "semantic.k"

module VERIFICATION
  imports MPY

  // Independent mathematical contract for prime hexadecimal digits.  Since
  // each target is a distinct one-character string, summing the six counts is
  // exactly the number of characters in {2, 3, 5, 7, B, D}.
  syntax Int ::= primeHexCount(String) [function, total]
  rule primeHexCount(S) =>
       countAllOccurrences(S, "2")
    +Int countAllOccurrences(S, "3")
    +Int countAllOccurrences(S, "5")
    +Int countAllOccurrences(S, "7")
    +Int countAllOccurrences(S, "B")
    +Int countAllOccurrences(S, "D")
endmodule
