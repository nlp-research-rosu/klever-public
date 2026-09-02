requires "foundation.k"

module HELPER-BODY-MUTATION-SPEC
  imports FOUNDATION

  claim [mutated-helper-must-not-prove]:
    <k>
      #applyK(
        toCall(closureVal(
          ("ch", .ParamNames),
          Return(Bool(false)) .Stmts,
          0)),
        (str(iCons(97, .IntSeq)), .Vals))
      ~> .K
      =>
      true ~> .K
    </k>
    <env> 1 </env>
    <scopes>
      ( 0 |-> scope(
          ( "_is_vowel" |-> closureVal(
              ("ch", .ParamNames),
              Return(Bool(false)) .Stmts,
              0)
            "get_closest_vowel" |-> closureVal(
              ("word", .ParamNames),
              getClosestBody,
              0) ),
          parent(-1))
        1 |-> scope(
          ( "word"   |-> str(strToCodes("bab"))
            "result" |-> str(.IntSeq)
            "found"  |-> false
            "i"      |-> 1 ),
          parent(0))
        -1 |-> BUILTINS )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
