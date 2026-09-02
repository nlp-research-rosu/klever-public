// #Top — the production shape, on the reference-shaped vCons flavor: a bare-variable entry
// claim (which fails alone, cf. spec-bare-refined-lbl.k) closes once the head-exposed
// invariant is its sibling in the module. Corrupting the postcondition (+Int 1) fails: non-vacuous.
requires "verif-overload.k"
module ENTRY-INVARIANT-SPEC
  imports VERIF-OVERLOAD

  // loop invariant — head-exposed cons form
  claim <k> floop(list(vCons(I:Int, IS:IntVs))) => .K </k>
        <acc> A:Int => sumV(vCons(I, IS), A) </acc> [all-path]

  // entry — bare IS:IntVs behind one neutral step
  claim <k> loopLbl(floop(list(IS:IntVs))) => .K </k>
        <acc> A:Int => sumV(IS, A) </acc> [all-path]
endmodule
