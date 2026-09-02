requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: count starts at 1 instead of 0. The original
  // empty-input postcondition must therefore be rejected.
  claim [changed-initial-count]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            Assign(Name("count"), Int(1))
            Assign(Name("num"), Int(0))
            Assign(Name("text"), Str(""))
            For(Name("num"), Name("nums"), filterBody())
            Return(Name("count")))))
      ~> Call(Name("specialFilter"), list(.ValSeq))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "specialFilter"
                 |-> closureVal(
                       "nums",
                       Assign(Name("count"), Int(1))
                       Assign(Name("num"), Int(0))
                       Assign(Name("text"), Str(""))
                       For(Name("num"), Name("nums"), filterBody())
                       Return(Name("count")),
                       0),
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
