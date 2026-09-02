// probe.k — Q4 keysBelow discharge probe. Q4's variant-B circularity
// re-application leaves ¬(0<HLM+1 ∧ HLM+1<HLM+2 ∧ keysBelow((AN|->..)
// (HLM|->..)HREST, HLM+2)) as an unrefuted remainder although every conjunct
// follows from the PC (0<AN<HLM ∧ keysBelow(HREST,HLM)). This probe feeds the
// EXACT conjunction to a positive k-cell context: green means the peel+absorb
// lemmas reduce it there and the failure is specific to the claim-application
// (#Not remainder) context; red localizes the broken reduction step.

requires "../../src/lemmas.k"

module Q4KB-PROBE
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax KItem ::= #pb(Bool)
  rule <k> #pb(true) => .K ... </k>
endmodule
