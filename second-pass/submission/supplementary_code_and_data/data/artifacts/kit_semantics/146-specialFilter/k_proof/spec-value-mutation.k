requires "verification.k"

module SPEC-VALUE-MUTATION
  imports VERIFICATION

  // Deliberately opposite interpretation for a qualifying ground value.
  claim [fifteen-does-not-count]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            specialFilterStmts())))
      ~> Call(
           Name("specialFilter"),
           list(vCons(15, .ValSeq)))
      => 0
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
