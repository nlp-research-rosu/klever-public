requires "verification.k"

module REVIEWER-BRIDGE-CONTEXT-HELPER
  imports MAX-FILL-SUMMARY

  syntax KItem ::= "#reviewAfterSum"
  rule <k> I:Int ~> #reviewAfterSum => I +Int 100 ... </k>
endmodule

module REVIEWER-FIXED-CONTEXT
  imports REVIEWER-BRIDGE-CONTEXT-HELPER
endmodule

module REVIEWER-BRIDGED-CONTEXT
  imports REVIEWER-BRIDGE-CONTEXT-HELPER
  imports MAX-FILL-VERIFICATION
endmodule

module REVIEWER-BRIDGE-CONTEXT-SPEC
  imports REVIEWER-BRIDGE-CONTEXT-HELPER

  // The immediate continuation is observably result-bearing.  Both the fixed
  // call rule and the candidate dispatch twin must preserve and execute it.
  claim [sum-with-observable-suffix]:
    <k> #applyK(
          toCall(builtinV("sum")),
          (list(vCons(1, vCons(1, .ValSeq))), .Vals))
          ~> #reviewAfterSum
          => 102 </k>
endmodule
