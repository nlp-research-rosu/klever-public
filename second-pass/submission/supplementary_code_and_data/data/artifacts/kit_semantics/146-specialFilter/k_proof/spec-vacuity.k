requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false postcondition for the realizable empty input.
  claim [wrong-result-empty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            specialFilterStmts())))
      ~> Call(Name("specialFilter"), list(.ValSeq))
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
