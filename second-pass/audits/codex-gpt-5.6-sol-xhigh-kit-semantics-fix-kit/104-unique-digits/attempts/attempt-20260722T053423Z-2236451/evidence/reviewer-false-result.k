requires "verification.k"

module REVIEWER-FALSE-RESULT
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(list(VS:ValSeq), Name("n"),
        Assign(Name("text"), Call(Name("str"), Name("n")))
        If(BoolOp(
          "and",
          Compare(Str("0"), CmpOp("not in", Name("text"))),
          Compare(Str("2"), CmpOp("not in", Name("text"))),
          Compare(Str("4"), CmpOp("not in", Name("text"))),
          Compare(Str("6"), CmpOp("not in", Name("text"))),
          Compare(Str("8"), CmpOp("not in", Name("text")))),
          Expr(Call(Attribute(Name("result"), "append"), Name("n"))),
          .Stmts)
        .Stmts)
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        "x" |-> list(INPUT:ValSeq)
        "result" |-> ref(H:Int)
        "n" |-> (OLDN:Int => ?NEWN:Int)
        "text" |-> (str(OLDTEXT:IntSeq) => str(?NEWTEXT:IntSeq)),
        parent(0))
      0 |-> scope(GLOBALS:Map, parent(-1))
      -1 |-> builtinsScope
      SCOPES:Map
    </scopes>
    <heap>
      ... H |-> list(ACC:ValSeq => valSeqConcat(ACC, filterOdd(VS))) ...
    </heap>
    requires positiveInts(VS)
     andBool notBool "str" in_keys(GLOBALS)

  claim [unique-digits]:
    <k>
      Call(Name("unique_digits"), list(VS:ValSeq))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "unique_digits" |-> closureVal("x",
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("n"), Int(0))
          Assign(Name("text"), Str(""))
          For(Name("n"), Name("x"),
            Assign(Name("text"), Call(Name("str"), Name("n")))
            If(BoolOp(
              "and",
              Compare(Str("0"), CmpOp("not in", Name("text"))),
              Compare(Str("2"), CmpOp("not in", Name("text"))),
              Compare(Str("4"), CmpOp("not in", Name("text"))),
              Compare(Str("6"), CmpOp("not in", Name("text"))),
              Compare(Str("8"), CmpOp("not in", Name("text")))),
              Expr(Call(Attribute(Name("result"), "append"), Name("n"))),
              .Stmts)
            .Stmts)
          Return(Call(Name("sorted"), Name("result")))
          .Stmts,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(filterOdd(VS))
         1 |-> list(vCons(0, sortVS(filterOdd(VS))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires positiveInts(VS)
endmodule
