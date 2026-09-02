requires "verification.k"

module SPEC-MODULE-ONLY
  imports VERIFICATION

  claim
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
