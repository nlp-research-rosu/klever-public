requires "verification-no-iter-bridge.k"

module ITER-BRIDGE-CONNECTION
  imports VERIFICATION-NO-ITER-BRIDGE

  // These claims quantify over every continuation and all automatically
  // framed cells. They use only intsVS's constructor equations and the fixed
  // MPY list iterator rules, not the proposed priority bridges.
  claim [empty-connection]:
    <k> #iterNext(list(intsVS(.IntSeq))) ~> CONT
      => #iterDone ~> CONT
    </k>

  claim [cons-connection]:
    <k> #iterNext(list(intsVS(iCons(I:Int, R:IntSeq)))) ~> CONT
      => #iterYield(I, list(intsVS(R))) ~> CONT
    </k>
endmodule
