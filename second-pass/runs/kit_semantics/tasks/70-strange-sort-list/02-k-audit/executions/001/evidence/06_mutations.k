requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Satisfying witness input [1, 2]. The real result is [1, 2], while this
  // mutation demands [1, 1].
  claim [false-result]:
    <k>
      Call(Name("strange_sort_list"), list(vCons(1, vCons(2, .ValSeq))))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "strange_sort_list" |->
          closureVal(
            "lst",
            Assign(Name("ordered"), Call(Name("sorted"), Name("lst")))
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("left"), Int(0))
            Assign(
              Name("right"),
              BinOp("-", Call(Name("len"), Name("ordered")), Int(1)))
            While(
              Compare(Name("left"), CmpOp("<", Name("right"))),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("left"))))
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("right"))))
              AugAssign(Name("left"), "+", Int(1))
              AugAssign(Name("right"), "-", Int(1)))
            If(
              Compare(Name("left"), CmpOp("==", Name("right"))),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("left")))),
              .Stmts)
            Return(Name("result")),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(1, vCons(2, .ValSeq))))
      1 |-> list(vCons(1, vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The program term itself is mutated: its second append selects `left`
  // instead of `right`. On [1, 2] that body returns [1, 1], so the original
  // [1, 2] result obligation must be rejected.
  claim [changed-body]:
    <k>
      Call(Name("strange_sort_list"), list(vCons(1, vCons(2, .ValSeq))))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "strange_sort_list" |->
          closureVal(
            "lst",
            Assign(Name("ordered"), Call(Name("sorted"), Name("lst")))
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("left"), Int(0))
            Assign(
              Name("right"),
              BinOp("-", Call(Name("len"), Name("ordered")), Int(1)))
            While(
              Compare(Name("left"), CmpOp("<", Name("right"))),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("left"))))
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("left"))))
              AugAssign(Name("left"), "+", Int(1))
              AugAssign(Name("right"), "-", Int(1)))
            If(
              Compare(Name("left"), CmpOp("==", Name("right"))),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Subscript(Name("ordered"), Name("left")))),
              .Stmts)
            Return(Name("result")),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(1, vCons(2, .ValSeq))))
      1 |-> list(vCons(1, vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
