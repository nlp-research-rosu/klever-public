requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim [ground-mercury-earth]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Mercury"), strToCodes("Earth"))
        => tuple(vCons(str(strToCodes("Venus")), .ValSeq)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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

  claim [ground-jupiter-neptune]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Jupiter"), strToCodes("Neptune"))
        => tuple(
             vCons(str(strToCodes("Saturn")),
             vCons(str(strToCodes("Uranus")), .ValSeq))) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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

  claim [ground-reverse]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Neptune"), strToCodes("Mercury"))
        => tuple(
             vCons(str(strToCodes("Venus")),
             vCons(str(strToCodes("Earth")),
             vCons(str(strToCodes("Mars")),
             vCons(str(strToCodes("Jupiter")),
             vCons(str(strToCodes("Saturn")),
             vCons(str(strToCodes("Uranus")), .ValSeq))))))) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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

  claim [ground-equal]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Earth"), strToCodes("Earth"))
        => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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

  claim [ground-invalid]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Pluto"), strToCodes("Earth"))
        => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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

  claim [ground-nonascii-code]:
    <k> #loadAll(bfModule)
         ~> bfCall(iCons(128, .IntSeq), strToCodes("Earth"))
        => tuple(.ValSeq) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "bf" |-> closureVal(("planet1", "planet2"), bfBody, 0),
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
