requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "monotonic",
            Params("l"),
            Return(Bool(false)))
          Assign(
            Name("result"),
            Call(
              Name("monotonic"),
              list(vCons(1, vCons(2, vCons(4, vCons(20, .ValSeq)))))))))
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
