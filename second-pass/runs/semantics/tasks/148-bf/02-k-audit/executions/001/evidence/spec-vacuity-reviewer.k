requires "verification.k"

module BF-SPEC-VACUITY-REVIEWER
  imports BF-VERIFICATION

  // Deliberately false: all six interior planets lie between Mercury and
  // Neptune, so the submitted function cannot return the empty tuple.
  claim
    <k>
      bfRun(Str("Mercury"), Str("Neptune"))
    =>
      tuple(.ValSeq)
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
endmodule
