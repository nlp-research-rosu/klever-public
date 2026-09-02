requires "verification.k"

module AUDIT-FALSE-MUTATION
  imports VERIFICATION

  // The satisfying input is the documented example; both Python executions
  // and fresh K execution return 9. This deliberately demands 8.
  claim [false-answer-eight]:
    <k>
      #loadAll(Module(
        FuncDef(
          "do_algebra",
          Params("operator", "operand"),
          Assign(Name("expression"), Str(""))
          Assign(Name("oprn"), Int(0))
          Assign(Name("oprt"), Str(""))
          For(
            TupleExpr(Name("oprn"), Name("oprt")),
            Call(
              Name("zip"),
              Name("operand"),
              BinOp("+", Name("operator"), ListExpr(Str("")))),
            AugAssign(
              Name("expression"),
              "+",
              BinOp(
                "+",
                Call(Name("str"), Name("oprn")),
                Name("oprt"))))
          Return(Call(Name("eval"), Name("expression"))))
        Assign(
          Name("answer"),
          Call(
            Name("do_algebra"),
            list(vCons(
              str(iCons(43, .IntSeq)),
              vCons(
                str(iCons(42, .IntSeq)),
                vCons(str(iCons(45, .IntSeq)), .ValSeq)))),
            list(vCons(2, vCons(3, vCons(4, vCons(5, .ValSeq)))))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "answer" |-> 8
        "do_algebra" |-> ?FUNCTION:Val,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
