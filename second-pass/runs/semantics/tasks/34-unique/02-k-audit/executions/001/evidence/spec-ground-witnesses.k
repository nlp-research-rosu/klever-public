requires "verification.k"

module UNIQUE-GROUND-WITNESSES
  imports UNIQUE-VERIFICATION

  // member-summary precondition witness: 2 occurs in [1, 2, 1].
  claim [member-ground]:
    <k>
      #memberAcc(
        2,
        list(vCons(1, vCons(2, vCons(1, .ValSeq)))))
      => true
    </k>

  // unique-loop precondition witness. Starting accumulator [9] and loop input
  // [2, 1, 2] produce first-seen accumulator [9, 2, 1], and item ends as 2.
  claim [loop-ground]:
    <k>
      #loop(
        list(vCons(2, vCons(1, vCons(2, .ValSeq)))),
        Name("item"),
        uniqueLoopBody)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        .Map
          [ "l" <- list(vCons(2, vCons(1, vCons(2, .ValSeq)))) ]
          [ "result" <- ref(0) ]
          [ "item" <- 99 => 2 ],
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(vCons(9, .ValSeq))
      =>
      0 |-> list(vCons(9, vCons(2, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Entry precondition witness using the literal submitted solution.mpy body,
  // not the proof-local uniqueBody abbreviation. Input [2, 1, 2] returns [1, 2].
  claim [literal-entry-ground]:
    <k>
      #loadAll(
        Module(
          FuncDef("unique", Params("l"),
            Assign(Name("result"), ListExpr(.Exprs))
            For(Name("item"), Name("l"),
              If(
                Compare(
                  Name("item"),
                  CmpOp("not in", Name("result"))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    Name("item"), .Exprs))
                .Stmts,
                .Stmts))
            Return(Call(Name("sorted"), Name("result"), .Exprs)))
          Assign(
            Name("answer"),
            Call(
              Name("unique"),
              list(vCons(2, vCons(1, vCons(2, .ValSeq))))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map
          [ "unique" <-
            closureVal(
              "l",
              Assign(Name("result"), ListExpr(.Exprs))
              For(Name("item"), Name("l"),
                If(
                  Compare(
                    Name("item"),
                    CmpOp("not in", Name("result"))),
                  Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      Name("item"), .Exprs))
                  .Stmts,
                  .Stmts))
              Return(Call(Name("sorted"), Name("result"), .Exprs)),
              0) ]
          [ "answer" <- ref(1) ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(2, vCons(1, .ValSeq)))
      1 |-> list(vCons(1, vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
