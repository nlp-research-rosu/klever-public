requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        str(S:IntSeq),
        Name("char"),
        If(
          Compare(Name("char"), CmpOp("!=", Str(" "))),
          AugAssign(Name("current"), "+", Name("char"))
          If(
            Compare(Name("char"), CmpOp("==", Str("("))),
            AugAssign(Name("depth"), "+", Int(1)) .Stmts,
            AugAssign(Name("depth"), "-", Int(1)) .Stmts)
          If(
            Compare(Name("depth"), CmpOp("==", Int(0))),
            Expr(Call(Attribute(Name("groups"), "append"), Name("current")))
            Assign(Name("current"), Str("")) .Stmts,
            .Stmts)
          .Stmts,
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        scope(
          "paren_string" |-> str(INPUT:IntSeq)
          "groups"       |-> ref(H:Int)
          "current"      |-> (str(CUR:IntSeq) => str(?FINALCUR:IntSeq))
          "depth"        |-> (D:Int => ?FINALD:Int)
          "char"         |-> (str(CH:IntSeq) => str(?FINALCH:IntSeq)),
          P:Parent)
      ...
    </scopes>
    <scopeLoc> NEXTSCOPE:Int </scopeLoc>
    <heap>
      ...
      H |-> (list(OUT:ValSeq)
             => list(scanParenGroups(S, D, CUR, OUT)))
      ...
    </heap>
    <heapLoc> NEXTHEAP:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [function-correct]:
    <k>
      Call(Name("separate_paren_groups"), str(S:IntSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |->
        scope(
          "separate_paren_groups" |->
            closureVal(
              "paren_string",
              Assign(Name("groups"), ListExpr(.Exprs))
              Assign(Name("current"), Str(""))
              Assign(Name("depth"), Int(0))
              Assign(Name("char"), Str(""))
              For(
                Name("char"),
                Name("paren_string"),
                If(
                  Compare(Name("char"), CmpOp("!=", Str(" "))),
                  AugAssign(Name("current"), "+", Name("char"))
                  If(
                    Compare(Name("char"), CmpOp("==", Str("("))),
                    AugAssign(Name("depth"), "+", Int(1)) .Stmts,
                    AugAssign(Name("depth"), "-", Int(1)) .Stmts)
                  If(
                    Compare(Name("depth"), CmpOp("==", Int(0))),
                    Expr(
                      Call(
                        Attribute(Name("groups"), "append"),
                        Name("current")))
                    Assign(Name("current"), Str("")) .Stmts,
                    .Stmts)
                  .Stmts,
                  .Stmts)
                .Stmts)
              Return(Name("groups"))
              .Stmts,
              0),
          parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(separateParenGroupsSpec(S))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validParenInput(S)
endmodule
