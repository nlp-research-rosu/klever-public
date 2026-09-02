requires "verification.k"

module WORDS-STRING-SPEC-VACUITY
  imports WORDS-STRING-VERIFICATION

  // Fresh false result mutation: prepend an extra "X" token to the required
  // result. The original precondition is unchanged. For the satisfying witness
  // CS = .IntSeq (the empty Python string), execution returns [], not ["X"].
  claim
    <k>
      Call(wordsStringFunction, (str(CS), .Exprs))
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
          str(iCons(88, .IntSeq)),
          wordsStringExpected(CS)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
