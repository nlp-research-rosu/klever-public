requires "verification.k"

module SPEC-COMBINED
  imports VERIFICATION

  // Loop invariant.  The function frame is popped at the destination, so
  // loop-local updates disappear and only the returned accumulator remains.
  claim
    <k>
      (#loop(list(stringVals(.StringSeq)), Name("string"),
        If(Compare(Name("result"), CmpOp("is", NoneVal)),
          Assign(Name("result"), Name("string")),
          If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp("<=", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("result")),
            If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("string")),
            .Stmts))))
      ~> Return(Name("result"))
      ~> #endcall)
      => (noneV ~> CONT:K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> CLOSURE:Val, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> ARG:Val
         "result" |-> noneV
         "string" |-> CURRENT:Val,
         parent(0))
      => 0 |-> scope("longest" |-> CLOSURE, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) RESTSTACK:List
      => RESTSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop-init-empty)]

  // The first string replaces the None sentinel unconditionally.
  claim
    <k>
      (#loop(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))), Name("string"),
        If(Compare(Name("result"), CmpOp("is", NoneVal)),
          Assign(Name("result"), Name("string")),
          If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp("<=", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("result")),
            If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("string")),
            .Stmts))))
      ~> Return(Name("result"))
      ~> #endcall)
      => (longestAcc(str(CS), REST) ~> CONT:K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> CLOSURE:Val, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> ARG:Val
         "result" |-> noneV
         "string" |-> CURRENT:Val,
         parent(0))
      => 0 |-> scope("longest" |-> CLOSURE, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) RESTSTACK:List
      => RESTSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop-init-cons)]

  // String-accumulator base case.
  claim
    <k>
      (#loop(list(stringVals(.StringSeq)), Name("string"),
        If(Compare(Name("result"), CmpOp("is", NoneVal)),
          Assign(Name("result"), Name("string")),
          If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp("<=", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("result")),
            If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("string")),
            .Stmts))))
      ~> Return(Name("result"))
      ~> #endcall)
      => (str(BESTCODES:IntSeq) ~> CONT:K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> CLOSURE:Val, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> ARG:Val
         "result" |-> str(BESTCODES)
         "string" |-> CURRENT:Val,
         parent(0))
      => 0 |-> scope("longest" |-> CLOSURE, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) RESTSTACK:List
      => RESTSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop-empty)]

  // A strictly longer head replaces the accumulator.
  claim
    <k>
      (#loop(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))), Name("string"),
        If(Compare(Name("result"), CmpOp("is", NoneVal)),
          Assign(Name("result"), Name("string")),
          If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp("<=", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("result")),
            If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("string")),
            .Stmts))))
      ~> Return(Name("result"))
      ~> #endcall)
      => (longestAcc(str(CS), REST) ~> CONT:K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> CLOSURE:Val, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> ARG:Val
         "result" |-> str(BESTCODES:IntSeq)
         "string" |-> CURRENT:Val,
         parent(0))
      => 0 |-> scope("longest" |-> CLOSURE, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) RESTSTACK:List
      => RESTSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(CS) >Int isLen(BESTCODES)
    [label(loop-longer)]

  // A shorter or tied head retains the earlier accumulator.
  claim
    <k>
      (#loop(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))), Name("string"),
        If(Compare(Name("result"), CmpOp("is", NoneVal)),
          Assign(Name("result"), Name("string")),
          If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp("<=", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("result")),
            If(Compare(
            Call(Name("len"), Name("string")),
            CmpOp(">", Call(Name("len"), Name("result")))),
            Assign(Name("result"), Name("string")),
            .Stmts))))
      ~> Return(Name("result"))
      ~> #endcall)
      => (longestAcc(str(BESTCODES:IntSeq), REST) ~> CONT:K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> CLOSURE:Val, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> ARG:Val
         "result" |-> str(BESTCODES)
         "string" |-> CURRENT:Val,
         parent(0))
      => 0 |-> scope("longest" |-> CLOSURE, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) RESTSTACK:List
      => RESTSTACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(CS) <=Int isLen(BESTCODES)
    [label(loop-retain)]

  // Loading solution.mpy installs exactly the closure used below.
  claim
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List", "Optional")
        FuncDef("longest", Params("strings"),
          Assign(Name("result"), NoneVal)
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            If(Compare(Name("result"), CmpOp("is", NoneVal)),
              Assign(Name("result"), Name("string")),
              If(Compare(
                Call(Name("len"), Name("string")),
                CmpOp("<=", Call(Name("len"), Name("result")))),
                Assign(Name("result"), Name("result")),
                If(Compare(
                  Call(Name("len"), Name("string")),
                  CmpOp(">", Call(Name("len"), Name("result")))),
                  Assign(Name("result"), Name("string")),
                  .Stmts))))
          Return(Name("result")))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
      => 0 |-> scope("longest" |-> longestSolution, parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(load-solution)]

  // Calls cover the two constructors of every finite string sequence.
  claim
    <k>
      Call(Name("longest"), list(stringVals(.StringSeq)), .Exprs)
      => noneV
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("longest" |-> longestSolution, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(call-empty)]

  claim
    <k>
      Call(Name("longest"),
        list(stringVals(sCons(HEAD:IntSeq, TAIL:StringSeq))),
        .Exprs)
      => (#bindP(("strings", .ParamNames),
                 (list(stringVals(sCons(HEAD, TAIL))), .Vals))
          ~> (Assign(Name("result"), NoneVal)
              Assign(Name("string"), NoneVal)
              For(Name("string"), Name("strings"),
                If(Compare(Name("result"), CmpOp("is", NoneVal)),
                  Assign(Name("result"), Name("string")),
                  If(Compare(
                    Call(Name("len"), Name("string")),
                    CmpOp("<=", Call(Name("len"), Name("result")))),
                    Assign(Name("result"), Name("result")),
                    If(Compare(
                      Call(Name("len"), Name("string")),
                      CmpOp(">", Call(Name("len"), Name("result")))),
                      Assign(Name("result"), Name("string")),
                      .Stmts))))
              Return(Name("result")))
          ~> #endcall)
    </k>
    <env> 0 => 1 </env>
    <scopes>
      (0 |-> scope("longest" |-> longestSolution, parent(-1))
       -1 |-> builtinsScope
      => 0 |-> scope("longest" |-> longestSolution, parent(-1))
         -1 |-> builtinsScope
         1 |-> scope(.Map, parent(0)))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List => ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(call-cons-dispatch)]

  // The result-constraining theorem absent from the candidate.
  claim
    <k>
      Call(Name("longest"),
        list(stringVals(sCons(HEAD:IntSeq, TAIL:StringSeq))),
        .Exprs)
      => longestAcc(str(HEAD), TAIL)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("longest" |-> longestSolution, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(omitted-entry-nonempty)]
endmodule
