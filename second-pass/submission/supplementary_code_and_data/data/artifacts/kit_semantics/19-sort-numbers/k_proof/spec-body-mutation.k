requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // A material helper mutation: every numeral is assigned key 9.
  claim [mutated-key-body]:
    <k>
      Call(Name("sort_numbers"), str(CS:IntSeq))
      =>
      expectedSortNumbers(CS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> closureVal(
                                    ("number", .ParamNames),
                                    (Return(Int(9)) .Stmts),
                                    0)
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
