requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Already established independently; retained as the recursive helper.
  claim [entry-call]:
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

  // Deliberately false: append an extra ASCII '0' to the required result.
  // Witness X=8, B=3: execution returns "22", while this demands "220".
  claim [false-load]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("change_base"), Int(X), Int(B))
      => str(seqConcat(baseDigits(X, B), iCons(48, .IntSeq)))
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
