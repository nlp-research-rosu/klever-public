requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed constructor term is materially changed: result initializes
  // to 2 instead of 0. On the satisfying empty-list input, the original
  // theorem's postcondition is therefore false.
  claim [changed-executed-body]:
    <k>
      #loadAll(Module(
        FuncDef(
          "sum_squares",
          Params("lst"),
          Assign(Name("result"), Int(2))
          Assign(Name("index"), Int(0))
          Assign(Name("value"), Int(0))
          For(Name("value"), Name("lst"), sumSquaresLoopBody)
          Return(Name("result"))
          .Stmts)))
      ~> Call(Name("sum_squares"), ref(0))
      =>
      0
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?GLOBALS:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
