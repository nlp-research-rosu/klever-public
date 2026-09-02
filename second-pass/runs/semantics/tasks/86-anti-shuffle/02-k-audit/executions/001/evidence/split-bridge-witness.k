requires "verification.k"

// The proof-local bridge returns a custom iterator and performs no allocation.
// This is a false conclusion about the supplied semantics for the ground input
// "a b", whose real split result is an allocated list object.
module SPLIT-BRIDGE-FALSE-EXTENDED
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim <k>
    #applyK(
      toCall(boundMethodV(
        str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
        "split")),
      (str(iCons(32, .IntSeq)), .Vals))
    =>
    wordsObj(
      wCons(
        iCons(97, .IntSeq),
        wCons(iCons(98, .IntSeq), .Words)))
  </k>
  <heap> .Map </heap>
  <heapLoc> 0 </heapLoc>
endmodule

// The supplied semantics performs the allocation and returns ref(0).
module SPLIT-BRIDGE-TRUE-BASE
  imports ANTI-SHUFFLE-BASE

  claim <k>
    #applyK(
      toCall(boundMethodV(
        str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
        "split")),
      (str(iCons(32, .IntSeq)), .Vals))
    =>
    ref(0)
  </k>
  <heap>
    .Map
    =>
    0 |-> list(
      vCons(
        str(iCons(97, .IntSeq)),
        vCons(str(iCons(98, .IntSeq)), .ValSeq)))
  </heap>
  <heapLoc> 0 => 1 </heapLoc>
endmodule
