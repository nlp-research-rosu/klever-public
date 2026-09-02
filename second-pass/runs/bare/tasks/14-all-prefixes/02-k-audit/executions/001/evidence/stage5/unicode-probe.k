requires "../src/candidate/semantic.k"

module UNICODE-PROBE
  imports MPY

  syntax Program ::= "LenProbe" "(" String ")"
                   | "PrefixProbe" "(" String "," Int ")"

  rule <k> LenProbe(S) => lenVal(strVal(S)) ... </k>
  rule <k> PrefixProbe(S, I) => prefixVal(strVal(S), intVal(I)) ... </k>
endmodule
