requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      #loadAll(getClosestProgram)
      ~> Call(
           Name("get_closest_vowel"),
           (str(strToCodes("yogurt")), .Exprs))
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
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
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
