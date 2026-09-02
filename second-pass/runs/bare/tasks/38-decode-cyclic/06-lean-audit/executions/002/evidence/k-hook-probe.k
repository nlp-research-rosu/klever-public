requires "domains.md"

module PROBE-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports MAP

  syntax Pgm ::= "le" "(" Int "," Int ")"
               | "len" "(" String ")"
               | "sub" "(" String "," Int "," Int ")"
               | "upd" "(" Map "," Int "," Int ")"
endmodule

module PROBE
  imports PROBE-SYNTAX
  imports INT
  imports STRING
  imports MAP

  configuration <k> $PGM:Pgm </k>

  rule le(X, Y) => X <=Int Y
  rule len(S) => lengthString(S)
  rule sub(S, START, END) => substrString(S, START, END)
  rule upd(M, KEY, VALUE) => M [ KEY <- VALUE ]
endmodule
