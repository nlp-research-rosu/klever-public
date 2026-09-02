// FAIL — the claim you'd naturally write: bare IS:Ints where a Vals payload is expected.
// The nil case discharges as an equation, but rule application never case-splits (narrows)
// the injected variable against the cons, so the proof sticks holding "IS is not nil".
requires "verif-overload.k"
module BARE-REFINED-SPEC
  imports VERIF-OVERLOAD
  claim <k> floopU(listU(IS:Ints)) => .K </k> <acc> A:Int => sumU(IS, A) </acc> [all-path]
endmodule
