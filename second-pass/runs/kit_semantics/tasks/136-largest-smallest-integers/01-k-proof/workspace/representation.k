requires "reference-semantics/semantics.k"

module INT-VAL-REP
  imports MPY

  // A structural, one-for-one embedding of arbitrary finite Int sequences
  // into the reference semantics' heterogeneous value-sequence sort.
  syntax ValSeq ::= intVals(IntSeq)

  rule intVals(.IntSeq) => .ValSeq
  rule intVals(iCons(I:Int, IS:IntSeq))
    => vCons(I, intVals(IS))

  // Expose exactly one constructor at the only observer used by the program.
  // The supplied #iterNext rules then perform the actual iteration step.
  rule <k>
    #iterNext(list(intVals(.IntSeq)))
    => #iterNext(list(.ValSeq))
    ...
  </k>

  rule <k>
    #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
    => #iterNext(list(vCons(I, intVals(IS))))
    ...
  </k>
endmodule
