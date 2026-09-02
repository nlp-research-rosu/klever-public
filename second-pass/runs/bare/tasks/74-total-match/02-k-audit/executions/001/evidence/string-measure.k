requires "domains.md"

module STRING-MEASURE
  imports INT
  imports STRING

  syntax KItem ::= "measure" "(" String ")"
  rule measure(S) => lengthString(S)

  configuration <k> $PGM:KItem </k>
endmodule
