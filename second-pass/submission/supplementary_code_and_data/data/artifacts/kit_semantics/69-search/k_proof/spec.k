requires "verification.k"

module SPEC
  imports VERIFICATION

  // The inner loop adds exactly the number of occurrences of candidate in
  // REM to the running frequency. It otherwise preserves the function state.
  claim [inner-loop]:
    <k>
      #loop(
        list(REM:ValSeq),
        Name("item"),
        If(
          Compare(Name("item"), CmpOp("==", Name("candidate"))),
          Assign(
            Name("frequency"),
            BinOp("+", Name("frequency"), Int(1))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "lst"       |-> ref(H:Int)
        "answer"    |-> A:Int
        "candidate" |-> X:Val
        "frequency" |-> (
          C:Int => C +Int frequencyOf(projectIntTotal(X), REM))
        "item"      |-> (OLDITEM:Val => ?NEWITEM:Val),
        parent(0))
      ...
    </scopes>
    <heap> ... H |-> list(FULL:ValSeq) ... </heap>
    requires isIntVal(X) andBool allPositive(REM)

  // The outer loop folds every remaining candidate using its exact frequency
  // in FULL. The existential loop-local values are intentionally unobserved.
  claim [outer-loop]:
    <k>
      #loop(
        list(REM:ValSeq),
        Name("candidate"),
        Assign(Name("frequency"), Int(0))
        For(
          Name("item"),
          Name("lst"),
          If(
            Compare(Name("item"), CmpOp("==", Name("candidate"))),
            Assign(
              Name("frequency"),
              BinOp("+", Name("frequency"), Int(1))),
            .Stmts))
        If(
          Compare(Name("frequency"), CmpOp(">=", Name("candidate"))),
          If(
            Compare(Name("candidate"), CmpOp(">", Name("answer"))),
            Assign(
              Name("answer"),
              BinOp("+", Name("candidate"), Int(0))),
            .Stmts),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "lst"       |-> ref(H:Int)
        "answer"    |-> (A:Int => searchSummary(REM, FULL, A))
        "candidate" |-> (OLDCAND:Val => ?NEWCAND:Val)
        "frequency" |-> (OLDFREQ:Int => ?NEWFREQ:Int)
        "item"      |-> (OLDITEM:Val => ?NEWITEM:Val),
        parent(0))
      ...
    </scopes>
    <heap> ... H |-> list(FULL:ValSeq) ... </heap>
    requires allPositive(FULL) andBool allPositive(REM)

  // Whole-program target: load the exact translated definition, resolve and
  // call search, execute its body, and return the mathematical fold result.
  claim [search-program]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "search",
            Params("lst"),
            Assign(Name("answer"), UnaryOp("-", Int(1)))
            Assign(Name("candidate"), Int(1))
            Assign(Name("frequency"), Int(0))
            Assign(Name("item"), Int(1))
            For(
              Name("candidate"),
              Name("lst"),
              Assign(Name("frequency"), Int(0))
              For(
                Name("item"),
                Name("lst"),
                If(
                  Compare(
                    Name("item"),
                    CmpOp("==", Name("candidate"))),
                  Assign(
                    Name("frequency"),
                    BinOp("+", Name("frequency"), Int(1))),
                  .Stmts))
              If(
                Compare(
                  Name("frequency"),
                  CmpOp(">=", Name("candidate"))),
                If(
                  Compare(
                    Name("candidate"),
                    CmpOp(">", Name("answer"))),
                  Assign(
                    Name("answer"),
                    BinOp("+", Name("candidate"), Int(0))),
                  .Stmts),
                .Stmts))
            Return(Name("answer")))))
      ~> Call(Name("search"), ref(0))
      => searchSummary(INPUT, INPUT, -1) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        (.Map => "search" |-> ?SEARCHCLOSURE:Val),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> 0 |-> list(INPUT:ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires INPUT =/=K .ValSeq andBool allPositive(INPUT)
endmodule
