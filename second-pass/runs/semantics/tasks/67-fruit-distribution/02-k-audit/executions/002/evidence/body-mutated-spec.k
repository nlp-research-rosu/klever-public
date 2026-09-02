requires "body-mutated-verification.k"

module BODY-MUTATED-SPEC
  imports BODY-MUTATED-VERIFICATION

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           str(fruitSentenceCodes(A, B)), N, .Exprs)
      => N -Int A -Int B
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >=Int 0
     andBool B >=Int 0
     andBool A +Int B <=Int N

  // The prompt's examples are also proof claims.  Unlike the general claim,
  // these use ordinary Str literals and therefore execute the reference
  // semantics' concrete splitWS and intDigAcc definitions.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           Str("5 apples and 6 oranges"), Int(19), .Exprs)
      => 8
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           Str("0 apples and 1 oranges"), Int(3), .Exprs)
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           Str("2 apples and 3 oranges"), Int(100), .Exprs)
      => 95
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("fruit_distribution"),
           Str("100 apples and 1 oranges"), Int(120), .Exprs)
      => 19
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
