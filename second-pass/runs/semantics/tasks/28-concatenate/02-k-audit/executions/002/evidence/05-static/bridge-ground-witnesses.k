requires "verification-no-bridge.k"

module BRIDGE-GROUND-WITNESSES
  imports CONCATENATE-NO-BRIDGE

  claim [empty-right]:
    <k>
      applyBin("+", str(iCons(120, .IntSeq)), str(.IntSeq))
      =>
      str(iCons(120, .IntSeq))
    </k>

  claim [nonempty-right]:
    <k>
      applyBin(
        "+",
        str(iCons(120, .IntSeq)),
        str(iCons(97, iCons(98, .IntSeq)))
      )
      =>
      str(iCons(120, iCons(97, iCons(98, .IntSeq))))
    </k>
endmodule
