requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false mutation: sort_third([1]) cannot return an empty list.
  claim [false-result]:
    <k>
      Call(
        Name("sort_third"),
        (list(vCons(1, .ValSeq)), .Exprs))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "sort_third" |->
           closureVal(
             ("l", .ParamNames),
             Assign(
               Name("thirds"),
               Call(
                 Name("sorted"),
                 (Subscript(
                    Name("l"),
                    Slice(NoBound, NoBound, Int(3))),
                  .Exprs)))
             Assign(Name("result"), ListExpr(.Exprs))
             Assign(Name("i"), Int(0))
             While(
               Compare(
                 Name("i"),
                 CmpOp(
                   "<",
                   Call(Name("len"), (Name("l"), .Exprs)))),
               If(
                 Compare(
                   BinOp("%", Name("i"), Int(3)),
                   CmpOp("==", Int(0))),
                 (Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      (Subscript(
                         Name("thirds"),
                         BinOp("//", Name("i"), Int(3))),
                       .Exprs)))
                  .Stmts),
                 (Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      (Subscript(Name("l"), Name("i")), .Exprs)))
                  .Stmts))
               AugAssign(Name("i"), "+", Int(1))
               .Stmts)
             Return(Name("result"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (0 |-> list(vCons(1, .ValSeq))
       1 |-> list(vCons(1, .ValSeq))
       2 |-> list(.ValSeq))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
