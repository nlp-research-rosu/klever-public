requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant: ACC is the already-produced prefix, I is the next even
  // index, and OVS is the unconsumed iterator suffix.  append mutates the
  // result object in place, so the loop performs no fresh allocation.
  claim [loop-correct]:
    <k>
      #iterNext(list(OVS))
      ~> #loopStep(Name("odd"), loopBody)
      ~> K
    =>
      K
    </k>
    <env> L </env>
    <scopes>
      (L |-> scope(
        ("l" |-> LV)
        ("evens" |-> ref(EH))
        ("odds" |-> ref(OH))
        ("result" |-> ref(RH))
        ("i" |-> I)
        ("odd" |-> ODD),
        parent(0)))
      SC
    =>
      (L |-> scope(
        ("l" |-> LV)
        ("evens" |-> ref(EH))
        ("odds" |-> ref(OH))
        ("result" |-> ref(RH))
        ("i" |-> advancedIndex(I, OVS))
        ("odd" |-> ?ODD2),
        parent(0)))
      SC
    </scopes>
    <heap>
      (EH |-> list(EVS))
      (OH |-> list(OALL))
      (RH |-> list(ACC))
      HEAP
    =>
      (EH |-> list(EVS))
      (OH |-> list(OALL))
      (RH |-> list(valSeqConcat(ACC, pairedVS(EVS, OVS, I))))
      HEAP
    </heap>
  // Entry-point theorem.  sortVS is the supplied semantics' trusted,
  // opaque ascending sort.  assembledEvenSort alternates that sorted even
  // subsequence with the untouched odd subsequence.
  claim [sort-even-correct]:
    <k>
      Call(Name("sort_even"), list(VS))
      ~> #observeResult
    =>
      list(
        assembledEvenSort(
          sortVS(evenIndices(VS)),
          oddIndices(VS)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP </heap>
    <heapLoc> 0 => ?HL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
