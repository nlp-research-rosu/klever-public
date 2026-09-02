requires "connection-no-iter-bridge.k"

module CONNECTION-NO-ITER-BRIDGE-SPEC
  imports CONNECTION-NO-ITER-BRIDGE

  claim [empty]:
    <k>
      #iterNext(list(intValsNoIterBridge(.IntSeq)))
      => #iterDone
      ...
    </k>

  claim [cons]:
    <k>
      #iterNext(list(intValsNoIterBridge(iCons(I:Int, IS:IntSeq))))
      => #iterYield(I, list(intValsNoIterBridge(IS)))
      ...
    </k>
endmodule
