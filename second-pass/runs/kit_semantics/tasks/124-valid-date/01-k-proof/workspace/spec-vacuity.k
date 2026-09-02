requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: 03-11-2000 is valid, so the real function returns
  // true.  Gate A5 requires this claim to be rejected.
  claim [false-result]:
    <k>
      #loadAll(validDateProgram)
        ~> Call(Name("valid_date"), Str("03-11-2000"))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
