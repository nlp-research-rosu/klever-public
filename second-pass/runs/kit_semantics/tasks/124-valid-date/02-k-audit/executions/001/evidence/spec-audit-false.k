requires "verification.k"

module SPEC-AUDIT-FALSE
  imports VERIFICATION

  // Deliberately false result mutation. "03-11-2000" satisfies the entry
  // configuration and the submitted program returns true, not false.
  claim [valid-witness-returns-false]:
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
