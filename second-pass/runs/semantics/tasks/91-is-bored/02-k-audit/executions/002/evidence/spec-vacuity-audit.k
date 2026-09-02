requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: both Python implementations and the positive K claim
  // return 0 for this satisfying ground entry state.
  claim
    <k>
      Call(Name("is_bored"), Str("Hello world"))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          boredFunctionBody,
          0
        ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-result-hello)]
endmodule
