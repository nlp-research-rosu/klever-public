requires "verification-no-bridge.k"

module PARSE-MUSIC-NO-BRIDGE-OBSERVER
  imports PARSE-MUSIC-BASE

  syntax KItem ::= "#probeRef"
  rule <k> V:Val ~> #probeRef => isRefV(V) ... </k>
endmodule
