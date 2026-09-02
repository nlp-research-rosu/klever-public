requires "no-bridge-observer.k"

module PARSE-MUSIC-NO-BRIDGE-CONTEXT-SPEC
  imports PARSE-MUSIC-NO-BRIDGE-OBSERVER

  // Fixed supplied semantics returns a new reference and allocates split data.
  claim
    <k> #applyK(
          toCall(
            boundMethodV(
              str(musicCodes(whole(.Music))),
              "split")),
          .Vals)
         ~> #probeRef
        => true ~> .K
    </k>
    <heap>
      .Map
      => 0 |-> list(
           splitWS(
             musicCodes(whole(.Music)),
             .IntSeq,
             .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
endmodule
