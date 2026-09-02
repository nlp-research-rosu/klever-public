requires "semantic.k"
requires "solution-program.k"

module SORTED-LIST-VERIFICATION
  imports SOLUTION-PROGRAM
  imports BOOL
  imports INT
  imports STRING

  // Independent mathematical specification: remove odd-length strings and
  // insert every remaining string by the (length, lexicographic) key.
  syntax Words ::= evenSorted ( Words ) [function]
                 | insertByKey ( String , Words ) [function]
                 | insertAfterDecision ( Bool , String , String , Words ) [function]
                 | keepAfterDecision ( Bool , String , Words ) [function]
                 | sortedListSumSpec ( Words ) [function]
  syntax Bool ::= keyLess ( String , String ) [function]

  rule keyLess(S, T)
    => (lengthString(S) <Int lengthString(T))
       orBool ((lengthString(S) ==Int lengthString(T)) andBool (S <String T))

  rule sortedListSumSpec(WS) => sortByKey(filterEven(WS))

  rule evenSorted(.Words) => .Words
  rule evenSorted(S, SS)
    => keepAfterDecision(
         lengthString(S) %Int 2 ==Int 0,
         S,
         evenSorted(SS))
  rule keepAfterDecision(B, S, SS) => insertByKey(S, SS)
    requires B
  rule keepAfterDecision(B, S, SS) => SS
    requires notBool B

  rule insertByKey(S, .Words) => S
  rule insertByKey(S, T, TS)
    => insertAfterDecision(keyLess(S, T), S, T, TS)
  rule insertAfterDecision(B, S, T, TS) => S, T, TS
    requires B
  rule insertAfterDecision(B, S, T, TS) => T, insertByKey(S, TS)
    requires notBool B

endmodule
