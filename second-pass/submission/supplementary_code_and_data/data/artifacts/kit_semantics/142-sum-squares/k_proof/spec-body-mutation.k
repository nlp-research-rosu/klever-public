requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Material mutation: initialize result to 1.  The correct empty-list
  // postcondition must no longer be provable.
  claim [mutated-body]:
    <k>
      #loadAll(Module(
        FuncDef(
          "sum_squares",
          Params("lst"),
          Assign(Name("result"), Int(1))
          Assign(Name("index"), Int(0))
          Assign(Name("value"), Int(0))
          For(Name("value"), Name("lst"), sumSquaresLoopBody)
          Return(Name("result"))
          .Stmts)))
      ~> Call(Name("sum_squares"), ref(0))
      =>
      sumSquaresAcc(.ValSeq, 0, 0)
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
