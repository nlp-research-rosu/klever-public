requires "helper-verification.k"

module LOOP-CONNECTION-SPEC
  imports HELPER-VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(Name("i"), CmpOp(">", Int(0))),
        getClosestLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => str(closestScan(CS, I, R, F))
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
          ( "word"   |-> str(CS)
            "result" |-> str(R)
            "found"  |-> F
            "i"      |-> I ),
          parent(0))
        -1 |-> BUILTINS )
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
        -1 |-> BUILTINS )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
     andBool I +Int 1 <Int isLen(CS)
endmodule
