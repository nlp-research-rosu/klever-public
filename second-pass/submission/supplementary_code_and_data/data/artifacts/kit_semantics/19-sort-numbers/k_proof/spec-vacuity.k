requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation: a valid call returns a string, not None.
  claim [wrong-result]:
    <k>
      Call(Name("sort_numbers"), str(CS:IntSeq))
      =>
      noneV
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
