requires "reference-semantics/semantics.k"

// Reviewer-authored bridge-free definition. It deliberately omits all three
// proof-local acceleration rules from VERIFICATION-BASE.
module BRIDGE-BASE
  imports MPY

  syntax ValSeq ::= intValsAudit(IntSeq)
  rule intValsAudit(.IntSeq) => .ValSeq
  rule intValsAudit(iCons(I:Int, R:IntSeq)) => vCons(I, intValsAudit(R))
endmodule

module BRIDGE-CONNECTION-SPEC
  imports BRIDGE-BASE

  claim [empty-iterator]:
    <k>
      #iterNext(list(intValsAudit(.IntSeq)))
      => #iterDone
      ...
    </k>

  claim [nonempty-iterator]:
    <k>
      #iterNext(list(intValsAudit(iCons(I:Int, R:IntSeq))))
      => #iterYield(I, list(intValsAudit(R)))
      ...
    </k>

  claim [head-subscript]:
    <k>
      valSeqAt(intValsAudit(iCons(I:Int, R:IntSeq)), 0)
      => I
      ...
    </k>
endmodule
