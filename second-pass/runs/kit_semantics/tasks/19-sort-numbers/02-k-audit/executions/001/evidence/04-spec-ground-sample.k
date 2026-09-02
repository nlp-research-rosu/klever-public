requires "verification.k"

module SPEC-GROUND-SAMPLE
  imports VERIFICATION

  // This postcondition is true in both Python implementations. It probes
  // whether the proof backend itself connects opaque sortKeyVS to that value.
  claim [sample-concrete-result]:
    <k>
      Call(Name("sort_numbers"), str(strToCodes("three one five")))
      =>
      str(strToCodes("one three five"))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(splitWS(strToCodes("three one five"), .IntSeq, .ValSeq))
      1 |-> list(sortKeyVS(
                    splitWS(strToCodes("three one five"), .IntSeq, .ValSeq),
                    numberKeyClosure))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
