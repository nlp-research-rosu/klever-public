requires "verification.k"

module SPEC-VACUITY-INVALID-ARBITRARY-CONTINUATION
  imports VERIFICATION

  // Deliberately false: append one extra zero digit to every result.
  // Ground witness X=0, B=2 satisfies the precondition; execution returns "",
  // while the mutated destination requires "0".
  claim
    <k>
      #applyK(
        toCall(changeBaseClosure),
        (X, B, .Vals))
      ~> K
      => str(seqConcat(baseDigits(X, B), iCons(48, .IntSeq)))
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
