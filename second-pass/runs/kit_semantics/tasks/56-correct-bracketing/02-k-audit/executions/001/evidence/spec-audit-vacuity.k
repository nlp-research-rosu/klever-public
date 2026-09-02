requires "spec.k"

module SPEC-AUDIT-VACUITY
  imports SPEC

  // Fresh reviewer mutation: "<>" satisfies bracketChars and the submitted
  // function returns true, while this changed obligation requires false.
  claim [false-result-balanced-pair]:
    <k>
      Call(Name("correct_bracketing"), str(iCons(60, iCons(62, .IntSeq))))
      => ?RESULT:Bool
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "correct_bracketing" |->
          closureVal(
            ("brackets", .ParamNames),
            Assign(Name("balance"), Int(0))
            Assign(Name("valid"), Bool(true))
            Assign(Name("bracket"), Str(""))
            For(Name("bracket"), Name("brackets"),
              If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
                AugAssign(Name("balance"), "+", Int(1)),
                AugAssign(Name("balance"), "-", Int(1)))
              If(Compare(Name("balance"), CmpOp("<", Int(0))),
                Assign(Name("valid"), Bool(false)),
                .Stmts))
            Return(
              BoolOp(
                "and",
                Name("valid"),
                Compare(Name("balance"), CmpOp("==", Int(0))))),
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
    ensures ?RESULT ==Bool false
endmodule
