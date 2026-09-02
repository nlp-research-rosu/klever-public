requires "verification.k"

module AUDIT-CONTEXT-PROBE
  imports CHOOSE-NUM-VERIFICATION

  syntax KItem ::= "#observeResult"
  rule <k> I:Int ~> #observeResult => I +Int 100 ... </k>
endmodule
