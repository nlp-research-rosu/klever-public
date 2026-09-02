requires "verification-real-encoding.k"

module STAGE5-ITERATOR-CONNECTION-SPEC
  imports EXCHANGE-VERIFICATION-REAL

  // Bridge-free connection: these use only the structural intSeqVals
  // embedding and the supplied MPY-LIST #iterNext rules.
  claim [empty-connection]:
    <k>
      #iterNext(list(intSeqVals(.IntSeq)))
      =>
      #iterDone
    </k>

  claim [cons-connection]:
    <k>
      #iterNext(list(intSeqVals(iCons(I:Int, R:IntSeq))))
      =>
      #iterYield(I, list(intSeqVals(R)))
    </k>
endmodule
