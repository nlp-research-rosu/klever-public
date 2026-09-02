// FAIL — discriminator for spec-bare-refined.k: the same bare claim behind one neutral
// loopLbl step, which makes the claim's own circularity permanently inapplicable. Still stuck
// at the same place => it is RULE application that cannot narrow, not a step-0 artifact.
requires "verif-overload.k"
module BARE-REFINED-LBL-SPEC
  imports VERIF-OVERLOAD
  claim <k> loopLbl(floopU(listU(IS:Ints))) => .K </k>
        <acc> A:Int => sumU(IS, A) </acc> [all-path]
endmodule
