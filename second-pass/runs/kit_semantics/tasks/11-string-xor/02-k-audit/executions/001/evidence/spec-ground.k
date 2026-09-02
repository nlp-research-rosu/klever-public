requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim [documented-example]:
    <k>
      Call(
        Name("string_xor"),
        str(iCons(48, iCons(49, iCons(48, .IntSeq)))),
        str(iCons(49, iCons(49, iCons(48, .IntSeq))))
      )
      =>
      str(iCons(49, iCons(48, iCons(48, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "string_xor" |->
          closureVal(
            ("a", "b"),
            Assign(Name("result"), Str(""))
            Assign(Name("x"), Str(""))
            Assign(Name("y"), Str(""))
            For(
              TupleExpr(Name("x"), Name("y")),
              Call(Name("zip"), Name("a"), Name("b")),
              If(
                Compare(Name("x"), CmpOp("==", Name("y"))),
                AugAssign(Name("result"), "+", Str("0")),
                AugAssign(Name("result"), "+", Str("1"))
              )
            )
            Return(Name("result")),
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

  claim [empty-witness]:
    <k>
      Call(Name("string_xor"), str(.IntSeq), str(.IntSeq))
      =>
      str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "string_xor" |->
          closureVal(
            ("a", "b"),
            Assign(Name("result"), Str(""))
            Assign(Name("x"), Str(""))
            Assign(Name("y"), Str(""))
            For(
              TupleExpr(Name("x"), Name("y")),
              Call(Name("zip"), Name("a"), Name("b")),
              If(
                Compare(Name("x"), CmpOp("==", Name("y"))),
                AugAssign(Name("result"), "+", Str("0")),
                AugAssign(Name("result"), "+", Str("1"))
              )
            )
            Return(Name("result")),
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
