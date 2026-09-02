requires "bridge-base.k"

module BRIDGE-SPEC
  imports BRIDGE-BASE

  // Universal connection theorem over every Int value. The compiled fixed
  // semantics defines isInt as true exactly on inj{Int,KItem}(I), so this is
  // extensionally the complete ground match domain of the candidate guard.
  // The arbitrary continuation and all omitted cells remain framed.
  claim [iter-int-connection]:
    <k> #iterNext(list(vCons(I:Int, REST:ValSeq)))
      => #iterYield(intValue(I), list(REST)) ... </k>
endmodule
