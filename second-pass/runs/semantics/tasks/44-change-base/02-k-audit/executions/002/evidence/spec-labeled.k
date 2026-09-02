requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [apply]:
    <k>
      #applyK(
        toCall(changeBaseClosure),
        (X, B, .Vals))
      ~> K
      => str(baseDigits(X, B))
      ~> K
    </k>
    <env> L </env>
    <scopes>
      (0 |-> scope(
        ("change_base" |-> changeBaseClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
      FRAMES
    </scopes>
    <scopeLoc> N </scopeLoc>
    <heap> H </heap>
    <heapLoc> HL </heapLoc>
    <stack> ST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EC </exit-code>
    requires X >=Int 0 andBool B >=Int 2 andBool B <Int 10
     andBool N >Int 0
     andBool freshScopes(N, FRAMES)

  claim [module]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("change_base"), Int(X), Int(B))
      => str(baseDigits(X, B))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        "change_base" |-> changeBaseClosure,
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0 andBool B >=Int 2 andBool B <Int 10
endmodule
