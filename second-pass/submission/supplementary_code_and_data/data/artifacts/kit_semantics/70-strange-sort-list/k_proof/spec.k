requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
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
      ~> (
           If(
             Compare(Name("left"), CmpOp("==", Name("right"))),
             Expr(
               Call(
                 Attribute(Name("result"), "append"),
                 Subscript(Name("ordered"), Name("left")))),
             .Stmts)
           Return(Name("result"))
           .Stmts
         )
      ~> #endcall
      => ref(HR)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(
         "lst"       |-> list(VS)
         "ordered"   |-> ref(HO)
         "result"    |-> ref(HR)
         "left"      |-> L
         "right"     |-> R,
         parent(0)))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      HO |-> list(S)
      HR |-> (list(A) => list(strangeAcc(A, S, L, R)))
    </heap>
    <heapLoc> HL </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L >=Int 0

  claim [entry-point]:
    <k> Call(Name("strange_sort_list"), list(VS)) => ref(1) </k>
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
      0 |-> list(sortVS(VS))
      1 |-> list(
        strangeAcc(
          .ValSeq,
          sortVS(VS),
          0,
          vsLen(sortVS(VS)) -Int 1))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
