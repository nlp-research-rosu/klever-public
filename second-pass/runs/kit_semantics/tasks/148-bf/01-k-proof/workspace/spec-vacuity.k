requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: Venus lies between Mercury and Earth.
  claim [false-empty-result]:
    <k> #loadAll(bfModule)
         ~> bfCall(strToCodes("Mercury"), strToCodes("Earth"))
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
