requires "verification.k"

module PARSE-MUSIC-BRIDGE-OBSERVER
  imports PARSE-MUSIC-BASE

  syntax KItem ::= "#probeRef"
  rule <k> V:Val ~> #probeRef => isRefV(V) ... </k>
endmodule
