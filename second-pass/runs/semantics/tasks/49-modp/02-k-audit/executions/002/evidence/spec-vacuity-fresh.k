requires "verification.k"

module MODP-SPEC-VACUITY-FRESH
  imports MODP-VERIFICATION

  // Fresh false result obligation.  The satisfying input (n=3,p=5) returns 3,
  // so requiring 4 must leave a semantic residual rather than close.
  claim
    <k>
      ( #loadAll(modpProgram)
        ~> Call(Name("modp"), (Int(3), Int(5), .Exprs)) )
      => (4 ~> .K)
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
endmodule
