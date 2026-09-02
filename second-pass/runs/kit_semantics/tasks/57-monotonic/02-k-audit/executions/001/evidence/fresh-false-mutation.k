requires "verification.k"

module AUDIT-FALSE-MUTATION
  imports VERIFICATION

  // [1, 20, 4, 10] is neither nondecreasing nor nonincreasing.
  // This deliberately false mutation requires the executed function to return true.
  claim [nonmonotonic-is-true]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "monotonic",
            Params("l"),
            Return(
              BoolOp(
                "or",
                Compare(
                  Name("l"),
                  CmpOp("==", Call(Name("sorted"), Name("l")))),
                Compare(
                  Name("l"),
                  CmpOp(
                    "==",
                    Call(
                      Name("sorted"),
                      Name("l"),
                      KwArg("reverse", Bool(true))))))))
          Assign(
            Name("result"),
            Call(
              Name("monotonic"),
              list(vCons(1, vCons(20, vCons(4, vCons(10, .ValSeq)))))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("monotonic" |-> ?F:Val
                           "result" |-> ?R:Bool), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?H:Map </heap>
    <heapLoc> 0 => ?HL:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool true
endmodule
