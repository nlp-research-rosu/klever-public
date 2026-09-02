// FAIL — the "why not simply" row: IS:IntVs claim on the subsort-only definition. Stuck at
// step 0 with ZERO branches: without the overload equations, inj(.IntVs) and .ValSeq are two
// DIFFERENT empty lists, so no rule (not even nil) relates to the injected variable at all.
requires "verif-subsort.k"
module REFINED-SUBSORT-SPEC
  imports VERIF-SUBSORT
  claim <k> cloop(list(IS:IntVs)) => .K </k> <acc> A:Int => lenI(IS, A) </acc> [all-path]
endmodule
