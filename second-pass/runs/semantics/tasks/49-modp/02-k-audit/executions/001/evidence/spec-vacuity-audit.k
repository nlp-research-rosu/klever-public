requires "verification.k"

module MODP-SPEC-VACUITY-AUDIT
  imports MODP-VERIFICATION

  // Ground witness N=3, P=5 satisfies N >= 0 and P > 0.
  // The real result is 3; this deliberately and falsely demands 3 + 1.
  claim
    <k>
      ( #loadAll(modpProgram)
        ~> Call(Name("modp"), (Int(3), Int(5), .Exprs)) )
      => ((specModp(3, 5) +Int 1) ~> .K)
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
