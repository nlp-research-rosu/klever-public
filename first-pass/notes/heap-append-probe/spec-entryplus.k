requires "verification.k"

module HAP-ENTRYPLUS-SPEC
  imports HEAP-APPEND-PROBE-VERIFICATION

claim
    <k>
      FuncDef("build_plus", Params("n"),
        Assign(Name("out"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n")),
          Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("i")))))
        Return(Name("out")))
      Assign(Name("res"), Call(Name("build_plus"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "build_plus" <- ?_:Val ] [ "res" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(plusFold(0, N, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

endmodule
