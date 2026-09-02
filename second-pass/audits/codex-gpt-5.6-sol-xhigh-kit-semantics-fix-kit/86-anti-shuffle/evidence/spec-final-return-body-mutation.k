requires "verification.k"

module AUDIT-FINAL-RETURN-MUTATION
  imports VERIFICATION-FULL

  claim [anti-shuffle]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "insert_char",
            Params("word", "char"),
            Assign(Name("prefix"), Str(""))
            Assign(Name("suffix"), Name("word"))
            Assign(Name("current"), Str(""))
            For(
              Name("current"),
              Name("word"),
              If(
                Compare(Name("char"), CmpOp("<", Name("current"))),
                Return(
                  BinOp(
                    "+",
                    BinOp("+", Name("prefix"), Name("char")),
                    Name("suffix"))),
                Assign(
                  Name("prefix"),
                  BinOp("+", Name("prefix"), Name("current")))
                Assign(
                  Name("suffix"),
                  Subscript(
                    Name("suffix"),
                    Slice(Int(1), NoBound, NoBound)))))
            Return(BinOp("+", Name("prefix"), Name("char"))))
          FuncDef(
            "anti_shuffle",
            Params("s"),
            Assign(Name("result"), Str(""))
            Assign(Name("word"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("s"),
              If(
                Compare(Name("char"), CmpOp("==", Str(" "))),
                Assign(
                  Name("result"),
                  BinOp(
                    "+",
                    BinOp("+", Name("result"), Name("word")),
                    Str(" ")))
                Assign(Name("word"), Str("")),
                Assign(
                  Name("word"),
                  Call(
                    Name("insert_char"),
                    Name("word"),
                    Name("char")))))
            Return(Str("x"))
            .Stmts)))
      ~> Call(Name("anti_shuffle"), str(CODES:IntSeq))
      => str(antiFinish(.IntSeq, .IntSeq, CODES))
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires asciiCodes(CODES)
endmodule
