requires "domains.md"

module STRING-PROBE
  imports STRING
  imports INT

  syntax KItem ::= "probeLen" "(" String ")"
                 | "probeSub" "(" String "," Int "," Int ")"
                 | "lenEmpty"
                 | "lenAscii"
                 | "lenAccent"
                 | "lenAstral"
                 | "lenCombining"
                 | "subFull"
                 | "subMiddle"
                 | "subUnicode"
                 | "subEmpty"

  configuration <k> $PGM:KItem </k>

  rule probeLen(S) => lengthString(S)
  rule probeSub(S, I, J) => substrString(S, I, J)
  rule lenEmpty => lengthString("")
  rule lenAscii => lengthString("abc")
  rule lenAccent => lengthString("é")
  rule lenAstral => lengthString("🙂")
  rule lenCombining => lengthString("é")
  rule subFull => substrString("abcdef", 0, 6)
  rule subMiddle => substrString("abcdef", 1, 4)
  rule subUnicode => substrString("a🙂éz", 1, 3)
  rule subEmpty => substrString("abcdef", 3, 3)
endmodule
