requires "verification.k"

module REVIEWER-FALSE-SPEC
  imports VERIFICATION

  // Satisfying input CS = "bab". The real result is "a" (code 97), so the
  // empty-string destination below is deliberately false.
  claim [bab-is-not-empty]:
    <k>
      #loadAll(getClosestProgram)
      ~> Call(
           Name("get_closest_vowel"),
           ( str(
               iCons(98,
               iCons(97,
               iCons(98, .IntSeq)))),
             .Exprs ))
      =>
      str(.IntSeq)
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
