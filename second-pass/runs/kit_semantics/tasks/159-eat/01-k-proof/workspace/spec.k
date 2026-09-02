requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [eat-enough]:
    <k>
      Call(Name("eat"), Int(NUMBER:Int), Int(NEED:Int), Int(REMAINING:Int))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "eat" |-> closureVal(
          "number", "need", "remaining", .ParamNames,
          If(
            Compare(Name("need"), CmpOp("<=", Name("remaining"))),
            Return(
              ListExpr(
                BinOp("+", Name("number"), Name("need")),
                BinOp("-", Name("remaining"), Name("need"))
              )
            ),
            .Stmts
          )
          Return(
            ListExpr(
              BinOp("+", Name("number"), Name("remaining")),
              Int(0)
            )
          ),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(
          NUMBER +Int NEED,
          vCons(REMAINING -Int NEED, .ValSeq)
        )
      )
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      0 <=Int NUMBER andBool NUMBER <=Int 1000
      andBool 0 <=Int NEED andBool NEED <=Int 1000
      andBool 0 <=Int REMAINING andBool REMAINING <=Int 1000
      andBool NEED <=Int REMAINING

  claim [eat-insufficient]:
    <k>
      Call(Name("eat"), Int(NUMBER:Int), Int(NEED:Int), Int(REMAINING:Int))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "eat" |-> closureVal(
          "number", "need", "remaining", .ParamNames,
          If(
            Compare(Name("need"), CmpOp("<=", Name("remaining"))),
            Return(
              ListExpr(
                BinOp("+", Name("number"), Name("need")),
                BinOp("-", Name("remaining"), Name("need"))
              )
            ),
            .Stmts
          )
          Return(
            ListExpr(
              BinOp("+", Name("number"), Name("remaining")),
              Int(0)
            )
          ),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(
          NUMBER +Int REMAINING,
          vCons(0, .ValSeq)
        )
      )
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      0 <=Int NUMBER andBool NUMBER <=Int 1000
      andBool 0 <=Int NEED andBool NEED <=Int 1000
      andBool 0 <=Int REMAINING andBool REMAINING <=Int 1000
      andBool NEED >Int REMAINING
endmodule
