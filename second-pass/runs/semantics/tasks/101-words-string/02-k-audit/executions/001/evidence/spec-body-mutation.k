requires "verification-body-mutation.k"

module WORDS-STRING-SPEC-BODY-MUTATION
  imports WORDS-STRING-VERIFICATION-BODY-MUTATION

  claim
    <k>
      Call(wordsStringFunctionBodyMutation, (str(CS), .Exprs))
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
      0 |-> list(wordsStringExpectedBodyMutation(CS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
