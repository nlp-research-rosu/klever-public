requires "verification-bridge-free.k"

module BRIDGE-CONNECTION
  imports VERIFICATION-BRIDGE-FREE

  claim
    <k> #iterNext(list(stringVals(.StringSeq))) => #iterDone ... </k>
    [label(empty-connection)]

  claim
    <k> #iterNext(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))))
      => #iterYield(str(CS), list(stringVals(REST))) ... </k>
    [label(cons-connection)]

endmodule
