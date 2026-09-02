requires "verification-body-mutant.k"

module MODP-SPEC-BODY-MUTANT
  imports MODP-VERIFICATION-BODY-MUTANT

  claim
    <k>
      ( #loadAll(modpProgramMutant)
        ~> Call(Name("modp"), (Int(N), Int(P), .Exprs)) )
      => (specModpMutantBodyTest(N, P) ~> .K)
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
    requires N >=Int 0 andBool P >Int 0
endmodule
