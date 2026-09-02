requires "verification.k"

module SPEC-AUDITOR-VACUITY
  imports VERIFICATION

  // Fresh false mutation: demand the real summary followed by an extra '!'.
  // For the satisfying input "three one five", both Python implementations
  // return "one three five", not "one three five!".
  claim [sort-numbers-extra-bang]:
    <k>
      Call(Name("sort_numbers"), str(CS:IntSeq))
      =>
      str(
        seqConcat(
          joinCodes(
            strToCodes(" "),
            sortKeyVS(
              splitWS(CS, .IntSeq, .ValSeq),
              numberKeyClosure)),
          iCons(33, .IntSeq)))
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
      0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
      1 |-> list(sortKeyVS(
                    splitWS(CS, .IntSeq, .ValSeq),
                    numberKeyClosure))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumberWords(splitWS(CS, .IntSeq, .ValSeq))
endmodule
