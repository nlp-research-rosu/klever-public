requires "verification.k"

module SPEC-ORIGINAL-BRIDGE-WITNESS
  imports VERIFICATION

  // This is false for the exact submitted helper body under fixed semantics:
  // Python list indexing normalizes -1, so helper([5], -1, 0) returns 0.
  // The candidate's #targetCall rule uses valSeqAt directly and proves 1.
  claim [wrong-negative-index-result]:
    <k>
      #applyK(
        toCall(#helperClosure),
        (ref(0), -1, 0, .Vals))
    =>
      1
    </k>
    <heap> 0 |-> list(vCons(5, .ValSeq)) </heap>
endmodule
