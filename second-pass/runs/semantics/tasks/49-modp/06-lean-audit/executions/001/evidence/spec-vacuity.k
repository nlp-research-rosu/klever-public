requires "verification.k"

module MODP-SPEC-VACUITY
  imports MODP-VERIFICATION

  claim
    <k>
      ( #loadAll(modpProgram)
        ~> Call(Name("modp"), (Int(N), Int(P), .Exprs)) )
      => ((specModp(N, P) +Int 1) ~> .K)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
                  "modp" |-> closureVal(
                    ("n", "p", .ParamNames), modpBody, 0),
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
