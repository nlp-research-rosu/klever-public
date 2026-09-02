requires "verification.k"

module SPEC-NESTED-LIST-WITNESS
  imports VERIFICATION

  // targetValid(mainCall, ...) is true for this ValSeq. Fixed semantics
  // structurally compares the two inner lists and returns 0. The candidate
  // target rules compare distinct refs with ==K and prove 1.
  claim [wrong-nested-list-result]:
    <k>
      #applyK(toCall(#mainClosure), (ref(0), .Vals))
    =>
      1
    </k>
    <heap>
      0 |-> list(vCons(ref(1), vCons(ref(2), .ValSeq)))
      1 |-> list(vCons(5, .ValSeq))
      2 |-> list(vCons(5, .ValSeq))
    </heap>
endmodule
