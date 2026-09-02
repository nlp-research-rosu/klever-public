requires "verification.k"

module HAP-ENTRYSQ-SPEC
  imports HEAP-APPEND-PROBE-VERIFICATION

claim
    <k>
      FuncDef("build_squares", Params("n"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n")),
          Expr(Call(Attribute(Name("result"), "append"), BinOp("*", Name("i"), Name("i")))))
        Return(Name("result")))
      Assign(Name("res"), Call(Name("build_squares"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "build_squares" <- ?_:Val ] [ "res" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(sqFold(0, N, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Claim 4: entry (plus builder) — the final heap carries garbage; the result
  // entry is found by unification.
  
endmodule
