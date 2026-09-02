requires "connection.k"

module CONNECTION-SPEC
  imports CONNECTION

  claim [int-vals-empty-iterator]:
    <k>
      #iterNext(list(intVals(.IntSeq)))
      => #iterDone
      ...
    </k>

  claim [int-vals-cons-iterator]:
    <k>
      #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
      => #iterYield(I, list(intVals(IS)))
      ...
    </k>
endmodule
