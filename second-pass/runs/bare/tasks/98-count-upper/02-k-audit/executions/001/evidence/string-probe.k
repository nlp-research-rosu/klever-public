requires "domains.md"

module STRING-PROBE-SYNTAX
  imports DOMAINS

  syntax Probe ::= "probeLen" "(" String ")"
                 | "probeSubstr" "(" String "," Int "," Int ")"
endmodule

module STRING-PROBE
  imports STRING-PROBE-SYNTAX

  configuration <k> $PGM:Probe </k>

  rule probeLen(S) => lengthString(S)
  rule probeSubstr(S, START, END) => substrString(S, START, END)
endmodule
