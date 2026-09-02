requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Keep the proved recursive-call summary available as the circularity used
  // by the whole-module target.
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

  // Deliberately false whole-module result: append one extra zero digit.
  // Ground witness X=0, B=2 satisfies the precondition; execution returns "",
  // while this destination requires "0".
  claim
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
