requires "verification.k"

module BF-SPEC
  imports BF-VERIFICATION

  // ---- Entry — result == bfRes over symbolic planet-name strings.
  claim
    <k>
      FuncDef("bf", Params("planet1", "planet2"),
          Assign(
            Name("planet_names"),
            TupleExpr(
              Str("Mercury"),
              Str("Venus"),
              Str("Earth"),
              Str("Mars"),
              Str("Jupiter"),
              Str("Saturn"),
              Str("Uranus"),
              Str("Neptune")))
          If(BoolOp(
            "or",
            Compare(Name("planet1"), CmpOp("not in", Name("planet_names"))),
            Compare(Name("planet2"), CmpOp("not in", Name("planet_names"))),
            Compare(Name("planet1"), CmpOp("==", Name("planet2")))),
            Return(TupleExpr(.Exprs)),
            .Stmts)
          Assign(
            Name("planet1_index"),
            Call(Attribute(Name("planet_names"), "index"), Name("planet1")))
          Assign(
            Name("planet2_index"),
            Call(Attribute(Name("planet_names"), "index"), Name("planet2")))
          If(Compare(Name("planet1_index"), CmpOp("<", Name("planet2_index"))),
            Return(
              Subscript(
                Name("planet_names"),
                Slice(
                  BinOp("+", Name("planet1_index"), Int(1)),
                  Name("planet2_index"),
                  NoBound))),
            Return(
              Subscript(
                Name("planet_names"),
                Slice(
                  BinOp("+", Name("planet2_index"), Int(1)),
                  Name("planet1_index"),
                  NoBound)))))
      Assign(Name("result"), Call(Name("bf"), str(P1:IntSeq), str(P2:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "bf" <- ?_:Val ]
                       [ "result" <- bfRes(str(P1), str(P2)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
