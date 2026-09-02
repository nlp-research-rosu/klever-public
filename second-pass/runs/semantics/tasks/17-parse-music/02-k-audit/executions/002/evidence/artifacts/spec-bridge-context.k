requires "bridge-observer.k"

module PARSE-MUSIC-BRIDGE-CONTEXT-SPEC
  imports PARSE-MUSIC-BRIDGE-OBSERVER

  // The candidate bridge returns a non-reference iterator and allocates nothing.
  claim
    <k> #applyK(
          toCall(
            boundMethodV(
              str(musicCodes(whole(.Music))),
              "split")),
          .Vals)
         ~> #probeRef
        => false ~> .K
    </k>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
endmodule
