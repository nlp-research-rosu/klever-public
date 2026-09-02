requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [reverse-delete-loop]:
    <k>
      #loop(
        str(S:IntSeq),
        Name("ch"),
        If(
          Compare(Name("ch"), CmpOp("not in", Name("c"))),
          AugAssign(Name("result"), "+", Name("ch"))
          Assign(
            Name("reversed_result"),
            BinOp("+", Name("ch"), Name("reversed_result"))),
          .Stmts))
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      REST:Map
      L |-> scope(
        "s" |-> str(ORIGINAL:IntSeq)
        "c" |-> str(C:IntSeq)
        "result" |-> (str(A:IntSeq)
                      => str(deleteAcc(S, C, A)))
        "reversed_result" |-> (str(R:IntSeq)
                               => str(reverseDeleteAcc(S, C, R)))
        "ch" |-> (CH:Val => ?CH:Val),
        parent(0))
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires notBool L in_keys(REST)

  claim [reverse-delete-entry]:
    <k>
      Call(
        Name("reverse_delete"),
        (str(S:IntSeq), str(C:IntSeq), .Exprs))
      => tuple(
           vCons(
             str(deleteAcc(S, C, .IntSeq)),
             vCons(
               deleteAcc(S, C, .IntSeq)
                 ==K reverseDeleteAcc(S, C, .IntSeq),
               .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "reverse_delete" |->
          closureVal(
            ("s", "c", .ParamNames),
            Assign(Name("result"), Str(""))
            Assign(Name("reversed_result"), Str(""))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              If(
                Compare(Name("ch"), CmpOp("not in", Name("c"))),
                AugAssign(Name("result"), "+", Name("ch"))
                Assign(
                  Name("reversed_result"),
                  BinOp("+", Name("ch"), Name("reversed_result"))),
                .Stmts))
            Return(
              TupleExpr(
                Name("result"),
                Compare(
                  Name("result"),
                  CmpOp("==", Name("reversed_result")))))
            .Stmts,
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
endmodule
