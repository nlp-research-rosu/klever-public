requires "verification.k"

module AUDIT-GROUND
  imports VERIFICATION

  claim [empty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "strlen",
            Params("string"),
            Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts
          ) .Stmts
        )
      )
      ~> Call(Name("strlen"), (str(.IntSeq), .Exprs))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "strlen" |-> closureVal(
             "string" , .ParamNames,
             Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts,
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

  claim [abc]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "strlen",
            Params("string"),
            Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts
          ) .Stmts
        )
      )
      ~> Call(
           Name("strlen"),
           (str(iCons(97, iCons(98, iCons(99, .IntSeq)))), .Exprs)
         )
      => 3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "strlen" |-> closureVal(
             "string" , .ParamNames,
             Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts,
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

  claim [astral]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "strlen",
            Params("string"),
            Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts
          ) .Stmts
        )
      )
      ~> Call(Name("strlen"), (str(iCons(128578, .IntSeq)), .Exprs))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "strlen" |-> closureVal(
             "string" , .ParamNames,
             Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts,
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
