requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [sort-numbers]:
    <k>
      Call(Name("sort_numbers"), str(CS:IntSeq))
      =>
      expectedSortNumbers(CS)
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

  claim [key-zero]:
    <k> Call(Name("_number_key"), Str("zero")) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-one]:
    <k> Call(Name("_number_key"), Str("one")) => 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-two]:
    <k> Call(Name("_number_key"), Str("two")) => 2 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-three]:
    <k> Call(Name("_number_key"), Str("three")) => 3 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-four]:
    <k> Call(Name("_number_key"), Str("four")) => 4 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-five]:
    <k> Call(Name("_number_key"), Str("five")) => 5 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-six]:
    <k> Call(Name("_number_key"), Str("six")) => 6 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-seven]:
    <k> Call(Name("_number_key"), Str("seven")) => 7 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-eight]:
    <k> Call(Name("_number_key"), Str("eight")) => 8 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [key-nine]:
    <k> Call(Name("_number_key"), Str("nine")) => 9 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "_number_key" |-> numberKeyClosure
             "sort_numbers" |-> sortNumbersClosure,
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
