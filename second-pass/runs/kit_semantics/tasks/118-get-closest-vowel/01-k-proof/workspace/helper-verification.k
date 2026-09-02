requires "foundation.k"

module HELPER-VERIFICATION-SYNTAX
  imports FOUNDATION-SYNTAX
endmodule

module HELPER-VERIFICATION
  imports FOUNDATION

  // These exact-context call summaries are justified by the bridge-free
  // helper claims in connection-spec.k.  Their arbitrary k continuation is
  // contained by the CONT:K quantified in those claims; all other cells and
  // bindings are matched exactly and remain unchanged.
  rule
    <k>
      #applyK(
        toCall(closureVal(
          ("ch", .ParamNames),
          isVowelBody,
          0)),
        (str(iCons(C, .IntSeq)), .Vals))
      => true
      ...
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
    [priority(40)]

  rule
    <k>
      #applyK(
        toCall(closureVal(
          ("ch", .ParamNames),
          isVowelBody,
          0)),
        (str(iCons(C, .IntSeq)), .Vals))
      => false
      ...
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
    [priority(40)]
endmodule
