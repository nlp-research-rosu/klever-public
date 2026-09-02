requires "verification-body-mutant-audit.k"

module SPEC-BODY-MUTANT-AUDIT
  imports BODY-MUTANT-AUDIT

  claim [changed-executed-body-must-not-prove]:
    <k> #loadAll(auditMutantModule)
         ~> bfCall(strToCodes("Mercury"), strToCodes("Earth"))
        => tuple(vCons(str(strToCodes("Venus")), .ValSeq)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"),
                                                auditMutantBody, 0),
                    parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
