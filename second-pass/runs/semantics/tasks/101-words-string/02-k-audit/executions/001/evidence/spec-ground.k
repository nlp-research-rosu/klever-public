requires "verification.k"

module WORDS-STRING-SPEC-GROUND
  imports WORDS-STRING-VERIFICATION

  // Satisfying witness: s = "a,,b".
  claim
    <k>
      Call(
        wordsStringFunction,
        (str(iCons(97, iCons(44, iCons(44, iCons(98, .IntSeq))))), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(str(iCons(98, .IntSeq)), .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
