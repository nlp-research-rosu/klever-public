requires "../../../reference/src/lemmas.k"
module POW-PROBE
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  syntax Expr ::= Val
  syntax Int ::= ipow(Int, Int) [function, total, symbol(ipow), no-evaluators]
  // k-cell interception (reliable priority, like is_prime): catch ** BEFORE applyBin/^Int.
  rule <k> RV:Int ~> #binR("**", LV:Int) => ipow(LV, RV) ... </k> requires RV >=Int 0 [priority(40)]
endmodule
