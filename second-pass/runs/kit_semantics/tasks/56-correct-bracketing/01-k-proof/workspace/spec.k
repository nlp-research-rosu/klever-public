requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        str(CODES:IntSeq),
        Name("bracket"),
        If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(Compare(Name("balance"), CmpOp("<", Int(0))),
          Assign(Name("valid"), Bool(false)),
          .Stmts)
      ) => .K
      ...
    </k>
    <env> LOCAL:Int </env>
    <scopes>
      ...
      LOCAL |-> scope(
        "balance"  |-> (BAL:Int => BAL +Int bracketDelta(CODES))
        "bracket"  |-> (_OLD:Val => ?NEW:Val)
        "brackets" |-> ORIGINAL:Str
        "valid"    |-> (VALID:Bool
                        => VALID andBool bracketPrefixOK(CODES, BAL)),
        PARENT:Parent)
      ...
    </scopes>
    requires bracketChars(CODES)

  claim [correct-bracketing]:
    <k>
      Call(Name("correct_bracketing"), str(CODES:IntSeq))
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
    requires bracketChars(CODES)
    ensures ?RESULT ==Bool bracketCorrect(CODES)
endmodule
