requires "verification.k"

module REVIEWER-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result: 12 is > 10 but its last decimal digit is even.
  // The real program returns 0 for [12], so the claimed result 1 must fail.
  claim [twelve-wrongly-counts]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            specialFilterStmts())))
      ~> Call(Name("specialFilter"), list(vCons(12, .ValSeq)))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "specialFilter"
                 |-> closureVal("nums", specialFilterStmts(), 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
