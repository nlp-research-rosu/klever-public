requires "mutation-verification.k"

module MUTATION-SPEC
  imports MUTATION-VERIFICATION

  // The materially changed body must not satisfy the original result claim.
  claim [changed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            MUTATED-BODY
          )
          .Stmts
        )
      )
      ~> Call(
           Name("Strongest_Extension"),
           str(.IntSeq),
           list(.ValSeq),
           .Exprs
         )
      => expectedResult(.IntSeq, .ValSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               MUTATED-BODY,
               0
             ),
        parent(-1)
      )
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
