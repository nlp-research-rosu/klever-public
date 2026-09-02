module STRING-PROBE-SYNTAX
  imports STRING-SYNTAX
  syntax KItem ::= "Probe" "(" String ")"
endmodule

module STRING-PROBE
  imports STRING-PROBE-SYNTAX
  imports STRING
  imports INT

  configuration
    <k> $PGM:KItem </k>
    <length> 0 </length>
    <first> "" </first>
    <rest> "" </rest>

  rule <k> Probe(S) => .K </k>
       <length> _ => lengthString(S) </length>
       <first> _ => substrString(S, 0, 1) </first>
       <rest> _ => substrString(S, 1, lengthString(S)) </rest>
endmodule
