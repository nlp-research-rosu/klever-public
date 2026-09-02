requires "verification.k"

module CONTINUATION-MUTATION-SPEC
  imports VERIFICATION

  claim [changed-suffix-must-not-prove]:
    <k>
      #while(
        Compare(Name("i"), CmpOp(">", Int(0))),
        getClosestLoopBody)
      ~> ( Assign(Name("result"), Str("x"))
           Return(Name("result"))
           .Stmts )
      ~> #endcall
      => str(strToCodes("a"))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          ( "_is_vowel" |-> closureVal(
              ("ch", .ParamNames),
              isVowelBody,
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
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          ( "_is_vowel" |-> closureVal(
              ("ch", .ParamNames),
              isVowelBody,
              0)
            "get_closest_vowel" |-> closureVal(
              ("word", .ParamNames),
              getClosestBody,
              0) ),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
