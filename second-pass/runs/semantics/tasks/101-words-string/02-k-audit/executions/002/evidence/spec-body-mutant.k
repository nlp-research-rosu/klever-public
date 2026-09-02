requires "verification-body-mutant.k"

module WORDS-STRING-BODY-MUTANT-SPEC
  imports WORDS-STRING-BODY-MUTANT

  claim
    <k>
      Call(wordsStringFunctionMutant, (str(CS), .Exprs))
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
      0 |-> list(wordsStringExpected(CS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
