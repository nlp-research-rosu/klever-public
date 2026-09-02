requires "verification.k"

module SPEC-BODY-REVIEW
  imports VERIFICATION

  claim [loop-first]:
    <k>
      #loop(str(CS:IntSeq), Name("char"),
        If(Compare(Name("char"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(Compare(Name("balance"), CmpOp("<", Name("minimum"))),
          Assign(Name("minimum"), Name("balance")),
          .Stmts))
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "lst" |-> INPUT:Val
        "text" |-> TEXT:Val
        "balance" |-> (B:Int => scanBalance(CS, B))
        "minimum" |-> (M:Int => scanMinimum(CS, B, M))
        "char" |-> (OLD:Val => scanLast(CS, OLD)),
        P:Parent)
      ...
    </scopes>

  // The source contains a second syntactically identical scan.  This separate
  // claim records and proves the invariant obligation for that occurrence.
  claim [loop-second]:
    <k>
      #loop(str(CS:IntSeq), Name("char"),
        If(Compare(Name("char"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(Compare(Name("balance"), CmpOp("<", Name("minimum"))),
          Assign(Name("minimum"), Name("balance")),
          .Stmts))
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "lst" |-> INPUT:Val
        "text" |-> TEXT:Val
        "balance" |-> (B:Int => scanBalance(CS, B))
        "minimum" |-> (M:Int => scanMinimum(CS, B, M))
        "char" |-> (OLD:Val => scanLast(CS, OLD)),
        P:Parent)
      ...
    </scopes>

  claim [match-parens]:
    <k>
      Call(Name("match_parens"),
        list(vCons(str(A:IntSeq), vCons(str(B:IntSeq), .ValSeq))))
      => ?RESULT:Str
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "match_parens" |->
          closureVal("lst",
            Assign(
              Name("text"),
              BinOp(
                "+",
                Subscript(Name("lst"), Int(0)),
                Subscript(Name("lst"), Int(1))))
            Assign(Name("balance"), Int(0))
            Assign(Name("minimum"), Int(0))
            Assign(Name("char"), Str(""))
            For(Name("char"), Name("text"),
              If(Compare(Name("char"), CmpOp("==", Str("("))),
                AugAssign(Name("balance"), "+", Int(1)),
                AugAssign(Name("balance"), "-", Int(1)))
              If(Compare(Name("balance"), CmpOp("<", Name("minimum"))),
                Assign(Name("minimum"), Name("balance")),
                .Stmts))
            If(Compare(Name("balance"), CmpOp("==", Int(0))),
              If(Compare(Name("minimum"), CmpOp(">=", Int(0))),
                Return(Str("Yes")),
                .Stmts),
              .Stmts)
            Assign(
              Name("text"),
              BinOp(
                "+",
                Subscript(Name("lst"), Int(1)),
                Subscript(Name("lst"), Int(0))))
            Assign(Name("balance"), Int(0))
            Assign(Name("minimum"), Int(0))
            Assign(Name("char"), Str(""))
            For(Name("char"), Name("text"),
              If(Compare(Name("char"), CmpOp("==", Str("("))),
                AugAssign(Name("balance"), "+", Int(1)),
                AugAssign(Name("balance"), "-", Int(1)))
              If(Compare(Name("balance"), CmpOp("<", Name("minimum"))),
                Assign(Name("minimum"), Name("balance")),
                .Stmts))
            If(Compare(Name("balance"), CmpOp("==", Int(0))),
              If(Compare(Name("minimum"), CmpOp(">=", Int(0))),
                Return(Str("Yes")),
                .Stmts),
              .Stmts)
            Return(Str("Yes")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires parenCodes(A) andBool parenCodes(B)
    ensures ?RESULT ==K matchAnswer(A, B)
endmodule
