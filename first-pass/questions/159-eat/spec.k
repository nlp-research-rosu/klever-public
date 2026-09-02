requires "verification.k"

module EAT-SPEC
  imports EAT-VERIFICATION

  claim
    <k>
      FuncDef("eat", Params("number", "need", "remaining"),
        If(Compare(Name("need"), CmpOp("<=", Name("remaining"))),
          Return(ListExpr(BinOp("+", Name("number"), Name("need")),
                          BinOp("-", Name("remaining"), Name("need")))),
          Return(ListExpr(BinOp("+", Name("number"), Name("remaining")), Int(0)))))
      Assign(Name("result"), Call(Name("eat"), NUM:Int , ND:Int , REM:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "eat" <- ?_:Val ] [ "result" <- ref(?H2:Int) ], parent(-1))
    </scopes>
    // the returned list is a heap object (ListExpr allocates)
    <heap> .Map => (?H2 |-> ?LV:Val) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?LV ==K #if (ND <=Int REM)
             #then list(vCons(NUM +Int ND,  vCons(REM -Int ND, .ValSeq)))
             #else list(vCons(NUM +Int REM, vCons(0, .ValSeq))) #fi
    [all-path]
endmodule
