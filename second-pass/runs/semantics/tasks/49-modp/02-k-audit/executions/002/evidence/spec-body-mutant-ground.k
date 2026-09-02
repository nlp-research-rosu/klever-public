requires "verification-body-mutant.k"

module MODP-SPEC-BODY-MUTANT-GROUND
  imports MODP-VERIFICATION-BODY-MUTANT

  // Satisfying witness n=1, p=5: the real body returns 2, while the mutated
  // base-3 body returns 3.
  claim
    <k>
      ( #loadAll(modpProgramMutant)
        ~> Call(Name("modp"), (Int(1), Int(5), .Exprs)) )
      => (2 ~> .K)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
                  "modp" |-> closureVal(
                    ("n", "p", .ParamNames), modpBodyMutant, 0),
                  parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
