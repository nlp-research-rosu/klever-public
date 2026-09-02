requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [cyc-loop]:
    <k>
      #loop(
        str(REMAIN:IntSeq),
        Name("c"),
        Assign(
          Name("rotation"),
          BinOp(
            "+",
            Subscript(
              Name("rotation"),
              Slice(Int(1), NoBound, NoBound)),
            Name("c")))
        Assign(
          Name("result"),
          BoolOp(
            "or",
            Name("result"),
            Compare(Name("rotation"), CmpOp("in", Name("a"))))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        "a" |-> str(A:IntSeq)
        "b" |-> str(B:IntSeq)
        "c" |-> (str(CURRENT:IntSeq) => str(finalChar(REMAIN, CURRENT)))
        "result" |-> (
          FOUND:Bool
          =>
          cycScan(A, REMAIN, ROT, FOUND))
        "rotation" |-> (
          str(ROT:IntSeq)
          =>
          str(finalRotation(REMAIN, ROT))),
        parent(0))
      0 |-> scope(
        "cycpattern_check" |-> _CLOSURE:Val,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>

  claim [cycpattern-check]:
    <k>
      #loadAll(
        Module(
          FuncDef("cycpattern_check", Params("a", "b"),
            Expr(
              Str(
                "Return whether b or one of its rotations is a substring of a."))
            Assign(
              Name("result"),
              Compare(Name("b"), CmpOp("in", Name("a"))))
            Assign(Name("rotation"), Name("b"))
            Assign(Name("c"), Str(""))
            For(
              Name("c"),
              Subscript(
                Name("b"),
                Slice(
                  NoBound,
                  UnaryOp("-", Int(1)),
                  NoBound)),
              Assign(
                Name("rotation"),
                BinOp(
                  "+",
                  Subscript(
                    Name("rotation"),
                    Slice(Int(1), NoBound, NoBound)),
                  Name("c")))
              Assign(
                Name("result"),
                BoolOp(
                  "or",
                  Name("result"),
                  Compare(
                    Name("rotation"),
                    CmpOp("in", Name("a"))))))
            Return(Name("result")))))
      ~> Call(
           Name("cycpattern_check"),
           str(A:IntSeq),
           str(B:IntSeq))
      => cycPattern(A, B)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "cycpattern_check" |->
                closureVal(
                  ("a", "b"),
                  Expr(
                    Str(
                      "Return whether b or one of its rotations is a substring of a."))
                  Assign(
                    Name("result"),
                    Compare(Name("b"), CmpOp("in", Name("a"))))
                  Assign(Name("rotation"), Name("b"))
                  Assign(Name("c"), Str(""))
                  For(
                    Name("c"),
                    Subscript(
                      Name("b"),
                      Slice(
                        NoBound,
                        UnaryOp("-", Int(1)),
                        NoBound)),
                    Assign(
                      Name("rotation"),
                      BinOp(
                        "+",
                        Subscript(
                          Name("rotation"),
                          Slice(Int(1), NoBound, NoBound)),
                        Name("c")))
                    Assign(
                      Name("result"),
                      BoolOp(
                        "or",
                        Name("result"),
                        Compare(
                          Name("rotation"),
                          CmpOp("in", Name("a"))))))
                  Return(Name("result")),
                  0),
              parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
