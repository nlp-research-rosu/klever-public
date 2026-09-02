requires "verification.k"

module MONOTONIC-SPEC-BODY-MUTATION
  imports MONOTONIC-VERIFICATION

  // Materially changes the executed submitted body to `return False`.
  // The original first claim must therefore stop closing.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "monotonic",
            Params("l"),
            Expr(Str("Return whether l is monotonically nondecreasing or nonincreasing."))
            Return(Bool(false))
          )
        )
      )
      ~> Call(Name("monotonic"), list(VS:ValSeq))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nondecreasing(VS)
endmodule
