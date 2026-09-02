requires "foundation.k"

module CONNECTION-SPEC
  imports FOUNDATION

  claim [helper-vowel]:
    <k>
      #applyK(
        toCall(closureVal(
          ("ch", .ParamNames),
          isVowelBody,
          0)),
        (str(iCons(C, .IntSeq)), .Vals))
      ~> CONT:K
      =>
      true ~> CONT
    </k>
    <env> 1 </env>
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
          ( "word"   |-> str(CS)
            "result" |-> str(R)
            "found"  |-> F
            "i"      |-> I ),
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
    requires vowelPred(C)

  claim [helper-consonant]:
    <k>
      #applyK(
        toCall(closureVal(
          ("ch", .ParamNames),
          isVowelBody,
          0)),
        (str(iCons(C, .IntSeq)), .Vals))
      ~> CONT:K
      =>
      false ~> CONT
    </k>
    <env> 1 </env>
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
          ( "word"   |-> str(CS)
            "result" |-> str(R)
            "found"  |-> F
            "i"      |-> I ),
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
    requires notBool vowelPred(C)
endmodule
