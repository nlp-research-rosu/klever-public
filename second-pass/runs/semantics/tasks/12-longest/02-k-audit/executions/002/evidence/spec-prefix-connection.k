requires "verification.k"

module SPEC-PREFIX-CONNECTION
  imports VERIFICATION

  claim
    <k>
      (#bindP(("strings", .ParamNames),
              (list(stringVals(sCons(HEAD:IntSeq, TAIL:StringSeq))), .Vals))
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
      => (#loop(
            list(stringVals(sCons(HEAD, TAIL))),
            Name("string"),
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
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope("longest" |-> longestSolution, parent(-1))
      -1 |-> builtinsScope
      (1 |-> scope(.Map, parent(0))
       => 1 |-> scope(
            "strings" |-> list(stringVals(sCons(HEAD, TAIL)))
            "result" |-> noneV
            "string" |-> noneV,
            parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(prefix-to-loop)]
endmodule
