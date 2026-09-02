requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #while(
        Compare(Name("string"), CmpOp("!=", Str(""))),
        If(
          Call(Attribute(Name("string"), "startswith"), Name("substring")),
          AugAssign(Name("count"), "+", Int(1)),
          .Stmts)
        Assign(
          Name("string"),
          Subscript(Name("string"), Slice(Int(1), NoBound, NoBound))))
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "string"    |-> (str(S:IntSeq) => str(.IntSeq))
        "substring" |-> str(P:IntSeq)
        "count"     |-> (C:Int => C +Int overlapCount(S, P)),
        PAR:Parent)
      ...
    </scopes>
    requires notBool (P ==K .IntSeq)

  claim [target]:
    <k>
      Call(
        Name("how_many_times"),
        str(S:IntSeq),
        str(P:IntSeq))
      => ?R:Int
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "how_many_times" |->
          closureVal(
            ("string", "substring"),
            If(
              Compare(Name("substring"), CmpOp("==", Str(""))),
              Return(BinOp("+", Call(Name("len"), Name("string")), Int(1))),
              .Stmts)
            Assign(Name("count"), Int(0))
            While(
              Compare(Name("string"), CmpOp("!=", Str(""))),
              If(
                Call(Attribute(Name("string"), "startswith"), Name("substring")),
                AugAssign(Name("count"), "+", Int(1)),
                .Stmts)
              Assign(
                Name("string"),
                Subscript(Name("string"), Slice(Int(1), NoBound, NoBound))))
            Return(Name("count")),
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
    ensures ?R ==Int overlapCount(S, P)
endmodule
