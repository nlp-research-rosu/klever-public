requires "verification.k"

module SPEC-APPLY-ONLY
  imports VERIFICATION

  claim
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
endmodule
