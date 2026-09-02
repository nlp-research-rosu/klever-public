requires "verification-no-iter-bridge.k"

module SPEC-ITER-CONNECTION
  imports VERIFICATION-NO-ITER-BRIDGE

  claim
    <k> #iterNext(list(stringVals(.StringSeq))) => #iterDone ... </k>
    [label(iter-empty-connection)]

  claim
    <k>
      #iterNext(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))))
      => #iterYield(str(CS), list(stringVals(REST)))
      ...
    </k>
    [label(iter-cons-connection)]
endmodule
