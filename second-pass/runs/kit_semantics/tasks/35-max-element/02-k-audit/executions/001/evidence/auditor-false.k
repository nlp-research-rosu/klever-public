requires "verification.k"

module AUDITOR-FALSE
  imports VERIFICATION

  // Fresh auditor mutation: the real program returns 3 for [1, 3, 2].
  // Requiring 2 changes the result-bearing obligation while keeping the exact
  // submitted constructor body and a satisfiable concrete input.
  claim [wrong-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Call(Name("max"), Name("l")))
          )
        )
      )
      ~> Call(
           Name("max_element"),
           list(vCons(1, vCons(3, vCons(2, .ValSeq))))
         )
      => 2
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Call(Name("max"), Name("l"))) .Stmts),
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
