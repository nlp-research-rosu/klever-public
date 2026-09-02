requires "verification.k"

module IS-SORTED-VACUITY-AUDIT
  imports IS-SORTED-WITH-LOOP-LEMMA

  // Fresh reviewer mutation: negate the result-constraining postcondition.
  // INPUT = .IntSeq satisfies the precondition; the real and claimed result is
  // true, while this mutated destination demands false.
  claim [false-negated-result]:
    <k>
      #applyK(toCall(isSortedClosure),
              (list(intsToVals(INPUT:IntSeq)), .Vals))
      =>
      notBool scanResult(scanAll(true, 0, 0, INPUT))
    </k>
    <env> 0 => 0 </env>
    <scopes>
      0 |-> scope("is_sorted" |-> isSortedClosure, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope("is_sorted" |-> isSortedClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
endmodule
