requires "verification.k"

module BF-SPEC-GROUND-WITNESSES
  imports BF-VERIFICATION

  // Satisfies the valid-pair case represented inside #validCases.
  claim
    <k>
      bfRun(Str("Mercury"), Str("Neptune"))
    =>
      tuple(
        vCons(str(strToCodes("Venus")),
        vCons(str(strToCodes("Earth")),
        vCons(str(strToCodes("Mars")),
        vCons(str(strToCodes("Jupiter")),
        vCons(str(strToCodes("Saturn")),
        vCons(str(strToCodes("Uranus")), .ValSeq)))))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A="" satisfies every invalid-first conjunct; the second value is arbitrary.
  claim
    <k> bfRun(Str(""), Str("Neptune")) => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // A="Earth" is valid and B="" satisfies every invalid-second conjunct.
  claim
    <k> bfRun(Str("Earth"), Str("")) => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
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
