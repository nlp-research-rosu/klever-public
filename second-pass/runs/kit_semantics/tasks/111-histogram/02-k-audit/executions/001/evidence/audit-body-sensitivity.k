requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  claim [first-count-loop]:
    <k>
      #loop(
        str(REM:IntSeq),
        Name("candidate"),
        If(
          Compare(Name("candidate"), CmpOp("==", Name("letter"))),
          Assign(
            Name("count"),
            BinOp("+", Name("count"), Int(1))),
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      S:Map
      L |-> scope(
        "test"      |-> str(ORIG:IntSeq)
        "result"    |-> dictV(.ValSeq, .ValSeq)
        "max_count" |-> M:Int
        "letter"    |-> str(iCons(TARGET:Int, .IntSeq))
        "candidate" |-> (CANDIDATE:Val => ?FINALCANDIDATE:Val)
        "count"     |-> (
          N:Int
          =>
          countHistogramCode(REM, TARGET, N))
        "phase"     |-> 1,
        P:Parent)
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires notBool L in_keys(S)

  claim [second-count-loop]:
    <k>
      #loop(
        str(REM:IntSeq),
        Name("candidate"),
        If(
          Compare(Name("candidate"), CmpOp("==", Name("letter"))),
          Assign(
            Name("count"),
            BinOp("+", Name("count"), Int(1))),
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      S:Map
      L |-> scope(
        "test"      |-> str(ORIG:IntSeq)
        "result"    |-> dictV(KS:ValSeq, VS:ValSeq)
        "max_count" |-> M:Int
        "letter"    |-> str(iCons(TARGET:Int, .IntSeq))
        "candidate" |-> (CANDIDATE:Val => ?FINALCANDIDATE:Val)
        "count"     |-> (
          N:Int
          =>
          countHistogramCode(REM, TARGET, N))
        "phase"     |-> 2,
        P:Parent)
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires notBool L in_keys(S)

  claim [first-loop]:
    <k>
      #loop(
        str(REM:IntSeq),
        Name("letter"),
        If(
          Compare(Name("letter"), CmpOp("!=", Str(" "))),
          Assign(Name("count"), Int(0))
          For(
            Name("candidate"),
            Name("test"),
            If(
              Compare(
                Name("candidate"),
                CmpOp("==", Name("letter"))),
              Assign(
                Name("count"),
                BinOp("+", Name("count"), Int(1))),
              .Stmts)
            .Stmts)
          If(
            Compare(Name("count"), CmpOp(">", Name("max_count"))),
            Assign(Name("max_count"), Name("count")),
            .Stmts),
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      S:Map
      L |-> scope(
        "test"      |-> str(ORIG:IntSeq)
        "result"    |-> dictV(.ValSeq, .ValSeq)
        "max_count" |-> (M:Int => maxHistogramCount(REM, ORIG, M))
        "letter"    |-> (LETTER:Val => ?FINALLETTER:Val)
        "candidate" |-> (CANDIDATE:Val => ?FINALCANDIDATE:Val)
        "count"     |-> (COUNT:Int => ?FINALCOUNT:Int)
        "phase"     |-> 1,
        P:Parent)
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires notBool L in_keys(S)

  claim [second-loop]:
    <k>
      #loop(
        str(REM:IntSeq),
        Name("letter"),
        If(
          Compare(Name("letter"), CmpOp("!=", Str(" "))),
          Assign(Name("count"), Int(0))
          For(
            Name("candidate"),
            Name("test"),
            If(
              Compare(
                Name("candidate"),
                CmpOp("==", Name("letter"))),
              Assign(
                Name("count"),
                BinOp("+", Name("count"), Int(1))),
              .Stmts)
            .Stmts)
          If(
            Compare(Name("count"), CmpOp("==", Name("max_count"))),
            Assign(
              Subscript(Name("result"), Name("letter")),
              Name("count")),
            .Stmts),
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      S:Map
      L |-> scope(
        "test"      |-> str(ORIG:IntSeq)
        "result"    |-> (
          dictV(KS:ValSeq, VS:ValSeq)
          =>
          buildHistogram(REM, ORIG, M, KS, VS))
        "max_count" |-> M:Int
        "letter"    |-> (LETTER:Val => ?FINALLETTER:Val)
        "candidate" |-> (CANDIDATE:Val => ?FINALCANDIDATE:Val)
        "count"     |-> (COUNT:Int => ?FINALCOUNT:Int)
        "phase"     |-> 2,
        P:Parent)
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HNEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT:Int </exit-code>
    requires notBool L in_keys(S)

  claim [histogram-mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "histogram",
            Params("test"),
            Assign(Name("result"), DictExpr(.Entries))
            Assign(Name("max_count"), Int(0))
            Assign(Name("letter"), Str(""))
            Assign(Name("candidate"), Str(""))
            Assign(Name("count"), Int(0))
            Assign(Name("phase"), Int(1))
            For(
              Name("letter"),
              Name("test"),
              If(
                Compare(Name("letter"), CmpOp("!=", Str(" "))),
                Assign(Name("count"), Int(0))
                For(
                  Name("candidate"),
                  Name("test"),
                  If(
                    Compare(
                      Name("candidate"),
                      CmpOp("==", Name("letter"))),
                    Assign(
                      Name("count"),
                      BinOp("+", Name("count"), Int(1))),
                    .Stmts)
                  .Stmts)
                If(
                  Compare(
                    Name("count"),
                    CmpOp(">", Name("max_count"))),
                  Assign(Name("max_count"), Name("count")),
                  .Stmts),
                .Stmts)
              .Stmts)
            Assign(Name("phase"), Int(2))
            For(
              Name("letter"),
              Name("test"),
              If(
                Compare(Name("letter"), CmpOp("!=", Str(" "))),
                Assign(Name("count"), Int(0))
                For(
                  Name("candidate"),
                  Name("test"),
                  If(
                    Compare(
                      Name("candidate"),
                      CmpOp("==", Name("letter"))),
                    Assign(
                      Name("count"),
                      BinOp("+", Name("count"), Int(1))),
                    .Stmts)
                  .Stmts)
                If(
                  Compare(
                    Name("count"),
                    CmpOp("!=", Name("max_count"))),
                  Assign(
                    Subscript(Name("result"), Name("letter")),
                    Name("count")),
                  .Stmts),
                .Stmts)
              .Stmts)
            Return(Name("result"))
            .Stmts)))
      ~> Call(
        Name("histogram"),
        str(iCons(97, .IntSeq)))
      =>
      histogramResult(iCons(97, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "histogram" |->
          closureVal(
            "test",
            Assign(Name("result"), DictExpr(.Entries))
            Assign(Name("max_count"), Int(0))
            Assign(Name("letter"), Str(""))
            Assign(Name("candidate"), Str(""))
            Assign(Name("count"), Int(0))
            Assign(Name("phase"), Int(1))
            For(
              Name("letter"),
              Name("test"),
              If(
                Compare(Name("letter"), CmpOp("!=", Str(" "))),
                Assign(Name("count"), Int(0))
                For(
                  Name("candidate"),
                  Name("test"),
                  If(
                    Compare(
                      Name("candidate"),
                      CmpOp("==", Name("letter"))),
                    Assign(
                      Name("count"),
                      BinOp("+", Name("count"), Int(1))),
                    .Stmts)
                  .Stmts)
                If(
                  Compare(
                    Name("count"),
                    CmpOp(">", Name("max_count"))),
                  Assign(Name("max_count"), Name("count")),
                  .Stmts),
                .Stmts)
              .Stmts)
            Assign(Name("phase"), Int(2))
            For(
              Name("letter"),
              Name("test"),
              If(
                Compare(Name("letter"), CmpOp("!=", Str(" "))),
                Assign(Name("count"), Int(0))
                For(
                  Name("candidate"),
                  Name("test"),
                  If(
                    Compare(
                      Name("candidate"),
                      CmpOp("==", Name("letter"))),
                    Assign(
                      Name("count"),
                      BinOp("+", Name("count"), Int(1))),
                    .Stmts)
                  .Stmts)
                If(
                  Compare(
                    Name("count"),
                    CmpOp("!=", Name("max_count"))),
                  Assign(
                    Subscript(Name("result"), Name("letter")),
                    Name("count")),
                  .Stmts),
                .Stmts)
              .Stmts)
            Return(Name("result"))
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
    requires validHistogramInput(iCons(97, .IntSeq))
endmodule
