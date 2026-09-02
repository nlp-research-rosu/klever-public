module MAX-FLOAT-TEST-SYNTAX
  imports FLOAT
  syntax Exp ::= "nanLeft" | "nanRight"
endmodule

module MAX-FLOAT-TEST
  imports MAX-FLOAT-TEST-SYNTAX
  configuration <k> $PGM:Exp </k>
  rule <k> nanLeft => maxFloat(NaN, 1.0) ... </k>
  rule <k> nanRight => maxFloat(1.0, NaN) ... </k>
endmodule
