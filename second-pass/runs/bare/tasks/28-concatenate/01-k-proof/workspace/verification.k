module VERIFICATION
  imports MPY-SYNTAX

  // Mathematical left fold used by the reachability claims.
  syntax String ::= concatAcc(String, StrList) [function]
  rule concatAcc(ACC, .StrList) => ACC
  rule concatAcc(ACC, S :: REST) => concatAcc(ACC +String S, REST)
endmodule
