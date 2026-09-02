requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Satisfiable false mutation: current best is "x", remaining head is "ab",
  // but the destination incorrectly retains "x".
  claim
    <k>
      (#loop(
        list(stringVals(sCons(
          iCons(97, iCons(98, .IntSeq)),
          .StringSeq))),
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
      => (str(iCons(120, .IntSeq)) ~> .K)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope("longest" |-> longestSolution, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         "strings" |-> list(stringVals(sCons(
           iCons(97, iCons(98, .IntSeq)),
           .StringSeq)))
         "result" |-> str(iCons(120, .IntSeq))
         "string" |-> noneV,
         parent(0))
      => 0 |-> scope("longest" |-> longestSolution, parent(-1))
         -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-retain-longer)]
endmodule
