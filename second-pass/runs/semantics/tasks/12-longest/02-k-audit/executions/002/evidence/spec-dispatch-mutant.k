requires "verification-dispatch-mutant.k"

module SPEC-DISPATCH-MUTANT
  imports VERIFICATION-DISPATCH-MUTANT

  // The candidate's entry-theorem shape still closes for the wrong body,
  // because its destination is only that body's initial call frame.
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
              Return(NoneVal))
          ~> #endcall)
    </k>
    <env> 0 => 1 </env>
    <scopes>
      (0 |-> scope("longest" |-> longestMutant, parent(-1))
       -1 |-> builtinsScope
      => 0 |-> scope("longest" |-> longestMutant, parent(-1))
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
    [label(call-cons-dispatch-mutant)]
endmodule
