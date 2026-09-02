requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        str(REST:IntSeq),
        Name("char"),
        If(
          Compare(
            Name("char"),
            CmpOp("not in", Str("aeiouAEIOU"))),
          AugAssign(Name("result"), "+", Name("char")) .Stmts,
          .Stmts) .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        .Map
          [ "text"   <- str(TEXT:IntSeq) ]
          [ "result" <- (str(ACC:IntSeq)
                        => str(removeVowelsFrom(REST, ACC))) ]
          [ "char"   <- (str(OLD:IntSeq) => str(?LAST:IntSeq)) ],
        P:Parent)
      ...
    </scopes>

  claim [remove-vowels]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "remove_vowels",
            Params("text"),
            Assign(Name("result"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("text"),
              If(
                Compare(
                  Name("char"),
                  CmpOp("not in", Str("aeiouAEIOU"))),
                AugAssign(Name("result"), "+", Name("char")) .Stmts,
                .Stmts) .Stmts)
            Return(Name("result")) .Stmts)
          .Stmts))
      ~> Call(Name("remove_vowels"), (str(TEXT:IntSeq), .Exprs))
      => str(removeVowelsFrom(TEXT, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        .Map
        => .Map [
             "remove_vowels"
             <- closureVal(
                  "text",
                  Assign(Name("result"), Str(""))
                  Assign(Name("char"), Str(""))
                  For(
                    Name("char"),
                    Name("text"),
                    If(
                      Compare(
                        Name("char"),
                        CmpOp("not in", Str("aeiouAEIOU"))),
                      AugAssign(
                        Name("result"), "+", Name("char")) .Stmts,
                      .Stmts) .Stmts)
                  Return(Name("result")) .Stmts,
                  0)
           ],
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
